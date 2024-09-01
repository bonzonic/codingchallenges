import argparse
import os


def countNumberOfBytes(text_file):
    """
    Counts the number of bytes in a text_file

    Args:
        text_file (str): file to count the number of bytes

    Returns:
        int: number of bytes in the file
    """
    return os.path.getsize(text_file)


def countNumberOfLines(text_file):
    """
    Counts the number of lines in a text_file

    Args:
        text_file (str): file to count the number of lines

    Returns:
        int: number of lines in the file
    """
    with open(text_file, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines


def countNumberOfWords(text_file):
    """
    Counts the number of words in a text_file

    Args:
        text_file (str): file to count the number of words

    Returns:
        int: number of words in the file
    """
    word_count = 0
    with open(text_file, "r", encoding="utf8") as f:
        for lines in f.readlines():
            line = lines.rstrip()
            words = line.split()
            word_count += len(words)
    return word_count


def countNumberOfCharacters(text_file):
    """
    Counts the number of characters in a text_file

    Args:
        text_file (str): file to count the number of characters

    Returns:
        int: number of characters in the file
    """
    character_count = 0
    with open(text_file, "r", newline='', encoding="utf8") as f:
        content = f.read()
        character_count = len(content)
    return character_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Our version of a wc tool')
    parser.add_argument(
        '-c', help='Counts the number of bytes', type=str, required=False)
    parser.add_argument(
        '-l', help='Counts the number of lines', type=str, required=False)
    parser.add_argument(
        '-w', help='Counts the number of words', type=str, required=False)
    parser.add_argument(
        '-m', help='Counts the number of characters', type=str, required=False)
    parser.add_argument('filename', help='The file to analyze', type=str)

    args = parser.parse_args()
    if args.c:
        print(countNumberOfBytes(args.c), args.c)
    elif args.l:
        print(countNumberOfLines(args.l), args.l)
    elif args.w:
        print(countNumberOfWords(args.w), args.w)
    elif args.m:
        print(countNumberOfCharacters(args.m), args.m)
    elif args.filename:
        filename = args.filename
        print(f"{countNumberOfLines(filename)} {countNumberOfWords(filename)} {countNumberOfBytes(filename)} {filename}")
