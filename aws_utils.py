import boto3
from botocore.exceptions import NoCredentialsError



# Initialize the S3 client
s3 = boto3.client('s3')


def upload_file_to_s3(path_to_file, file_name, bucket):
    """
    Upload a file to an S3 bucket and return the URL to access it.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: URL to access the uploaded file
    """
    try:
        s3.upload_file(path_to_file, bucket, file_name)
        region = s3.meta.region_name
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"
        print(f"File {file_name} uploaded to {url}")

        return url

    except FileNotFoundError as e:
        print(f"The file {file_name} was not found")
        return None

    except NoCredentialsError:
        print("Credentials not available")

        return None


# Example usage
if __name__ == "__main__":

    # Upload an audio file
    audio_url = upload_file_to_s3(path_to_file="static/audio/test_3.wav",
                                  file_name='test_3.wav',
                                  bucket='police-radio-data')

    print(f"uploaded   {audio_url}")
