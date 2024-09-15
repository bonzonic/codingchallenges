"""
Name: Wong Yi Zhen Nicholas
StudentID: 32577869
"""
import sys
import os
import heapq


class Node:
    """Just a node
    """

    def __init__(self, value: int, left, right) -> None:
        """Initialize values

        Args:
            value (int): ascii value of the character
            left (Node): left child of Node
            right (Node): right child of Node
        """
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """Returns true if there is value, meaning it is the leaf of the graph

        Returns:
            bool: True or False
        """

        if self.value is not None:
            return True
        return False

    def get_left(self):
        """ Left child of the node

        Returns:
            Node: returns left child of node
        """
        return self.left

    def get_right(self):
        """Returns right child of node

        Returns:
           Node: right child of node
        """
        return self.right


class Binary:
    """Binary stuff that is managed by this binary class
    """

    def __init__(self) -> None:
        """Remove the bwtencoded.bin file if the file already existed
        """
        self.bitstring = ""
        if os.path.exists("bwtencoded.bin"):
            os.remove("bwtencoded.bin")
        self.file = open("bwtencoded.bin", "ab")

    def append_string(self, new_bitstring: str) -> None:
        """Append a string to the new bitstring

        Space Complexity: O(1)
        Time Complexity: O(N) where N is the length of the string due to string slicing by pack as bytes function

        Args:
            new_bitstring (str): string to be added and appended to the file
        """
        self.bitstring += new_bitstring
        self.pack_as_bytes()  # pack to bytes as soon as possible

    def pack_as_bytes(self) -> None:
        """Writing to the file if has 8 bits

        Space Complexity: O(1)
        Time Complexity: O(N) where N is the length of the string due to string slicing
        """
        while len(self.bitstring) >= 8:
            bitstring_to_write = self.bitstring[:8]
            self.bitstring = self.bitstring[8:]
            number_to_write = self.string_to_binary(bitstring_to_write)
            byte_to_write = number_to_write.to_bytes(1, byteorder="big")

            self.file.write(byte_to_write)

    def close(self) -> None:
        """Close the file
        """
        self.file.close()

    # def read_file(self):
    #     self.testing_file = open("bwtencoded.bin", "rb")
    #     data = self.testing_file.read(1)
    #     # print(integer_to_binary(int.from_bytes(data, byteorder="big")))
    #     while data:
    #         binary_value = integer_to_binary(int.from_bytes(data, byteorder="big")).zfill(8)
    #         print(binary_value)
    #         data = self.testing_file.read(1)

    def last_pack_as_bytes(self) -> None:
        """Pack the final bits by adding some 0's in the front

        Space Complexity: O(1)
        Time Complexity: O(N) where N is the length of the string due to string concatenation
        """

        bitstring_length = len(self.bitstring)
        remaining_length = 8 - bitstring_length
        self.bitstring += ("0" * remaining_length)
        self.pack_as_bytes()

    def string_to_binary(self, string: str) -> int:
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


def permutation(string: str) -> str:
    """BWT text construction

    Args:
        string (str): The string to be transformed

    Space Complexity: O(1)
    Time Complexity: O(N^3) where N is the length of the string due to string slicing and loops

    Returns:
        str: BWT of the string
    """
    return_arr = []
    for index in range(len(string)):
        new_char = ""
        for k in range(len(string)):
            new_char += string[(index + k) % len(string)]
        return_arr.append(new_char)
    return_arr = sorted(return_arr)

    # getting the last character of each string
    return_str = ""
    for str in return_arr:
        return_str += str[-1]
    return return_str


def encoding(string: str) -> None:
    """Encodes the string and adds them into the file

    Space Complexity: O(N) where N is the length of the string
    Time Complexity: O(N^2) where N is the length of the string

    Args:
        string (str): The string to be encoded
    """
    binary_class = Binary()

    # length of string
    string_length = len(string)
    elias_recursion(binary_class, integer_to_binary(
        string_length))  # appends the length right away

    # number of distinct characters
    unique_char_ascii, huffman_codeword = huffman(string)

    # compute lenght and encode in elias
    elias_recursion(binary_class, integer_to_binary(len(unique_char_ascii)))

    # for each distinct charatcer in bwt string
    for number in unique_char_ascii:
        # 7-bit ascii code word
        binary_class.append_string(
            integer_to_binary(number+36).zfill(7))  # O(N)

        huffman_code = huffman_codeword[number]

        # length of huffman code word
        elias_recursion(binary_class, integer_to_binary(len(huffman_code)))

        # huffman codeword
        binary_class.append_string(huffman_code)

    # IF EMPTY STRING, THIS IS GONNA CRASHHH
    temp_char = [string[0], 0]
    binary_class.append_string(huffman_codeword[ord(string[0]) - 36])

    # for each runlength encoded
    for char in string:

        if char != temp_char[0]:
            # add the length
            elias_recursion(binary_class, integer_to_binary(temp_char[1]))

            temp_char = [char, 1]

            huffman_code = huffman_codeword[ord(char) - 36]

            # append the string to the file
            binary_class.append_string(huffman_code)

        else:
            temp_char[1] += 1

    # at the end
    elias_recursion(binary_class, integer_to_binary(temp_char[1]))

    binary_class.last_pack_as_bytes()
    binary_class.close()


