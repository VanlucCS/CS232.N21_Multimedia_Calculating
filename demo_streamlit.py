# Demo nén và giả nén dữ liệu của hai thuật toán ARITHMETIC AND ADAPTIVE HUFFMAN với Streamlit
# Nhóm thực hiện:  
# Trần Văn Lực - 20521587  

# Ngô Ngọc Sương - 20521852  

# Nguyễn Văn Hợp - 20521358 

import streamlit as st
import pandas as pd
import sys

# Arithmetic Coding 
from collections import defaultdict
from fractions import Fraction
from decimal import Decimal
from time import time
import decimal
import os
import math

# Arithmetic Coding algothrim
def calculate_probabilities(text):
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1
    
    total_chars = len(text)
    probabilities = {}
    cumulative_prob = Fraction(0, 1)
    
    for char, freq in frequencies.items():
        probability = Fraction(freq, total_chars)
        probabilities[char] = (cumulative_prob, cumulative_prob + probability)
        cumulative_prob += probability
    
    return probabilities
def encode_text(text, probabilities):
    lower = Fraction(0, 1)
    upper = Fraction(1, 1)
    range_width = Fraction(1, 1)
    for char in text:
        range_start, range_end = probabilities[char]
        upper = lower + range_width * range_end
        lower = lower + range_width * range_start
        range_width = upper - lower
    
    return (lower+upper)/2
def decode_text(encoded_value, probabilities, text_length):
    decoded_text = ""
    value = encoded_value
    
    for _ in range(text_length):
        for char, (range_start, range_end) in probabilities.items():
            range_width = range_end - range_start
            if range_start <= value < range_start + range_width:
                decoded_text += char
                value = (value - range_start) / range_width
                break
    
    return decoded_text


# Adaptive Huffman algothrim
def get_freq(text):
    freq = dict()
    for c in text:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    freq = dict(sorted([(a,freq[a]) for a in freq if freq[a]>0.0], key = lambda el: el[1], reverse = True))
    Nin = sum([freq[a] for a in freq])
    freq = dict([(a,freq[a]/Nin) for a in freq])
    return freq
def encoded_text( text,code):
    encoded = ''
    for char in text:
        encoded += code[char]
    return encoded
def decoded_text(code, encoded):
    decoded = ''
    temp = ''
    for bit in encoded:
        temp += bit
        for char in code:
            if code[char] == temp:
                decoded += char
                temp = ''
    return decoded
def write_to_file(filename, text):
    f = open(filename, 'w+')
    f.write(text)
    f.close()
def read_from_file(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text
    print("%Compress = "+str(compress_percent(text, encoded, decoded, code)))
class Node(object):
    def __init__(self, parent=None, left=None, right=None, weight=0, symbol=''):
        super(Node, self).__init__()
        self._parent = parent
        self._left = left
        self._right = right
        self._weight = weight
        self._symbol = symbol
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, parent):
        self._parent = parent
    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, left):
        self._left = left
    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, right):
        self._right = right
    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, weight):
        self._weight = weight
    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol
class AdaptiveHuffman(object):
    def __init__(self):
        super(AdaptiveHuffman, self).__init__()
        self.NYT = Node(symbol="NYT")
        self.root = self.NYT
        self.nodes = []
        self.seen = [None] * 256

    def get_code(self, s, node, code=''):
        if node.left is None and node.right is None:
            return code if node.symbol == s else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(s, node.left, code+'0')
            if not temp and node.right is not None:
                temp = self.get_code(s, node.right, code+'1')
            return temp

    def find_largest_node(self, weight):
        for n in reversed(self.nodes):
            if n.weight == weight:
                return n

    def swap_node(self, n1, n2):
        i1, i2 = self.nodes.index(n1), self.nodes.index(n2)
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]
        tmp_parent = n1.parent
        n1.parent = n2.parent
        n2.parent = tmp_parent
        if n1.parent.left is n2:
            n1.parent.left = n1
        else:
            n1.parent.right = n1

        if n2.parent.left is n1:
            n2.parent.left = n2
        else:
            n2.parent.right = n2

    def insert(self, s):
        node = self.seen[ord(s)]
        if node is None:
            spawn = Node(symbol=s, weight=1)
            internal = Node(symbol='', weight=1, parent=self.NYT.parent,
                            left=self.NYT, right=spawn)
            spawn.parent = internal
            self.NYT.parent = internal
            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal
            self.nodes.insert(0, internal)
            self.nodes.insert(0, spawn)
            self.seen[ord(s)] = spawn
            node = internal.parent

        while node is not None:
            largest = self.find_largest_node(node.weight)
            if (node is not largest and node is not largest.parent and
                    largest is not node.parent):
                self.swap_node(node, largest)
            node.weight = node.weight + 1
            node = node.parent

    def encode(self, text):
        result = ''
        for s in text:
            if self.seen[ord(s)]:
                result += self.get_code(s, self.root)
            else:
                result += self.get_code('NYT', self.root)
                result += bin(ord(s))[2:].zfill(8)
            self.insert(s)
        return result


    def get_ascii(self, bin_str):
        return chr(int(bin_str, 2))

    def decode(self, text):
        result = ''

        symbol = self.get_ascii(text[:8])
        result += symbol
        self.insert(symbol)
        node = self.root

        i = 8
        while i < len(text):
            node = node.left if text[i] == '0' else node.right
            symbol = node.symbol

            if symbol:
                if symbol == 'NYT':
                    symbol = self.get_ascii(text[i+1:i+9])
                    i += 8
                result += symbol
                self.insert(symbol)
                node = self.root
            i += 1
        return result
