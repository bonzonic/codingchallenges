"""
Name: Wong Yi Zhen Nicholas
StudentID: 32577869
"""
import sys
import math


class Graph:
    """Graph to contain the root Node"""

    def __init__(self) -> None:
        """Initialize root node"""
        self.root = Node(None, None, None)


class Node:
    """Saves the value and the left and right child node"""

    def __init__(self, value: str, left, right) -> None:
        """Initializing the left, right child values along with the value itself

        Args:
            value (str): the value of the node
            left (Node): the left child of the node
            right (Node): the right child of the node
        """
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """Returns true or false if the node is a leaf

        Returns:
            bool: True/False
        """
        if self.value is not None:
            return True
        return False

    def get_left(self):
        """Getter for left child node

        Returns:
            Node: left child
        """
        return self.left

    def get_value(self) -> str:
        """Getter for value of the node

        Returns:
            str: Value of the node
        """
        return self.value

    def get_right(self):
        """Returns the right child of the node

        Returns:
            Node: right child of the node
        """
        return self.right

    def has_left(self) -> bool:
        """Returns True or False if the node has a left child or not

        Returns:
            bool: True or False depending on if the child has a left node
        """
        if self.get_left() is None:
            return False
        return True

    def has_right(self) -> bool:
        """Returns True or False if the node has a right child or not

        Returns:
            bool: True/False
        """
        if self.get_right() is None:
            return False
        return True


class BinaryPacker:
    """Binary Packer for unpacking bytes from the file"""

    def __init__(self, file: str) -> None:
        """Initializing values

        Args:
            file (str): The filename
        """
        self.file = open(file, "rb")
        self.bitstring = ""
        self.counter = 0

    def read_64bits(self) -> None:
        """Reading 64 bits

        Time Complexity: O(N) where N is the final length of the bitstring
        Space Complexity: O(1)
        """
        data = self.file.read(8)
        self.bitstring = self.bitstring[self.counter:]
        value = integer_to_binary(int.from_bytes(data, byteorder="big"))

        if len(value) <= 56:
            byte_number = math.ceil(len(value) / 8)
            self.bitstring += value.zfill(byte_number * 8)  # O(N)

        else:
            self.bitstring += value.zfill(64)
        self.counter = 0

    def close(self) -> None:
        """Closing the file"""
        self.file.close()

    def get_bitstring(self, length: int) -> str:
        """Get a certain length of the bitstring

        Args:
            length (int): The length it needs

        Time Complexity: O(N) where N is the final length of the bitstring
        Space Complexity: O(1)

        Returns:
            str: The section of the string
        """
        while length > len(self.bitstring) - self.counter:
            self.read_64bits()
        result = self.bitstring[self.counter: self.counter + length]
        self.add_counter(length)
        return result

    def add_counter(self, new_counter: int) -> None:
        """Adding counter to the bitstring

        Args:
            new_counter (int): The new counter to be added to the counter
        """
        self.counter += new_counter


def decoding(binary_class: BinaryPacker) -> str:
    """Decoding the bin file

    Args:
        binary_class (BinaryPacker): the binary class

    Time Complexity: O(NlogN) where N is the length of the string
    Space Complexity: O(N) where N is the length of the string

    Returns:
        str: The decoded string
    """
    string_length = decode_elias(binary_class)

    distinct_char_length = decode_elias(binary_class)

    graph = Graph()

    for _ in range(distinct_char_length):
        # ascii code
        codeword = binary_class.get_bitstring(7)
        character = chr(string_to_integer(codeword))

        # print(character)
        # length_huffman
        length_huffman_code = decode_elias(binary_class)

        # getting the huffman code
        # print(length_huffman_code)
        huffman_code = binary_class.get_bitstring(length_huffman_code)

        # construct huffman tree
        construct_huffman(graph.root, huffman_code, character)

    result_lst = []
    string_counter = 0
    while string_counter != string_length:
        value = decode_huffman(binary_class, graph.root)
        no_of_occurence = decode_elias(binary_class)
        counter = 0
        while counter < no_of_occurence:
            result_lst.append(value)
            counter += 1
        string_counter += counter

    # lf stuff
    result_str = lf(result_lst)

    return result_str


