import os
import json
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# Import database manager and AI profiling engines
from database import init_db, get_session, User, AcademicProfile, LearningPreferences, SkillAssessment, CareerInterest, QuizAttempt, LearningBehavior, SystemLog, DB_STATUS, log_event
from ai_engine import classify_student, identify_weak_areas, project_academic_performance, generate_recommendations, get_chatbot_response
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Database Connection
init_db()

# --- Seeding Admin User ---
def seed_admin():
    session_db = get_session()
    try:
        # Load admin config
        admin_email = "admin@learning.com"
        admin_password = "admin123"
        
        if os.path.exists("db_config.json"):
            try:
                with open("db_config.json", "r") as f:
                    config = json.load(f)
                    admin_email = config.get("ADMIN_EMAIL", admin_email)
                    admin_password = config.get("ADMIN_PASSWORD", admin_password)
            except Exception as e:
                print(f"Error loading admin config for seeding: {e}")
                
        # Check if admin already exists
        existing_admin = session_db.query(User).filter_by(email=admin_email).first()
        if not existing_admin:
            hashed_pwd = generate_password_hash(admin_password)
            admin = User(
                first_name="System",
                last_name="Administrator",
                email=admin_email,
                password_hash=hashed_pwd,
                phone="0000000000",
                age=30,
                gender="Other",
                institution="System Admin",
                role="admin"
            )
            session_db.add(admin)
            session_db.commit()
            print(f"Admin seeded successfully with email: {admin_email}")
            log_event("Admin", "Seed Admin Created", f"Admin account initialized with email: {admin_email}")
    except Exception as e:
        print(f"Error seeding admin user: {e}")
    finally:
        session_db.close()

seed_admin()

# --- Custom Middleware/Helper Decorators ---
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# --- Frontend HTML Page Routes ---

@app.route('/')
def login_page():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard_page'))
        return redirect(url_for('dashboard_page'))
    return render_template('index.html')

@app.route('/assessment')
@login_required
def assessment_page():
    # If student is an admin, redirect to admin
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard_page'))
    return render_template('assessment.html')

@app.route('/dashboard')
@login_required
def dashboard_page():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard_page'))
    return render_template('dashboard.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard_page():
    return render_template('admin_dashboard.html')

# --- Authentication APIs ---

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Invalid request payload"}), 400

    session_db = get_session()
    try:
        # Check if user already exists
        email = data.get('email', '').strip().lower()
        existing = session_db.query(User).filter_by(email=email).first()
        if existing:
            return jsonify({"success": False, "message": "Email is already registered"}), 400

        # Validate passwords match
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match"}), 400

        # Create basic details
        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=email,
            phone=data.get('phone'),
            password_hash=hashed_password,
            age=int(data.get('age', 0)) if data.get('age') else None,
            gender=data.get('gender'),
            institution=data.get('college_name'),
            role='student'
        )
        session_db.add(new_user)
        session_db.flush() # Populate user ID

        # Academic Profile details
        new_academic = AcademicProfile(
            user_id=new_user.id,
            department=data.get('department'),
            course=data.get('course'),
            year=data.get('year'),
            semester=data.get('semester'),
            subjects_interested=json.dumps(data.get('subjects_interested', [])),
            current_cgpa=float(data.get('current_cgpa', 0.0)) if data.get('current_cgpa') else 0.0,
            preferred_languages=json.dumps(data.get('preferred_languages', []))
        )
        session_db.add(new_academic)

        # Learning Preferences
        new_prefs = LearningPreferences(
            user_id=new_user.id,
            preferred_method=json.dumps(data.get('preferred_method', [])),
            learning_speed=data.get('learning_speed'),
            daily_study_hours=float(data.get('daily_study_hours', 0.0)) if data.get('daily_study_hours') else 0.0,
            difficulty_level=data.get('difficulty_level')
        )
        session_db.add(new_prefs)

        # Skill self-ratings
        new_skills = SkillAssessment(
            user_id=new_user.id,
            programming=int(data.get('skill_programming', 1)),
            aptitude=int(data.get('skill_aptitude', 1)),
            mathematics=int(data.get('skill_math', 1)),
            communication=int(data.get('skill_communication', 1))
        )
        session_db.add(new_skills)

        # Career Interests
        new_career = CareerInterest(
            user_id=new_user.id,
            interests=json.dumps(data.get('career_interests', []))
        )
        session_db.add(new_career)

        session_db.commit()

        # Write System Audit Log
        log_event("Auth", "Student Registration", f"Student {new_user.first_name} {new_user.last_name} ({email}) registered.")

        # Establish log in session
        session['user_id'] = new_user.id
        session['email'] = new_user.email
        session['name'] = f"{new_user.first_name} {new_user.last_name}"
        session['role'] = new_user.role

        return jsonify({"success": True, "redirect": url_for('assessment_page')})
    except Exception as e:
        session_db.rollback()
        print(f"Error during registration: {e}")
        return jsonify({"success": False, "message": f"Database insertion error: {str(e)}"}), 500
    finally:
        session_db.close()

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password')

    session_db = get_session()
    try:
        user = session_db.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"success": False, "message": "Incorrect email or password"}), 401

        # Save session variables
        session['user_id'] = user.id
        session['email'] = user.email
        session['name'] = f"{user.first_name} {user.last_name}"
        session['role'] = user.role

        log_event("Auth", "User Login", f"User {user.email} logged in with role {user.role}.")

        redirect_url = url_for('admin_dashboard_page') if user.role == 'admin' else url_for('dashboard_page')
        return jsonify({"success": True, "redirect": redirect_url})
    except Exception as e:
        return jsonify({"success": False, "message": f"Login process error: {str(e)}"}), 500
    finally:
        session_db.close()

