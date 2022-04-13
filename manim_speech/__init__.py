from contextlib import contextmanager

from manim_speech.speech_synthesizer import SpeechSynthesizer
import os
from manim import Scene
from manim_speech.modify_audio import get_duration
from .azure_interface import AzureTTS


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

    def add_voiceover_text(self, text: str, subcaption_buff=0.1):
        if not hasattr(self, "speech_synthesizer"):
            raise Exception(
                "You need to call init_voiceover() before adding a voiceover."
            )

        path = self.speech_synthesizer.synthesize_from_text(text)
        tracker = VoiceoverTracker(self, path)
        self.add_sound(path)
        self.current_tracker = tracker

        if self.create_subcaption:
            self.add_subcaption(
                text, duration=max(0, tracker.duration - subcaption_buff)
            )

        return tracker

    def add_voiceover_ssml(self, ssml: str):
        raise NotImplementedError("SSML input not implemented yet.")

    def wait_for_voiceover(self):
        if not hasattr(self, "current_tracker"):
            return
        if self.current_tracker is None:
            return

        remaining_duration = self.current_tracker.get_remaining_duration()
        if remaining_duration != 0:
            self.wait(remaining_duration)

    @contextmanager
    def voiceover(self, text=None, ssml=None):
        if text is None and ssml is None:
            raise ValueError("Please specify either a voiceover text or SSML string.")

        try:
            if text is not None:
                yield self.add_voiceover_text(text)
            elif ssml is not None:
                yield self.add_voiceover_ssml(ssml)
        finally:
            self.wait_for_voiceover()
