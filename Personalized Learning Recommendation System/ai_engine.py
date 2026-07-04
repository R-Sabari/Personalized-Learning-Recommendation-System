import json

# Curated recommendations library based on topic and difficulty level
RECOMMENDATION_LIBRARY = {
    "Java basics": {
        "Beginner": {
            "videos": [
                {"title": "Java Programming Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=A74TOX803D0", "source": "freeCodeCamp"},
                {"title": "Java Basics & Setup Step-by-Step", "url": "https://www.youtube.com/watch?v=eIrMbAQSU34", "source": "Programming with Mosh"}
            ],
            "pdfs": [
                {"title": "Java Basics Cheat Sheet (PDF)", "url": "https://www.cheat-sheets.org/saved-copy/java-cheat-sheet-v1.pdf", "source": "Cheat-Sheets.org"},
                {"title": "Introduction to Java Notes (PDF)", "url": "https://www.cs.princeton.edu/courses/archive/spr19/cos226/lectures/11Introduction.pdf", "source": "Princeton CS"}
            ],
            "practice": "Solve 10 beginner-level Java syntax exercises on variables and data types."
        },
        "Intermediate": {
            "videos": [
                {"title": "Java Packages, Access Modifiers, and Scope", "url": "https://www.youtube.com/watch?v=hBh_CC5y8-s", "source": "Telusko"}
            ],
            "pdfs": [
                {"title": "Intermediate Java Notes", "url": "https://math.hws.edu/javanotes/", "source": "JavaNotes Online"}
            ],
            "practice": "Build a CLI banking system utilizing multiple packages and scope rules."
        },
        "Advanced": {
            "videos": [
                {"title": "Advanced Java Features: Multithreading & Streams", "url": "https://www.youtube.com/watch?v=gp5aM5Z9jL0", "source": "Java Techie"}
            ],
            "pdfs": [
                {"title": "Java Garbage Collection Tuning Guide (PDF)", "url": "https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/gctuning.pdf", "source": "Oracle Docs"}
            ],
            "practice": "Implement a high-performance multithreaded web scraper in Java."
        }
    },
    "Loops": {
        "Beginner": {
            "videos": [
                {"title": "Loops in Java - For, While, and Do-While", "url": "https://www.youtube.com/watch?v=0983_r4z2rA", "source": "Kunals Kushwaha Tutorials"}
            ],
            "pdfs": [
                {"title": "Iterative Control Flow Guide (PDF)", "url": "https://pages.cs.wisc.edu/~cs302/notes/JavaControlFlow.pdf", "source": "Wisconsin CS"}
            ],
            "practice": "Write programs to print star patterns and generate Fibonacci numbers."
        },
        "Intermediate": {
            "videos": [
                {"title": "Enhancing Performance: Nested Loops vs. Hashing", "url": "https://www.youtube.com/watch?v=AOPGmds8B-E", "source": "NeetCode"}
            ],
            "pdfs": [
                {"title": "Loop Invariants & Analysis (PDF)", "url": "https://web.stanford.edu/class/archive/cs/cs103/cs103.1164/handouts/080%20Loop%20Invariants.pdf", "source": "Stanford CS"}
            ],
            "practice": "Optimize nested array scanning from O(N^2) to O(N) using a Hash Map."
        },
        "Advanced": {
            "videos": [
                {"title": "Parallel Loops and Concurrent Collections", "url": "https://www.youtube.com/watch?v=48-gY5F0Z-0", "source": "Defog Tech"}
            ],
            "pdfs": [
                {"title": "Java Concurrency & Multi-core Loops", "url": "https://www.oracle.com/technical-resources/articles/java/ma14-architect-concurrent.html", "source": "Oracle Technology"}
            ],
            "practice": "Implement a parallel matrix multiplication program using concurrent thread loops."
        }
    },
    "Arrays": {
        "Beginner": {
            "videos": [
                {"title": "Introduction to Arrays in Java/C++", "url": "https://www.youtube.com/watch?v=eXJvIFP10hE", "source": "GeeksforGeeks"}
            ],
            "pdfs": [
                {"title": "Introduction to Arrays Guide (PDF)", "url": "https://www.cs.cmu.edu/~mrmiller/15-110/Handouts/arrays.pdf", "source": "CMU CS"}
            ],
            "practice": "Write code to find the maximum, minimum, and average elements in a user-input array."
        },
        "Intermediate": {
            "videos": [
                {"title": "Two-Pointer Techniques & Sliding Window on Arrays", "url": "https://www.youtube.com/watch?v=HtSuA80DuPI", "source": "NeetCode"}
            ],
            "pdfs": [
                {"title": "Sliding Window and Two Pointer Methods (PDF)", "url": "https://web.stanford.edu/class/cs9/lectures/sliding-window.pdf", "source": "Stanford CS"}
            ],
            "practice": "Solve the maximum sum subarray (Kadane's Algorithm) and 2-Sum problem."
        },
        "Advanced": {
            "videos": [
                {"title": "Sparse Arrays, Segment Trees, and Fenwick Trees", "url": "https://www.youtube.com/watch?v=2FShdqn-k80", "source": "Tushar Roy"}
            ],
            "pdfs": [
                {"title": "Dynamic Array Resizing & Cost Analysis (PDF)", "url": "https://inst.eecs.berkeley.edu/~cs61b/fa20/materials/lectures/lect18.pdf", "source": "UC Berkeley CS"}
            ],
            "practice": "Implement a Segment Tree to handle dynamic range minimum queries in O(log N) time."
        }
    },
    "OOP concepts": {
        "Beginner": {
            "videos": [
                {"title": "Object-Oriented Programming (OOP) Explained in 10 Minutes", "url": "https://www.youtube.com/watch?v=pTB0EiLXFMc", "source": "Mosh Hamedani"}
            ],
            "pdfs": [
                {"title": "Object-Oriented Programming Principles (PDF)", "url": "https://pages.cs.wisc.edu/~hasti/cs302/examples/OOPconceptSummary.pdf", "source": "Wisconsin CS"}
            ],
            "practice": "Create classes representing real-world objects using inheritance and encapsulation."
        },
        "Intermediate": {
            "videos": [
                {"title": "Interfaces, Abstract Classes, and Polymorphism in Depth", "url": "https://www.youtube.com/watch?v=lhELGQAvyCI", "source": "Corey Schafer"}
            ],
            "pdfs": [
                {"title": "SOLID Design Principles Detailed Handbook (PDF)", "url": "https://www.cs.colorado.edu/~kena/classes/5448/f12/presentation-materials/solid.pdf", "source": "Colorado CS"}
            ],
            "practice": "Design a payment gateway simulator supporting multiple providers using polymorphism."
        },
        "Advanced": {
            "videos": [
                {"title": "Creational, Structural, and Behavioral Design Patterns", "url": "https://www.youtube.com/watch?v=v9ejT8FO-7I", "source": "Christopher Okhravi"}
            ],
            "pdfs": [
                {"title": "Design Patterns Handbook Reference (PDF)", "url": "https://www.cs.unc.edu/~stotts/comp524/patterns.pdf", "source": "UNC CS"}
            ],
            "practice": "Implement an event-driven system using the Observer and Factory design patterns."
        }
    },
    "Quantitative Aptitude": {
        "Beginner": {
            "videos": [
                {"title": "Quantitative Aptitude Basics: Percentages & Ratios", "url": "https://www.youtube.com/watch?v=04d3jG5L9Xk", "source": "CareerRide"}
            ],
            "pdfs": [
                {"title": "Quant Formulas Reference Cheat Sheet (PDF)", "url": "https://d2cyt36b7wnvt9.cloudfront.net/exams/wp-content/uploads/2021/09/23171804/Quantitative-Aptitude-Formula-Sheet.pdf", "source": "Formula Sheets Guide"}
            ],
            "practice": "Solve 20 fundamental questions on ratio, proportion, percentages, and simple interest."
        },
        "Intermediate": {
            "videos": [
                {"title": "Time, Speed, Distance & Work Short Tricks", "url": "https://www.youtube.com/watch?v=q6g3tB6Vp4g", "source": "Feel Free to Learn"}
            ],
            "pdfs": [
                {"title": "Intermediate Quantitative Aptitude Practice Book", "url": "https://www.careerbless.com/aptitude/qa/home.php", "source": "RS Aggarwal Selected Notes"}
            ],
            "practice": "Practice complex relative speed problems (trains, boats & streams) and work sharing."
        },
        "Advanced": {
            "videos": [
                {"title": "Permutations, Combinations & Probability Advanced", "url": "https://www.youtube.com/watch?v=mDylUvF3j_g", "source": "Wifistudy"}
            ],
            "pdfs": [
                {"title": "Introductory Probability Textbook (PDF)", "url": "https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/amsbook.mac.pdf", "source": "Dartmouth Math"}
            ],
            "practice": "Solve advanced probability problems and multi-dataset bar/radar chart calculations."
        }
    },
    "Logical reasoning": {
        "Beginner": {
            "videos": [
                {"title": "Logical Reasoning: Syllogisms & Blood Relations", "url": "https://www.youtube.com/watch?v=zR0C4G9m-f0", "source": "Adda247"}
            ],
            "pdfs": [
                {"title": "Logical Deductions & Syllogism Guide (PDF)", "url": "https://www.law.nyu.edu/sites/default/files/Syllogisms%20Guide.pdf", "source": "NYU Law"}
            ],
            "practice": "Complete 15 puzzles on directional sense, blood relations, and coding-decoding."
        },
        "Intermediate": {
            "videos": [
                {"title": "Seating Arrangements & Puzzle Solving Strategies", "url": "https://www.youtube.com/watch?v=B1b_aTq_Jks", "source": "Unacademy"}
            ],
            "pdfs": [
                {"title": "Logical reasoning questions and answers", "url": "https://www.indiabix.com/logical-reasoning/questions-and-answers/", "source": "IndiaBix Prep"}
            ],
            "practice": "Solve 5 double-row seating arrangement puzzles with multiple attributes."
        },
        "Advanced": {
            "videos": [
                {"title": "Critical Reasoning: Arguments, Assumptions & Conclusions", "url": "https://www.youtube.com/watch?v=d_k8zZ2p34w", "source": "Meritshine"}
            ],
            "pdfs": [
                {"title": "Formal Symbolic Logic Cheat Sheet (PDF)", "url": "https://www.princeton.edu/~harman/Logic/symbolic-logic.pdf", "source": "Princeton Philosophy"}
            ],
            "practice": "Evaluate complex syllogisms, weak/strong argument cases, and binary logic riddles."
        }
    }
}

