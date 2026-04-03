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

# # # # # # # # # # # import streamlit as st
# # # # # # # # # # # import os
# # # # # # # # # # # import tempfile

# # # # # # # # # # # from backend.services.stt import transcribe
# # # # # # # # # # # from backend.services.retrieval import find_order, get_policy
# # # # # # # # # # # from backend.services.llm import generate_response
# # # # # # # # # # # from backend.services.tts import text_to_speech
# # # # # # # # # # # from backend.services.context import get_context

# # # # # # # # # # # # ---------- UI ----------
# # # # # # # # # # # st.set_page_config(page_title="Voice AI Support Assistant", layout="centered")
# # # # # # # # # # # st.title("Voice AI Support Assistant")
# # # # # # # # # # # st.write("Speak your query about orders, returns, or policies")

# # # # # # # # # # # # ---------- session memory ----------
# # # # # # # # # # # if "history" not in st.session_state:
# # # # # # # # # # #     st.session_state.history = []

# # # # # # # # # # # # ---------- audio input ----------
# # # # # # # # # # # audio_value = st.audio_input("Record your voice", key="voice_input")  # key added

# # # # # # # # # # # if audio_value is not None:
# # # # # # # # # # #     # save temp audio
# # # # # # # # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
# # # # # # # # # # #         tmp_input.write(audio_value.getvalue())
# # # # # # # # # # #         input_audio_path = tmp_input.name

# # # # # # # # # # #     st.audio(input_audio_path)

# # # # # # # # # # #     with st.spinner("Processing..."):

# # # # # # # # # # #         # ---------- STT ----------
# # # # # # # # # # #         transcription = transcribe(input_audio_path)
# # # # # # # # # # #         st.subheader("Transcription")
# # # # # # # # # # #         st.write(transcription)
# # # # # # # # # # #         st.session_state.history.append({"user": transcription})

# # # # # # # # # # #         # ---------- Context ----------
# # # # # # # # # # #         context = get_context(transcription)
# # # # # # # # # # #         if context is None:
# # # # # # # # # # #             if "return" in transcription.lower():
# # # # # # # # # # #                 context = get_policy("returns")
# # # # # # # # # # #             elif "refund" in transcription.lower():
# # # # # # # # # # #                 context = get_policy("refunds")
# # # # # # # # # # #             elif "policy" in transcription.lower():
# # # # # # # # # # #                 context = get_policy("returns")

# # # # # # # # # # #         # ---------- LLM ----------
# # # # # # # # # # #         response = generate_response(
# # # # # # # # # # #             transcription,
# # # # # # # # # # #             context,
# # # # # # # # # # #             st.session_state.history
# # # # # # # # # # #         )

# # # # # # # # # # #         # ---------- Exit ----------
# # # # # # # # # # #         if "bye" in transcription.lower():
# # # # # # # # # # #             response = "Thank you for calling. Goodbye."

# # # # # # # # # # #         st.session_state.history.append({"assistant": response})

# # # # # # # # # # #         # ---------- UI response ----------
# # # # # # # # # # #         st.subheader("Response")
# # # # # # # # # # #         st.write(response)

# # # # # # # # # # #         # ---------- Conversation ----------
# # # # # # # # # # #         st.divider()
# # # # # # # # # # #         st.subheader("Conversation")
# # # # # # # # # # #         for msg in st.session_state.history:
# # # # # # # # # # #             if "user" in msg:
# # # # # # # # # # #                 st.write("🧑:", msg["user"])
# # # # # # # # # # #             else:
# # # # # # # # # # #                 st.write("🤖:", msg["assistant"])

# # # # # # # # # # #         # ---------- TTS ----------
# # # # # # # # # # #         os.makedirs("audio", exist_ok=True)
# # # # # # # # # # #         output_audio = os.path.join("audio", "output.wav")
# # # # # # # # # # #         text_to_speech(response, output_audio)
# # # # # # # # # # #         st.subheader("Voice Response")
# # # # # # # # # # #         st.audio(output_audio)

# # # # # # # # # # #         # ---------- Auto loop ----------
# # # # # # # # # # #         if "bye" not in transcription.lower():
# # # # # # # # # # #             st.info("Listening again... Speak now 🎤")
# # # # # # # # # # #             st.rerun()  # re-run app to take next input




# # # # # # # # # # import streamlit as st
# # # # # # # # # # from streamlit_webrtc import webrtc_streamer, WebRtcMode
# # # # # # # # # # import av
# # # # # # # # # # import os

# # # # # # # # # # from backend.services.stt import transcribe
# # # # # # # # # # from backend.services.retrieval import find_order, get_policy
# # # # # # # # # # from backend.services.llm import generate_response
# # # # # # # # # # from backend.services.tts import text_to_speech
# # # # # # # # # # from backend.services.context import get_context

# # # # # # # # # # st.set_page_config(page_title="Voice AI Support Assistant", layout="centered")
# # # # # # # # # # st.title("Voice AI Support Assistant")
# # # # # # # # # # st.write("Your assistant is listening. Say 'bye' to end the conversation.")

