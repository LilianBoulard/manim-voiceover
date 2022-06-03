from copy import deepcopy
import os
import json
import hashlib
from dotenv import load_dotenv

from ..speech_synthesizer import SpeechSynthesizer
from ..modify_audio import adjust_speed

# from pyttsx3 import Engine
from gtts import gTTS, gTTSError

load_dotenv()


class GTTSSpeechSynthesizer(SpeechSynthesizer):
    def __init__(self, **kwargs):
        SpeechSynthesizer.__init__(self, **kwargs)

    def _synthesize_text(self, text, output_dir=None, path=None):
        if output_dir is None:
            output_dir = self.output_dir

        # data = {"text": text, "engine": self.engine.__dict__}
        data = {"text": text, "engine": "gtts"}
        dumped_data = json.dumps(data)
        data_hash = hashlib.sha256(dumped_data.encode("utf-8")).hexdigest()
        # file_extension = ".mp3"

        # if path is None:
        #     path = os.path.join(output_dir, data_hash + file_extension)

        #     if os.path.exists(path):
        #         return path
        if path is None:
            audio_path = os.path.join(output_dir, data_hash + ".mp3")
            json_path = os.path.join(output_dir, data_hash + ".json")

            if os.path.exists(json_path):
                return json.loads(open(json_path, "r").read())
        else:
            audio_path = path
            json_path = os.path.splitext(path)[0] + ".json"

        tts = gTTS(text)
        try:
            tts.save(audio_path)
        except gTTSError:
            raise Exception("gTTS requires an internet connection to work.")

        json_dict = {
            # "ssml": ssml,
            # "word_boundaries": word_boundaries,
            "original_audio": audio_path,
            "json_path": json_path,
        }

        return json_dict
