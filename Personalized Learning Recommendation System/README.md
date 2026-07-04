# Personalized Learning Recommendation System 🎓

A full-stack AI-powered adaptive learning platform that tailors content recommendations to individual learners based on their performance, preferences, and learning patterns.

## 🚀 Features

- **AI-Powered Recommendations** — Uses ML-based AI engine to personalize content delivery
- **Adaptive Assessments** — Dynamic quiz and assessment system that adjusts to learner level
- **Student Dashboard** — Visual progress tracking, skill maps, and performance analytics
- **Admin Dashboard** — Manage users, content, and monitor platform-wide learning metrics
- **Flask Backend** — Lightweight Python web server with SQLite persistence
- **Responsive UI** — Clean, mobile-friendly HTML/CSS frontend

## 🛠️ Tech Stack

| Layer        | Technology               |
|--------------|--------------------------|
| Backend      | Python 3, Flask           |
| AI Engine    | Custom ML recommendation  |
| Database     | SQLite (via SQLAlchemy)   |
| Frontend     | HTML5, CSS3, JavaScript   |
| Templating   | Jinja2                    |

## 📁 Project Structure

```
Personalized-Learning-Recommendation-System/
├── app.py                  # Flask application entry point
├── ai_engine.py            # AI recommendation engine
├── database.py             # Database models and helpers
├── db_config.json          # Database configuration
├── templates/
│   ├── index.html          # Landing / login page
│   ├── dashboard.html      # Student dashboard
│   ├── assessment.html     # Assessment / quiz page
│   └── admin_dashboard.html # Admin panel
└── static/
    └── css/
        └── styles.css      # Global stylesheet
```

## ⚙️ Setup & Run

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/R-Sabari/Personalized-Learning-Recommendation-System.git
cd Personalized-Learning-Recommendation-System

# Install dependencies
pip install flask

# Run the application
python app.py
```

### Access
Open your browser at: **http://localhost:5000**

## 📊 How It Works

1. **Learner Registration** — Users sign up and complete an initial skill assessment
2. **AI Analysis** — The AI engine analyses performance data and builds a learner profile
3. **Content Recommendation** — Personalised learning paths are generated dynamically
4. **Continuous Adaptation** — Recommendations update in real-time as learners progress

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## 📄 License

This project is open-source under the [MIT License](LICENSE).
