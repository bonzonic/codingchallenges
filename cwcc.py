import argparse
import os

def countNumberOfBytes(text_file):
    print(os.path.getsize(text_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Our version of a wc tool!')
    parser.add_argument('-c', dest="wc", help='wc tool', type=str)

    args = parser.parse_args()
    text_file = args.wc
    countNumberOfBytes(text_file)


