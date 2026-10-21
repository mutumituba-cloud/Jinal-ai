# Jinal AI

Jinal AI is a personal voice assistant demo for voice-to-voice conversations. It listens to the user, converts speech to text, generates a reply, and speaks the answer back out loud.

Features:
- Voice input via microphone
- Voice output via text-to-speech
- Smart replies using OpenAI (optional)
- Hindi, Nepali, and English support
- Simple personal assistant workflow

## Quick start

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment file and add your OpenAI key if needed:
   ```bash
   cp .env.example .env
   ```

4. Run the assistant:
   ```bash
   python main.py
   ```

5. Say something like:
   - "Hello Jinal"
   - "Namaste Jinal"
   - "Mera naam Jinal hai"
   - "Timi kasto chau?"

6. To exit, say: "stop", "exit", or "bye"

## Notes

- The OpenAI API key is optional. If not set, Jinal AI will respond with a local fallback reply.
- For microphone support, install PortAudio on your system if needed.
  - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
  - macOS: `brew install portaudio`

## Project purpose

This repository is a starter version of a voice-to-voice personal assistant inspired by the idea of a Jinal AI assistant that can respond naturally in everyday spoken language.