# # # # # # # # # # if "history" not in st.session_state:
# # # # # # # # # #     st.session_state.history = []
# # # # # # # # # # if "running" not in st.session_state:
# # # # # # # # # #     st.session_state.running = True

# # # # # # # # # # if "audio_buffer" not in st.session_state:
# # # # # # # # # #     st.session_state.audio_buffer = []

# # # # # # # # # # def audio_frame_callback(frame: av.AudioFrame):
# # # # # # # # # #     audio_array = frame.to_ndarray()
# # # # # # # # # #     st.session_state.audio_buffer.append(audio_array.T)

# # # # # # # # # #     # Process every 3 seconds of audio
# # # # # # # # # #     import numpy as np
# # # # # # # # # #     import soundfile as sf
# # # # # # # # # #     import time

# # # # # # # # # #     buffer_len = sum([len(chunk) for chunk in st.session_state.audio_buffer])
# # # # # # # # # #     if buffer_len > frame.sample_rate * 3:  # ~3 seconds
# # # # # # # # # #         audio_full = np.concatenate(st.session_state.audio_buffer, axis=0)
# # # # # # # # # #         st.session_state.audio_buffer = []

# # # # # # # # # #         sf.write("temp_input.wav", audio_full, samplerate=frame.sample_rate)

# # # # # # # # # #         transcription = transcribe("temp_input.wav")
# # # # # # # # # #         if transcription.strip():
# # # # # # # # # #             st.session_state.history.append({"user": transcription})
# # # # # # # # # #         st.write("🧑 User:", transcription)

# # # # # # # # # #         # Get context
# # # # # # # # # #         context = get_context(transcription)
# # # # # # # # # #         if context is None:
# # # # # # # # # #             if "return" in transcription.lower():
# # # # # # # # # #                 context = get_policy("returns")
# # # # # # # # # #             elif "refund" in transcription.lower():
# # # # # # # # # #                 context = get_policy("refunds")
# # # # # # # # # #             elif "policy" in transcription.lower():
# # # # # # # # # #                 context = get_policy("returns")

# # # # # # # # # #         # Generate response
# # # # # # # # # #         response = generate_response(transcription, context, st.session_state.history)
# # # # # # # # # #         st.session_state.history.append({"assistant": response})
# # # # # # # # # #         st.write("🤖 Assistant:", response)

# # # # # # # # # #         # Convert response to speech
# # # # # # # # # #         os.makedirs("audio", exist_ok=True)
# # # # # # # # # #         text_to_speech(response, "audio/output.wav")

# # # # # # # # # #         # Play the audio back
# # # # # # # # # #         st.audio("audio/output.wav")

# # # # # # # # # #         # Stop condition
# # # # # # # # # #         if "bye" in transcription.lower():
# # # # # # # # # #             st.session_state.running = False
# # # # # # # # # #             st.write("Conversation ended. Say 'Start' to begin again.")

# # # # # # # # # #     return frame

# # # # # # # # # # # Start WebRTC stream
# # # # # # # # # # webrtc_streamer(
# # # # # # # # # #     key="voice-agent",
# # # # # # # # # #     mode=WebRtcMode.SENDRECV,
# # # # # # # # # #     audio_frame_callback=audio_frame_callback,
# # # # # # # # # #     media_stream_constraints={"audio": True, "video": False},
# # # # # # # # # # )

# # # import os
# # # import gradio as gr
# # # from services.stt import transcribe
# # # from services.llm import generate_response
# # # from services.tts import text_to_speech
# # # from services.context import get_context
# # # from services.retrieval import get_policy

# # # # Keep conversation history
# # # history = []

# # # # Ensure audio folder exists
# # # os.makedirs("audio", exist_ok=True)

# # # def voice_agent(audio_file):
# # #     global history

# # #     # ---------- STT ----------
# # #     transcription = transcribe(audio_file)

# # #     # Append user message to history
# # #     history.append({"user": transcription})

# # #     # ---------- Context ----------
# # #     context = get_context(transcription)
# # #     if context is None:
# # #         if "return" in transcription.lower():
# # #             context = get_policy("returns")
# # #         elif "refund" in transcription.lower():
# # #             context = get_policy("refunds")
# # #         elif "policy" in transcription.lower():
# # #             context = get_policy("returns")

# # #     # ---------- LLM ----------
# # #     response = generate_response(transcription, context, history)

# # #     # Append agent response to history
# # #     history.append({"assistant": response})

# # #     # ---------- Exit ----------
# # #     if "bye" in transcription.lower():
# # #         response += "\n[Conversation ended]"
    
# # #     # ---------- TTS ----------
# # #     output_audio_path = "audio/output.wav"
# # #     text_to_speech(response, output_audio_path)

