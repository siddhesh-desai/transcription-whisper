from setuptools import setup, find_packages

setup(
    name="whisper-transcribe-cli",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "watchdog",
        "openai-whisper",
    ],
    entry_points={
        "console_scripts": [
            "whisper-transcribe=transcriptor.cli:app",
        ],
    },
)
