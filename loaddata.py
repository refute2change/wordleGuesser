import os

def load_data():
    # Check if the file exists
    if not os.path.exists("5letters.txt"):
        print("File not found!")
        return None

    # Load the data from the file
    with open("5letters.txt", "r") as f:
        words = f.read().splitlines()

    return words
