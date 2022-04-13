from contextlib import contextmanager
from multiprocessing.sharedctypes import Value
from . import azure
import os
from manim import Scene
from manim_speech.modify_audio import get_duration


class SpeechSynthesizer:
    def __init__(self, tts_config, output_dir="media/tts"):
        self.tts_config = tts_config
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def synthesize_from_text(self, text, path=None):
        if "\n" in text:
            text = text.replace("\n", " ")

        if isinstance(self.tts_config, azure.AzureTTSConfig):
            return azure.azure_synthesize_text(
                text, self.tts_config, self.output_dir, path=path
            )


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
    def init_voiceover(self, config):
        self.speech_synthesizer = SpeechSynthesizer(config)
        self.current_tracker = None

    def add_voiceover_text(self, text: str):
        path = self.speech_synthesizer.synthesize_from_text(text)
        tracker = VoiceoverTracker(self, path)
        self.add_sound(path)
        self.current_tracker = tracker
        return tracker

    def add_voiceover_ssml(self, ssml: str):
        raise NotImplementedError("SSML input not implemented yet.")

    def wait_for_voiceover(self):
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