# --- Core Profiling Functions ---

def classify_student(score_percentage):
    """
    Score Level
    0-40: Beginner
    41-70: Intermediate
    71-100: Advanced
    """
    if score_percentage <= 40:
        return "Beginner"
    elif score_percentage <= 70:
        return "Intermediate"
    else:
        return "Advanced"

def identify_weak_areas(quiz_results):
    """
    Analyzes quiz results dict (question ID to boolean correctness)
    Returns list of weak topics
    """
    # Mapping of question topics:
    # Q1: Java basics, Q2: Loops, Q3: Arrays, Q4: OOP concepts, Q5: Quantitative Aptitude, Q6: Logical reasoning
    topic_mapping = {
        "q1": "Java basics",
        "q2": "Loops",
        "q3": "Arrays",
        "q4": "OOP concepts",
        "q5": "Quantitative Aptitude",
        "q6": "Logical reasoning"
    }
    
    weak_topics = []
    for q_id, correct in quiz_results.items():
        if not correct and q_id in topic_mapping:
            weak_topics.append(topic_mapping[q_id])
            
    return weak_topics

def project_academic_performance(current_cgpa, study_hours, quiz_score, max_scale=10.0):
    """
    Predicts a projected CGPA base on current performance metrics.
    Handles standard GPA (4.0 scale) and Indian CGPA (10.0 scale) dynamically.
    """
    scale = 10.0 if current_cgpa > 4.0 else 4.0
    
    # Baseline projection begins with current CGPA
    projection = current_cgpa
    
    # Study hour factor: target is 3 hours a day
    study_factor = (study_hours - 3.0) * (0.05 if scale == 4.0 else 0.12)
    
    # Quiz factor: target is 70%
    quiz_factor = (quiz_score - 70.0) * (0.005 if scale == 4.0 else 0.015)
    
    # Calculate projection
    projected = current_cgpa + study_factor + quiz_factor
    
    # Clamp results to valid bounds
    projected = max(0.0, min(scale, projected))
    
    return round(projected, 2), scale

