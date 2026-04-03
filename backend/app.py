import streamlit as st
import os
import tempfile

from services.noise_reduction import reduce_noise
from services.stt import transcribe
from services.retrieval import find_order, get_policy
from services.llm import generate_response
from services.tts import text_to_speech
from services.context import get_context
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av


st.set_page_config(page_title="Voice AI Support Assistant", layout="centered")
st.title("Voice AI Support Assistant")
st.write("Speak your query about orders, returns, or policies")

import streamlit as st

if "history" not in st.session_state:
    st.session_state.history = []

audio_value = st.audio_input("Record your voice")

if audio_value is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
        tmp_input.write(audio_value.getvalue())
        input_audio_path = tmp_input.name

    st.audio(input_audio_path)

    with st.spinner("Processing..."):

        denoised_path = os.path.join("audio", "denoised.wav")
        # If you don't use noise reduction, copy input
        denoised_path = input_audio_path

        transcription = transcribe(denoised_path)

        st.subheader("Transcription")
        st.write(transcription)

        st.session_state.history.append({"user": transcription})

        # context
        context = get_context(transcription)

        if context is None:
            if "return" in transcription.lower():
                context = get_policy("returns")
            elif "refund" in transcription.lower():
                context = get_policy("refunds")
            elif "policy" in transcription.lower():
                context = get_policy("returns")

        response = generate_response(
            transcription,
            context,
            st.session_state.history
        )

        st.session_state.history.append({"assistant": response})

        st.subheader("Response")
        st.write(response)

        # conversation view
        st.divider()
        st.subheader("Conversation")

        for msg in st.session_state.history:
            if "user" in msg:
                st.write("🧑:", msg["user"])
            else:
                st.write("🤖:", msg["assistant"])

        # exit condition
        if "bye" in transcription.lower():
            response = "Thank you for calling. Goodbye."

        output_audio = os.path.join("audio", "output.wav")
        text_to_speech(response, output_audio)

        st.subheader("Voice Response")
        st.audio(output_audio)

