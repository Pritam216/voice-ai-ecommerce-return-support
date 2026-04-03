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









# import os
# from dotenv import load_dotenv
# import asyncio

# load_dotenv()

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# from deepgram import DeepgramClient
# dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# from deepgram import DeepgramClient

# DEEPGRAM_API_KEY = "your_api_key_here"
# dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# def transcribe(audio_path):
#     """Simple synchronous transcription using Deepgram."""
#     import asyncio

#     async def _transcribe():
#         with open(audio_path, "rb") as f:
#             audio_bytes = f.read()
#         response = await dg_client.transcription.prerecorded(
#             audio=audio_bytes,
#             mimetype="audio/wav",
#             options={
#                 "model": "nova-3",
#                 "punctuate": True,
#                 "language": "en"
#             }
#         )
#         return response

#     # Run async function synchronously
#     response = asyncio.run(_transcribe())
#     transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
#     return transcript


# import os
# from deepgram import Deepgram
# import nest_asyncio
# import asyncio
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# nest_asyncio.apply()  # Fix async issues in Streamlit

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# dg_client = Deepgram(DEEPGRAM_API_KEY)

# def transcribe(audio_path: str) -> str:
#     """
#     Transcribe an audio file to text using Deepgram STT.
    
#     Args:
#         audio_path (str): Path to the audio file.
    
#     Returns:
#         str: Transcribed text.
#     """
#     # Read audio file bytes
#     with open(audio_path, "rb") as f:
#         audio_bytes = f.read()

#     # Async call to Deepgram
#     async def transcribe_async():
#         return await dg_client.transcription.prerecorded(
#             audio=audio_bytes,
#             mimetype="audio/wav",  # adjust if mp3/m4a
#             options={
#                 "punctuate": True,
#                 "model": "nova",
#                 "language": "en-US"
#             }
#         )

#     # Run async inside sync code
#     response = asyncio.get_event_loop().run_until_complete(transcribe_async())

#     # Extract transcript
#     transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
#     return transcript.strip()

# Test
# if __name__ == "__main__":
#     print(transcribe("audio.wav"))

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# def transcribe(audio_path):
#     url = "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&language=en"

#     headers = {
#         "Authorization": f"Token {DEEPGRAM_API_KEY}",
#         "Content-Type": "audio/wav"
#     }

#     with open(audio_path, "rb") as f:
#         audio = f.read()

#     response = requests.post(url, headers=headers, data=audio)
#     result = response.json()

#     transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
#     return transcript


# import os
# from deepgram import DeepgramClient
# from dotenv import load_dotenv

# load_dotenv()

# # Load API key from environment
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# # Create the client correctly using DeepgramClient
# dg_client = DeepgramClient(api_key=DG_API_KEY)

# # async def transcribe(audio_file_path: str) -> str:
# #     """Transcribe WAV audio using Deepgram SDK."""
# #     # Read file bytes
# #     with open(audio_file_path, "rb") as f:
# #         audio_bytes = f.read()

# #     # Call the transcription endpoint (listen.v1.media)
# #     response = await dg_client.listen.v1.media.transcribe_file(
# #         request=audio_bytes,
# #         model="nova-3",
# #         smart_format=True,
# #         punctuate=True
# #     )

# #     # Extract text
# #     transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
# #     return transcript

# # GOOD
# def transcribe(file_path):
#     response = dg_client.listen.v1.media.transcribe_file(
#         file_path,
#         model="general",
#         language="en"
#     )
#     return response['results']['channels'][0]['alternatives'][0]['transcript']


# from deepgram import DeepgramClient
# import os

# from dotenv import load_dotenv

# load_dotenv()

# # Load API key from environment
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# dg_client = DeepgramClient(api_key=DG_API_KEY)

# def transcribe(file_path):
#     # Make sure to use keyword arguments only
#     response = dg_client.listen.v1.media.transcribe_file(
#         source=file_path,       # <-- must use 'source='
#         model='general',        # keyword argument
#         language='en'           # keyword argument
#     )
#     # Get the transcript string
#     transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
#     return transcript