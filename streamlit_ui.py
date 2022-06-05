import streamlit as st
import os
import sys

def open_raw_file(filename):
    """opens a raw file and returns it as a single string"""
    with open(filename) as inp:
        return inp.read()


def main():

    path = os.getcwd()
    
    target_path = path + sys.argv[1] + "/en.tok.off.pos.aut"

    raw_text = open_raw_file(target_path)

    lines = raw_text.split("\n")

    line_list = []

    for line in lines:
        new_line = line.split(" ")
        line_list.append(new_line)

    print_string = ""

    for item in line_list:
        if len(item) > 4:
            if len(item) > 5:
                if "https" in item[6]:
                    print_string += " ["+ item[3] +"]("+ item[6]+ ")"
            else:
                print_string += " " + item[3]

    st.write(print_string)

if __name__ == "__main__":
    main()