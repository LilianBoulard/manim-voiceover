#!/usr/bin/env python

from distutils.core import setup

setup(
    name="manim-speech",
    version="0.0.1",
    description="Manim plugin for speech synthesis and voiceover generation",
    author="prism0x",
    author_email="",
    url="",
    install_requires=[
        "manim",
        "sox",
        "azure-cognitiveservices-speech",
        "python-dotenv",
        "pygments",
        "pyttsx3",
        "gTTS",
    ],
    packages=["manim_speech"],
)
