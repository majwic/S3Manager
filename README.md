# S3 Utility App with Client-Side Encryption/Decryption
This S3 Utility App utilizes the boto3 library to interact with Amazon S3 services. The app allows users to perform the following operations:
- Create and delete S3 buckets.
- Upload and dowload files to and from S3 buckets.
- Use client-side encryption and decryption by entering a password for added security. This ensures that plaintext data is never sent over the net.

## Setup
### Prerequisites
- Python installed on your machine
- Install boto3 library
- Install cryptography library
- Install PyQt5 library
### Configuration
Before running the app, you need to set up AWS credentials on your system. This can be done by creating the follwing file at ~/.aws/credentials

Inside this credential file, add the following:

`[default]`

`aws_access_key_id = <your aws access key id>`

`aws_secret_access_key = <your aws secret access key>`

### Running the App
1. Clone the Repository
2. Run the utility app using Python `python main.py`

## Note on Security
- Never share your AWS credentials or encryption password with anyone.
- Ensure that you encryption password is strong and not easily guessable.
