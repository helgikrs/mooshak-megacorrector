#i/usr/bin/python
import corrector
import os
import re
import subprocess
import sys
import re

filename = re.compile(r'^\[([^]]*)\](.*)')

def check_cppcheck():
    args = [ '/usr/bin/cppcheck', '--enable=style,unusedFunction,missingInclude', '--error-exitcode=1', corrector.submission_directory() ]
    p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    errs = p.stderr.read()
    if errs:
        for line in errs.splitlines():
            m = re.search(filename, line)
            if m:
                print '[%s]%s'%(os.path.basename(m.group(1)),m.group(2))
            else:
                print line
    return (p.returncode == 0)

def main(**kwargs):
    print "C++ Check Static Analyzer"

    if check_cppcheck():
        return (corrector.CORR_OK, corrector.ACCEPTED)
    else:
        return (corrector.CORR_ERROR, corrector.STATIC_ANALYSIS_ERROR)
