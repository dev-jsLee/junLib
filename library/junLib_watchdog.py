import os
import sys
import time
from . import junLib

# watchdog 임포트
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class folder_watchdogs(FileSystemEventHandler):
    def __init__(self, target_path, action=None, time_interval=1):
        self.action = action
        self.target_path = target_path
        self.observer = Observer()
        self.time_interval = self.validate_time_interval(time_interval)
        self.is_running = False

    def start_watchdog(self):
        if not self.is_running:
            self.observer = Observer()
            self.observer.schedule(self, path=self.target_path, recursive=True)
            self.observer.start()
            self.is_running = True  # Update the status to True when the watchdog is started

    def stop_watchdog(self):
        self.is_running = False

    def set_action(self, action):
        self.action = action

    def on_modified(self, event):
        if event.is_directory:
            return

        if self.action is not None:
            return self.action()

    def pause_watchdog(self):
        if self.is_running:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.is_running = False  # Update the status to False when the watchdog is paused


    def resume_watchdog(self):
        self.observer.start()

    def validate_time_interval(self, time_interval):
        while True:
            try:
                time_interval = int(time_interval)
                if time_interval < 1:
                    print("Time interval should be 1 second or more. Please enter a valid value.")
                else:
                    return time_interval
            except ValueError:
                print("Invalid input. Please enter a valid time interval in seconds.")

    def run(self):
        self.is_running = True
        event_handler = FileSystemEventHandler()
        event_handler.on_any_event = self.action

        observer = Observer()
        observer.schedule(event_handler, path=self.path, recursive=True)
        observer.start()

        try:
            while self.is_running:
                time.sleep(self.time_interval)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

if __name__ == "__main__":
    def custom_action():
        print("File has been modified!")

    target_path = input("Enter the target path to watch: ")
    time_interval = input('Enter time interval (default 1 second): ')
    handler = folder_watchdogs(target_path, action=custom_action, time_interval=time_interval)
    handler.run()
