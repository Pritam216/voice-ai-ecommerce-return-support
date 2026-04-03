from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe(audio_path):
    segments, _ = model.transcribe(audio_path)
    text = " ".join([seg.text for seg in segments])
    return text.strip()


# import os
# from deepgram import DeepgramClient
# from dotenv import load_dotenv

# load_dotenv()

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")  # store your key in .env

# # Initialize Deepgram client
# dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# def transcribe(audio_path: str) -> str:
#     """
#     Transcribe a local audio file to text using Deepgram v1 API.

#     Args:
#         audio_path (str): Path to the audio file (wav, mp3, m4a).

#     Returns:
#         str: Transcribed text.
#     """
#     try:
#         with open(audio_path, "rb") as f:
#             audio_bytes = f.read()

#         # Call Deepgram API
#         response = dg_client.listen.v1.media.transcribe_file(
#             audio=audio_path,
#             model="nova-3",
#             language="en",
#             smart_format=True
#         )

#         # Access the transcript
#         transcript = response.results.channels[0].alternatives[0].transcript
#         return transcript.strip()

#     except Exception as e:
#         print(f"Error transcribing audio: {e}")
#         return ""
