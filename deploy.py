import os

import boto3

BUCKET_NAME = 'personal-news-site'
UPLOAD_IMAGES = False
DIRECTORIES_TO_UPLOAD = [
    'articles',
    'authors'
]
FILES_TO_UPLOAD = [
    'index.html',
    'styles.css',
]


def upload_directory(client, path, bucketname):
    for root, dirs, files in os.walk(path):
        for file in files:
            relative_path_to_file = os.path.join(root, file)
            upload_file(client, relative_path_to_file, bucketname)


def upload_file(client, relative_path_to_file, bucketname):
    content_type = get_content_type(relative_path_to_file)
    if 'image' in content_type and not UPLOAD_IMAGES:
        print(f"Skipping image file {relative_path_to_file} with content_type {content_type}")
        return
    print(f"Uploading {relative_path_to_file} to {relative_path_to_file} with content_type {content_type}")
    client.upload_file(relative_path_to_file,
                       bucketname,
                       relative_path_to_file,
                       ExtraArgs={'ContentType':f'{content_type}'})


def get_content_type(filename):
    if filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.txt'):
        return 'text/plain'
    elif filename.endswith('.json'):
        return 'application/json'
    elif filename.endswith('.ico'):
        return 'image/x-icon'
    elif filename.endswith('.svg'):
        return 'image/svg+xml'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.jpeg') or filename.endswith('.jpg'):
        return 'image/jpeg'
    elif filename.endswith('.png'):
        return 'image/png'


def run():
    print("Uploading website")
    session = boto3.Session(profile_name='news-site-admin')
    s3 = session.client('s3')
    for filename in FILES_TO_UPLOAD:
        upload_file(s3, filename, BUCKET_NAME)
    for directory in DIRECTORIES_TO_UPLOAD:
        upload_directory(s3, directory, BUCKET_NAME)
    print("Finished")


if __name__ == "__main__":
    run()
