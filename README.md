Note to self: After reviewing this code this evening, I have changed and learnt so much since last laying eyes on this code 3 years ago. 
Hence, I should revist this and revamp it in Python 3 🙃

---

## Synopsis
***
* Tool to open up various storage formats and to convert between them.
* v0.0.1

## Objective

Write a command line tool which:
- shows how you would take some sets of personal data
    - name,
    - address,
    - phone_number
- serialise them/deserialise them in at least 2 formats.
- display it in at least 2 different ways (no need to use a GUI Framework).
- text output/HTML or any other human readable format is fine.

There is no need to support manual data entry - you could manually write a file
in one of your chosen formats to give you your input test data.

Write it in such a way that it would be easy for a developer:
- to add support for additional storage formats
- to query a list of currently supported formats
- to supply an alternative reader/writer for one of the supported formats

This should ideally show Object-Oriented Design and Design Patterns Knowledge,
were not looking for use of advanced Language constructs.

Provide reasonable Unit Test coverage.



## Examples
***
* <current_path> \> ```cd <path_to_repo>/src```
* python main.py -q
* python main.py -i ../data/personal.xml -r html
* python main.py -i ../data/personal.xml -o ../output/personal_out.json
* python main.py -i ../data/personal.xml


### Requirements
* Python 2.7 > installed and python.exe can be found from $PATH


## Installation
***
download https://github.com/uncojohnco/test-file-handler/archive/develop.zip or clone `https://github.com/uncojohnco/test-file-handler.git`

1. <current_path> \> ```cd <path_to_repo>/src```
2. <path_to_repo>/src \> ```python main.py -h```
