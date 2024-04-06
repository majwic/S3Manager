import boto3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QPushButton

class S3FileManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main layout
        layout = QVBoxLayout()

        # Create layout for file upload
        upload_layout = self.setup_upload_layout()

        # Create widget for selected bucket
        selected_bucket = self.setup_selected_bucket()

        # Set up scroll area for displaying files
        scroll_area = self.setup_scroll_area()

        # Create layout for file download
        download_layout = self.setup_download_layout()

        # Add layouts to main layout
        layout.addLayout(upload_layout)
        layout.addWidget(selected_bucket)
        layout.addWidget(scroll_area)
        layout.addLayout(download_layout)

        # Set main layout
        self.setLayout(layout)

        # Set widget background color
        #self.setStyleSheet("background-color: black;")

    def setup_upload_layout(self):
        upload_layout = QHBoxLayout()

        # Input field for upload file name
        self.upload_file_name = QLineEdit()
        self.upload_file_name.setPlaceholderText("Enter File Name")
        upload_layout.addWidget(self.upload_file_name)

        # Input field for upload password
        self.upload_password_input = QLineEdit()
        self.upload_password_input.setPlaceholderText("Enter Password")
        upload_layout.addWidget(self.upload_password_input)

        # Button for uploading file
        self.upload_button = QPushButton("Upload File")
        upload_layout.addWidget(self.upload_button)

        return upload_layout
    
    def setup_selected_bucket(self):
        # Set up bucket QLabel
        self.selected_bucket = QLabel("None", self)

        return self.selected_bucket


    def setup_scroll_area(self):
        # Set up scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Layout for file buttons
        self.file_buttons_layout = QVBoxLayout()
        self.file_buttons_layout.setAlignment(Qt.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.file_buttons_layout)

        scroll_area.setWidget(scroll_widget)

        return scroll_area
    
    def setup_download_layout(self):
        download_layout = QHBoxLayout()

        # Input field for download file name
        self.download_file_name = QLineEdit()
        self.download_file_name.setPlaceholderText("Enter File Name")
        download_layout.addWidget(self.download_file_name)

        # Input field for download password
        self.download_password_input = QLineEdit()
        self.download_password_input.setPlaceholderText("Enter Password")
        download_layout.addWidget(self.download_password_input)

        # Button for downloading file
        self.download_button = QPushButton("Download File")
        download_layout.addWidget(self.download_button)

        return download_layout
    
    def populate_file_buttons(self, bucket:str):
        # Create an S3 client
        s3 = boto3.client('s3')
        file_names = []
        self.file_buttons = []
        self.clear_file_buttons_layout()

        # Use the paginator to retrieve a list of all objects in the bucket
        paginator = s3.get_paginator('list_objects_v2')
        operation_parameters = {'Bucket': bucket}

        # Iterate over each page of the bucket's objects
        for page in paginator.paginate(**operation_parameters):
            if 'Contents' in page:
                # Get each object name
                for obj in page['Contents']:
                    file_names.append(obj['Key'])

        # Create button for each file and add to layout
        for file in file_names:
            button = QPushButton(file)
            self.file_buttons.append(button)
            self.file_buttons_layout.addWidget(button)

    def clear_file_buttons_layout(self):
        while self.file_buttons_layout.count():
            item = self.file_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
