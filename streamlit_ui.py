# filename: wikificator.py
# author: Mathijs Afman, Maxim van der Maesen de Sombreff, Thijmen Adam
# description: Takes a wikificated file and shows it with clickable links.
# usage: streamlit run streamlit_ui.py
# date: 05-06-2022

import streamlit as st
import sys

def open_raw_file(filename):
    """opens a raw file and returns it as a single string"""
    with open(filename) as inp:
        return inp.read()


def main():

    # target_path = path + sys.argv[1] + "/en.tok.off.pos.aut"

    target_input = st.file_uploader("Please upload a .aut file here", type=["aut"])

    if target_input != None:
        # raw_text = raw_file.read()
        target_path = target_input.read().decode()

        lines = target_path.split("\n")

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

    else:
        st.write("You should upload a .aut file, created by the wikificator.py"
                 " file that is included with the files of this project.")

if __name__ == "__main__":
    main()