st.set_page_config(page_title="CS232")
# st.title("TÍNH TOÁN ĐA PHƯƠNG TIỆN - CS232 ")
st.title("DEMO nén dữ liệu văn bản - CS232")
tab1, tab2 = st.tabs(["ARITHMETIC", "ADAPTIVE HUFFMAN"])

with tab1:
    cols = st.columns(2)
    
    decoded_text = ""
    with cols[0]:
        # st.write("Encoded")
        c = st.radio("Cách nhập",('Text', 'From file'),key=8)
        encode_input = ""
        if c == 'Text':
            encode_input = st.text_input("Nhập input",key=1)
        else:
            uploaded_file = st.file_uploader("Upload an txt file", type=["txt","docx"],key=10)
            if uploaded_file is not None:
                encode_input = uploaded_file.read().decode("utf-8")
        # st.write(encode_input)
        encode  = st.button("Nén",key=3)
        if encode:
            # ARITHMETIC decode process
            text = encode_input
            start_time = time()

            probabilities = calculate_probabilities(text)
            encoded_value = encode_text(text, probabilities)
            encoded_value_float = float(encoded_value)
            end_time = time()
            execution_time = end_time - start_time
            st.write("Thời gian mã hóa: {0:.4f} s".format(execution_time))
            decoded_text = decode_text(encoded_value, probabilities, len(text))


            # ARITHMETIC encode output
            st.write("Encoded value:", encoded_value_float)
            # df_probabilities = pd.DataFrame(probabilities.items(), columns=['Symbol', 'Range'])
            # st.write("Encoded probabilities:", probabilities)

            # Performance
            st.write("Input size:", sys.getsizeof(text))
            compressed_size = sys.getsizeof(encoded_value)+sys.getsizeof(probabilities)
            st.write("Arithmetic Coding compressed size:", compressed_size)
            st.write("Compession ratio: {:.2f} ".format(1/((compressed_size)/(sys.getsizeof(text)))))
            st.write("Compession performance: {:.2%} ".format((1 - (compressed_size/(sys.getsizeof(text))))))


    with cols[1]:
      Decode = st.button("Giải Nén",key=6)
      if Decode:
        text = encode_input
        probabilities = calculate_probabilities(text)
        encoded_value = encode_text(text, probabilities)
        encoded_value_float = float(encoded_value)
        # decode
        start_time = time()
        decoded_text = decode_text(encoded_value, probabilities, len(text))
        end_time = time()
        decode_time = end_time - start_time
        st.write("Thời gian giải mã: {0:.4f} s".format(decode_time))
        st.write(decoded_text)



with tab2:
    cols = st.columns(2)
    decoded_text = ""
    with cols[0]:

        c = st.radio("Cách nhập",('Text', 'From file'),key=7)
        encode_input = ""
        if c == 'Text':
            encode_input = st.text_input("Nhập input",key=2)
        else:
            uploaded_file = st.file_uploader("Upload an txt file", type=["txt","docx"],key=9)
            if uploaded_file is not None:
                encode_input = uploaded_file.read().decode("utf-8")
        encode  = st.button("Nén",key=4)
        if encode:
            # AdaptiveHuffman decode process
            text = encode_input
            start_time = time()
            encoded = AdaptiveHuffman().encode(text)
            end_time = time()

            execution_time = end_time - start_time
            st.write("Thời gian mã hóa: {0:.4f} s".format(execution_time))


            # AdaptiveHuffman encode output
            st.write("Encoded value:", encoded[:100],"...")

            # Performance
            st.write("Data file size:", sys.getsizeof(text))
            st.write("Adaptive Huffman compressed length:", int(len(encoded)/8))
            st.write("Compession ratio: {:.2f} ".format(1/(int(len(encoded)/8)/(sys.getsizeof(text)))))
            st.write("Compession performance: {:.2%} ".format((1 - (int(len(encoded)/8)/(sys.getsizeof(text))))))


    with cols[1]:
        Decode = st.button("Giải Nén",key=5)
        if Decode:
            text = encode_input
            encoded = AdaptiveHuffman().encode(text)
            # decode
            start_time = time()
            decoded = AdaptiveHuffman().decode(encoded)
            end_time = time()
            decode_time = end_time - start_time

            st.write("Thời gian giải mã: {0:.4f} s".format(decode_time))
            st.write(decoded)
