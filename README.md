# SkillTrack 🚀
### Personal Skill & Career Readiness Tracker

> **"Track your skills. Prove your projects. Measure your job readiness."**

---

## 📌 Project Description & Purpose

**SkillTrack** is a career-readiness web application for students. It helps a student understand how prepared they are for a target job role by comparing:

1. **Required job-role skills**
2. **Current self-assessed skill proficiency**
3. **Project-based skill evidence**
4. **Placement fundamentals**

Rather than simply displaying an arbitrary percentage, SkillTrack answers:
- What skills does my target role require?
- How strong am I in each skill?
- Which skills have I actually demonstrated through projects?
- How strong are my placement fundamentals?
- How job-ready am I overall?
- What should I improve next?

---

## 💡 Problem Statement & Solution

- **The Problem**: Students often struggle to assess whether they are truly ready for entry-level tech roles. Relying solely on course completion or theoretical study leaves huge gaps in practical project evidence and core placement fundamentals.
- **The Solution**: SkillTrack provides a dynamic gap analysis engine that correlates self-assessed skill proficiencies, GitHub-verified project evidence, and computer science placement fundamentals into a unified, actionable readiness index.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | HTML5, Vanilla CSS3 (Custom Grid/Flexbox, Glassmorphic Dark UI), Vanilla JavaScript (ES6 `fetch`) |
| **Backend** | Core Python 3 (Standard Library only — `http.server`, `json`, `urllib.parse`, `unittest`) |
| **HTTP Communication** | Custom `BaseHTTPRequestHandler` implementation over standard HTTP |
| **Data Storage** | Local JSON files (`data/roles.json`, `data/user_data.json`) |
| **Testing** | Built-in Python `unittest` module |

> **Note on Architecture Choice**:  
> Version 2 intentionally uses Python's built-in `http.server` module instead of external frameworks like Flask, Django, or FastAPI. This project was developed to strengthen **Core Python fundamentals** while learning HTML, CSS, JavaScript, and HTTP communication protocols without hiding business logic behind framework abstractions.

---

## 🏗️ Application Architecture

```
                    SkillTrack
                        |
              +---------+---------+
              |                   |
              v                   v
          FRONTEND             PYTHON
              |                   |
      HTML/CSS/JavaScript    Core Python
              |                   |
              +--------HTTP-------+
                        |
                        v
                      JSON
                        |
                        v
                   Local Files
```

### Server & API Architecture:
```
Browser (Vanilla JS fetch)
   │
   ├── GET  /                  -> Serves frontend static index.html
   ├── GET  /api/roles         -> Returns role templates (Data Analyst, Web Dev, etc.)
   ├── GET  /api/user          -> Returns current user profile data
   ├── GET  /api/readiness     -> Calculates & returns numerical readiness metrics
   ├── GET  /api/analysis      -> Returns skill-gap & recommendation analysis
   ├── POST /api/user/role     -> Switches target job role template
   ├── POST /api/skills        -> Adds a custom skill
   ├── PUT  /api/skills        -> Updates skill proficiencies
   ├── DELETE /api/skills      -> Deletes a custom skill
   ├── POST /api/projects      -> Adds project (Enforces max 5, GitHub link mandatory)
   ├── PUT  /api/projects      -> Updates an existing project
   ├── DELETE /api/projects    -> Deletes a project
   └── PUT  /api/fundamentals  -> Updates placement fundamental scores
```

---

## 📐 Calculation Formulas

SkillTrack executes all mathematical and analytical calculations entirely on the Core Python backend:

1. **Skill Readiness (50% Weight)**:
   $$\text{Skill Readiness} = \frac{\sum \text{Proficiency of Required Skills}}{\text{Total Required Skills}}$$

2. **Project Skill Coverage**:
   $$\text{Coverage \%} = \frac{\text{Unique Required Skills Demonstrated in Projects}}{\text{Total Required Skills}} \times 100$$

3. **Project Readiness (30% Weight)**:
   $$\text{Project Readiness} = (\text{Completion \%} \times 0.20) + (\text{GitHub Evidence \%} \times 0.20) + (\text{Skill Coverage \%} \times 0.60)$$
   *Note: Completion % is calculated as $\frac{\text{Project Count}}{5} \times 100$. GitHub Evidence % measures valid GitHub URLs.*

4. **Placement Readiness (20% Weight)**:
   $$\text{Placement Readiness} = \frac{\sum \text{Proficiency of Placement Fundamentals}}{\text{Total Fundamentals}}$$

5. **Overall Job Readiness**:
   $$\text{Overall Job Readiness} = (\text{Skill Readiness} \times 0.50) + (\text{Project Readiness} \times 0.30) + (\text{Placement Readiness} \times 0.20)$$

---

## 📂 Project Structure

```
SkillTrack/
│
├── backend/
│   ├── main.py          # Application entry point (Server launcher)
│   ├── server.py        # Custom BaseHTTPRequestHandler implementation
│   ├── models.py        # Core Python OOP classes (Skill, Project, Role, Profile)
│   ├── calculator.py    # Readiness calculations logic
│   ├── analysis.py      # Rule-based skill-gap & priority recommendation engine
│   ├── storage.py       # JSON file reading/writing layer with exception safety
│   └── validation.py   # Backend parameter & project constraint validation
│
├── frontend/
│   ├── index.html       # Single-page application structure & modals
│   ├── css/
│   │   └── style.css    # Custom glassmorphic styling, progress bars & themes
│   └── js/
│       └── app.js       # UI state management & REST API fetch communication
│
├── data/
│   ├── roles.json       # Predefined job role skill templates
│   └── user_data.json   # Persistent local user state
│
├── tests/
│   ├── test_models.py
│   ├── test_calculator.py
│   ├── test_analysis.py
│   ├── test_validation.py
│   └── test_storage.py
│
├── README.md
└── .gitignore
```

---

## ⚡ How to Run SkillTrack (GitHub Quick Start)

### Prerequisites
- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/)).
- **Zero Third-Party Dependencies**: No `pip install` required! Uses Python's built-in standard library only.
- Any modern web browser (Chrome, Firefox, Edge, Safari).

### 🚀 Quick Start (Clone & Run)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chintalasiri8-code/SkillTrack.git
   cd SkillTrack
   ```

2. **Run the application**:
   - **Cross-Platform (Any OS)**:
     ```bash
     python run.py
     ```
   - **Windows (1-Click)**:
     Double-click `run.bat` or run in CMD:
     ```cmd
     run.bat
     ```
   - **macOS / Linux (1-Click)**:
     ```bash
     chmod +x run.sh
     ./run.sh
     ```

3. **Open in Browser**:
   Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 🧪 Running Unit Tests

Run the full automated test suite using Python's built-in `unittest` module:
```bash
python -m unittest discover -s tests
```

---

## 🔮 Future Improvements (Version 3 Scope)

In future releases after mastering web frameworks:
- **Framework Migration**: Migrate backend to Flask or FastAPI for production routing.
- **Database Storage**: Replace local JSON storage with SQLite / PostgreSQL.
- **GitHub API Integration**: Verify repository existence, commit frequency, and language breakdown live via GitHub API.
- **Authentication**: Multi-user accounts with secure password hashing.
- **Visual Analytics**: Interactive radar and trend charts.

---

## 🎓 Learning Outcomes
- Applied Object-Oriented Programming (OOP) in Core Python without frameworks.
- Created custom HTTP endpoints using Python's standard library `http.server`.
- Built clean client-server communication using JavaScript `fetch()`.
- Implemented robust backend validation and persistent JSON file handling.
- Designed a modern, accessible UI with CSS Grid and Flexbox.
