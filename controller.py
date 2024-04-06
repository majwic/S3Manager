import boto3
import os
from encryption_utils import *
from botocore.exceptions import ClientError
from functools import partial
from Widgets.S3BucketManager import S3BucketManagerWidget
from Widgets.S3FileManager import S3FileManagerWidget
from PyQt5.QtWidgets import QMessageBox, QFileDialog

def connect_handlers(bucket_manager_widget:S3BucketManagerWidget, file_manager_widget:S3FileManagerWidget):
    # Get reference to the create and delete buttons from the S3BucketManagerWidget
    create_button = bucket_manager_widget.create_button
    delete_button = bucket_manager_widget.delete_button

    # Connect the bucket list buttons
    connect_bucket_list(bucket_manager_widget, file_manager_widget)

    # Connect click events for the create and delete buttons
    create_button.clicked.connect(lambda: create_button_clicked(bucket_manager_widget, file_manager_widget))
    delete_button.clicked.connect(lambda: delete_button_clicked(bucket_manager_widget, file_manager_widget))

    # Get reference to the upload and download buttons from the S3FileManagerWidget
    upload_button = file_manager_widget.upload_button
    download_button = file_manager_widget.download_button

    # Connect click events for the upload and download buttons
    upload_button.clicked.connect(lambda: upload_button_clicked(file_manager_widget))
    download_button.clicked.connect(lambda: download_button_clicked(file_manager_widget))

def connect_bucket_list(bucket_manager_widget:S3BucketManagerWidget, file_manager_widget:S3FileManagerWidget):
    # Iterate over each bucket button in bucket list
    for bucket_button in bucket_manager_widget.bucket_buttons:
        # Connect the click event of each bucket button to a function
        bucket_name = bucket_button.text()
        bucket_button.clicked.connect(partial(bucket_button_clicked, bucket_manager_widget, file_manager_widget, bucket_name))

def connect_file_list(file_manager_widget:S3FileManagerWidget):
    # Iterate over each file button in file list
    for file_button in file_manager_widget.file_buttons:
        #Connect the click event of each file button to a function
        file_name = file_button.text()
        file_button.clicked.connect(partial(file_button_clicked, file_manager_widget, file_name))

def bucket_button_clicked(bucket_manager_widget:S3BucketManagerWidget, file_manager_widget:S3FileManagerWidget, bucket_button:str):
    # Set the text of the delete bucket input to the text of the clicked bucket button 
    delete_bucket_input = bucket_manager_widget.delete_bucket_name_input
    delete_bucket_input.setText(bucket_button)

    # Populate file manager widget with file buttons
    file_manager_widget.populate_file_buttons(bucket_button)
    connect_file_list(file_manager_widget)

    # Update bucket name for currently displayed bucket objects
    selected_bucket_name = file_manager_widget.selected_bucket
    selected_bucket_name.setText(bucket_button)

def file_button_clicked(file_manager_widget:S3FileManagerWidget, file_button:str):
    # Set the text of the download file input tot the text of the clicked bucket button
    download_file_input = file_manager_widget.download_file_name
    download_file_input.setText(file_button)

def create_button_clicked(bucket_manager_widget:S3BucketManagerWidget, file_manager_widget:S3FileManagerWidget):
    # Get the name of the bucket to create from input field
    create_bucket_name = bucket_manager_widget.create_bucket_name_input

    try:
        # Attempt to create the bucket using Boto3
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=create_bucket_name.text())

        # Update the bucket buttons and reconnect their click signals
        bucket_manager_widget.populate_bucket_buttons()
        connect_bucket_list(bucket_manager_widget, file_manager_widget)
    except ClientError as e:
        # Show an error message if bucket creation fails
        QMessageBox.critical(bucket_manager_widget, 'Error', str(e))

def delete_button_clicked(bucket_manager_widget:S3BucketManagerWidget, file_manager_widget:S3FileManagerWidget):
    # Get the name of the bucket to delete from the input field
    delete_bucket_name = bucket_manager_widget.delete_bucket_name_input

    try:
        # Attempt to delete the bucket using Boto3
        s3_client = boto3.client('s3')
        s3_client.delete_bucket(Bucket=delete_bucket_name.text())
        
        # Update the bucket buttons and reconnect their click signals
        bucket_manager_widget.populate_bucket_buttons()
        connect_bucket_list(bucket_manager_widget, file_manager_widget)
    except ClientError as e:
        # Show an error message if bucket deletion fails
        QMessageBox.critical(bucket_manager_widget, 'Error', str(e))

def upload_button_clicked(file_manager_widget:S3FileManagerWidget):
    # Get upload input parameters
    upload_file_name = file_manager_widget.upload_file_name.text()
    upload_password = file_manager_widget.upload_password_input.text()

    if len(upload_file_name) <= 0 or len(upload_password) <= 0:
        return
    
    options = QFileDialog.Options()
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(file_manager_widget, "Select File", "", "All Files (*)", options=options)

    if not file_path:
        return
    
    encrypt_file_path = encrypt_file(file_path, upload_password, upload_file_name)

    s3 = boto3.client('s3')
    try:
        response = s3.upload_file(encrypt_file_path, file_manager_widget.selected_bucket.text(), encrypt_file_path)
    except ClientError as e:
         # Show an error message if bucket deletion fails
        QMessageBox.critical(file_manager_widget, 'Error', str(e))
        return
    
    file_manager_widget.populate_file_buttons(file_manager_widget.selected_bucket.text())
    connect_file_list(file_manager_widget)

    os.remove(encrypt_file_path)

def download_button_clicked(file_manager_widget:S3FileManagerWidget):
    # Get upload input parameters
    download_file_name = file_manager_widget.download_file_name.text()
    download_password = file_manager_widget.download_password_input.text()

    if len(download_file_name) <= 0 or len(download_password) <= 0:
        return
    
    options = QFileDialog.Options()
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getSaveFileName(file_manager_widget, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)

    if not file_path:
        return
    
    s3 = boto3.client('s3')
    with open(file_path, 'wb') as f:
        s3.download_fileobj(file_manager_widget.selected_bucket.text(), download_file_name, f)

    decrypt_file(file_path, download_password)