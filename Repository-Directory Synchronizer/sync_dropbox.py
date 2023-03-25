import os
import time
import argparse
import shutil
import dropbox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Synchronizer(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir, filter_exts, access_token):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.filter_exts = filter_exts
        self.access_token = access_token
        self.dbx = dropbox.Dropbox(access_token)

    def on_any_event(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_ext = os.path.splitext(file_path)[1]
        file_name = os.path.basename(file_path)
        dest_file_path = os.path.join(self.dest_dir, file_name)
        dbx_file_path = "/" + os.path.relpath(dest_file_path, self.dest_dir).replace("\\", "/")

        if self.filter_exts and file_ext not in self.filter_exts:
            return

        if event.event_type == 'created' or event.event_type == 'modified':
            print(f"Copying {file_path} to {dest_file_path}")
            shutil.copy2(file_path, dest_file_path)
            with open(dest_file_path, "rb") as f:
                self.dbx.files_upload(f.read(), dbx_file_path, mode=dropbox.files.WriteMode("overwrite"))

        elif event.event_type == 'deleted':
            if os.path.exists(dest_file_path):
                print(f"Deleting {dest_file_path}")
                os.remove(dest_file_path)
                self.dbx.files_delete_v2(dbx_file_path)

def main():
    parser = argparse.ArgumentParser(description="Synchronize a source directory with a Dropbox folder.")
    parser.add_argument("src_dir", help="The source directory to synchronize.")
    parser.add_argument("dest_dir", help="The destination Dropbox folder to synchronize to.")
    parser.add_argument("-f", "--filter", help="Filter files by extension (e.g. '.txt,.docx').")
    parser.add_argument("-t", "--token", help="Dropbox API access token.")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src_dir)
    dest_dir = os.path.abspath(args.dest_dir)
    filter_exts = [] if not args.filter else args.filter.split(',')

    if not os.path.exists(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist.")
        return

    if not args.token:
        print("Error: No Dropbox API access token provided.")
        return

    observer = Observer()
    observer.schedule(Synchronizer(src_dir, dest_dir, filter_exts, args.token), src_dir, recursive=True)
    observer.start()

    print(f"Synchronizing {src_dir} with Dropbox folder '{dest_dir}'...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
