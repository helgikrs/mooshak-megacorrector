#!/usr/bin/python
import corrector
import os

def main(*args, **kwargs):
    print "Time limit checker"

    tle_file = os.path.join(corrector.submission_directory(), ".time_limit_exceeded")

    if os.path.exists(tle_file):
        print "Execution took to long."
        os.unlink(tle_file)
        return (corrector.CORR_ERROR, corrector.TIME_LIMIT_EXCEEDED)
    else:
        print "Execution was within the time limit."
