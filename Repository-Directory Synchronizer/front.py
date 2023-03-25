import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sync import Synchronizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("Repository Synchronizer")
        self.setGeometry(100, 100, 600, 400)

        # Source directory label and input box
        self.src_label = QLabel("Source Directory:", self)
        self.src_label.move(10, 10)
        self.src_input = QLineEdit(self)
        self.src_input.setGeometry(10, 30, 400, 30)

        # Destination directory label and input box
        self.dest_label = QLabel("Destination Directory:", self)
        self.dest_label.move(10, 70)
        self.dest_input = QLineEdit(self)
        self.dest_input.setGeometry(10, 90, 400, 30)

        # Filter extension label and input box
        self.filter_label = QLabel("Filter by Extension (comma-separated):", self)
        self.filter_label.move(10, 130)
        self.filter_input = QLineEdit(self)
        self.filter_input.setGeometry(10, 150, 400, 30)

        # Dropbox API access token label and input box
        self.token_label = QLabel("Dropbox API Access Token:", self)
        self.token_label.move(10, 190)
        self.token_input = QLineEdit(self)
        self.token_input.setGeometry(10, 210, 400, 30)

        # Start/Stop button
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(10, 250, 100, 30)
        self.start_button.clicked.connect(self.start_synchronizer)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(120, 250, 100, 30)
        self.stop_button.clicked.connect(self.stop_synchronizer)
        self.stop_button.setEnabled(False)

        # Status label
        self.status_label = QLabel("Idle", self)
        self.status_label.setGeometry(10, 290, 200, 30)

        # Synchronizer object
        self.synchronizer = None

    def start_synchronizer(self):
        src_dir = self.src_input.text()
        dest_dir = self.dest_input.text()
        filter_exts = self.filter_input.text().split(',')
        token = self.token_input.text()

        if not os.path.exists(src_dir):
            self.status_label.setText("Error: Source directory does not exist.")
            return

        if not token:
            self.status_label.setText("Error: No Dropbox API access token provided.")
            return

        self.synchronizer = Synchronizer(src_dir, dest_dir, filter_exts, token)
        self.synchronizer_thread = QThread()
        self.synchronizer.moveToThread(self.synchronizer_thread)
        self.synchronizer_thread.started.connect(self.synchronizer.start)
        self.synchronizer.finished.connect(self.synchronizer_thread.quit)
        self.synchronizer.finished.connect(self.synchronizer.deleteLater)
        self.synchronizer_thread.finished.connect(self.synchronizer_thread.deleteLater)
        self.synchronizer_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Synchronizing...")

    def stop_synchronizer(self):
        if self.synchronizer:
            self.synchronizer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status