def decode_elias(binary_class: BinaryPacker) -> int:
    """Elias decoder

    Args:
        binary_class (BinaryPacker): the binary class which holds the bits

    Time Complexity: O(NlogN) where N is the number of bits of the elias representation encoded integer
    Space Complexity: O(1)

    Returns:
        int: An integer decoded by elias
    """
    component = binary_class.get_bitstring(1)
    while component[0] != "1":
        component = "1" + component[1:]

        component_length = string_to_integer(component) + 1

        component = binary_class.get_bitstring(component_length)

    return string_to_integer(component)


def construct_huffman(root: Node, string: str, value: str, counter: int = 0) -> Node:
    """ Constructing the huffman tree

    Args:
        root (Node): The root of the graph
        string (str): The huffman codeword
        value (str): The character of the huffman codeword
        counter (int, optional): counter of the string. Defaults to 0.

    Time Complexity: O(log N) where N is the number of nodes
    Space Complexity: O(log N) where N is the number of nodes

    Returns:
        Node: The root of the graph
    """
    # base case
    if counter == len(string):
        node = Node(value, None, None)
        return node

    if string[counter] == "0":
        if root.has_left():
            root.left = construct_huffman(
                root.get_left(), string, value, counter + 1)
        else:
            node = Node(None, None, None)
            root.left = construct_huffman(node, string, value, counter + 1)

    else:
        if root.has_right():
            root.right = construct_huffman(
                root.get_right(), string, value, counter + 1)
        else:
            node = Node(None, None, None)
            root.right = construct_huffman(node, string, value, counter + 1)

    return root


def decode_huffman(binary_class: BinaryPacker, node: Node) -> str:
    """Huffman decoder

    Args:
        binary_class (BinaryPacker): The binary class
        node (Node): Usually the root of the graph

    Time Complexity: O(log N) where N is the number of nodes of the graph
    Space Complexity: O(log N) where N is the number of nodes of the graph

    Returns:
        str: The result string 
    """
    # base case
    if node.is_leaf():
        return node.get_value()

    bit = binary_class.get_bitstring(1)

    if bit == "0":
        return decode_huffman(binary_class, node.get_left())
    else:
        return decode_huffman(binary_class, node.get_right())


def string_to_integer(string: str) -> int:
    """Converts binary string to integer value

    Args:
        string (str): binary string that consists of 0's and 1's

    Space Complexity: O(1)
    Time Complexity: O(N) where N is the length of the string

    Returns:
        int: The integer value of that binary string
    """
    result_number = 0
    string_length = len(string)

    for index, char in enumerate(string):
        if char == "1":
            temp_number = 1 << (string_length - index - 1)
            result_number |= temp_number

    return result_number


def integer_to_binary(number: int) -> str:
    """Returns a binary string with the "0b" chopped off

    Args:
        number (int): The integer to be changed to a binary string

    Space Complexity: O(1)
    Time Complexity: O(log N) where N is the number of the bits of that integer

    Returns:
        str: The binary string without the front part of "0b"
    """
    return bin(number)[2:]


def lf(last_column: list[str]) -> str:
    """LF mapping to invert a bwt

    Args:
        last_column (list[str]): The last column of the bwt table

    Time Complexity: O(NlogN) where N is the length of the string 
    Space Complexity: O(N) where N is the length of the string

    Returns:
        str: The original string
    """
    # get first column
    first_column = sorted(last_column)  # O(N log N)

    # compute rank
    rank_array = rank(first_column)

    # milestone creation
    milestones = milestone_creation(last_column)

    result_array = [None] * (len(last_column) - 1)

    result_idx = len(last_column) - 2

    index = 0

    for _ in range(1, len(last_column)):
        last_column_character = last_column[index]
        ascii_last_column_character = ord(last_column_character) - 36

        # getting rank value
        rank_value = rank_array[ascii_last_column_character]

        # get number of occurrences
        number = no_of_occurrences(
            milestones,
            last_column,
            last_column_character,
            index,
            ascii_last_column_character,
        )

        # get position
        pos = rank_value + number
        result_array[result_idx] = first_column[pos]
        result_idx -= 1
        # check the next character

        # print(last_column[index], rank_value, number, first_column[pos])
        index = pos

    result_str = "".join(result_array)

    return result_str


