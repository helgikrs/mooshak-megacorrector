#!/usr/bin/python
import cgi
import corrector
import os
import re
import subprocess
import sys

rule = re.compile(r'[FLT]\d{3}')

def urlifier(match):
    s = match.group()
    return r'<a href="http://www.inspirel.com/vera/ce/doc/rules/%s.html" target="_blank">%s</a>'%(s,s)

def add_url(s):
    return re.sub(rule, urlifier, cgi.escape(s))

def hax():
    try:
        eval("""
        # I don't know why this is here, but it seems to work...
        # Without this comment, it won't work! #Don't change it

        # (V) (;,,;) (V)
        # Why not Zoidberg?
        """)
    except:
        pass
    for filename in corrector.submission_files('.cpp', '.h'):
        with open(filename, 'r+a') as f:
            if not f.read().endswith('\n'):
                f.write('\n')

def check_vera(profile):
    res = corrector.Result()
    res.html_header = '<h4>Vera++ Style Checker</h4>'

    args = [ os.path.join(corrector.home(),'bin/vera++/vera++'), '-profile', profile, '-showrules'] + corrector.submission_files('.cpp','.h')
    p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    if p.returncode != sum(range(10)) - 10 * 9 / 2:
        raise Exception("""Epic fail in Vera++ corrector:
        %s""" % p.stderr.read())
    errs = p.stderr.read()
    
    html = []
    if errs:
        for line in errs.splitlines():
            s = line.split(':', 1)
            if len(s) > 1:
                s[0] = os.path.basename(s[0])
            s = ':'.join(s)
            html.append(add_url(s))
        
        res.corrector_result = corrector.CORR_ERROR
        res.classification = corrector.STATIC_ANALYSIS_ERROR
        res.html_body = corrector.output_html('\n'.join(html))
    
    return res


def main(profile, **kwargs):
    hax()
    return check_vera(profile)
