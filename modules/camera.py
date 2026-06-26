from streamlit_webrtc import VideoTransformerBase


class VideoProcessor(VideoTransformerBase):

    def transform(self, frame):

        return frame.to_ndarray(format="bgr24")