import requests
import os
from pydub import AudioSegment
from pydub.playback import play

def speak_with_openai_api(text, api_url, api_key, voice="alloy", output_path="/tmp/openai_tts_output.mp3"):
    """
    Send text to OpenAI-compatible voice API, save and play the returned audio.
    Args:
        text (str): Text to synthesize.
        api_url (str): API endpoint URL.
        api_key (str): API key for authentication.
        voice (str): Voice model to use (default: 'alloy').
        output_path (str): Where to save the audio file.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tts-1",
        "input": text,
        "voice": voice
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        audio = AudioSegment.from_file(output_path)
        play(audio)
    else:
        print(f"TTS API error: {response.status_code} {response.text}")
