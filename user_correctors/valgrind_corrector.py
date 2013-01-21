#!/usr/bin/python
import corrector
import os
import re

rex = re.compile(r".*ERROR SUMMARY: (\d+) errors.*")
valgrind_file = os.path.join(corrector.submission_directory(), ".valgrind_log")

def read_valgrind():
    return open(valgrind_file).read()

def check_valgrind():
    data = read_valgrind()
    arr = data.split('\n')
    number_of_errors = int(rex.match(arr[-2]).group(1))

    if number_of_errors:
        print data.replace("\n", "\r\n")
        return (corrector.CORR_ERROR, corrector.MEMORY_ERROR)
    else:
        print "No memory errors found."

def main(*args, **kwargs):
    if os.path.exists(valgrind_file):
        print "Valgrind Corrector"
        return check_valgrind()
