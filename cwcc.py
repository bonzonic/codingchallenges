import argparse
import os


def countNumberOfBytes(text_file):
    """
    Counts the number of bytes in a text_file

    Args:
        text_file (str): file to count the number of bytes

    Returns:
        void
    """
    print(os.path.getsize(text_file), text_file)


def countNumberOfLines(text_file):
    """
    Counts the number of lines in a text_file

    Args:
        text_file (str): file to count the number of lines

    Returns:
        void
    """
    with open(text_file, "rb") as f:
        num_lines = sum(1 for _ in f)
    print(num_lines, text_file)


def countNumberOfWords(text_file):
    """
    Counts the number of words in a text_file

    Args:
        text_file (str): file to count the number of words

    Returns:
        void
    """
    word_count = 0
    with open(text_file, "r", encoding="utf8") as f:
        for lines in f.readlines():
            line = lines.rstrip()
            words = line.split()
            word_count += len(words)
    print(word_count, text_file)


def countNumberOfCharacters(text_file):
    """
    Counts the number of characters in a text_file

    Args:
        text_file (str): file to count the number of characters

    Returns:
        void
    """
    character_count = 0
    with open(text_file, "r", newline='', encoding="utf8") as f:
        content = f.read()
        character_count = len(content)

    print(character_count, text_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Our version of a wc tool')
    parser.add_argument('-c', help='Counts the number of bytes', type=str)
    parser.add_argument('-l', help='Counts the number of lines', type=str)
    parser.add_argument('-w', help='Counts the number of words', type=str)
    parser.add_argument('-m', help='Counts the number of characters', type=str)

    args = parser.parse_args()
    if args.c:
        countNumberOfBytes(args.c)
    elif args.l:
        countNumberOfLines(args.l)
    elif args.w:
        countNumberOfWords(args.w)
    elif args.m:
        countNumberOfCharacters(args.m)
