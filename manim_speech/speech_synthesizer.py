import os
import json
import hashlib

from .modify_audio import adjust_speed


class SpeechSynthesizer:
    def __init__(self, global_speed=None, output_dir=None):
        # self.tts_config = tts_config
        if output_dir is None:
            output_dir = "media/tts"
        if global_speed is None:
            global_speed = 1.00

        self.global_speed = global_speed
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def synthesize_from_text(self, text: str, path=None):
        # Replace newlines with lines, reduce multiple consecutive spaces to single
        text = text.replace("\n", " ")
        text = " ".join(text.split())

        path = self._synthesize_text(text, output_dir=None, path=path)

        if self.global_speed != 1:
            split_path = os.path.splitext(path)
            adjusted_path = split_path[0] + "_adjusted" + split_path[1]
            adjust_speed(path, adjusted_path, self.global_speed)
            path = adjusted_path

        return path

    def get_data_hash(self, data):
        dumped_data = json.dumps(data)
        data_hash = hashlib.sha256(dumped_data.encode("utf-8")).hexdigest()
        return data_hash

    def _synthesize_text(self, text, output_dir=None, path=None):
        raise NotImplementedError(
            "This is the base class. Please extend this and implement the required methods."
        )
