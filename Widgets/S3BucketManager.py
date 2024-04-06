import boto3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QVBoxLayout, QScrollArea

class S3BucketManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main layout
        layout = QVBoxLayout()

        # Create layout for bucket creation
        create_bucket_layout = self.setup_bucket_creation_layout()

        # Set up scroll area for displaying buckets
        scroll_area = self.setup_scroll_area()

        # Create layout for bucket deletion
        delete_bucket_layout = self.setup_bucket_deletion_layout()

        # Add layouts to main layout
        layout.addLayout(create_bucket_layout)
        layout.addWidget(scroll_area)
        layout.addLayout(delete_bucket_layout)

        # Populate bucket buttons
        self.populate_bucket_buttons()

        # Set main layout
        self.setLayout(layout)

        # Set widget background color
        #self.setStyleSheet("background-color: black;")

    def setup_bucket_creation_layout(self):
        create_bucket_layout = QHBoxLayout()

        # Input field for bucket name
        self.create_bucket_name_input = QLineEdit()
        self.create_bucket_name_input.setPlaceholderText("Enter Bucket Name")
        create_bucket_layout.addWidget(self.create_bucket_name_input)

        # Button for creating bucket
        self.create_button = QPushButton("Create Bucket")
        create_bucket_layout.addWidget(self.create_button)

        return create_bucket_layout

    def setup_scroll_area(self):
        # Set up scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Layout for bucket buttons
        self.bucket_buttons_layout = QVBoxLayout()
        self.bucket_buttons_layout.setAlignment(Qt.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.bucket_buttons_layout)

        scroll_area.setWidget(scroll_widget)

        return scroll_area
    
    def setup_bucket_deletion_layout(self):
        delete_bucket_layout = QHBoxLayout()

        # Input field for bucket name
        self.delete_bucket_name_input = QLineEdit()
        self.delete_bucket_name_input.setPlaceholderText("Enter Bucket Name")
        delete_bucket_layout.addWidget(self.delete_bucket_name_input)

        # Button for deleting bucket
        self.delete_button = QPushButton("Delete Bucket")
        delete_bucket_layout.addWidget(self.delete_button)

        return delete_bucket_layout

    def populate_bucket_buttons(self):
        # Get list of buckets from S3
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        self.bucket_buttons = []
        self.clear_bucket_buttons_layout()

        # Create button for each bucket and add to layout
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            button = QPushButton(bucket_name)
            self.bucket_buttons.append(button)
            self.bucket_buttons_layout.addWidget(button)

    def clear_bucket_buttons_layout(self):
        while self.bucket_buttons_layout.count():
            item = self.bucket_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()