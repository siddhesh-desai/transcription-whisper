# This is the basic logic of working of the transcriptor. It processes the folder, transcribes the files and then watches for any changes in the folder and transcribes the new files as well. Just for direct testing

import constants
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


def process_folder(folderPath: str):
    """
    Ye function ek folder ke andar ke saare relevant files (jo hum transcribe karenge e.g. MOV, MP4 vegere) ko return karta hai
    """
    import os

    relevant_files = []

    # relevant files append karo
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(constants.AVAILABLE_EXTENSIONS):
                relevant_files.append(os.path.join(root, file))

    return relevant_files


def transcribe(fileList: list):
    """
    Ye function ek list of files leke usko transcribe karke, txt file main store karke, wo text files ka path return karta hai
    """
    import whisper
    import os

    output_files = []

    try:
        # Model load kiya
        model = whisper.load_model(constants.MODEL)

        for i in fileList:
            # Transcribe kiya
            result = model.transcribe(i)

            # Output file banaya
            output_file = os.path.splitext(i)[0] + ".txt"

            # Save karna
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])

            output_files.append(output_file)

        return output_files

    except Exception as e:

        print(e)
        return None

    return output_files


class TranscriptorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"event type: {event.event_type}  path : {event.src_path}")

        if event.is_directory:
            return

        if event.src_path.lower().endswith(constants.AVAILABLE_EXTENSIONS):
            print(f"[+] Transcribing {event.src_path}")
            transcribe([event.src_path])
            print(f"[+] Transcription Done")

    def on_deleted(self, event):
        print(f"event type: {event.event_type}  path : {event.src_path}")

        if event.is_directory:
            return

        if event.src_path.lower().endswith(constants.AVAILABLE_EXTENSIONS):
            if os.path.exists(os.path.splitext(event.src_path)[0] + ".txt"):
                print(f"[+] Deleting {os.path.splitext(event.src_path)[0] + '.txt'}")
                os.remove(os.path.splitext(event.src_path)[0] + ".txt")
                print(f"Deleted {os.path.splitext(event.src_path)[0] + '.txt'}")


if __name__ == "__main__":

    # Initial transcribe karo
    folder_to_transcribe = "D:\\Music"
    print(f"[+] Processing folder {folder_to_transcribe}")

    relevant_files = process_folder(folder_to_transcribe)
    print(f"[+] Following files will be transcribed: {relevant_files}")

    transcribe(relevant_files)
    print("[+] Initial Transcription Done")

    # Watcher declare karo
    print("[+] Starting Watcher")
    observer = Observer()
    event_handler = TranscriptorHandler()
    observer.schedule(event_handler, path=folder_to_transcribe, recursive=True)

    # Watcher start karo
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[+] Stopping Watcher")
        observer.stop()

    observer.join()
