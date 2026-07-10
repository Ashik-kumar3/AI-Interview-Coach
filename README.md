# 🎤 AI Interview Coach - Intelligent Interview Preparation Platform

## Project Overview

Many students and fresh graduates have strong technical knowledge but struggle to perform effectively in interviews due to poor communication, weak eye contact, nervous body language, and lack of interview practice. As a result, they often face rejection despite having the required skills.

AI Interview Coach is an intelligent interview preparation system that helps candidates assess and improve their interview performance. Using Computer Vision, Speech Recognition, and Natural Language Processing (NLP), it evaluates eye contact, head stability, posture, communication skills, and answer quality during HR and technical interviews. The system generates detailed performance reports with personalized feedback, enabling users to identify weaknesses, monitor improvement, and build confidence before real interviews.

---

# 🚀 Features

## 🎥 Real-Time Computer Vision Analysis

- Eye Contact Detection
- Head Stability Analysis
- Posture Analysis
- Confidence Score Calculation
- Live Performance Metrics

---

## 🎤 Speech Analysis

- Audio Recording
- Speech-to-Text Transcription using Faster Whisper
- Speaking Speed (Words Per Minute)
- Filler Word Detection
- Communication Score Calculation

---

## 🧠 AI Answer Evaluation

### HR Interview Evaluation

- Soft Skill Assessment
- Communication Quality Analysis
- Motivation Detection
- Personalized HR Feedback

### Technical Interview Evaluation

- Semantic Similarity Scoring
- Keyword Matching
- Missing Concept Detection
- Technical Answer Evaluation
- Question-wise Performance Analysis

---

## 📄 Automated Report Generation

- Interview Summary
- Question-wise Performance Report
- Communication Metrics
- Confidence Analysis
- Personalized Feedback
- Downloadable PDF Report

---

## 💻 Interactive Streamlit Dashboard

- Live Webcam Feed
- Live Computer Vision Analysis
- Interview Question Navigation
- Real-Time Transcript Display
- Answer Evaluation Panel
- PDF Report Download

---

# 🔄 Project Workflow

1. Start a new interview session.
2. Select the interview mode:
   - HR Interview
   - Technical Interview
   - HR + Technical Interview
3. Answer interview questions while maintaining eye contact.
4. MediaPipe analyzes facial landmarks and posture in real time.
5. Audio is recorded and transcribed using Faster Whisper.
6. HR or Technical answers are automatically evaluated.
7. Performance metrics are calculated.
8. A detailed interview report and downloadable PDF are generated.

---

# 🛠 Tech Stack

### Programming Language

- Python

### Frontend

- Streamlit

### Computer Vision

- OpenCV
- MediaPipe

### Speech Recognition

- Faster Whisper

### Natural Language Processing

- Sentence Transformers
- Transformers
- Scikit-learn

### Deep Learning

- PyTorch

### Report Generation

- ReportLab

---

# 📂 Project Structure

```text
AI_Interview_Coach/
│
├── assets/
│   ├── answer_key.json
│   ├── hr_questions.txt
│   └── technical_questions.txt
│
├── modules/
│   ├── analysis.py
│   ├── answer_evaluator.py
│   ├── camera.py
│   ├── hr_evaluator.py
│   ├── interview_manager.py
│   ├── interview_session.py
│   ├── pdf_report.py
│   ├── questions.py
│   ├── report.py
│   └── speech_analysis.py
│
├── recordings/
├── reports/
│
├── streamlit_app.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/AI-Interview-Coach.git
```

Move into the project directory

```bash
cd AI-Interview-Coach
```

Create a virtual environment

```bash
python -m venv env
```

### Activate Virtual Environment

**Windows**

```bash
env\Scripts\activate
```

**Linux / macOS**

```bash
source env/bin/activate
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Application

Launch the Streamlit application

```bash
streamlit run streamlit_app.py
```

The legacy OpenCV-based version is also available:

```bash
python main.py
```

---

# 📊 Current Capabilities

- ✅ HR Interview Simulation
- ✅ Technical Interview Simulation
- ✅ Mixed Interview Mode
- ✅ Real-Time Eye Contact Detection
- ✅ Head Stability Analysis
- ✅ Posture Detection
- ✅ Confidence Score Calculation
- ✅ Faster Whisper Speech Recognition
- ✅ HR Answer Evaluation
- ✅ Technical Answer Evaluation
- ✅ Question-wise Feedback
- ✅ Automated PDF Report Generation
- ✅ Interactive Streamlit Interface

---

# 📄 Sample Output

The system automatically generates a professional interview report containing:

- Interview Summary
- Question-wise Scores
- Speech Analysis
- Eye Contact Score
- Head Stability Score
- Posture Score
- Confidence Score
- Personalized Feedback
- Downloadable PDF Report

---

# 🚀 Future Improvements

- Resume-based personalized interview questions
- LLM-powered answer evaluation
- Emotion detection using facial expressions
- Voice tone and sentiment analysis
- Interview performance analytics dashboard
- Interview history tracking
- Cloud deployment
- Multi-language interview support

---

# 👨‍💻 Author

**Ashik Kumar**

AI/ML Engineer
