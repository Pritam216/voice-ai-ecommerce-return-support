# # from gtts import gTTS

# # def text_to_speech(text, output_path="audio/output.mp3"):
# #     tts = gTTS(text=text, lang="en")
# #     tts.save(output_path)
# #     return output_path

import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

def text_to_speech(text, output_path="audio/output.wav"):
    url = "https://api.sarvam.ai/text-to-speech"

    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model": "bulbul:v2",
        "voice": "meera",
        "language": "en-IN"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200:
        if "audio" in data:
            audio_base64 = data["audio"]
        elif "audios" in data:
            audio_base64 = data["audios"][0]
        else:
            raise Exception(f"Unexpected response: {data}")

        audio_bytes = base64.b64decode(audio_base64)

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        return output_path
    else:
        raise Exception(f"TTS Error: {response.text}")