# # #     # Prepare chat history for display
# # #     chat_text = ""
# # #     for msg in history:
# # #         if "user" in msg:
# # #             chat_text += f"🧑: {msg['user']}\n"
# # #         else:
# # #             chat_text += f"🤖: {msg['assistant']}\n"

# # #     return chat_text, output_audio_path

# # # # ---------- Gradio Interface ----------
# # # iface = gr.Interface(
# # #     fn=voice_agent,
# # #     inputs=gr.Audio(label="Speak your query", type="filepath"),
# # #     outputs=[gr.Textbox(label="Conversation History"), gr.Audio(label="Voice Response")],
# # #     title="Voice AI Support Assistant",
# # #     description="Speak your query about orders, returns, or policies. Say 'bye' to end conversation."
# # # )

# # # iface.launch(share=True)


# # import os
# # import gradio as gr
# # import asyncio
# # import soundfile as sf
# # import tempfile
# # from services.stt import transcribe_audio
# # from services.llm import generate_response
# # from services.tts import text_to_speech
# # from services.context import get_context
# # from services.retrieval import get_policy

# # # Keep conversation history
# # history = []

# # # Ensure audio folder exists
# # os.makedirs("audio", exist_ok=True)

# # def voice_agent(audio_file_path):
# #     global history

# #     if audio_file_path is None:
# #         return "No audio provided.", None

# #     # ---------- STT ----------
# #     # audio_input is (sample_rate, np_array)
# #     if isinstance(audio_input, tuple):
# #         samplerate, data = audio_input
# #         tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
# #         sf.write(tmp_file.name, data, samplerate)
# #         audio_file_path = tmp_file.name
# #     else:
# #         audio_file_path = audio_input  # already a path

# #     transcription = asyncio.run(transcribe_audio(audio_file_path))

# #     # Append user message to history
# #     history.append({"user": transcription})

# #     # ---------- Context ----------
# #     context = get_context(transcription)
# #     if context is None:
# #         if "return" in transcription.lower():
# #             context = get_policy("returns")
# #         elif "refund" in transcription.lower():
# #             context = get_policy("refunds")
# #         elif "policy" in transcription.lower():
# #             context = get_policy("returns")

# #     # ---------- LLM ----------
# #     response = generate_response(transcription, context, history)

# #     # Append agent response to history
# #     history.append({"assistant": response})

# #     # ---------- Exit ----------
# #     if "bye" in transcription.lower():
# #         response += "\n[Conversation ended]"

# #     # ---------- TTS ----------
# #     output_audio_path = "audio/output.wav"
# #     text_to_speech(response, output_audio_path)

# #     # Prepare chat history for display
# #     chat_text = ""
# #     for msg in history:
# #         if "user" in msg:
# #             chat_text += f"🧑: {msg['user']}\n"
# #         else:
# #             chat_text += f"🤖: {msg['assistant']}\n"

# #     data, samplerate = sf.read(output_audio_path)
# #     return chat_text, (samplerate, data)

# #     # Convert to numpy array for Gradio
    

# # # ---------- Gradio Interface ----------
# # iface = gr.Interface(
# #     fn=voice_agent,
# #     inputs=gr.Audio(type="filepath", label="Upload your voice query"),
# #     outputs=[
# #         gr.Textbox(label="Conversation History", lines=10, interactive=False),
# #         gr.Audio(label="Voice Response", type="filepath")
# #     ],
# #     title="Voice AI Support Assistant",
# #     description="Speak your query about orders, returns, or policies. Say 'bye' to end conversation."
# # )

# # iface.launch(share=True)


# # # # # # # # from fastapi import FastAPI, WebSocket
# # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # import os
# # # # # # # # import tempfile
# # # # # # # # from backend.services.stt import transcribe
# # # # # # # # from backend.services.tts import text_to_speech
# # # # # # # # from backend.services.llm import generate_response
# # # # # # # # from backend.services.retrieval import get_policy
# # # # # # # # from backend.services.context import get_context

# # # # # # # # app = FastAPI()

# # # # # # # # # Store chat history per session
# # # # # # # # chat_history = []

# # # # # # # # @app.get("/")
# # # # # # # # async def get():
# # # # # # # #     with open("frontend/index.html") as f:
# # # # # # # #         return HTMLResponse(f.read())

# # # # # # # # @app.websocket("/ws")
# # # # # # # # async def websocket_endpoint(websocket: WebSocket):
# # # # # # # #     await websocket.accept()
# # # # # # # #     session_history = []  # Keep chat history per session

# # # # # # # #     while True:
# # # # # # # #         try:
# # # # # # # #             # Receive audio chunk from frontend
# # # # # # # #             data = await websocket.receive_bytes()

# # # # # # # #             # Save incoming audio chunk
# # # # # # # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
# # # # # # # #                 tmp_audio.write(data)
# # # # # # # #                 audio_path = tmp_audio.name

# # # # # # # #             # Transcribe audio
# # # # # # # #             transcription = transcribe(audio_path)
# # # # # # # #             session_history.append({"user": transcription})

