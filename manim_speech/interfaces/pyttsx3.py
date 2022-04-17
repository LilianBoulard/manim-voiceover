from copy import deepcopy
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
        file_extension = ".mp3"

        if path is None:
            path = os.path.join(output_dir, data_hash + file_extension)

            if os.path.exists(path):
                return path

        self.engine.save_to_file(text, path)
        self.engine.runAndWait()
        self.engine.stop()

        return path
