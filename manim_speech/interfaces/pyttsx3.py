from copy import deepcopy
from email.mime import audio
import os
import json
import hashlib
from dotenv import load_dotenv

from ..speech_synthesizer import SpeechSynthesizer
from ..modify_audio import adjust_speed
from pyttsx3 import Engine

load_dotenv()


class PyTTSX3SpeechSynthesizer(SpeechSynthesizer):
    def __init__(self, engine: Engine, **kwargs):
        self.engine = engine
        SpeechSynthesizer.__init__(self, **kwargs)

    def _synthesize_text(self, text, output_dir=None, path=None):
        if output_dir is None:
            output_dir = self.output_dir

        # data = {"text": text, "engine": self.engine.__dict__}
        data = {"text": text, "engine": "pyttsx3"}
        dumped_data = json.dumps(data)
        data_hash = hashlib.sha256(dumped_data.encode("utf-8")).hexdigest()
        # file_extension = ".mp3"

        if path is None:
            audio_path = os.path.join(output_dir, data_hash + ".mp3")
            json_path = os.path.join(output_dir, data_hash + ".json")

            if os.path.exists(json_path):
                return json.loads(open(json_path, "r").read())
        else:
            audio_path = path
            json_path = os.path.splitext(path)[0] + ".json"

        self.engine.save_to_file(text, audio_path)
        self.engine.runAndWait()
        self.engine.stop()

        json_dict = {
            "original_audio": audio_path,
            "json_path": json_path,
        }

        return json_dict
