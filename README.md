# WC-tool
Own version of the Unix command line tool wc!  
Challenge: https://codingchallenges.fyi/challenges/challenge-wc

# Functionalities
These arguments simulate the wc tool in unix. There are 4 arguments it accepts:
```
cwcc.py -c <filename> -> counts the number of bytes in the file
cwcc.py -l <filename> -> counts the number of lines in the file
cwcc.py -m <filename> -> counts the number of characters in the file
cwcc.py -w <filename> -> counts the number of words in the file
cwcc.py <filename> -> displays number of lines, bytes and words of the file
```

# How To Use
1. Clone the repo and go to the 1-wctool directory by executing the code below in the terminal.
```
cd 1-wctool
```

2. There is a sample test.txt file to be used. An example of running the tool would be below.
```
python cwcc.py -l test.txt
```
