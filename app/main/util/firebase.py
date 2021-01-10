from firebase_admin import storage
import os
from pathlib import Path


class Firebase:
    """ A light wrapper class on firebase services."""

    def __init__(self):
        self.bucket = storage.bucket()

    def upload(self, from_path, remove_on_completion = False):
        """ 
        Sync method uploading the specified path.
        Return: The public access url.
        """

        blob = self.bucket.blob(Path(from_path).name)
        blob.upload_from_filename(from_path)
        blob.make_public()

        if remove_on_completion:
            os.remove(from_path)

        # return blob.public_url, blob.media_link
        return blob

    def delete(self, file_name):
        """ 
        Sync method delete file.
        """
        blob = self.bucket
        return blob.delete_blob(Path(file_name).name)
