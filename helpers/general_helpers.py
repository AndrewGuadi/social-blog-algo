import json


def write_to_json(data, filename='./data/categories.json'):
    """
    Writes the provided data to a JSON file.

    Args:
    - data: The data to be written to the file. This should be a Python dictionary or list.
    - filename: The name of the file where the data should be written. Defaults to 'categories.json'.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to the JSON file: {e}")



def read_json(file_path):
    """
    Reads a JSON file and returns the data.

    :param file_path: The path to the JSON file.
    :return: The data from the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data



def write_markdown_file(file_path, content):
    """
    Writes the provided content to a Markdown (.md) file.

    :param file_path: The path where the Markdown file will be saved.
    :param content: The content to write into the Markdown file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content successfully written to {file_path}")