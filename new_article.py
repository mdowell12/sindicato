"""
Create a new article at the provided path (modify ARTICLE_FOLDER below).
The script expects that you've copied the contents of a Google doc to your clipboard
before running.

python ./new_article.py
"""
import os
import subprocess


ARTICLE_FOLDER = './articles/neighborhood/broadcast_08_24'

ARTICLE_TEMPLATE = './templates/article.html'
PARAGRAPH_TEMPLATE = './templates/paragraph.html'
ARTICLE_CONTENTS_TO_BE_REPLACED = 'ARTICLE_CONTENTS_TO_BE_REPLACED'
TEXT_TO_BE_REPLACED = 'TEXT_TO_BE_REPLACED'


def create_article(path, contents):
    # Do not overwrite an existing article
    if os.path.exists(ARTICLE_FOLDER):
        print("Folder already exists at path, exiting.")
        return
    # Make article directory
    os.makedirs(ARTICLE_FOLDER)
    # Make img directory
    os.makedirs(ARTICLE_FOLDER + "/img")
    # Make index.html
    with open(ARTICLE_TEMPLATE, 'r') as f:
        template = f.read()
    with open(PARAGRAPH_TEMPLATE, 'r') as f:
        paragrah_template = f.read()
    with open(ARTICLE_FOLDER + "/index.html", "w") as f:
        formatted_contents = format_contents(contents, paragrah_template)
        article = template.replace(ARTICLE_CONTENTS_TO_BE_REPLACED, formatted_contents)
        f.write(article)
    return


def format_contents(contents, paragraph_template):
    # Fix apostrophe
    contents = contents.replace(b'\xe2\x80\x99', b"'")
    # Fix quotation marks, start and end
    contents = contents.replace(b'\xe2\x80\x9c', b"\"")
    contents = contents.replace(b'\xe2\x80\x9d', b"\"")
    # No need to be binary string
    contents = contents.decode('ascii')
    # Create HTML elements for each paragraph
    paragraphs = contents.split('\n')
    result = []
    for paragraph in paragraphs:
        if paragraph.strip():
            result.append(paragraph_template.replace(TEXT_TO_BE_REPLACED, paragraph))
    return '\n'.join(result)


def get_contents_from_clipboard():
    result = subprocess.run('pbpaste', capture_output=True)
    if result.returncode != 0:
        print("Failed to get contents from clipboard")
        return None
    return result.stdout


def run():
    print(f"Creating new article at path {ARTICLE_FOLDER}")
    contents = get_contents_from_clipboard()
    create_article(ARTICLE_FOLDER, contents)
    print("Finished")


if __name__ == "__main__":
    run()