# # # # # # # #             # Context / retrieval
# # # # # # # #             context = get_context(transcription)
# # # # # # # #             if context is None:
# # # # # # # #                 if "return" in transcription.lower():
# # # # # # # #                     context = get_policy("returns")
# # # # # # # #                 elif "refund" in transcription.lower():
# # # # # # # #                     context = get_policy("refunds")
# # # # # # # #                 elif "policy" in transcription.lower():
# # # # # # # #                     context = get_policy("returns")

# # # # # # # #             # Generate response using LLM
# # # # # # # #             response = generate_response(transcription, context, session_history)
# # # # # # # #             session_history.append({"assistant": response})

# # # # # # # #             # Convert response to audio
# # # # # # # #             os.makedirs("audio", exist_ok=True)
# # # # # # # #             output_audio_path = os.path.join("audio", "output.wav")
# # # # # # # #             text_to_speech(response, output_audio_path)

# # # # # # # #             # Send transcription + text response + base64 audio to client
# # # # # # # #             import base64
# # # # # # # #             with open(output_audio_path, "rb") as f:
# # # # # # # #                 audio_b64 = base64.b64encode(f.read()).decode("utf-8")

# # # # # # # #             await websocket.send_json({
# # # # # # # #                 "transcription": transcription,
# # # # # # # #                 "response": response,
# # # # # # # #                 "audio_b64": audio_b64
# # # # # # # #             })

# # # # # # # #             # Stop session if user says bye
# # # # # # # #             if "bye" in transcription.lower():
# # # # # # # #                 break

# # # # # # # #         except Exception as e:
# # # # # # # #             print("Error:", e)
# # # # # # # #             break

# # # # # # # #     await websocket.close()


# # # # # # # # # backend/app.py
# # # # # # # # from fastapi import FastAPI, WebSocket
# # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # import os
# # # # # # # # import tempfile

# # # # # # # # from backend.services.stt import transcribe
# # # # # # # # from backend.services.tts import text_to_speech
# # # # # # # # from backend.services.llm import generate_response
# # # # # # # # from backend.services.retrieval import get_policy
# # # # # # # # from backend.services.context import get_context

# # # # # # # # app = FastAPI()

# # # # # # # # # ---------- Store chat history per session ----------
# # # # # # # # chat_history = []

# # # # # # # # # ---------- Serve frontend ----------
# # # # # # # # @app.get("/")
# # # # # # # # async def get():
# # # # # # # #     with open("frontend/index.html") as f:
# # # # # # # #         return HTMLResponse(f.read())

# # # # # # # # # ---------- WebSocket for continuous voice ----------
# # # # # # # # @app.websocket("/ws")
# # # # # # # # async def websocket_endpoint(websocket: WebSocket):
# # # # # # # #     await websocket.accept()
# # # # # # # #     try:
# # # # # # # #         while True:
# # # # # # # #             data = await websocket.receive_bytes()

# # # # # # # #             # Save audio temporarily
# # # # # # # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
# # # # # # # #                 tmp_audio.write(data)
# # # # # # # #                 audio_path = tmp_audio.name

# # # # # # # #             # STT
# # # # # # # #             transcription = transcribe(audio_path).strip()
# # # # # # # #             if not transcription:
# # # # # # # #                 await websocket.send_json({"error": "No speech detected"})
# # # # # # # #                 continue

# # # # # # # #             # Context / Retrieval
# # # # # # # #             context = get_context(transcription)
# # # # # # # #             if context is None:
# # # # # # # #                 if "return" in transcription.lower():
# # # # # # # #                     context = get_policy("returns")
# # # # # # # #                 elif "refund" in transcription.lower():
# # # # # # # #                     context = get_policy("refunds")
# # # # # # # #                 elif "policy" in transcription.lower():
# # # # # # # #                     context = get_policy("returns")

# # # # # # # #             # Combine context with transcription
# # # # # # # #             prompt = (context + "\n\n" if context else "") + transcription

# # # # # # # #             # Generate response
# # # # # # # #             response = generate_response(prompt, chat_history)

# # # # # # # #             # Update chat history in Cohere format
# # # # # # # #             chat_history.append({"role": "USER", "message": transcription})
# # # # # # # #             chat_history.append({"role": "CHATBOT", "message": response})

# # # # # # # #             # TTS
# # # # # # # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_out:
# # # # # # # #                 output_audio_path = tmp_audio_out.name
# # # # # # # #                 text_to_speech(response, output_audio_path)

# # # # # # # #             # Send JSON to client
# # # # # # # #             await websocket.send_json({"transcription": transcription, "response": response})

# # # # # # # #             # Send audio bytes
# # # # # # # #             with open(output_audio_path, "rb") as f:
# # # # # # # #                 await websocket.send_bytes(f.read())

# # # # # # # #             # Exit
# # # # # # # #             if "bye" in transcription.lower():
# # # # # # # #                 break

