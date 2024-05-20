from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

class BlobClient:

    def __init__(self) -> None:
        CONNECTION_STRING = os.env('STORAGE_CONNECTION_STRING')
        self.BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(CONNECTION_STRING)

        CONTAINER_NAME = "recipemanager"
        self.CONTAINER_CLIENT = self.BLOB_SERVICE_CLIENT.get_container_client(container=CONTAINER_NAME)

    def list_blobs(self):
        try:
            blob_list = self.CONTAINER_CLIENT.list_blobs()
            return [blob.name for blob in blob_list]
        except Exception as e:
            print(f"Error listing blobs: {e}")

    def upload_blob(self, file_path, blob_name):
        try:
            with open(file_path, "rb") as data:
                blob_client = self.CONTAINER_CLIENT.get_blob_client(blob_name)
                blob_client.upload_blob(data)
        except Exception as e:
            print(f"Error uploading blob: {e}")


# TESTING
if __name__ == "__main__":
    blobclient = BlobClient()

    # blobclient.upload_blob("./README.md", "readme")
    print(blobclient.list_blobs())