def generate_recommendations(weak_topics, level):
    """
    Returns curated course recommendations based on user level and weak areas.
    If a topic is weak, returns 'Beginner' or 'Intermediate' contents to help build core.
    If strong (not in weak areas), returns 'Advanced' or 'Intermediate' content to challenge.
    """
    recs = []
    all_topics = ["Java basics", "Loops", "Arrays", "OOP concepts", "Quantitative Aptitude", "Logical reasoning"]
    
    for topic in all_topics:
        is_weak = topic in weak_topics
        # Determine recommended level for this topic
        if is_weak:
            # If the user is Advanced but failed this topic, recommend Intermediate. Else recommend Beginner.
            rec_level = "Intermediate" if level == "Advanced" else "Beginner"
        else:
            # If the user passed and is at least Intermediate, recommend Advanced. Else recommend Intermediate.
            rec_level = "Advanced" if level in ["Intermediate", "Advanced"] else "Intermediate"
            
        topic_library = RECOMMENDATION_LIBRARY.get(topic, {}).get(rec_level, {})
        
        if topic_library:
            recs.append({
                "topic": topic,
                "status": "Needs Review" if is_weak else "Proficient",
                "recommended_level": rec_level,
                "videos": topic_library.get("videos", []),
                "pdfs": topic_library.get("pdfs", []),
                "practice": topic_library.get("practice", "")
            })
            
    return recs

