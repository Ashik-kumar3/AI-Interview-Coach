import streamlit as st
import time
from modules.questions import load_questions
from streamlit_webrtc import webrtc_streamer
from modules.camera import VideoProcessor
from modules.analysis import analysis
from modules.speech_analysis import (
    start_recording,
    stop_recording,
    speech_to_text
)
from modules.answer_evaluator import evaluate_answer
from modules.hr_evaluator import evaluate_hr_answer
from modules.interview_session import InterviewSession

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

# ---------------- Header ----------------

st.title("🎤 AI Interview Coach")

st.caption(
    "AI-Powered Interview Preparation Platform"
)

st.info(
    "Practice HR and Technical interviews with real-time Computer Vision and Speech Analysis."
)

st.divider()

# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("🎤 AI Interview Coach")

    st.markdown("---")

    interview_mode = st.radio(
        "Interview Mode",
        [
            "HR Interview",
            "Technical Interview",
            "HR + Technical Interview"
        ]
    )

    st.markdown("---")

    st.subheader("🖥 System Status")

    st.success("📷 Camera Ready")

    st.success("🎤 Microphone Ready")

    st.success("🤖 Faster Whisper")

    st.success("📄 PDF Report Enabled")

    # Load questions according to interview mode

    if interview_mode == "HR Interview":

        questions = load_questions(
            "assets/hr_questions.txt"
        )

    elif interview_mode == "Technical Interview":

        questions = load_questions(
            "assets/technical_questions.txt"
        )

    else:

        hr_questions = load_questions(
            "assets/hr_questions.txt"
        )

        technical_questions = load_questions(
            "assets/technical_questions.txt"
        )

        questions = hr_questions + technical_questions

    st.markdown("---")

st.subheader("📊 Interview Dashboard")

card1, card2, card3, card4 = st.columns(4)

with card1:

    st.metric(
        "⏱ Duration",
        "10-15 min"
    )

with card2:

    st.metric(
        "📷 Camera",
        "Ready"
    )

with card3:

    st.metric(
        "🎤 Mic",
        "Ready"
    )

with card4:

    st.metric(
        "🤖 Whisper",
        "Active"
    )

st.markdown("---")

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False 

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "audio_stream" not in st.session_state:
    st.session_state.audio_stream = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "answer_score" not in st.session_state:
    st.session_state.answer_score = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "keywords_found" not in st.session_state:
    st.session_state.keywords_found = []

if "missing_keywords" not in st.session_state:
    st.session_state.missing_keywords = []

if "interview_session" not in st.session_state:
    st.session_state.interview_session = InterviewSession()

if st.button(
    "▶ Start Interview",
    use_container_width=True
):
    st.session_state.interview_started = True
    st.session_state.question_index = 0
    st.session_state.start_time = time.time()
    st.rerun()

st.divider()

st.info(
    "This AI Interview Coach evaluates communication skills, body language, eye contact, posture and speaking performance to help candidates prepare for real interviews."
)

# ---------------- Interview Screen ----------------