# # # # # # # #     except Exception as e:
# # # # # # # #         print("WebSocket error:", e)
# # # # # # # #     finally:
# # # # # # # #         if websocket.client_state.name != "DISCONNECTED":
# # # # # # # #             await websocket.close()

# # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # app.mount("/static", StaticFiles(directory="frontend"), name="static")/


# # # # # # # # backend/app.py
# # # # # # # from fastapi import FastAPI, UploadFile, File, Form
# # # # # # # from fastapi.responses import HTMLResponse, JSONResponse
# # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # import os
# # # # # # # import tempfile
# # # # # # # import base64

# # # # # # # from backend.services.stt import transcribe
# # # # # # # from backend.services.tts import text_to_speech
# # # # # # # from backend.services.llm import generate_response
# # # # # # # from backend.services.retrieval import get_policy
# # # # # # # from backend.services.context import get_context

# # # # # # # app = FastAPI()

# # # # # # # # Serve static frontend files (CSS, JS)
# # # # # # # app.mount("/static", StaticFiles(directory="frontend"), name="static")

# # # # # # # # ---------- Store chat history per session ----------
# # # # # # # chat_history = []

# # # # # # # # ---------- Serve frontend ----------
# # # # # # # @app.get("/")
# # # # # # # async def get_frontend():
# # # # # # #     with open("frontend/index.html") as f:
# # # # # # #         return HTMLResponse(f.read())

# # # # # # # # ---------- POST endpoint for voice chat ----------
# # # # # # # @app.post("/api/chat")
# # # # # # # async def chat(audio: UploadFile = File(...)):
# # # # # # #     # Save uploaded audio temporarily
# # # # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
# # # # # # #         tmp_audio.write(await audio.read())
# # # # # # #         audio_path = tmp_audio.name

# # # # # # #     # ---------- STT ----------
# # # # # # #     transcription = transcribe(audio_path).strip()
# # # # # # #     if not transcription:
# # # # # # #         return JSONResponse({"error": "No speech detected"}, status_code=400)

# # # # # # #     # ---------- Context / Retrieval ----------
# # # # # # #     context = get_context(transcription)
# # # # # # #     if context is None:
# # # # # # #         if "return" in transcription.lower():
# # # # # # #             context = get_policy("returns")
# # # # # # #         elif "refund" in transcription.lower():
# # # # # # #             context = get_policy("refunds")
# # # # # # #         elif "policy" in transcription.lower():
# # # # # # #             context = get_policy("returns")

# # # # # # #     # ---------- Prepare prompt ----------
# # # # # # #     prompt = (context + "\n\n" if context else "") + transcription

# # # # # # #     # ---------- Generate LLM response ----------
# # # # # # #     response_text = generate_response(prompt, chat_history)

# # # # # # #     # ---------- Update chat history ----------
# # # # # # #     chat_history.append({"role": "USER", "message": transcription})
# # # # # # #     chat_history.append({"role": "CHATBOT", "message": response_text})

# # # # # # #     # ---------- TTS ----------
# # # # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_out:
# # # # # # #         output_audio_path = tmp_audio_out.name
# # # # # # #         text_to_speech(response_text, output_audio_path)

# # # # # # #     # Convert audio to base64 so it can be sent over JSON
# # # # # # #     with open(output_audio_path, "rb") as f:
# # # # # # #         audio_bytes = f.read()
# # # # # # #         audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

# # # # # # #     # ---------- Return JSON ----------
# # # # # # #     return JSONResponse({
# # # # # # #         "transcription": transcription,
# # # # # # #         "response": response_text,
# # # # # # #         "audio_base64": audio_base64
# # # # # # #     })

# # # # # # # backend/app.py
# # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # from fastapi.responses import HTMLResponse, JSONResponse
# # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # import os
# # # # # # import tempfile
# # # # # # import base64

# # # # # # from backend.services.stt import transcribe
# # # # # # from backend.services.tts import text_to_speech
# # # # # # from backend.services.llm import generate_response
# # # # # # from backend.services.retrieval import get_policy
# # # # # # from backend.services.context import get_context

# # # # # # app = FastAPI()

# # # # # # app.mount("/static", StaticFiles(directory="frontend"), name="static")

# # # # # # # ---------- Store chat history ----------
# # # # # # chat_history = []

# # # # # # @app.get("/")
# # # # # # async def get_frontend():
# # # # # #     with open("frontend/index.html") as f:
# # # # # #         return HTMLResponse(f.read())

# # # # # # @app.post("/api/chat")
# # # # # # async def chat(audio: UploadFile = File(...)):
# # # # # #     # Save uploaded audio temporarily
# # # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
# # # # # #         tmp_audio.write(await audio.read())
# # # # # #         audio_path = tmp_audio.name

# # # # # #     # ---------- STT ----------
# # # # # #     transcription = transcribe(audio_path).strip()
# # # # # #     if not transcription:
# # # # # #         return JSONResponse({"error": "No speech detected"}, status_code=400)

