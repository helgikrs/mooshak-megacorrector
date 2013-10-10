#!/usr/bin/python
import corrector
import re
import os
import optparse
import difflib
import imp
import cgi

# diff_file = os.path.join(corrector.submission_directory(), '.p_specific_corrector_diff')

def main(checker='precheck.py', **kwargs):

    try:
        res = corrector.Result()
        res.corrector_result = corrector.CORR_OK
        res.classification = corrector.ACCEPTED
        res.html_header = "<h4>Pre-check</h4>"

        problem_dir = os.path.dirname(os.environ['SOLUTION'])
        checker_file = os.path.join(problem_dir, checker)
        chk = imp.load_source('chk', checker_file)

	if chk.precheck(res):
            res.corrector_result = corrector.CORR_OK
            res.classification = corrector.ACCEPTED
        else:
            res.corrector_result = corrector.CORR_OK
            res.classification = corrector.STATIC_ANALYSIS_ERROR

        return res

    except Exception, ex:
        #print(ex)
        import traceback
        res.html_body = traceback.format_exc()
        res.corrector_result = corrector.CORR_OK 
        res.classification = corrector.REQUIRES_REEVALUATION
        return res


#        if chk.check(expected=expected, obtained=obtained):
#            print "Correct answer"
#            if kwargs['has_error']:
#                res.corrector_result = corrector.CORR_OK
#                res.classification = corrector.ACCEPTED_WITH_ERRORS
#            else:
#                res.corrector_result = corrector.CORR_OK
#                res.classification = corrector.ACCEPTED
#        else:
#            res.corrector_result = corrector.CORR_ERROR
#            res.classification = corrector.WRONG_ANSWER
#
#            if (diff or show_inp) and show_diff():
#                res.html_body = ''
#
#                if show_inp:
#                    res.html_body += '<h5>Input</h5>'
#                    with open(corrector.input()) as inp:
#                        res.html_body += '''<div style="white-space: pre;font-family:
#                                monospace; background: white; margin: 2mm; padding:
#                                    3mm; ont-size:
#                                        0.81em">%s</div>'''%cgi.escape(inp.read())
#
#                if diff:
#                    differ = difflib.HtmlDiff(tabsize=4)
#                    res.html_body += '''<div style="background: white; margin: 2mm; padding: 3mm">
#    <p style="font-family: monospace; font-size: 0.81em; color: red">Output was not correct</p>
#    <h4>Difference between obtained and expected output</h4>'''
#                    res.html_body += differ.make_table(
#                                obtained.splitlines()[:MAXLINES],
#                                expected.splitlines()[:MAXLINES],
#                                'Obtained output', 'Expected output')
#                    res.html_body += '</div>'
#                    if len(expected.splitlines()) > MAXLINES or len(obtained.splitlines()) > MAXLINES:
#                        res.html_body += "<p>Output truncated..</p>"
#
#                    corrector.touch(diff_file)
#            else:
#                print "Output was not correct"

