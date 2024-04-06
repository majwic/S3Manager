import boto3
from botocore.exceptions import ClientError
from Widgets.S3BucketManager import S3BucketManagerWidget
from PyQt5.QtWidgets import QMessageBox

def connect_handlers(bucket_manager_widget:S3BucketManagerWidget):
    # Get reference to the create and delete buttons from the S3BucketManagerWidget
    create_button = bucket_manager_widget.create_button
    delete_button = bucket_manager_widget.delete_button

    # Connect the bucket list buttons
    connect_bucket_list(bucket_manager_widget)

    # Connect click events for the create and delete buttons
    create_button.clicked.connect(lambda: create_button_clicked(bucket_manager_widget))
    delete_button.clicked.connect(lambda: delete_button_clicked(bucket_manager_widget))

def connect_bucket_list(bucket_manager_widget:S3BucketManagerWidget):
    # Iterate over each bucket button in bucket list
    for list_button in bucket_manager_widget.bucket_buttons:
        # Connect the click event of each bucket button to a function
        # The lambda function captures the current value of the list_button to avoid potential late binding issues
        list_button.clicked.connect(lambda: list_button_clicked(bucket_manager_widget, list_button.text()))

def list_button_clicked(bucket_manager_widget:S3BucketManagerWidget, list_button:str):
    # Set the text of the delete bucket input to the text of the clicked bucket button 
    delete_bucket_input = bucket_manager_widget.delete_bucket_name_input
    delete_bucket_input.setText(list_button)

def create_button_clicked(bucket_manager_widget:S3BucketManagerWidget):
    # Get the name of the bucket to create from input field
    create_bucket_name = bucket_manager_widget.create_bucket_name_input

    try:
        # Attempt to create the bucket using Boto3
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=create_bucket_name.text())

        # Update the bucket buttons and reconnect their click signals
        bucket_manager_widget.populate_bucket_buttons()
        connect_bucket_list(bucket_manager_widget)
    except ClientError as e:
        # Show an error message if bucket creation fails
        QMessageBox.critical(bucket_manager_widget, 'Error', str(e))

def delete_button_clicked(bucket_manager_widget:S3BucketManagerWidget):
    # Get the name of the bucket to delete from the input field
    delete_bucket_name = bucket_manager_widget.delete_bucket_name_input

    try:
        # Attempt to delete the bucket using Boto3
        s3_client = boto3.client('s3')
        s3_client.delete_bucket(Bucket=delete_bucket_name.text())
        
        # Update the bucket buttons and reconnect their click signals
        bucket_manager_widget.populate_bucket_buttons()
        connect_bucket_list(bucket_manager_widget)
    except ClientError as e:
        # Show an error message if bucket deletion fails
        QMessageBox.critical(bucket_manager_widget, 'Error', str(e))
