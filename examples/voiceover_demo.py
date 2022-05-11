from manim import *
import pygments.styles as code_styles
from manim_speech import VoiceoverScene
from manim_speech.interfaces.azure import AzureSpeechSynthesizer
from manim_speech.interfaces.pyttsx3 import PyTTSX3SpeechSynthesizer
from manim_speech.interfaces.gtts import GTTSSpeechSynthesizer
from manim_speech.interfaces.recording_mapper import RecordingMapper
import pyttsx3

code_style = code_styles.get_style_by_name("monokai")


class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # Initialize speech synthesis using Azure's TTS API
        self.init_voiceover(
            AzureSpeechSynthesizer(
                voice="en-US-AriaNeural", style="newscast-casual", global_speed=1.15
            )
        )
        # self.init_voiceover(RecordingMapper("voiceover_demo_recording.mp3"))

        # self.init_voiceover(PyTTSX3SpeechSynthesizer(pyttsx3.init(), global_speed=1.15))
        # self.init_voiceover(GTTSSpeechSynthesizer(global_speed=1.15))

        banner = ManimBanner().scale(0.5)

        with self.voiceover(text="Hey Manim Community!"):
            self.play(
                banner.create(),
            )

        tracker = self.add_voiceover_text(
            "Today, I want to show you how you can generate voiceovers directly in your Python code."
        )

        self.play(banner.expand())
        self.wait(tracker.get_remaining_duration(buff=-1))
        self.play(FadeOut(banner))

        demo_code = Code(
            code='''tracker = self.add_voiceover_text(
    """AI generated voices have become realistic
        enough for use in most content. Using neural
        text-to-speech frees you from the painstaking
        process of recording and manually syncing
        audio to your video."""
)
self.play(Write(demo_code), run_time=tracker.duration)''',
            insert_line_no=False,
            style=code_style,
            background="window",
            font="Consolas",
            language="python",
        ).rescale_to_fit(12, 0)

        tracker = self.add_voiceover_text(
            """AI generated voices have become realistic
                enough for use in most content. Using neural
                text-to-speech frees you from the painstaking
                process of recording and manually syncing
                audio to your video."""
        )
        self.play(Write(demo_code), run_time=tracker.duration)

        with self.voiceover(
            text="""As you can see, Manim started playing this voiceover,
                right as the code object started to be drawn.
                Let's see some more examples."""
        ):
            pass

        self.play(FadeOut(demo_code))

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak."):
            self.play(Create(circle))

        with self.voiceover(text="Let's shift it to the left 2 units."):
            self.play(circle.animate.shift(2 * LEFT))

        with self.voiceover(text="Now, let's transform it into a square."):
            self.play(Transform(circle, square))

        with self.voiceover(text="I would go on, but you get the idea."):
            self.play(FadeOut(circle))

        demo_code2 = Code(
            code="""class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        self.init_voiceover(AzureTTS(
            voice="en-US-AriaNeural",
            style="newscast-casual",
            global_speed=1.15
        ))
        circle = Circle()

        with self.voiceover(text="This circle is drawn as I speak."):
            self.play(Create(circle))

        with self.voiceover(text="Let's shift it to the left 2 units."):
            self.play(circle.animate.shift(2 * LEFT))""",
            insert_line_no=False,
            style=code_style,
            background="window",
            font="Consolas",
            language="python",
        ).rescale_to_fit(12, 0)

        with self.voiceover(text="Let's see how the API works!"):
            self.play(FadeIn(demo_code2.background_mobject))

        with self.voiceover(
            text="""First, we create a scene using
            the Voiceover Scene class from the plugin."""
        ):
            self.play(FadeIn(demo_code2.code[:2]))

        with self.voiceover(
            text="""Then, we initialize the voiceover by giving it
            the appropriate speech synthesizer. In this example, we use
            Azure Text-to-speech."""
        ):
            self.play(FadeIn(demo_code2.code[2]))

        with self.voiceover(
            text="""We use the English speaking neural voice called Aria."""
        ):
            self.play(FadeIn(demo_code2.code[3]))

        with self.voiceover(text="""We use the style called "newscast casual"."""):
            self.play(FadeIn(demo_code2.code[4]))

        with self.voiceover(
            text="""Finally, we give an option to speed up the voiceover
            playback fifteen percent, because the default is a bit too slow."""
        ):
            self.play(FadeIn(demo_code2.code[5:7]))

        with self.voiceover(
            text="""With the configuration out of the way, it is time to animate."""
        ):
            pass

        with self.voiceover(text="""Let's initialize the circle object."""):
            self.play(FadeIn(demo_code2.code[7:8]))

        with self.voiceover(
            text="""Then, we need to tell the scene to start narrating,
            by calling the function "self-dot-voiceover"."""
        ):
            self.play(FadeIn(demo_code2.code[9]))

        with self.voiceover(
            text="""By wrapping our animation inside a "with-statement",
            we ensure that once it finishes playing, it will also wait for
            the voiceover playback to finish."""
        ):
            self.play(FadeIn(demo_code2.code[10]))

        with self.voiceover(
            text="""This is extremely convenient, and let's you chain
            voiceovers back to back without having to think how long they are."""
        ):
            pass

        with self.voiceover(
            text="""We just need to repeat the same pattern with self-dot-voiceover and with-statements."""
        ):
            self.play(FadeIn(demo_code2.code[11:]))

        self.wait()

        with self.voiceover(
            text="""You can use this Manim plugin to generate
            voiceovers for your own projects."""
        ):
            self.play(FadeOut(demo_code2))

        with self.voiceover(text="Check out the GitHub repo shown on your screen."):
            self.play(FadeIn(Tex("https://github.com/MathBlocks/manim-speech")))

        self.wait(5)
