from manim import *
import pygments.styles as code_styles
from manim_speech import VoiceoverScene
from manim_speech.interfaces.gtts import GTTSSpeechSynthesizer


class Example1(VoiceoverScene):
    def construct(self):
        self.init_voiceover(GTTSSpeechSynthesizer())

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text="Now, let's transform it into a square.") as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait()
