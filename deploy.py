import os

import boto3

BUCKET_NAME = 'personal-news-site'
UPLOAD_IMAGES_FOR_ARTICLES_WITH_NAME_THAT_INCLUDES = [
    # 'overcast'
]
DIRECTORIES_TO_UPLOAD = [
    'articles',
    'authors',
    'meta',
    'favicon'
]
FILES_TO_UPLOAD = [
    'index.html',
    'styles.css',
    'styles-responsive-test.css',
]


def upload_directory(client, path, bucketname):
    for root, dirs, files in os.walk(path):
        for file in files:
            relative_path_to_file = os.path.join(root, file)
            upload_file(client, relative_path_to_file, bucketname)


def upload_file(client, relative_path_to_file, bucketname):
    if 'DS_Store' in relative_path_to_file:
        return
    content_type = get_content_type(relative_path_to_file)
    if is_image_file(content_type) and not should_upload_image(relative_path_to_file):
        print(f"Skipping image file {relative_path_to_file} with content_type {content_type}")
        return
    headers = get_headers_for_file(content_type)
    print(f"Uploading {relative_path_to_file} to {relative_path_to_file} with headers {headers}")
    client.upload_file(relative_path_to_file,
                       bucketname,
                       relative_path_to_file,
                       ExtraArgs=headers)


def get_headers_for_file(content_type):
    result = {
        'ContentType':f'{content_type}',
    }
    if is_image_file(content_type):
        # 30 day image cache
        result['CacheControl'] = 'max-age=2592000'
    return result


def should_upload_image(relative_path_to_file):
    for partial_article_name in UPLOAD_IMAGES_FOR_ARTICLES_WITH_NAME_THAT_INCLUDES:
        if partial_article_name in relative_path_to_file:
            return True
    return False


def is_image_file(content_type):
    return 'image' in content_type


def get_content_type(filename):
    if filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.txt'):
        return 'text/plain'
    elif filename.endswith('.json') or filename.endswith('.webmanifest'):
        return 'application/json'
    elif filename.endswith('.ico'):
        return 'image/x-icon'
    elif filename.endswith('.svg'):
        return 'image/svg+xml'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.JPG'):
        return 'image/jpeg'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.webp'):
        return 'image/png'
    raise Exception("Unknown content type for file " + filename)


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
