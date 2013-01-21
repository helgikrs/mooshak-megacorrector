#!/usr/bin/python
import corrector
import os
import re

rex = re.compile(r".*ERROR SUMMARY: (\d+) errors.*")
valgrind_file = os.path.join(corrector.submission_directory(), ".valgrind_log")

def read_valgrind():
    return open(valgrind_file).read()

def check_valgrind():
    res = corrector.Result()
    res.html_header = '<h4>Valgrind Corrector</h4>'
    data = read_valgrind()
    arr = data.split('\n')
    number_of_errors = int(rex.match(arr[-2]).group(1))

    if number_of_errors:
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