# # # # # #     # ---------- Context / Retrieval ----------
# # # # # #     context = get_context(transcription)
# # # # # #     if context is None:
# # # # # #         if "return" in transcription.lower():
# # # # # #             context = get_policy("returns")
# # # # # #         elif "refund" in transcription.lower():
# # # # # #             context = get_policy("refunds")
# # # # # #         elif "policy" in transcription.lower():
# # # # # #             context = get_policy("returns")

# # # # # #     # ---------- Ensure context is string ----------
# # # # # #     context_text = f"please give me information only anout the query in short"
# # # # # #     if isinstance(context, dict):
# # # # # #         # Extract 'text' or 'content' field from dict
# # # # # #         if "text" in context:
# # # # # #             context_text += context["text"]
# # # # # #         elif "content" in context:
# # # # # #             context_text += context["content"]
# # # # # #         else:
# # # # # #             context_text += str(context)
# # # # # #     elif isinstance(context, str):
# # # # # #         context_text += context

# # # # # #     # ---------- Prepare prompt ----------
# # # # # #     prompt = (context_text + "\n\n" if context_text else "") + transcription

# # # # # #     # ---------- Generate LLM response ----------
# # # # # #     response_text = generate_response(prompt, chat_history)

# # # # # #     # ---------- Update chat history ----------
# # # # # #     chat_history.append({"role": "USER", "message": transcription})
# # # # # #     chat_history.append({"role": "CHATBOT", "message": response_text})

# # # # # #     # ---------- TTS ----------
# # # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_out:
# # # # # #         output_audio_path = tmp_audio_out.name
# # # # # #         text_to_speech(response_text, output_audio_path)

# # # # # #     # Convert audio to base64 for JSON
# # # # # #     with open(output_audio_path, "rb") as f:
# # # # # #         audio_bytes = f.read()
# # # # # #         audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

# # # # # #     return JSONResponse({
# # # # # #         "transcription": transcription,
# # # # # #         "response": response_text,
# # # # # #         "audio_base64": audio_base64
# # # # # #     })


# # # # # import streamlit as st
# # # # # import sounddevice as sd
# # # # # from scipy.io.wavfile import write
# # # # # import tempfile
# # # # # from services import stt, tts, llm, context

# # # # # st.set_page_config(page_title="Voice AI E-commerce Assistant")
# # # # # st.title("🎤 Voice AI E-commerce Assistant (Mic Input)")

# # # # # # Initialize chat history
# # # # # context.init_session()

# # # # # # Reset chat history
# # # # # if st.button("Reset Chat"):
# # # # #     context.reset_history()

# # # # # # Recording settings
# # # # # fs = 16000  # 16kHz sample rate
# # # # # duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

# # # # # if st.button("Record"):
# # # # #     st.info("Recording... Speak now!")
# # # # #     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
# # # # #     sd.wait()
# # # # #     st.success("Recording complete!")

# # # # #     # Save recording to temporary WAV file
# # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
# # # # #         write(tmp.name, fs, recording)
# # # # #         audio_path = tmp.name

# # # # #     # 1️⃣ Transcribe with STT
# # # # #     transcript = stt.transcribe_audio(audio_path)
# # # # #     if transcript.strip():
# # # # #         st.markdown(f"**You:** {transcript}")

# # # # #         # 2️⃣ Generate response from LLM with chat history
# # # # #         assistant_text = llm.generate_response(transcript, st.session_state.history)

# # # # #         # 3️⃣ Add to chat history
# # # # #         context.add_message(transcript, assistant_text)

# # # # #         # 4️⃣ Convert LLM response to speech
# # # # #         audio_bytes = tts.synthesize_speech(assistant_text)
# # # # #         st.audio(audio_bytes, format="audio/mp3")

# # # # #         st.markdown(f"**Assistant:** {assistant_text}")
# # # # #     else:
# # # # #         st.warning("Could not transcribe your voice. Try again.")

# # # # # # Display chat history
# # # # # st.subheader("Chat History")
# # # # # for chat in st.session_state.history:
# # # # #     st.markdown(f"**You:** {chat['user']}")
# # # # #     st.markdown(f"**Assistant:** {chat['assistant']}")

# # # # # import streamlit as st
# # # # # import tempfile
# # # # # import asyncio
# # # # # from services.stt import transcribe
# # # # # from services.llm import generate_response
# # # # # from services.tts import synthesize_speech
# # # # # from services.utils import find_order_info, get_policy_response

# # # # # st.set_page_config(page_title="Voice AI Support Assistant")
# # # # # st.title("🛍️ Voice AI Support (Browser Mic Input)")

# # # # # if "history" not in st.session_state:
# # # # #     st.session_state.history = []

# # # # # user_id = st.text_input("Enter your User ID", value="U1")

# # # # # # Browser mic input (HTML trick)
# # # # # st.markdown(
# # # # #     """
# # # # #     <input type="file" accept="audio/*" capture id="mic_input">
# # # # #     """,
# # # # #     unsafe_allow_html=True
# # # # # )