# --- AI Chat Study Assistant Chatbot Response Simulator ---

def get_chatbot_response(question, user_profile):
    """
    Simulates a highly specialized AI tutor that adapts answers
    to the student's level, career interests, and academic background.
    """
    question_lower = question.lower()
    
    name = user_profile.get("first_name", "Student")
    level = user_profile.get("level", "Beginner")
    weak_topics = user_profile.get("weak_topics", [])
    career = user_profile.get("career", "Software Developer")
    
    # Specialized answers for key concepts
    if "recursion" in question_lower:
        return f"""### Hello {name}! Let's master **Recursion** together. 💡

Since your career target is **{career}** and your current level is **{level}**, I've formulated a visual guide.

#### What is Recursion?
Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem. Think of it like looking into a mirror reflecting another mirror!

Every recursive function MUST have two parts:
1. **Base Case:** The condition under which the function stops calling itself (without this, you get a `StackOverflowError`!).
2. **Recursive Step:** The part where the function calls itself with a reduced parameter.

#### Code Example (Factorial in Java/Python):
```python
def factorial(n):
    # 1. Base Case
    if n <= 1:
        return 1
    # 2. Recursive Step
    return n * factorial(n - 1)
```

#### Mini-Quiz Challenge for You:
What happens if you run `factorial(5)`?
* A) It runs infinitely.
* B) It returns `120` after 5 stack frames.
* C) It crashes.
*(Reply with your explanation, and I will check your code!)*"""

    elif "sql join" in question_lower or "join" in question_lower:
        return f"""### Let's crack **SQL Joins**, {name}! 🗄️

As a budding **{career}**, managing relational data is a crucial skill. Let's break down SQL Joins visually.

#### The Core Types of SQL Joins:
1. **INNER JOIN:** Returns records that have matching values in both tables. (Intersections)
2. **LEFT JOIN:** Returns all records from the left table, and matched records from the right. (Unmatched right cells are `NULL`)
3. **RIGHT JOIN:** Returns all records from the right table, and matched records from the left.
4. **FULL JOIN:** Returns all records when there is a match in either left or right table.

#### Visual Diagram:
```
   Table A [Left]          Table B [Right]
  [ID | Name   ]          [ID | Dept   ]
  [1  | Alice  ]   <--->  [1  | Eng    ]  <-- MATCH!
  [2  | Bob    ]          [3  | Sales  ]
```

#### SQL Query Example:
```sql
SELECT users.first_name, academic_profiles.department
FROM users
INNER JOIN academic_profiles ON users.id = academic_profiles.user_id;
```

#### Practice Problem:
If Table A has 3 rows and Table B has 4 rows, what is the maximum number of rows a LEFT JOIN could return?
*(Hint: Think about what happens if all records map or no records map!)*"""

    elif "loop" in question_lower:
        return f"""### Master Iteration: **Loops & Control Flow** 🔄

Hello {name}! Loops are the engine of software logic. Since your profile indicates **{level}** level competency, let's look at loop structures.

#### 1. For Loop (Count-Controlled)
Best used when you know *exactly* how many times you need to repeat a block of code.
```java
for (int i = 0; i < 5; i++) {{
    System.out.println("Iteration: " + i);
}}
```

#### 2. While Loop (Condition-Controlled)
Repeats as long as a boolean expression remains true. Check the condition *before* executing.
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

#### Pro-Tip for {level}s:
Make sure your loop variables always progress towards the stopping condition to avoid **Infinite Loops**, which hang the memory of your program!

What topic would you like me to explain next? Arrays, OOP, or Logical Reasoning? Let me know!"""

    elif "oop" in question_lower or "object" in question_lower or "class" in question_lower:
        return f"""### The 4 Pillars of **OOP (Object-Oriented Programming)** 🏛️

OOP is the backbone of languages like Java, C++, and Python. Let's look at the core principles:

1. **Encapsulation:** Wrapping variables and methods inside a class and hiding details (using `private` fields and public getters/setters).
2. **Inheritance:** Enabling a new class (child) to acquire properties of an existing class (parent). Keeps code *DRY (Don't Repeat Yourself)*.
3. **Polymorphism:** "Many forms." Allowing different classes to respond to the same method call in their own unique way (Method Overriding).
4. **Abstraction:** Hiding complex implementation details and showing only the essential features (using abstract classes/interfaces).

#### Code Challenge:
Can you name a scenario where you would use an `Interface` instead of an `Abstract Class`? 
*(Let's discuss. Write your thoughts below!)*"""

    elif "array" in question_lower:
        return f"""### Understanding **Arrays & Memory Offsets** 📊

An array is a linear data structure that stores elements of the same type in contiguous memory locations.

#### Key Characteristics:
* **Index-Based:** First element is at index `0`, last at `length - 1`.
* **Fixed Size:** Once created, you cannot dynamically change its size.
* **Random Access:** You can read any index instantly in O(1) time.

```python
# Declaring a simple array in Python
grades = [92, 85, 78, 90, 88]
print(grades[0]) # Output: 92 (Instant access!)
```

#### Career Insights for a future **{career}**:
When arrays are insufficient due to size limitations, we switch to **Dynamic Arrays** (like `ArrayList` in Java or `vector` in C++) or **Linked Lists**. Since you are working at **{level}** level, knowing when to choose an array over a linked list is a vital design interview question!

Would you like a sample problem on array scanning?"""

    # Fallback default AI response tailored to their profile
    weak_area_str = ", ".join(weak_topics) if weak_topics else "None! Outstanding job."
    return f"""### Personalized AI Study Guide 🚀

Hi **{name}**, I am your AI learning assistant. I have reviewed your profile and current study metrics:
* **Current Skill Classification:** `{level}`
* **Career Goal:** `{career}`
* **Detected Weak Areas:** `{weak_area_str}`

#### Study Recommendation:
{"I suggest we start with basic coding loops or OOP principles to build a solid foundation." if level == "Beginner" else "Let's focus on logic puzzles or advanced array optimizations to bump your score to the next tier."}

Ask me any specific question you have! For example:
* *"Explain Recursion with examples"*
* *"Help me understand SQL Joins"*
* *"Give me a practice problem on For Loops"*"""
