# manim-speech

`manim-speech` is a [Manim](https://manim.community) plugin that helps you add voiceovers to your Manim videos directly in your code, without using a video editor. It allows you to do two very important things:

1. **Develop your animation with an auto-generated AI voice** without having to re-record and re-sync the audio every time you make a change to your screenplay.
2. When you are ready to release the final cut, **record the actual voiceover with a microphone, and replace the AI-generated voice with your recording** by changing a few lines of code.

In other words, it is possible to produce entire videos without ever having to use an external video editor. Watch the YouTube video for a brief tour of the functionality offered by `manim-speech`:

[![Manim-speech YouTube introduction](http://img.youtube.com/vi/3S-8fsuxHVI/0.jpg)](http://www.youtube.com/watch?v=3S-8fsuxHVI "How to add voiceovers to your Manim videos easily with manim-speech")

It currently supports [Azure Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/), [gTTS](https://github.com/pndurette/gTTS/) and [pyttsx3](https://github.com/nateshmbhat/pyttsx3).

## Install in development mode

`manim-speech` is in active development, so we recommend you to install it in development mode:

```sh
# Clone the repository and change directory
git clone git@github.com:MathBlocks/manim-speech.git
cd manim-speech/

# Install the package in development mode
pip3 install --editable .

# Render and play an example
manim -pql examples/gtts-example.py --disable_caching
```

If you only hear the first line, you need to run `manim` with the `--disable_caching` flag. This is due to a bug in Manim and will be fixed in the future.

[The example above](examples/gtts-example.py) uses [gTTS](https://github.com/pndurette/gTTS/) which calls the Google Translate API and therefore needs an internet connection to work. If it throws an error, there might be a problem with your internet connection or the Google Translate API.

<!-- Once SoX is installed, proceed with installing `manim-speech`:

```sh
cd manim-speech
python setup.py install
``` -->

### Installing SoX

`manim-speech` can make the output from speech synthesizers faster or slower using [SoX](http://sox.sourceforge.net/). For this to work, version 14.4.2 or higher needs to be installed.

To install SoX on Mac with Homebrew:

```brew install sox```

On Debian based distros:

```sudo apt-get install sox```

or install [from source](https://sourceforge.net/projects/sox/files/sox/).

## Basic Usage

To use `manim-speech`, you simply import the `VoiceoverScene` class from the plugin

```py
from manim_speech import VoiceoverScene
```

You make sure your Scene classes inherit from `VoiceoverScene`:

```py
class MyAwesomeScene(VoiceoverScene):
    def construct(self):
        ...
```

`manim-speech` offers multiple text-to-speech engines, some proprietary and some free. A good one to start with is gTTS, which uses Google Translate's proprietary API. We found out that this is the best beginner's solution in terms of cross-platform compatibility.

```py
from manim_speech import VoiceoverScene
from manim_speech.interfaces import GTTSSpeechSynthesizer

class MyAwesomeScene(VoiceoverScene):
    def construct(self):
        self.set_speech_synthesizer(GTTSSpeechSynthesizer())
```

The logic for adding a voiceover is pretty simple. Wrap the animation inside a `with` block that calls `self.voiceover()`:

```py
with self.voiceover(text="This circle is drawn as I speak.") as tracker:
    ... # animate whatever needs to be animated here
```

Manim will animate whatever is inside that with block. If the voiceover hasn't finished by the end of the animation, Manim simply waits until it does. You can further use the `tracker` object for getting the total or remaining duration of the voiceover programmatically, which gives you finer control over the video:

```py
with self.voiceover(text="This circle is drawn as I speak.") as tracker:
    self.play(Create(circle), run_time=tracker.duration)
```

Using with-blocks results in clean code, allows you to chain sentences back to back and also serve as a documentation of sorts, as the video is neatly compartmentalized according to whatever lines are spoken during the animations.

See the [examples directory](./examples) for more examples. We recommend starting with the [gTTS example](https://github.com/MathBlocks/manim-speech/blob/main/examples/gtts-example.py).

## Configuring Azure

The highest quality text-to-speech services available to the public is currently offered by Microsoft Azure. To use it, you need to create an Azure account.

Then, you need to find out your subscription key and service region. Check out [Azure docs](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/) for more details.

Create a file called `.env` that contains your authentication information in the same directory where you call Manim.

```sh
AZURE_SUBSCRIPTION_KEY="..."
AZURE_SERVICE_REGION="..."
```