# # # # # audio_file = st.file_uploader("Or upload a voice file (WAV/MP3)", type=["wav","mp3"])

# # # # # if audio_file and st.button("Send") and user_id:
# # # # #     # Save to temp file
# # # # #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
# # # # #         f.write(audio_file.getvalue())
# # # # #         tmp_path = f.name

# # # # #     # STT: voice → text
# # # # #     transcript = asyncio.run(transcribe(tmp_path))
# # # # #     st.write(f"**You said:** {transcript}")

# # # # #     # Dataset lookup
# # # # #     order = find_order_info(user_id, transcript)
# # # # #     policy_text = get_policy_response(transcript)

# # # # #     if order:
# # # # #         answer = f"Order {order['order_id']} for {order['item']} is {order['status']}."
# # # # #         if order.get("delivery_date"):
# # # # #             answer += f" Delivered on {order['delivery_date']}."
# # # # #         if order.get("expected_delivery"):
# # # # #             answer += f" Expected delivery: {order['expected_delivery']}."
# # # # #     elif policy_text:
# # # # #         answer = policy_text
# # # # #     else:
# # # # #         answer = generate_response(transcript, st.session_state.history)

# # # # #     # TTS: text → speech
# # # # #     audio_response = synthesize_speech(answer)

# # # # #     # Add chat history
# # # # #     st.session_state.history.append({"user": transcript, "assistant": answer})

# # # # #     st.write(f"**Assistant:** {answer}")
# # # # #     st.audio(audio_response, format="audio/wav")

# # # # # # Chat history
# # # # # if st.session_state.history:
# # # # #     st.markdown("### Chat History")
# # # # #     for h in st.session_state.history:
# # # # #         st.markdown(f"**You:** {h['user']}")
# # # # #         st.markdown(f"**Bot:** {h['assistant']}")

# # # # import os
# # # # import gradio as gr
# # # # from services.stt import transcribe   # normal call, not async
# # # # from services.llm import generate_response
# # # # from services.tts import synthesize_speech
# # # # from services.utils import find_order_info, get_policy_response

# # # # # Keep conversation history
# # # # history = []

# # # # # Ensure audio folder exists
# # # # os.makedirs("audio", exist_ok=True)

# # # # def voice_agent(audio_file_path, user_id="U1"):
# # # #     global history

# # # #     if audio_file_path is None:
# # # #         return "No audio received.", None

# # # #     # ---------- STT ----------
# # # #     transcription = transcribe(audio_file_path)  # <- no await
# # # #     if not transcription:
# # # #         return "Could not transcribe audio.", None

# # # #     history.append({"user": transcription})

# # # #     # ---------- Dataset & Policy ----------
# # # #     order = find_order_info(user_id, transcription)
# # # #     policy_text = get_policy_response(transcription)

# # # #     if order:
# # # #         response = f"Order {order['order_id']} for {order['item']} is {order['status']}."
# # # #         if order.get("delivery_date"):
# # # #             response += f" Delivered on {order['delivery_date']}."
# # # #         if order.get("expected_delivery"):
# # # #             response += f" Expected delivery: {order['expected_delivery']}."
# # # #     elif policy_text:
# # # #         response = policy_text
# # # #     else:
# # # #         response = generate_response(transcription, history)

# # # #     history.append({"assistant": response})

# # # #     if "bye" in transcription.lower():
# # # #         response += "\n[Conversation ended]"

# # # #     output_audio_path = "audio/output.wav"
# # # #     synthesize_speech(response, output_audio_path)

# # # #     chat_text = ""
# # # #     for msg in history:
# # # #         if "user" in msg:
# # # #             chat_text += f"🧑: {msg['user']}\n"
# # # #         else:
# # # #             chat_text += f"🤖: {msg['assistant']}\n"

# # # #     return chat_text, output_audio_path

# # # # iface = gr.Interface(
# # # #     fn=voice_agent,
# # # #     inputs=[gr.Audio(label="Speak your query", type="filepath"),
# # # #             gr.Textbox(label="User ID", value="U1")],
# # # #     outputs=[gr.Textbox(label="Conversation History"), gr.Audio(label="Voice Response")],
# # # #     title="🛍️ Voice AI Support Assistant",
# # # #     description="Speak your query about orders, returns, or policies. Say 'bye' to end conversation."
# # # # )

# # # # iface.launch(share=True)


# # # # app.py

# # # # app.py
# # # import os
# # # import json
# # # from dotenv import load_dotenv
# # # import gradio as gr
# # # from deepgram import DeepgramClient

# # # # Load API keys
# # # load_dotenv()
# # # DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# # # # Initialize Deepgram client
# # # dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# # # # Load data
# # # with open("data/orders.json") as f:
# # #     orders = json.load(f)

# # # with open("data/policies.json") as f:
# # #     policies = json.load(f)

# # # # --- Helper functions ---

