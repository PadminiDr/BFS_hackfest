import os
import zipfile
from  dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

container_name = os.environ.get("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_client = blob_service_client.get_container_client(container_name)

def upload_file_to_blob(file_path, container, blob_path=None):
    blob_path = blob_path or file_path
    blob_client = container_client.get_blob_client(blob_path)

    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data)

def upload_directory_to_blob(directory_path, container_client, blob_path=None):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, directory_path)
            upload_file_to_blob(file_path, container_client, os.path.join(blob_path or "", relative_path))


def upload_zip_to_blob(zip_path, container_client, extract_to_blob=True):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        if extract_to_blob:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("temp")
                upload_directory_to_blob("temp", container_client)
                # Clean up extracted files
                os.system('rm -r temp')
        else:
            upload_file_to_blob(zip_path, container_client)

def upload_to_blob(path):
    if os.path.isfile(path):
        if zipfile.is_zipfile(path):
            upload_zip_to_blob(path, container_client)
        else:
            upload_file_to_blob(path, container_client)
    elif os.path.isdir(path):
        upload_directory_to_blob(path, container_client)
    else:
        print("The provided path is neither a file nor a directory.")

path = "your_file_or_directory_path"  # Replace with your path
upload_to_blob(path)