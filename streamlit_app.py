import streamlit as st
import time
from modules.questions import load_questions
from streamlit_webrtc import webrtc_streamer

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

# ---------------- Header ----------------

st.title("🎤 AI Interview Coach")

st.divider()

# ---------------- Two Columns ----------------

left, right = st.columns([2,1])

with left:

    st.subheader("Interview Mode")

    interview_mode = st.radio(
        "",
        [
            "HR Interview",
            "Technical Interview",
            "HR + Technical Interview"
        ]
    )

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

    st.subheader("Interview Information")

    col1,col2 = st.columns(2)

    with col1:

        st.metric(
            "Estimated Time",
            "10-15 min"
        )

        st.metric(
            "Speech Model",
            "Faster Whisper"
        )

    with col2:

        st.metric(
            "Camera",
            "Ready"
        )

        st.metric(
            "Microphone",
            "Ready"
        )

    st.markdown("---")

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False 

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    if st.button(
        "▶ Start Interview",
        use_container_width=True
    ):
        st.session_state.interview_started = True
        st.session_state.question_index = 0
        st.session_state.start_time = time.time()
        st.rerun()

with right:

    st.subheader("Features")

    st.success("Eye Contact Analysis")

    st.success("Head Pose Tracking")

    st.success("Posture Detection")

    st.success("Speech Analysis")

    st.success("Confidence Score")

    st.success("Personalized Feedback")

st.divider()

st.info(
    "This AI Interview Coach evaluates communication skills, body language, eye contact, posture and speaking performance to help candidates prepare for real interviews."
)

# ---------------- Interview Screen ----------------

if st.session_state.interview_started:

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

    top1, top2 = st.columns(2)

    with top1:

        st.markdown(
            f"### ⏱ Duration : {minutes:02d}:{seconds:02d}"
        )

    with top2:

        st.markdown(
            f"### Question {st.session_state.question_index + 1} / {len(questions)}"
        )

    st.info(
        questions[
            st.session_state.question_index
        ]
    )

    st.markdown("---")

    col1, col2 = st.columns([3,1])

    with col1:

        st.subheader("📷 Live Interview")

        webrtc_streamer(
            key="camera",
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
        )

    st.markdown("### Interview Controls")

    button1, button2 = st.columns(2)

    with button1:

        if st.button("⬅ Previous"):

            if st.session_state.question_index > 0:

                st.session_state.question_index -= 1

                st.rerun()

    with button2:

        if st.button("➡ Next"):

            if st.session_state.question_index < len(questions)-1:

                st.session_state.question_index += 1

                st.rerun()

    with col2:

        st.subheader("Live Analysis")

        st.metric(
            "Eye Contact",
            "--"
        )

        st.metric(
            "Head Stability",
            "--"
        )

        st.metric(
            "Posture",
            "--"
        )

        st.metric(
            "Confidence",
            "--"
        )
    
    st.markdown("---")

    if st.button(
        "Finish Interview",
        type="primary",
        use_container_width=True
    ):
        st.success(
            "Interview Finished!"
        )

        st.write(
            f"Duration : {minutes:02d}:{seconds:02d}"
        )

        st.session_state.interview_started = False