@app.route('/api/auth/logout')
def api_logout():
    email = session.get('email')
    if email:
        log_event("Auth", "User Logout", f"User {email} logged out.")
    session.clear()
    return redirect(url_for('login_page'))

# --- Student Assessment APIs ---

@app.route('/api/assessment/submit', methods=['POST'])
@login_required
def api_assessment_submit():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Missing assessment results"}), 400

    answers = data.get('answers', {})
    time_taken = int(data.get('time_taken', 0))

    # Correct answers definition
    # Q1: C, Q2: B, Q3: C, Q4: D, Q5: A, Q6: A
    correct_key = {
        "q1": "C", # String
        "q2": "B", # 02
        "q3": "C", # arr[2]
        "q4": "D", # Abstraction
        "q5": "A", # 72 km/h
        "q6": "A"  # Brother
    }

    # Evaluate responses
    results = {}
    score_count = 0
    incorrect_records = []
    
    question_labels = {
        "q1": "Java primitives (Java basics)",
        "q2": "Loop execution (Loops)",
        "q3": "Array indexing (Arrays)",
        "q4": "OOP Abstraction (OOP concepts)",
        "q5": "Train Speed Problems (Quantitative Aptitude)",
        "q6": "Blood Relations Riddle (Logical reasoning)"
    }

    for q_id, correct_ans in correct_key.items():
        user_ans = answers.get(q_id, '').strip()
        is_correct = (user_ans == correct_ans)
        results[q_id] = is_correct
        if is_correct:
            score_count += 1
        else:
            incorrect_records.append({
                "question": question_labels.get(q_id, q_id),
                "your_answer": user_ans,
                "correct_answer": correct_ans
            })

    total_questions = len(correct_key)
    score_percentage = (score_count / total_questions) * 100
    accuracy = score_percentage # In a 6-question quiz, accuracy is simply percentage correct

    # Identify weak areas and classify student level
    weak_areas = identify_weak_areas(results)
    level_classified = classify_student(score_percentage)

    session_db = get_session()
    try:
        new_attempt = QuizAttempt(
            user_id=session['user_id'],
            score_percentage=score_percentage,
            accuracy=accuracy,
            time_taken_seconds=time_taken,
            incorrect_answers=json.dumps(incorrect_records),
            weak_areas=json.dumps(weak_areas),
            level_classified=level_classified
        )
        session_db.add(new_attempt)

        # Seed initial learning behavior entries based on weak topics to kickstart tracking
        for topic in ["Java basics", "Loops", "Arrays", "OOP concepts", "Quantitative Aptitude", "Logical reasoning"]:
            existing_behavior = session_db.query(LearningBehavior).filter_by(user_id=session['user_id'], topic=topic).first()
            if not existing_behavior:
                is_weak = topic in weak_areas
                init_behavior = LearningBehavior(
                    user_id=session['user_id'],
                    topic=topic,
                    time_spent_minutes=5 if is_weak else 15, # mock initial tracking times
                    attempts=1,
                    completion_rate=20.0 if is_weak else 60.0
                )
                session_db.add(init_behavior)

        session_db.commit()
        log_event("Quiz", "Quiz Submitted", f"Student {session['email']} scored {score_percentage:.1f}% and classified as {level_classified}.")
        return jsonify({"success": True, "score": score_percentage, "level": level_classified})
    except Exception as e:
        session_db.rollback()
        print(f"Error saving quiz submission: {e}")
        return jsonify({"success": False, "message": f"Database save failed: {str(e)}"}), 500
    finally:
        session_db.close()

