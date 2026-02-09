from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audio-tools",
    version="0.1.0",
    author="vanderh4",
    description="Simple implementations of audio tools (recorder, stt, tts)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanderh4/audio-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sounddevice>=0.4.6",
        "scipy>=1.11.0",
        "numpy>=1.24.0",
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
    ],
)