def huffman(string: str) -> tuple[list[int], list[str]]:
    """Huffman encoding

    Args:
        string (str): The string to be encoded

    Space Complexity: O(N) where N is the length of the heap array
    Time Complexity: O(NlogN) where N is the length of the heap array and log N due to the push and pop operations of the heap 

    Returns:
        tuple[list[int], list[str]]: first element is the list of distinct characters in ascii representation, the second element is the huffman codeword for each alphabet
    """

    # getting the frequencies for each letter
    count = [None] * 91

    unique_char_ascii = []  # list that contains ascii values

    for char in string:
        ascii_char = ord(char) - 36

        if count[ascii_char] is None:
            count[ascii_char] = 1
            unique_char_ascii.append(ascii_char)

        else:
            count[ascii_char] += 1

    # heapify stuff
    heap_array = []
    heapq.heapify(heap_array)
    node_array = []

    for char in unique_char_ascii:
        # heapq.heappush(heap_array, (count[char], char, Node(char, None, None)))
        heapq.heappush(heap_array, (count[char], char, -1))

    while len(heap_array) > 1:
        item1 = heapq.heappop(heap_array)
        item2 = heapq.heappop(heap_array)

        # not an intermediate node
        if item1[2] != -1:
            left_node = node_array[item1[2]]

        else:
            left_node = Node(item1[1], None, None)

        if item2[2] != -1:
            right_node = node_array[item2[2]]

        else:
            right_node = Node(item2[1], None, None)

        combination_node = Node(None, left_node, right_node)

        length_node_array = len(node_array)

        node_array.append(combination_node)

        heapq.heappush(heap_array, (item1[0]+item2[0], -1, length_node_array))

    # deconstruct tree time
    root = heapq.heappop(heap_array)
    array = [None] * 91
    if root[2] == -1:
        array[root[1]] = "0"
    else:
        huffman_codeword = deconstruct_tree(node_array[root[2]], array)
    return unique_char_ascii, huffman_codeword


def deconstruct_tree(root: Node, array, result_string="") -> list[str]:
    """Deconstruct the tree to provide the huffman code for each letter

    Args:
        root (Node): the root of the graph
        array (_type_): the array to store the huffman code value for each letter
        result_string (str, optional): the resulting value of the huffman code

    Space Complexity: O(logk) where k is the number of nodes in the tree
    Time Complexity: O(logk) where k is the number of nodes in the tree

    Returns:
        list[str]: An array, storing the huffman code for all of the letters
    """

    # base case
    if root.is_leaf():
        array[root.value] = result_string
    else:
        left = root.get_left()
        right = root.get_right()

        if left is not None:
            deconstruct_tree(root.left, array, result_string+"0")

        if right is not None:
            deconstruct_tree(root.right, array, result_string+"1")

    return array


def elias_recursion(binary_class: Binary, binary_string: str) -> None:
    """Recursion form of elias

    Space Complexity: O(logN) where N is the length of the binary_string
    Time Complexity: O(NlogN) where N is the length of the binary_string 

    Args:
        binary_class (Binary): The binary class
        binary_string (str): Binary representation of the string you wish to encode in elias
    """

    # base case, has the first few elias codes as these are common, to be more efficient
    if len(binary_string) == 1:
        binary_class.append_string(binary_string)
        return

    binary_length = len(binary_string) - 1
    binary_new_string = "0" + bin(binary_length)[3:]  # O(N)

    # call the recursion first
    elias_recursion(binary_class, binary_new_string)

    # append to binary class
    binary_class.append_string(binary_string)


def q2(string) -> None:
    """Q2 stuff

    Time Complexity: O(N^3) due to creation of bwt string
    Space Complexity: O(N) where N is the length of the string

    Args:
        string (_type_): input string
    """
    string += "$"
    bwt_string = permutation(string)
    encoding(bwt_string)


if __name__ == "__main__":
    _, text_file = sys.argv
    text_file_content = open(text_file)

    for line in text_file_content:
        text = line.strip()

    q2(text)
    text_file_content.close()
