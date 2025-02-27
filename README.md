# whisper-transcribe-cli

## Description

`whisper-transcribe-cli` is a command-line tool that helps transcribe video and audio files using OpenAI's Whisper model. It is particularly useful for generating transcripts for a large number of files in nested folders. Once the transcription is complete, the tool creates text files at the same location as the source files.

## Installation

To install the package, use the following command:

```sh
pip install whisper-transcribe-cli==0.1.1
```

## Usage

To start using `whisper-transcribe-cli`, you can run the following commands:

```sh
whisper-transcribe D:\Music --watch
```

```sh
whisper-transcribe PATH [WHISPER_MODEL] --watch
```

```sh
whisper-transcribe . --watch
```

### Parameters

- `PATH` (required): The path to the directory containing the files to be transcribed. Use `.` to transcribe files in the current directory.
- `WHISPER_MODEL` (optional): The Whisper model to use. Defaults to `tiny`. Available models are `tiny`, `base`, `small`, `medium`, `large`, `turbo` (in increasing order of better results).
- `--watch` (optional): Detects changes and transcribes new files as they are added. If omitted, the tool runs once and exits.
- `--no-watch` (optional): Runs the tool one time without watching for changes. By default, `--no-watch` is enabled.

## Example

To transcribe files in the `D:\Music` directory using the default `tiny` model and watch for new files:

```sh
whisper-transcribe D:\Music --watch
```

To transcribe files in a specified path using the `base` model without watching for new files:

```sh
whisper-transcribe D:\Music base --no-watch
```

To transcribe files in the current directory using the default `tiny` model and watch for new files:

```sh
whisper-transcribe . --watch
```
