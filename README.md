# 🎧 Voice AI Support Assistant (E-commerce Returns)

---

## 🛠️ Technologies Used

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://github.com/guillaumekln/faster-whisper">
    <img src="https://img.shields.io/badge/FasterWhisper-Model-orange" alt="Faster Whisper">
  </a>
  <a href="https://developers.google.com/generative-ai">
    <img src="https://img.shields.io/badge/GoogleGemini-API-red" alt="Google Gemini">
  </a>
  <a href="https://cohere.ai/">
    <img src="https://img.shields.io/badge/Cohere-API-purple" alt="Cohere API">
  </a>
  <a href="https://sarvam.ai/">
    <img src="https://img.shields.io/badge/SarvamAI-TTS-green" alt="Sarvam AI">
  </a>
  <a href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/Streamlit-UI-blue" alt="Streamlit">
  </a>
</p>

---

## 📖 Project Details

This project is a **Voice-Enabled Support Assistant** for an e-commerce platform focusing on **orders and returns**.  

The system can:  
- Accept a **voice query** from the user  
- Convert **speech → text** (STT) using **Faster Whisper**  
- Generate a response using **LLM APIs** (**Gemini** and **Cohere**)  
- Convert the response back to **speech** using **Sarvam AI TTS**  
- Display conversation and audio response in a **Streamlit web UI**  

The assistant can handle queries such as:  
- "Where is my order?"  
- "I want to return a product"  
- "What’s your refund policy?"  

---

## ⚡ How to Use

1. Clone the repository:  
```bash
git clone <your-repo-url>
cd voice-ai-ecommerce-return-support
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the app in your browser, click **Record your voice**, ask your query, and listen to the response.

---

## ⚙️ Architecture

1. **STT (Speech to Text)**: Faster Whisper
2. **Context Handling**: Internal order & policy dataset
3. **LLM Response**: Google Gemini API + Cohere API
4. **TTS (Text to Speech)**: Sarvam AI
5. **UI**: Streamlit

---

## 🏆 Challenges

* **STT Accuracy**:

  * Faster Whisper provides excellent transcription but **performs best on GPU**.
  * Tried using **Deepgram API**, but encountered **API issues** (TypeErrors and asyncio conflicts).

* **LLM APIs**:

  * Experimented with both **Gemini** and **Cohere** to handle conversation context.
  * Integration required **careful prompt engineering** for context + chat history.

* **TTS Performance**:

  * Sarvam AI is **fast and natural**, while **gTTS** was slower for longer responses.

* **Streamlit Limitations**:

  * Handling audio files from `st.audio_input` required **proper conversion and storage** to pass to STT and TTS.

---

## 💡 How Challenges Were Solved

* Switched to **Faster Whisper** for local transcription to avoid Deepgram issues.
* Combined **Gemini + Cohere** to improve contextual responses.
* Used **Sarvam API** for TTS due to speed and clarity.
* Managed conversation **history** internally to maintain coherent multi-turn dialogue.
* Added **noise reduction** using `noisereduce` and `librosa` for cleaner STT input.

---

## ✅ Conclusion

This project demonstrates a **fully functional voice AI assistant** for e-commerce support.
It leverages **STT, LLM, TTS, and Streamlit** for a seamless **voice-based interaction**.

Despite API issues and integration challenges, careful selection of tools and combination of **Faster Whisper, Gemini, Cohere, and Sarvam AI** resulted in a **fast, accurate, and user-friendly voice assistant**.

Future improvements:

* Deploy on **GPU server** for faster transcription.
* Add **real-time streaming with WebRTC**.
* Extend LLM knowledge with **RAG (retrieval-augmented generation)** for dynamic order data.

---

## 📂 Dataset

* `orders.json` → contains order details for users
* `policies.json` → contains return/refund policies

---