# # # def transcribe(audio_file_path):
# # #     """
# # #     Transcribe a local audio file using Deepgram.
# # #     """
# # #     # Deepgram expects file in bytes
# # #     with open(audio_file_path, "rb") as f:
# # #         response = dg_client.transcription.pre_recorded(
# # #             file=f,
# # #             mimetype="audio/wav",  # change to match your audio type
# # #             options={"punctuate": True}
# # #         )
# # #     transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
# # #     return transcript

# # # def find_order_info(user_id, text):
# # #     """Return order info if text mentions order_id or item."""
# # #     text_lower = text.lower()
# # #     for o in orders:
# # #         if o["user_id"] == user_id:
# # #             if o["order_id"].lower() in text_lower or o["item"].lower() in text_lower:
# # #                 return f"Order found: {o}"
# # #     return "No matching order found."

# # # def get_policy_response(text):
# # #     """Return relevant policy text if keyword matches."""
# # #     for key, info in policies.items():
# # #         if key.lower() in text.lower():
# # #             return f"{key} policy: {info}"
# # #     return None

# # # # --- Gradio chat function ---

# # # def voice_agent(audio, chat_history, user_id="user123"):
# # #     """
# # #     Process uploaded audio, transcribe it, check for order or policy info,
# # #     and return updated chat history.
# # #     """
# # #     if audio is None:
# # #         return chat_history, "Please upload an audio file."
    
# # #     # Transcribe
# # #     transcript = transcribe(audio.name)

# # #     # Find order or policy
# # #     order_response = find_order_info(user_id, transcript)
# # #     policy_response = get_policy_response(transcript)
    
# # #     bot_response = transcript
# # #     if order_response != "No matching order found.":
# # #         bot_response += f"\n{order_response}"
# # #     if policy_response:
# # #         bot_response += f"\n{policy_response}"

# # #     # Update chat history
# # #     chat_history = chat_history or []
# # #     chat_history.append(("You", transcript))
# # #     chat_history.append(("Bot", bot_response))

# # #     return chat_history, ""

# # # # --- Gradio UI ---

# # # with gr.Blocks() as demo:
# # #     gr.Markdown("## Voice AI Support Bot")
# # #     chat_history = gr.State([])

# # #     with gr.Row():
# # #         audio_input = gr.Audio(source="upload", type="file", label="Upload your voice message")
# # #         output_text = gr.Textbox(label="Bot Response", interactive=False)

# # #     chatbot = gr.Chatbot()
# # #     send_button = gr.Button("Send")

# # #     send_button.click(
# # #         voice_agent,
# # #         inputs=[audio_input, chat_history],
# # #         outputs=[chatbot, output_text],
# # #     )

# # # demo.launch()



# # app.py
# import os
# import asyncio
# import gradio as gr
# from services.stt import transcribe_audio      # Deepgram wrapper
# from services.llm import generate_response    # Cohere wrapper
# from services.tts import text_to_speech       # Sarvam TTS wrapper
# from services.context import get_context
# from services.retrieval import get_policy

# # Ensure audio folder exists
# os.makedirs("audio", exist_ok=True)

# # Keep conversation history
# history = []

# async def voice_agent(audio_file_path):
#     global history

#     # ---------- STT ----------
#     transcription = await transcribe_audio(audio_file_path)

#     # Append user message
#     history.append({"user": transcription})

#     # ---------- Context ----------
#     context = get_context(transcription)
#     transcription_lower = transcription.lower()
#     if context is None:
#         if "return" in transcription_lower:
#             context = get_policy("returns")
#         elif "refund" in transcription_lower:
#             context = get_policy("refunds")
#         elif "policy" in transcription_lower:
#             context = get_policy("returns")

#     # ---------- LLM ----------
#     response = generate_response(transcription, context, history)
#     history.append({"assistant": response})

#     # ---------- Exit ----------
#     if "bye" in transcription_lower:
#         response += "\n[Conversation ended]"

#     # ---------- TTS ----------
#     output_audio_path = "audio/output.wav"
#     text_to_speech(response, output_audio_path)

#     # Prepare chat history for display
#     chat_text = ""
#     for msg in history:
#         if "user" in msg:
#             chat_text += f"🧑: {msg['user']}\n"
#         else:
#             chat_text += f"🤖: {msg['assistant']}\n"

#     return chat_text, output_audio_path

# # ---------- Gradio Interface ----------
# iface = gr.Interface(
#     fn=lambda audio_file: asyncio.run(voice_agent(audio_file)),
#     inputs=gr.Audio(source="microphone", type="filepath", label="Speak your query"),
#     outputs=[
#         gr.Textbox(label="Conversation History"),
#         gr.Audio(label="Voice Response", type="filepath")
#     ],
#     title="Voice AI Support Assistant",
#     description="Speak your query about orders, returns, or policies. Say 'bye' to end conversation."
# )

# if __name__ == "__main__":
#     iface.launch(share=False)
