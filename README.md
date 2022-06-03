# manim-speech

This is a [Manim](https://manim.community) plugin for generating voiceovers for your Manim animations.

It currently supports [Azure Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/), [gTTS](https://github.com/pndurette/gTTS/) and [pyttsx3](https://github.com/nateshmbhat/pyttsx3).

## Install in development mode

`manim-speech` is in active development, so we recommend you to install it in development mode:

```sh
# Clone the repository and change directory
git clone git@github.com:MathBlocks/manim-speech.git
cd manim-speech/

# Install the package in development mode
pip3 install --editable .

# Render and play the first example
manim -pql examples/example1.py --disable_caching
```

If you only hear the first line, you need to run `manim` with the `--disable_caching` flag. This is due to a bug in Manim and will be fixed in the future.

[The first example](examples/example1.py) uses [gTTS](https://github.com/pndurette/gTTS/) which calls the Google Translate API and therefore needs an internet connection to work. If it throws an error, there might be a problem with your internet connection or the Google Translate API.

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

## Examples

See the [examples directory](./examples).

## Configuring Azure

The highest quality text-to-speech available to the public is currently offered by Microsoft Azure.

Create a file called `.env` in the same directory where you call Manim with your authentication information.

For Azure, you need to specify your subscription key and service region. Check out [Azure docs](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/) for more details.

```sh
AZURE_SUBSCRIPTION_KEY="..."
AZURE_SERVICE_REGION="..."
```