if st.session_state.interview_started:

    st.subheader("🎯 Current Question")

    st.success(
        questions[
            st.session_state.question_index
        ]
    )

    st.caption(
        "Answer naturally while looking at the camera."
    )

    
    progress = (
        st.session_state.question_index + 1
    ) / len(questions)

    st.progress(progress)

    elapsed = int(
        time.time() -
        st.session_state.start_time
    )

    minutes = elapsed // 60
    seconds = elapsed % 60

    remaining = (
        len(questions)
        - st.session_state.question_index
        - 1
    )

    progress_col1, progress_col2, progress_col3 = st.columns(3)

    with progress_col1:
        st.metric(
            "⏱ Duration",
            f"{minutes:02d}:{seconds:02d}"
        )

    with progress_col2:
        st.metric(
            "📄 Question",
            f"{st.session_state.question_index + 1}/{len(questions)}"
        )

    with progress_col3:
        st.metric(
            "📌 Remaining",
            remaining
        )

    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("📷 Live Interview")

        webrtc_streamer(
            key="camera",
            video_processor_factory=VideoProcessor,
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
        )
        
        st.markdown("### 🎤 Audio Recording")

        r1, r2 = st.columns(2)

        with r1:

            if st.button(
                "🎙 Start Recording",
                use_container_width=True
            ):

                if st.session_state.audio_stream is None:

                    st.session_state.audio_stream = start_recording()

                    st.success("Recording Started")

        with r2:

            if st.button(
                "⏹ Stop Recording",
                use_container_width=True
            ):

                if st.session_state.audio_stream is not None:

                    audio_file = stop_recording(
                        st.session_state.audio_stream
                    )
                          
                    st.session_state.audio_stream = None

                    transcript = speech_to_text(
                        audio_file
                    )

                    st.session_state.transcript = transcript

                    current_question = questions[
                        st.session_state.question_index
                    ]

                    if interview_mode == "HR Interview":

                        score, feedback = evaluate_hr_answer(
                            current_question,
                            transcript
                        )

                        st.session_state.answer_score = score
                        st.session_state.feedback = feedback

                        st.session_state.keywords_found = []
                        st.session_state.missing_keywords = []

                    else:

                        score, found, missing, feedback = evaluate_answer(
                            current_question,
                            transcript
                        )

                        st.session_state.answer_score = score
                        st.session_state.feedback = feedback
                        st.session_state.keywords_found = found
                        st.session_state.missing_keywords = missing

                    st.success("Recording Completed")

                    st.rerun()

        st.markdown("### Interview Controls")

        if st.session_state.transcript:

            st.subheader("📝 Transcript")

            st.text_area(

                "Answer",

                st.session_state.transcript,

                height=150

            )

        if st.session_state.answer_score is not None:

            st.markdown("### ⭐ Answer Evaluation")

            st.metric(
                "Score",
                f"{st.session_state.answer_score}%"
            )

            if st.session_state.keywords_found:

                st.success(
                    "Keywords Found: " +
                    ", ".join(
                        st.session_state.keywords_found
                    )
                )

            if st.session_state.missing_keywords:

                st.warning(
                    "Missing Keywords: " +
                    ", ".join(
                        st.session_state.missing_keywords
                    )
                )

            st.info(
                st.session_state.feedback
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            previous = st.button(
                "⬅ Previous",
                use_container_width=True
            )

        with c2:
            next_btn = st.button(
                "➡ Next",
                use_container_width=True
            )

        with c3:
            finish = st.button(
                "🟥 Finish",
                type="primary",
                use_container_width=True
            )

    with col2:

        st.subheader("Live Analysis")

        st.metric(
            "👀 Eye Contact",
            f"{analysis.eye_contact}%"
        )
        st.progress(analysis.eye_contact / 100)

        st.metric(
            "🙂 Head Stability",
            f"{analysis.head_stability}%"
        )
        st.progress(analysis.head_stability / 100)

        st.metric(
            "🧍 Posture",
            f"{analysis.posture}%"
        )
        st.progress(analysis.posture / 100)

        st.metric(
            "💪 Confidence",
            f"{analysis.confidence}%"
        )
        st.progress(analysis.confidence / 100)
    
    st.markdown("---")

    if previous:

        if st.session_state.question_index > 0:
            
            st.session_state.transcript = ""
            st.session_state.answer_score = None
            st.session_state.feedback = ""
            st.session_state.keywords_found = []
            st.session_state.missing_keywords = []
            st.session_state.question_index -= 1

            st.rerun()


    if next_btn:

        if st.session_state.question_index < len(questions) - 1:

            current_question = questions[
                st.session_state.question_index
            ]

            st.session_state.interview_session.add_result(

                question=current_question,

                answer=st.session_state.transcript,

                answer_score=st.session_state.answer_score,

                keywords_found=st.session_state.keywords_found,

                missing_keywords=st.session_state.missing_keywords,

                feedback=st.session_state.feedback

            )

            st.session_state.transcript = ""
            st.session_state.answer_score = None
            st.session_state.feedback = ""
            st.session_state.keywords_found = []
            st.session_state.missing_keywords = []

            st.session_state.question_index += 1

            st.rerun()


    if finish:
        
        st.write(
            st.session_state.interview_session.results
        )
        
        st.success(
            "Interview Finished!"
        )

        st.write(
            f"Duration : {minutes:02d}:{seconds:02d}"
        )

        st.session_state.interview_started = False

        st.markdown("---")

        st.caption(
            "Built with ❤️ using Python • Streamlit • OpenCV • MediaPipe • Faster Whisper"
        )

        st.rerun()