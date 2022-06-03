from contextlib import contextmanager
from math import ceil
import json
# import os

from manim import Scene, config
from manim_speech.modify_audio import get_duration
from manim_speech.speech_synthesizer import SpeechSynthesizer
from .helper import chunks

SCRIPT_FILE_PATH = "media/script.txt"


class VoiceoverTracker:
    def __init__(self, scene: Scene, path):
        self.scene = scene
        self.path = path
        self.data = json.loads(open(path, "r").read())
        self.duration = get_duration(self.data["final_audio"])
        # last_t = scene.last_t
        last_t = scene.renderer.time
        if last_t is None:
            last_t = 0
        self.start_t = last_t
        self.end_t = last_t + self.duration

    def get_remaining_duration(self, buff=0):
        # result= max(self.end_t - self.scene.last_t, 0)
        result = max(self.end_t - self.scene.renderer.time + buff, 0)
        # print(result)
        return result


class VoiceoverScene(Scene):
    def init_voiceover(
        self,
        speech_synthesizer: SpeechSynthesizer,
        create_subcaption: bool = True,
        create_script: bool = True,
    ):
        self.speech_synthesizer = speech_synthesizer
        self.current_tracker = None
        self.create_subcaption = create_subcaption
        self.create_script = create_script

        open(SCRIPT_FILE_PATH, "w")

    def add_voiceover_text(
        self, text: str, subcaption_buff=0.1, max_subcaption_len=70, subcaption=None
    ):
        if not hasattr(self, "speech_synthesizer"):
            raise Exception(
                "You need to call init_voiceover() before adding a voiceover."
            )

        dict_ = self.speech_synthesizer.synthesize_from_text(text)
        tracker = VoiceoverTracker(self, dict_["json_path"])
        self.add_sound(dict_["final_audio"])
        self.current_tracker = tracker

        if self.create_script:
            self.save_to_script_file(text)

        if self.create_subcaption:
            if subcaption is None:
                subcaption = text

            self.add_wrapped_subcaption(
                subcaption,
                tracker.duration,
                subcaption_buff=subcaption_buff,
                max_subcaption_len=max_subcaption_len,
            )

        return tracker

    def add_wrapped_subcaption(
        self,
        subcaption: str,
        duration: float,
        subcaption_buff=0.1,
        max_subcaption_len: int = 70,
    ):
        subcaption = " ".join(subcaption.split())
        n_chunk = ceil(len(subcaption) / max_subcaption_len)
        tokens = subcaption.split(" ")
        chunk_len = ceil(len(tokens) / n_chunk)
        chunks_ = list(chunks(tokens, chunk_len))
        try:
            assert len(chunks_) == n_chunk or len(chunks_) == n_chunk - 1
        except AssertionError:
            import ipdb; ipdb.set_trace()

        subcaptions = [" ".join(i) for i in chunks_]
        subcaption_weights = [
            len(subcaption) / len("".join(subcaptions)) for subcaption in subcaptions
        ]

        current_offset = 0
        for idx, subcaption in enumerate(subcaptions):
            chunk_duration = duration * subcaption_weights[idx]
            self.add_subcaption(
                subcaption,
                duration=max(chunk_duration - subcaption_buff, 0),
                offset=current_offset,
            )
            current_offset += chunk_duration

    def add_voiceover_ssml(self, ssml: str):
        raise NotImplementedError("SSML input not implemented yet.")

    def save_to_script_file(self, text: str):
        text = " ".join(text.split())

        # script_file_path = Path(config.get_dir("output_file")).with_suffix(".script.srt")

        with open(SCRIPT_FILE_PATH, "a") as f:
            f.write(text)
            f.write("\n\n")

    def wait_for_voiceover(self):
        if not hasattr(self, "current_tracker"):
            return
        if self.current_tracker is None:
            return

        self.safe_wait(self.current_tracker.get_remaining_duration())

    def safe_wait(self, duration: float):
        if duration > 1 / config["frame_rate"]:
            self.wait(duration)

    @contextmanager
    def voiceover(self, text=None, ssml=None, **kwargs):
        if text is None and ssml is None:
            raise ValueError("Please specify either a voiceover text or SSML string.")

        try:
            if text is not None:
                yield self.add_voiceover_text(text, **kwargs)
            elif ssml is not None:
                yield self.add_voiceover_ssml(ssml, **kwargs)
        finally:
            self.wait_for_voiceover()
