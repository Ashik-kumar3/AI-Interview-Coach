import streamlit as st
import time
from modules.questions import load_questions
from streamlit_webrtc import webrtc_streamer
from modules.camera import VideoProcessor
from modules.analysis import analysis
from modules.speech_analysis import (
    start_recording,
    stop_recording,
    speech_to_text,
    calculate_wpm,
    count_fillers
)
from modules.answer_evaluator import evaluate_answer
from modules.hr_evaluator import evaluate_hr_answer
from modules.llm.factory import get_llm
from modules.interview_session import InterviewSession
from modules.report import generate_report
from modules.pdf_report import generate_pdf_report

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

llm = get_llm()

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

if "recording_started" not in st.session_state:
    st.session_state.recording_started = False

if "recording_start_time" not in st.session_state:
    st.session_state.recording_start_time = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "answer_score" not in st.session_state:
    st.session_state.answer_score = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "llm_result" not in st.session_state:
    st.session_state.llm_result = None  

if "keywords_found" not in st.session_state:
    st.session_state.keywords_found = []

if "missing_keywords" not in st.session_state:
    st.session_state.missing_keywords = []

if "wpm" not in st.session_state:
    st.session_state.wpm = 0

if "fillers" not in st.session_state:
    st.session_state.fillers = 0

