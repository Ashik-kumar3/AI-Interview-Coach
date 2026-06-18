# AI Interview Coach

## Project Overview

Many students and fresh graduates have strong technical knowledge but struggle to perform effectively in interviews due to poor communication, weak eye contact, nervous body language, and lack of interview practice. As a result, they often face rejection despite having the required skills.

AI Interview Coach is an intelligent interview preparation system that helps candidates assess and improve their interview performance. Using Computer Vision and Speech Analysis, it evaluates eye contact, head movements, posture, speaking pace, and filler word usage while answering interview questions.

The system generates a performance report with actionable feedback, helping candidates identify weaknesses, track improvement, and build confidence before real interviews.


---

## Features

### Computer Vision Analysis

* Eye Contact Detection
* Head Pose Analysis
* Posture Analysis
* Confidence Score Calculation

### Interview Simulation

* Real-Time Interview Question Display
* Question Progress Tracking
* Interview Duration Tracking

### Speech Analysis

* Audio Recording
* Speech-to-Text Transcription using Faster Whisper
* Words Per Minute (WPM) Calculation
* Filler Word Detection
* Communication Score Calculation

### Reporting

* Automated Interview Report Generation
* Performance Metrics Summary
* Interview Questions Tracking
* Report Saving in Text Format

---

## Project Workflow

1. Start the interview session.
2. Interview questions are displayed on the screen.
3. MediaPipe tracks eye contact, head movement, and posture.
4. Audio is recorded and analyzed.
5. Speech is transcribed using Faster Whisper.
6. Communication metrics are calculated.
7. A final interview report is generated automatically.

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* Faster Whisper
* NumPy
* SciPy
* SoundDevice

---

## Project Structure

```text
AI_Interview_Coach/
│
├── assets/
│   └── questions.txt
│
├── modules/
│   ├── confidence.py
│   ├── eye_contact.py
│   ├── head_pose.py
│   ├── posture.py
│   ├── questions.py
│   ├── report.py
│   └── speech_analysis.py
│
├── recordings/
├── reports/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI_Interview_Coach
```

Create a virtual environment:

```bash
python -m venv env
```

Activate the environment:

### Windows

```bash
env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python main.py
```

Press:

```text
Q
```

to end the interview session and generate the report.

---

## Sample Report

```text
===================================

INTERVIEW REPORT

===================================

Interview Duration : 52 seconds

Eye Contact Score : 81%
Head Stability Score : 1%
Posture Score : 79%
Confidence Score : 53.65%

Speech Analysis

Speaking Speed : 85.38 WPM
Filler Words : 1
Communication Score : 84.0%

Interview Questions Asked:

- Tell me about yourself.
- Explain one of your projects.

Overall Rating : Average

===================================
```

---

## Future Improvements

* Simultaneous Audio and Video Recording
* Streamlit Web Interface
* PDF Report Generation
* Interview Transcript Export
* Personalized Feedback Suggestions
* Advanced Communication Analytics
