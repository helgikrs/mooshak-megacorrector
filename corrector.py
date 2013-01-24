import sys
import re
import os
import optparse

# CORRECTOR CLASSIFICATIONS
# ---------------------------
# 0 - OK
# 1 - Warning
# 2 - Error
# ---------------------------

CORR_OK      = 0
CORR_WARNING = 1
CORR_ERROR   = 2

# MOOSHAK CLASSIFICATIONS
# ---------------------------
#  0 - Accepted
#  1 - Presentation Error
#  2 - Wrong Answer
#  3 - Output Limit Exceeded
#  4 - Memory Limit Exceeded
#  5 - Time Limit Exceeded
#  6 - Invalid Function
#  7 - Runtime Error
#  8 - Compile Time Error
#  9 - Invalid Submission
# 10 - Program Size Exceeded
# 11 - Requires Reevaluation
# 12 - Evaluating
# 13 - Memory Error
# 14 - Static Analysis error
# 15 - Accepted With Errors
# ---------------------------

ACCEPTED                =    0
PRESENTATION_ERROR      =    1
WRONG_ANSWER            =    2
OUTPUT_LIMIT_EXCEEDED   =    3
MEMORY_LIMIT_EXCEEDED   =    4
TIME_LIMIT_EXCEEDED     =    5
INVALID_FUNCTION        =    6
RUNTIME_ERROR           =    7
COMPILE_TIME_ERROR      =    8
INVALID_SUBMISSION      =    9
PROGRAM_SIZE_EXCEEDED   =   10
REQUIRES_REEVALUATION   =   11
EVALUATING              =   12
MEMORY_ERROR            =   13
STATIC_ANALYSIS_ERROR   =   14
ACCEPTED_WITH_ERRORS    =   15

classifications = [
     "Accepted",
     "Presentation Error",
     "Wrong Answer",
     "Output Limit Exceeded",
     "Memory Limit Exceeded",
     "Time Limit Exceeded",
     "Invalid Function",
     "Runtime Error",
     "Compile Time Error",
     "Invalid Submission,",
     "Program Size Exceeded",
     "Requires Reevaluation",
     "Evaluating",
     "Memory Error",
     "Static Analysis error",
     "Correct Output With Errors",
]

output_template = '<div style="white-space: pre;font-family: monospace; background: white; margin: 2mm; padding: 3mm; color: %s; font-size: 0.81em">%s</div>'

_previous_corrector = int(os.environ.get('PREVIOUS_CORRECTOR', -1))

def home():                 return os.environ['HOME']
def program():              return os.environ['PROGRAM']
def input():                return os.environ["INPUT"]
def expected():             return open(os.environ['EXPECTED']).read().strip()
def obtained():             return open(os.environ['OBTAINED']).read().strip()
def classify_code():        return int(os.environ['CLASSIFY_CODE'])
def previous_corrector():   return _previous_corrector 
def error():                return os.environ['ERROR']
def args():                 return os.environ['ARGS']
def context():              return os.environ['CONTEXT']
def submission_directory(): return os.path.dirname(program())

def is_error(classification):
    return classification > 0

def error_name(err):
    if err == -1:
        return ''
    if 0 < err < len(classifications):
        return classifications[err]
    return 'Uknown Error'

def submission_files(*args):
    res = []
    for root, dirs, files in os.walk(submission_directory()):
        for f in files:
            if any(f.endswith(ext) for ext in args):
                res.append(os.path.join(root,f))
    return res

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def output_html(output, color='red'):
    return output_template%(color,output)

class Result:
    def __init__(self, corrector_result=CORR_OK, classification=ACCEPTED):
        self.corrector_result = corrector_result
        self.classification = classification
        self.html_before = None
        self.html_after = None
        self.html_body = None
        self.html_header = None