# --- Student Dashboard APIs ---

@app.route('/api/dashboard/stats')
@login_required
def api_dashboard_stats():
    user_id = session['user_id']
    session_db = get_session()
    try:
        # Query models
        user = session_db.query(User).filter_by(id=user_id).first()
        academic = session_db.query(AcademicProfile).filter_by(user_id=user_id).first()
        prefs = session_db.query(LearningPreferences).filter_by(user_id=user_id).first()
        skills = session_db.query(SkillAssessment).filter_by(user_id=user_id).first()
        career = session_db.query(CareerInterest).filter_by(user_id=user_id).first()
        
        # Get the latest quiz attempt
        latest_attempt = session_db.query(QuizAttempt).filter_by(user_id=user_id).order_by(QuizAttempt.completed_at.desc()).first()
        
        # Get behaviors
        behaviors = session_db.query(LearningBehavior).filter_by(user_id=user_id).all()

        if not latest_attempt:
            # User has not taken the quiz yet
            return jsonify({
                "quiz_taken": False,
                "profile": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "age": user.age,
                    "gender": user.gender,
                    "college_name": user.institution
                }
            })

        # Process weak areas and recommendations
        weak_topics = json.loads(latest_attempt.weak_areas) if latest_attempt.weak_areas else []
        level = latest_attempt.level_classified

        # Calculate GPA Projection
        projected_cgpa, scale = project_academic_performance(
            current_cgpa=academic.current_cgpa if academic else 0.0,
            study_hours=prefs.daily_study_hours if prefs else 3.0,
            quiz_score=latest_attempt.score_percentage
        )

        recommendations = generate_recommendations(weak_topics, level)

        # Parse behavioral logs
        behavior_list = []
        for b in behaviors:
            behavior_list.append({
                "topic": b.topic,
                "time_spent": b.time_spent_minutes,
                "attempts": b.attempts,
                "completion_rate": b.completion_rate
            })

        # Formulate general profile payload
        payload = {
            "quiz_taken": True,
            "profile": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "college_name": user.institution,
                "course": academic.course if academic else "N/A",
                "department": academic.department if academic else "N/A",
                "cgpa": academic.current_cgpa if academic else 0.0,
                "projected_cgpa": projected_cgpa,
                "cgpa_scale": scale,
                "level": level,
                "career": json.loads(career.interests)[0] if career and career.interests and len(json.loads(career.interests)) > 0 else "Software Developer"
            },
            "quiz_metrics": {
                "score": latest_attempt.score_percentage,
                "accuracy": latest_attempt.accuracy,
                "time_taken": latest_attempt.time_taken_seconds,
                "incorrect_answers": json.loads(latest_attempt.incorrect_answers) if latest_attempt.incorrect_answers else []
            },
            "skills_rated": {
                "programming": skills.programming if skills else 3,
                "aptitude": skills.aptitude if skills else 3,
                "mathematics": skills.mathematics if skills else 3,
                "communication": skills.communication if skills else 3
            },
                        "weak_topics": weak_topics,
            "recommendations": recommendations,
            "behaviors": behavior_list,
            "preferences": {
                "learning_speed": prefs.learning_speed if prefs else "Medium",
                "daily_study_hours": prefs.daily_study_hours if prefs else 3.0,
                "method": json.loads(prefs.preferred_method) if prefs and prefs.preferred_method else ["Video"]
            },
            "can_retake_test": (sum(b["time_spent"] for b in behavior_list) >= 30)
        }
        return jsonify(payload)

    except Exception as e:
        print(f"Error fetching dashboard statistics: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

@app.route('/api/track/behavior', methods=['POST'])
@login_required
def api_track_behavior():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Missing payload"}), 400

    topic = data.get('topic')
    minutes = int(data.get('minutes_spent', 0))
    completion_delta = float(data.get('completion_delta', 0.0))

    if not topic:
        return jsonify({"success": False, "message": "Topic is required"}), 400

    session_db = get_session()
    try:
        behavior = session_db.query(LearningBehavior).filter_by(user_id=session['user_id'], topic=topic).first()
        if not behavior:
            behavior = LearningBehavior(
                user_id=session['user_id'],
                topic=topic,
                time_spent_minutes=minutes,
                attempts=1,
                completion_rate=min(100.0, max(0.0, completion_delta))
            )
            session_db.add(behavior)
        else:
            behavior.time_spent_minutes += minutes
            behavior.attempts += 1
            behavior.completion_rate = min(100.0, behavior.completion_rate + completion_delta)
            behavior.last_active = datetime.datetime.utcnow()

        session_db.commit()
        return jsonify({"success": True, "message": "Behavior tracked successfully"})
    except Exception as e:
        session_db.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

# --- Chatbot API ---

@app.route('/api/chat/ask', methods=['POST'])
@login_required
def api_chat_ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"success": False, "message": "No question asked"}), 400

    question = data.get('question')
    user_id = session['user_id']

    session_db = get_session()
    try:
        user = session_db.query(User).filter_by(id=user_id).first()
        latest_attempt = session_db.query(QuizAttempt).filter_by(user_id=user_id).order_by(QuizAttempt.completed_at.desc()).first()
        career = session_db.query(CareerInterest).filter_by(user_id=user_id).first()

        weak_topics = json.loads(latest_attempt.weak_areas) if latest_attempt and latest_attempt.weak_areas else []
        level = latest_attempt.level_classified if latest_attempt else "Beginner"
        career_str = json.loads(career.interests)[0] if career and career.interests and len(json.loads(career.interests)) > 0 else "Software Developer"

        user_profile = {
            "first_name": user.first_name,
            "level": level,
            "weak_topics": weak_topics,
            "career": career_str
        }

        # Query our AI responder
        reply = get_chatbot_response(question, user_profile)
        
        # Track that they asked a chat helper in our behavior logs!
        if len(weak_topics) > 0:
            # Help increment the study progress on their first weak topic
            topic_to_track = weak_topics[0]
            behavior = session_db.query(LearningBehavior).filter_by(user_id=user_id, topic=topic_to_track).first()
            if behavior:
                behavior.time_spent_minutes += 5 # chat consultation adds 5 mins
                behavior.completion_rate = min(100.0, behavior.completion_rate + 8.0)
                session_db.commit()

        return jsonify({"success": True, "reply": reply})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