def rank(first_column: list[str]) -> list[int]:
    """Computes the rank for inverting the bwt

    Args:
        first_column (list[str]): The first column of the bwt table

    Time Complexity: O(N) where N is the length of the first column
    Space Complexity: O(1) constant space

    Returns:
        list[int]: The rank list
    """
    result_array = [None] * 91

    for index, char in enumerate(first_column):
        ascii_char = ord(char) - 36
        if result_array[ascii_char] is None:
            result_array[ascii_char] = index

    return result_array


def no_of_occurrences(
    milestones: list[list[int]],
    last_column: list[str],
    character: str,
    index: int,
    ascii_char: int,
) -> int:
    """Finding the number of occurrences for a certain letter

    Args:
        milestones (list[list[int]]): All the milestones in an array
        last_column (list[str]): The last column of the bwt array
        character (str): A character which we are dealing with for the last column
        index (int): The current index
        ascii_char (int): The ascii value of that character

    Time Complexity: O(K) where K is index - milestone_index
    Space Complexity: O(1)

    Returns:
        int: The number of occurrences for that letter from 1...index
    """
    no_of_occurence = milestones[index][0][ascii_char]

    milestone_index = milestones[index][1]

    for idx in range(milestone_index, index):
        if last_column[idx] == character:
            no_of_occurence += 1

    return no_of_occurence


def milestone_creation(last_column: list[str]) -> list[list[int]]:
    """Creating multiple milestones to make the LF-mapping faster

    Args:
        last_column (list[str]): The last column of the bwt table

    Time Complexity: O(Nlogk) where k is index - prev_index and N is the length of the string
    Space Complexity: O(N) where N is the length of the string

    Returns:
        list[list[int]]: A table of milestones
    """
    length_string = len(last_column)

    milestone_array = []

    k = math.ceil(math.log2(length_string))

    prev_array = [0] * 91

    prev_index = 0

    for index in range(length_string):
        if index % k == 0:
            milestone = individual_milestone(
                last_column, index, prev_index, prev_array)
            milestone_array.append((milestone, index))
            prev_index = index
            prev_array = milestone

        else:
            milestone_array.append(
                (prev_array, prev_index)
            )  # just stores the reference, should be fine

    return milestone_array


def individual_milestone(
    last_column: list[str], index: int, prev_index: int, prev_array: list[int]
) -> list[int]:
    """Creating each individual milestone

    Args:
        last_column (list[str]): The last column of the bwt table
        index (int): The current index
        prev_index (int): The previous index that had the individual milestone created
        prev_array (list[int]): The previous array that had the individual milestone created

    Time Complexity: O(k) where k is index - prev_index
    Space Complexity: O(N) where N is the length of the prev_array

    Returns:
        list[int]: The milestone array
    """
    result_array = []

    # deep copy of the array
    for value in prev_array:
        result_array.append(value)

    # take the space instead
    for idx in range(prev_index, index):
        ascii_element = ord(last_column[idx]) - 36
        result_array[ascii_element] += 1

    return result_array


def q2(file):
    """Q2 stuff

    Args:
        file (str): The file that we are supposed to open
    """
    binary_class = BinaryPacker(file)

    string = decoding(binary_class)
    binary_class.close()

    file = open("recovered.txt", "w")
    file.write(string)
    file.close()


if __name__ == "__main__":
    _, text_file = sys.argv

    q2(text_file)
