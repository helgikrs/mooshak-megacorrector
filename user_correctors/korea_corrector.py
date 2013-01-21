#!/usr/bin/python
import corrector
import os
import re
import subprocess
import csv
import sys

output_file = os.path.join(corrector.submission_directory(), '.nsiqcppstyle')

def urlify(s):
    return r'<a href="http://nsiqcppstyle.appspot.com/rules/%s" target="_blank">%s</a>'%(s,s.split('_',4)[-1].replace('_',' '))


def formatted_output():
    with open(output_file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        
        html = []
        for row in reader:
            html.append( '%s:%s:%s (%s) %s'%(os.path.basename(row[0]), row[1], row[2], urlify(row[4]), row[3]) )
        if html:
            return corrector.output_html('\n'.join(html))
        return None    

def invade_korea(rule_file):
    args =  ' '.join([ os.path.join(corrector.home(),'bin/nsiqcppstyle/nsiqcppstyle'), '-o', output_file, '-f', rule_file, '--output=csv'] + corrector.submission_files('.cpp'))
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    
    res = corrector.Result()
    res.html_header = "<h4>N'SIQ Style Checker</h4>"
    res.html_body = formatted_output()
    if res.html_body:
        res.corrector_result = corrector.CORR_ERROR
        res.classification = corrector.STATIC_ANALYSIS_ERROR
    else:
        res.corrector_result = corrector.CORR_OK
        res.classification = corrector.ACCEPTED
    return res

def main(rule_file, **kwargs):
    return invade_korea(rule_file)
