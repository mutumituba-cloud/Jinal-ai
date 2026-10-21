import os
import re
import uuid

import speech_recognition as sr
from dotenv import load_dotenv
from gtts import gTTS
from playsound import playsound
from openai import OpenAI


load_dotenv()

LANGUAGE_MAP = {
    "en": ("en", "English"),
    "hi": ("hi", "Hindi"),
    "ne": ("ne", "Nepali"),
}


def detect_language(text: str) -> str:
    text_lower = text.lower()

    hindi_markers = [
        "namaste", "namaskar", "hi", "hello", "kya", "kaise", "aap", "mera",
        "mein", "bataiye", "hindi", "ham", "apka", "aaj", "kal"
    ]
    nepali_markers = [
        "namaste", "kasto", "timi", "malai", "nepali", "k cha", "sabai",
        "dherai", "khoj", "k garne", "ta", "huna", "kai"
    ]

    if any(marker in text_lower for marker in hindi_markers):
        return "hi"
    if any(marker in text_lower for marker in nepali_markers):
        return "ne"
    return "en"


def build_reply(prompt: str, language: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    lang_name = LANGUAGE_MAP.get(language, LANGUAGE_MAP["en"])[1]

    if api_key:
        client = OpenAI(api_key=api_key)
        system_prompt = (
            f"You are Jinal AI, a helpful personal voice assistant. "
            f"Answer in {lang_name}. Keep the response short, warm, and clear. "
            f"If the user uses Hindi or Nepali, reply naturally in that language."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    prompt_lower = prompt.lower()
    if "hello" in prompt_lower or "namaste" in prompt_lower:
        return "Namaste! Main Jinal AI hoon. Aap se baat karke khush laga. Aap kya karna chahte ho?"
    if "time" in prompt_lower or "samay" in prompt_lower:
        return "Main abhi waqt dekh nahi sakta, lekin main aapki madad ke liye ready hoon."
    if "weather" in prompt_lower or "mausam" in prompt_lower:
        return "Mausam ki jankari ke liye aap internet ya weather app use kar sakte hain. Main aapko help kar sakta hoon."
    if "bye" in prompt_lower or "exit" in prompt_lower or "stop" in prompt_lower:
        return "Alvida! Jinal AI se baat karne ke liye dhanyavaad."
    return "Main Jinal AI hoon. Aapka message suna gaya hai. Aap kuch aur pooch sakte hain."


def speak(text: str, language: str) -> None:
    lang_code = LANGUAGE_MAP.get(language, LANGUAGE_MAP["en"])[0]
    output_path = f"/tmp/jinal_ai_{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(output_path)
    playsound(output_path)
    os.remove(output_path)


def listen_for_voice(language: str) -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    lang_code = {
        "en": "en-US",
        "hi": "hi-IN",
        "ne": "ne-NP",
    }.get(language, "en-US")

    with sr.Microphone() as source:
        print("Jinal AI: Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)

    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""


def main() -> None:
    print("Jinal AI is ready. Say 'stop' to exit.")

    while True:
        user_input = listen_for_voice("en")
        if not user_input:
            print("Jinal AI: I couldn't hear you clearly. Please try again.")
            speak("Main ne aapko clearly suna nahi. Kripya phir se boliye.", "hi")
            continue

        clean_input = re.sub(r"\s+", " ", user_input).strip()
        print(f"You: {clean_input}")

        if clean_input.lower() in {"stop", "exit", "quit", "bye", "by", "bbye"}:
            farewell = "Alvida! Jinal AI se milkar khush laga."
            print(f"Jinal AI: {farewell}")
            speak(farewell, "hi")
            break

        detected_lang = detect_language(clean_input)
        response = build_reply(clean_input, detected_lang)
        print(f"Jinal AI: {response}")
        speak(response, detected_lang)


if __name__ == "__main__":
    main()