# --- Admin Dashboard APIs ---

@app.route('/api/admin/stats')
@admin_required
def api_admin_stats():
    session_db = get_session()
    try:
        # 1. Platform Metrics
        total_students = session_db.query(User).filter_by(role='student').count()
        total_quizzes = session_db.query(QuizAttempt).count()
        
        # Level distributions
        beg_count = session_db.query(QuizAttempt).filter_by(level_classified='Beginner').count()
        int_count = session_db.query(QuizAttempt).filter_by(level_classified='Intermediate').count()
        adv_count = session_db.query(QuizAttempt).filter_by(level_classified='Advanced').count()

        # 2. Student List Matrix
        students = session_db.query(User).filter_by(role='student').all()
        student_list = []
        for s in students:
            acad = session_db.query(AcademicProfile).filter_by(user_id=s.id).first()
            attempt = session_db.query(QuizAttempt).filter_by(user_id=s.id).order_by(QuizAttempt.completed_at.desc()).first()
            
            student_list.append({
                "id": s.id,
                "name": f"{s.first_name} {s.last_name}",
                "email": s.email,
                "college": s.institution,
                "cgpa": acad.current_cgpa if acad else 0.0,
                "quiz_score": attempt.score_percentage if attempt else None,
                "level": attempt.level_classified if attempt else "Unassessed",
                "registered_on": s.created_at.strftime("%Y-%m-%d %H:%M")
            })

        # 3. System Logs Stream
        logs = session_db.query(SystemLog).order_by(SystemLog.timestamp.desc()).limit(50).all()
        log_list = []
        for l in logs:
            log_list.append({
                "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "category": l.category,
                "action": l.action,
                "details": l.details
            })

        # 4. Database Diagnostics
        db_stats = {
            "active_db": DB_STATUS["active_db"],
            "status": DB_STATUS["status"],
            "details": DB_STATUS["details"],
            "log_count": session_db.query(SystemLog).count(),
            "user_table_size": session_db.query(User).count(),
            "quiz_table_size": session_db.query(QuizAttempt).count()
        }

        return jsonify({
            "success": True,
            "metrics": {
                "total_students": total_students,
                "total_quizzes": total_quizzes,
                "levels": {
                    "Beginner": beg_count,
                    "Intermediate": int_count,
                    "Advanced": adv_count
                }
            },
            "students": student_list,
            "logs": log_list,
            "db_diagnostics": db_stats
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

@app.route('/api/admin/users/delete', methods=['POST'])
@admin_required
def api_admin_delete_user():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    target_id = int(data.get('user_id'))
    session_db = get_session()
    try:
        user = session_db.query(User).filter_by(id=target_id, role='student').first()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        email = user.email
        session_db.delete(user)
        session_db.commit()

        log_event("Admin", "Delete Student", f"Admin deleted student account: {email}")
        return jsonify({"success": True, "message": "User account successfully deleted."})
    except Exception as e:
        session_db.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

@app.route('/api/admin/users/reset', methods=['POST'])
@admin_required
def api_admin_reset_quiz():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    target_id = int(data.get('user_id'))
    session_db = get_session()
    try:
        user = session_db.query(User).filter_by(id=target_id).first()
        if not user:
            return jsonify({"success": False, "message": "Student not found"}), 404

        # Delete all quiz attempts
        session_db.query(QuizAttempt).filter_by(user_id=target_id).delete()
        
        # Reset behaviors too to force recalculation on next attempt
        session_db.query(LearningBehavior).filter_by(user_id=target_id).delete()

        session_db.commit()

        log_event("Admin", "Reset Student Quiz", f"Admin reset quiz attempts for student: {user.email}")
        return jsonify({"success": True, "message": "Quiz attempts reset successfully. The student can now retake the assessment."})
    except Exception as e:
        session_db.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

@app.route('/api/assessment/reset', methods=['POST'])
@login_required
def api_student_reset_quiz():
    user_id = session['user_id']
    data = request.json or {}
    session_db = get_session()
    try:
        # Updated: allow specifying language and optional force retake
        language = data.get('language', 'en')
        force_retake = data.get('force', False)
        total_minutes = session_db.query(func.sum(LearningBehavior.time_spent_minutes)).filter_by(user_id=user_id).scalar() or 0
        if total_minutes < 30 and not force_retake:
            return jsonify({"success": False, "message": "Insufficient study time to retake test."}), 403
        # Delete existing attempts and behaviors
        session_db.query(QuizAttempt).filter_by(user_id=user_id).delete()
        session_db.query(LearningBehavior).filter_by(user_id=user_id).delete()
        session_db.commit()
        # Store selected language in session for upcoming quiz generation
        session['quiz_language'] = language
        log_event("Student", "Reset Quiz", f"Student {session.get('email')} reset their quiz attempts with language '{language}'.")
        return jsonify({"success": True, "message": f"Quiz reset successfully. You may retake the assessment in '{language}'."})
    except Exception as e:
        session_db.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        session_db.close()

if __name__ == '__main__':
    # Running local server
    app.run(debug=True, host='127.0.0.1', port=5000)
