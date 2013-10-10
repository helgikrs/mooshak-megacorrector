#!/usr/bin/python
import corrector
import os
import re

rex = re.compile(r".*ERROR SUMMARY: (\d+) errors.*")
valgrind_file = os.path.join(corrector.submission_directory(), ".valgrind_log")

def read_valgrind():
    return open(valgrind_file).read()

def error_count(data):
    arr = data.split('\n')
    match = rex.match(arr[-2])
    if match:
        number_of_errors = int(match.group(1))
    else:
        number_of_errors = 1

    return number_of_errors > 0

def sigsegv(data):
    return data.find("SIGSEGV") >= 0 

checkers = [error_count, sigsegv]

def show_error(data):
    for i in checkers:
        if i(data):
            return True
    return False

def check_valgrind():
    res = corrector.Result()
    res.html_header = '<h4>Valgrind Corrector</h4>'
    data = read_valgrind()

    if show_error(data):
        print data.replace("\n", "\r\n")
        res.html_before = '<p style="margin: 2mm">More information about the error messages produced by Valgrind can be found <a href="http://valgrind.org/docs/manual/mc-manual.html#mc-manual.errormsgs" target="_blank">here</a>.</p>'
        res.corrector_result = corrector.CORR_ERROR
        res.classification = corrector.MEMORY_ERROR
    else:
        print "No memory errors found."

    return res

def main(*args, **kwargs):
    if os.path.exists(valgrind_file):
        return check_valgrind()
