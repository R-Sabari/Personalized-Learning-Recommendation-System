import os
import json
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# Global Connection Info for Diagnostics
DB_STATUS = {
    "active_db": "sqlite",
    "status": "Disconnected",
    "details": "Initializing...",
    "tables_created": False
}

# --- Database Models ---

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    institution = Column(String(150), nullable=True)
    role = Column(String(20), default='student') # student, admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    academic_profile = relationship("AcademicProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    preferences = relationship("LearningPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skills = relationship("SkillAssessment", back_populates="user", uselist=False, cascade="all, delete-orphan")
    career = relationship("CareerInterest", back_populates="user", uselist=False, cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    behaviors = relationship("LearningBehavior", back_populates="user", cascade="all, delete-orphan")

class AcademicProfile(Base):
    __tablename__ = 'academic_profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    department = Column(String(100))
    course = Column(String(100))
    year = Column(String(10))
    semester = Column(String(10))
    subjects_interested = Column(Text) # JSON string array
    current_cgpa = Column(Float, default=0.0)
    preferred_languages = Column(Text) # JSON string array

    user = relationship("User", back_populates="academic_profile")

class LearningPreferences(Base):
    __tablename__ = 'learning_preferences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    preferred_method = Column(Text) # JSON string array
    learning_speed = Column(String(20)) # Slow, Medium, Fast
    daily_study_hours = Column(Float, default=0.0)
    difficulty_level = Column(String(20)) # Beginner, Intermediate, Advanced

    user = relationship("User", back_populates="preferences")

class SkillAssessment(Base):
    __tablename__ = 'skill_assessments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    programming = Column(Integer, default=1)
    aptitude = Column(Integer, default=1)
    mathematics = Column(Integer, default=1)
    communication = Column(Integer, default=1)

    user = relationship("User", back_populates="skills")

class CareerInterest(Base):
    __tablename__ = 'career_interests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    interests = Column(Text) # JSON string array

    user = relationship("User", back_populates="career")

class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score_percentage = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)
    time_taken_seconds = Column(Integer, nullable=False)
    incorrect_answers = Column(Text) # JSON mapping question details
    weak_areas = Column(Text) # JSON list of weak topics
    level_classified = Column(String(20)) # Beginner, Intermediate, Advanced
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")

class LearningBehavior(Base):
    __tablename__ = 'learning_behaviors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    topic = Column(String(100), nullable=False)
    time_spent_minutes = Column(Integer, default=0)
    attempts = Column(Integer, default=1)
    completion_rate = Column(Float, default=0.0) # 0 to 100
    last_active = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="behaviors")

class SystemLog(Base):
    __tablename__ = 'system_logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String(50)) # Auth, Quiz, Study, Admin, Database, System
    action = Column(String(100))
    details = Column(Text)

# --- Database Engine Setup ---

SessionLocal = None
engine = None

def init_db(config_path="db_config.json"):
    global SessionLocal, engine, DB_STATUS
    
    # Default local SQLite file path
    sqlite_db_path = "sqlite:///learning_system.db"
    
    db_uri = sqlite_db_path
    db_type = "sqlite"
    config = {}

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            db_type = config.get("DB_TYPE", "sqlite").lower()
            
            if db_type == "mysql":
                # mysql+pymysql://user:password@host:port/dbname
                db_uri = f"mysql+pymysql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config.get('DB_PORT', 3306)}/{config['DB_NAME']}"
            elif db_type == "postgresql":
                # postgresql+psycopg2://user:password@host:port/dbname
                db_uri = f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config.get('DB_PORT', 5432)}/{config['DB_NAME']}"
            else:
                db_uri = sqlite_db_path
                db_type = "sqlite"
        except Exception as e:
            print(f"Error reading DB configuration: {e}. Falling back to SQLite.")
            db_uri = sqlite_db_path
            db_type = "sqlite"
            DB_STATUS["details"] = f"Config Error: {str(e)}. Defaulted to SQLite."
    
    # Try connecting to the specified DB
    try:
        if db_type == "sqlite":
            engine = create_engine(db_uri, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(db_uri)
        
        # Test connection
        conn = engine.connect()
        conn.close()
        
        DB_STATUS["active_db"] = db_type
        DB_STATUS["status"] = "Connected"
        DB_STATUS["details"] = f"Connected successfully to {db_type} database."
    except Exception as e:
        print(f"Connection to custom database failed: {e}. Falling back to SQLite.")
        # Fallback to local SQLite
        db_type = "sqlite"
        engine = create_engine(sqlite_db_path, connect_args={"check_same_thread": False})
        DB_STATUS["active_db"] = "sqlite (fallback)"
        DB_STATUS["status"] = "Connected (Fallback)"
        DB_STATUS["details"] = f"Failed to connect to custom DB: {str(e)}. Running SQLite local fallback."

    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
        DB_STATUS["tables_created"] = True
    except Exception as e:
        print(f"Failed to create database tables: {e}")
        DB_STATUS["tables_created"] = False
        DB_STATUS["details"] += f" Table creation error: {str(e)}."

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    if SessionLocal is None:
        init_db()
    return SessionLocal()

# Log a system event
def log_event(category, action, details):
    session = get_session()
    try:
        new_log = SystemLog(
            category=category,
            action=action,
            details=details
        )
        session.add(new_log)
        session.commit()
    except Exception as e:
        print(f"Failed to write system log: {e}")
    finally:
        session.close()
