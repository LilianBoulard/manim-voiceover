from contextlib import contextmanager
from math import ceil

from manim_speech.speech_synthesizer import SpeechSynthesizer
import os
from manim import Scene
from manim_speech.modify_audio import get_duration
from .azure_interface import AzureTTS
from .helper import chunks


class VoiceoverTracker:
    def __init__(self, scene: Scene, path):
        self.scene = scene
        self.path = path
        self.duration = get_duration(path)
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
    ):
        self.speech_synthesizer = speech_synthesizer
        self.current_tracker = None
        self.create_subcaption = create_subcaption

    def add_voiceover_text(self, text: str, subcaption_buff=0.1, max_subcaption_len=70, subcaption=None):
        if not hasattr(self, "speech_synthesizer"):
            raise Exception(
                "You need to call init_voiceover() before adding a voiceover."
            )

        path = self.speech_synthesizer.synthesize_from_text(text)
        tracker = VoiceoverTracker(self, path)
        self.add_sound(path)
        self.current_tracker = tracker

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
        assert len(chunks_) == n_chunk

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

    def wait_for_voiceover(self):
        if not hasattr(self, "current_tracker"):
            return
        if self.current_tracker is None:
            return

        self.safe_wait(self.current_tracker.get_remaining_duration())

    def safe_wait(self, duration: float):
        if duration > 0.1:
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
