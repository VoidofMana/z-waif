import time
import os

assert os.name == 'nt' # type: ignore

import win32com.client
import utils.hotkeys
import utils.voice_splitter
import utils.zw_logging
import utils.soundboard
import utils.settings
import API.api_controller

is_speaking = False
cut_voice = False

def speak_line(s_message, refuse_pause):

    global cut_voice #, is_speaking
    cut_voice = False

    chunky_message = utils.voice_splitter.split_into_sentences(s_message)

    for chunk in chunky_message:
        try:
            # Play soundbaord sounds, if any
            pure_chunk = utils.soundboard.extract_soundboard(chunk)

            # Cut out if we are not speaking unless spoken to!
            if utils.settings.speak_only_spokento and not API.api_controller.last_message_received_has_own_name:
                continue

            # Remove any asterisks from being spoken
            pure_chunk = pure_chunk.replace("*", "")

            # Change any !!! or other multi-exclamations to single use
            pure_chunk = pure_chunk.replace("!!", "!")
            pure_chunk = pure_chunk.replace("!!!", "!")
            pure_chunk = pure_chunk.replace("!!!!", "!")
            pure_chunk = pure_chunk.replace("!!!!!", "!")

            if utils.settings.tts_mode == "api":
                # Load API connection settings only if needed
                from dotenv import load_dotenv
                load_dotenv()
                openai_api_url = os.environ.get("OPENAI_TTS_API_URL")
                openai_api_key = os.environ.get("OPENAI_TTS_API_KEY")
                openai_voice = os.environ.get("OPENAI_TTS_VOICE", "alloy")
                # Use OpenAI API TTS
                import utils.openai_tts
                utils.openai_tts.speak_with_openai_api(
                    pure_chunk,
                    api_url=openai_api_url,
                    api_key=openai_api_key,
                    voice=openai_voice
                )
            else:
                # Use system TTS
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(pure_chunk)

            if not refuse_pause:
                time.sleep(0.05)    # IMPORTANT: Mini-rests between chunks for other calculations in the program to run.
            else:
                time.sleep(0.001)   # Still have a mini-mini rest, even with pauses

            # Break free if we undo/redo, and stop reading
            if utils.hotkeys.NEXT_PRESSED or utils.hotkeys.REDO_PRESSED or cut_voice:
                cut_voice = False
                break

        except:
            utils.zw_logging.update_debug_log("Error with voice!")




    # Reset the volume cooldown so she don't pickup on herself
    utils.hotkeys.cooldown_listener_timer()

    set_speaking(False)

    return

# Midspeaking (still processing whole message)
def check_if_speaking() -> bool:
    return is_speaking

def set_speaking(set: bool):
    global is_speaking
    is_speaking = set

def force_cut_voice():
    global cut_voice
    cut_voice = True
