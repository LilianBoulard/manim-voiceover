from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.interfaces.azure import AzureSpeechSynthesizer


class BookmarkExample(VoiceoverScene):
    def construct(self):
        self.set_speech_synthesizer(
            AzureSpeechSynthesizer(
                voice="en-US-AriaNeural",
                style="newscast-casual",
            )
        )

        banner = ManimBanner().scale(0.25)
        manim_voiceover_title = Tex(r"\texttt{manim-voiceover}", font_size=64)

        VGroup(banner, manim_voiceover_title).arrange(buff=0.5).align_on_border(
            UP, buff=1
        )

        blist = BulletedList(
            "Trigger animations", "At any word", "Bookmarks", font_size=64
        ).shift(0.5 * DOWN)

        with self.voiceover(
            text="""The plugin Manim-Voiceover allows you to <bookmark mark='A'/>trigger
            animations <bookmark mark='B'/>at any word in the middle of a sentence by
            adding simple <bookmark mark='C'/>bookmarks to your text."""
        ) as tracker:
            self.play(
                banner.create(),
                Write(manim_voiceover_title),
                Write(Underline(manim_voiceover_title)),
                run_time=tracker.time_until_bookmark("A"),
            )

            self.play(
                Write(blist[0]), run_time=tracker.time_until_bookmark("B", limit=1)
            )
            self.safe_wait(tracker.time_until_bookmark("B"))
            self.play(
                Write(blist[1]), run_time=tracker.time_until_bookmark("C", limit=1)
            )
            self.safe_wait(tracker.time_until_bookmark("C"))
            self.play(Write(blist[2]))

        self.play(FadeOut(blist))

        sentence = "A quick brown fox jumps over the lazy dog."

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