if "communication_score" not in st.session_state:
    st.session_state.communication_score = 0

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

                    st.session_state.recording_start_time = time.time()

                    st.session_state.recording_started = True

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

                    if st.session_state.recording_start_time is not None:

                        recording_duration = max(
                            time.time() - st.session_state.recording_start_time,
                            1
                        )

                    else:

                        recording_duration = 1

                    st.session_state.wpm = calculate_wpm(
                        transcript,
                        recording_duration
                    )

                    st.session_state.fillers = count_fillers(
                        transcript
                    )

                    score = 100

                    # Ideal speaking speed
                    if st.session_state.wpm < 90:
                        score -= 25

                    elif st.session_state.wpm < 110:
                        score -= 10

                    elif st.session_state.wpm > 180:
                        score -= 25

                    elif st.session_state.wpm > 160:
                        score -= 10

                    # Penalty for filler words
                    score -= st.session_state.fillers * 3

                    st.session_state.communication_score = max(
                        0,
                        min(100, score)
                        )

                    st.session_state.recording_start_time = None

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

                        st.session_state.llm_result = llm.evaluate(
                            question=current_question,
                            answer=transcript,
                            expected_keywords=[]
                        )

                    elif interview_mode == "Technical Interview":

                        score, found, missing, tech_terms, feedback = evaluate_answer(
                            current_question,
                            transcript
                        )

                        st.session_state.answer_score = score
                        st.session_state.feedback = feedback
                        st.session_state.keywords_found = found
                        st.session_state.missing_keywords = missing


                        # AI Recruiter Evaluation
                        st.session_state.llm_result = llm.evaluate(
                            question=current_question,
                            answer=transcript,
                            expected_keywords=missing + found
                        )

                    else:

                        if current_question in hr_questions:

                            score, feedback = evaluate_hr_answer(
                                current_question,
                                transcript
                            )

                            st.session_state.answer_score = score
                            st.session_state.feedback = feedback
                            st.session_state.keywords_found = []
                            st.session_state.missing_keywords = []

                            st.session_state.llm_result = llm.evaluate(
                                question=current_question,
                                answer=transcript,
                                expected_keywords=[]
                            )

                        else:

                            score, found, missing,tech_terms, feedback = evaluate_answer(
                                current_question,
                                transcript
                            )

                            st.session_state.answer_score = score
                            st.session_state.feedback = feedback
                            st.session_state.keywords_found = found
                            st.session_state.missing_keywords = missing
                        
                            st.session_state.llm_result = llm.evaluate(
                                question=current_question,
                                answer=transcript,
                                expected_keywords=missing + found
                            )


                    st.success("Recording Completed")

                    st.session_state.recording_started = False

                    st.rerun()
        
        if st.session_state.recording_started:

            st.subheader("🎯 Current Question")

            st.success(
                questions[
                    st.session_state.question_index
                ]
            )

            st.caption(
                "Answer naturally while looking at the camera."
            )

        else:

            st.info(
                "Click 'Start Recording' to begin the interview."
            )

        st.markdown("### Interview Controls")

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

            # ---------------- AI Recruiter Evaluation ----------------

            if st.session_state.llm_result:

                llm = st.session_state.llm_result

                st.markdown("### 🤖 AI Recruiter Evaluation")

                st.metric(
                    "Recruiter Score",
                    f"{llm['score']}/100"
                )

                st.success(
                    f"**Communication:** {llm['communication_rating']}"
                )

                st.info(
                    f"**Hiring Recommendation:** {llm['hiring_recommendation']}"
                )

                st.write("**Strengths**")
                for item in llm["strengths"]:
                    st.write(f"✅ {item}")

                st.write("**Missing Concepts**")
                for item in llm["missing_concepts"]:
                    st.write(f"❌ {item}")

                st.write("**Improvements**")
                for item in llm["improvements"]:
                    st.write(f"💡 {item}")

                st.markdown("**Recruiter Feedback**")

                st.write(llm["recruiter_feedback"])

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

            st.session_state.recording_started = False

            st.session_state.answer_score = None

            st.session_state.feedback = ""

            st.session_state.llm_result = None

            st.session_state.keywords_found = []

            st.session_state.missing_keywords = []

            st.session_state.question_index -= 1

            st.rerun()

    if next_btn:

        if st.session_state.question_index < len(questions) - 1:

            current_question = questions[
                st.session_state.question_index
            ]

            if st.session_state.transcript:

                st.session_state.interview_session.add_result(

                    question=current_question,

                    answer=st.session_state.transcript,

                    answer_score=st.session_state.answer_score,

                    keywords_found=st.session_state.keywords_found,

                    missing_keywords=st.session_state.missing_keywords,

                    feedback=st.session_state.feedback,

                    llm_result=st.session_state.llm_result

                )

            st.session_state.transcript = ""
            st.session_state.recording_started = False
            st.session_state.answer_score = None
            st.session_state.llm_result = None
            st.session_state.feedback = ""
            st.session_state.keywords_found = []
            st.session_state.missing_keywords = []

            st.session_state.question_index += 1

            st.rerun()


    if finish:

        # Save current question before finishing

        current_question = questions[
            st.session_state.question_index
        ]

        if st.session_state.transcript:

            st.session_state.interview_session.add_result(

                question=current_question,

                answer=st.session_state.transcript,

                answer_score=st.session_state.answer_score,

                keywords_found=st.session_state.keywords_found,

                missing_keywords=st.session_state.missing_keywords,

                feedback=st.session_state.feedback,

                llm_result=st.session_state.llm_result

            ) 
        
        asked_questions = []

        feedback = []

        for result in st.session_state.interview_session.results:

            asked_questions.append(
                result["question"]
            )

            feedback.append(
                result["feedback"]
            )

        elapsed = int(
            time.time() -
            st.session_state.start_time
        )

        report, report_file = generate_report(

            eye_score=analysis.eye_contact,

            head_score=analysis.head_stability,

            posture_score=analysis.posture,

            confidence_score=analysis.confidence,

            interview_type=interview_mode,

            interview_duration=elapsed,

            asked_questions=asked_questions,

            wpm=st.session_state.wpm,

            fillers=st.session_state.fillers,

            communication_score=st.session_state.communication_score,

            feedback=feedback

        )

        pdf_file = generate_pdf_report(

            interview_type=interview_mode,

            interview_duration=elapsed,

            eye_score=analysis.eye_contact,

            head_score=analysis.head_stability,

            posture_score=analysis.posture,

            communication_score=st.session_state.communication_score,

            confidence_score=analysis.confidence,
            
            results=st.session_state.interview_session.results

        )
        
        st.success(
            "Interview Finished!"
        )

        st.text(report)

        st.write(
            f"Duration : {minutes:02d}:{seconds:02d}"
        )

        with open(pdf_file, "rb") as file:

            st.download_button(

                "📄 Download PDF Report",

                file,

                file_name="Interview_Report.pdf",

                mime="application/pdf"

            )
        
        st.session_state.recording_started = False

        if st.button(
            "🔄 Start New Interview",
            use_container_width=True
        ):

            st.session_state.interview_started = False

            st.session_state.question_index = 0

            st.session_state.transcript = ""

            st.session_state.answer_score = None

            st.session_state.feedback = ""

            st.session_state.llm_result = None

            st.session_state.keywords_found = []

            st.session_state.missing_keywords = []

            st.session_state.audio_stream = None

            st.session_state.interview_session = InterviewSession()
            
            st.session_state.recording_started = False

            st.session_state.wpm = 0

            st.session_state.fillers = 0

            st.session_state.communication_score = 0

            st.session_state.recording_start_time = None

            st.rerun()

        st.markdown("---")

        st.caption(
            "Built with ❤️ using Python • Streamlit • OpenCV • MediaPipe • Faster Whisper"
        )
