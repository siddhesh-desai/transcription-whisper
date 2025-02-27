import typer
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from transcriptor import constants
import whisper

app = typer.Typer()


def process_folder(folderPath: str):
    """Retrieve all relevant files for transcription"""
    relevant_files = []
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(constants.AVAILABLE_EXTENSIONS):
                relevant_files.append(os.path.join(root, file))
    return relevant_files


def transcribe(fileList: list):
    """Transcribe files and save output as .txt"""
    output_files = []
    try:
        model = whisper.load_model(constants.MODEL)
        for file in fileList:
            result = model.transcribe(file)
            output_file = os.path.splitext(file)[0] + ".txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            output_files.append(output_file)
        return output_files
    except Exception as e:
        typer.echo(f"Error: {e}", color=typer.colors.RED)
        return None


class TranscriptorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"event type: {event.event_type}  path : {event.src_path}")
        if event.is_directory:
            return
        if event.src_path.lower().endswith(constants.AVAILABLE_EXTENSIONS):
            typer.echo(f"[+] Transcribing {event.src_path}", color=typer.colors.YELLOW)
            transcribe([event.src_path])
            typer.echo(f"[+] Transcription Done", color=typer.colors.GREEN)

    def on_deleted(self, event):
        print(f"event type: {event.event_type}  path : {event.src_path}")
        if event.is_directory:
            return
        if event.src_path.lower().endswith(constants.AVAILABLE_EXTENSIONS):
            txt_file = os.path.splitext(event.src_path)[0] + ".txt"
            if os.path.exists(txt_file):
                typer.echo(f"[+] Deleting {txt_file}", color=typer.colors.RED)
                os.remove(txt_file)
                typer.echo(f"Deleted {txt_file}", color=typer.colors.RED)


@app.command("transcribe-files")
def start(
    folder_to_transcribe: str = typer.Argument(
        ".", help="Folder to transcribe", show_default=True
    ),
    watch: bool = typer.Option(
        False, help="Watch for new files and transcribe them", show_default=True
    ),
    whisper_model: str = typer.Argument(
        constants.MODEL,
        help="Model to be used for processing - tiny, base, small, medium, large, turbo",
        show_default=True,
    ),
):
    """Start the transcription process and watch for new files"""

    if not os.path.exists(folder_to_transcribe):
        typer.echo(
            f"Error: {folder_to_transcribe} does not exist", color=typer.colors.RED
        )
        return

    if not os.path.isdir(folder_to_transcribe):
        typer.echo(
            f"Error: {folder_to_transcribe} is not a folder", color=typer.colors.RED
        )
        return

    if folder_to_transcribe == ".":
        folder_to_transcribe = os.getcwd()

    typer.echo(
        f"[+] Processing folder {folder_to_transcribe}", color=typer.colors.YELLOW
    )
    relevant_files = process_folder(folder_to_transcribe)
    typer.echo(f"[+] Transcribing: {relevant_files}", color=typer.colors.YELLOW)
    transcribe(relevant_files)
    typer.echo("[+] Transcription Done", color=typer.colors.GREEN)

    if watch:
        observer = Observer()
        event_handler = TranscriptorHandler()
        observer.schedule(event_handler, path=folder_to_transcribe, recursive=True)

        observer.start()
        typer.echo("[+] Watcher Started", color=typer.colors.GREEN)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            typer.echo("[+] Watcher Stopped", color=typer.colors.RED)
            observer.stop()
        observer.join()


if __name__ == "__main__":
    app()
