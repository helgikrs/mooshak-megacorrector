#!/usr/bin/python
import corrector
import re
import os
import optparse
import difflib

# verbatim: Compares obtained and expected output verbatim. Overrides the --ignore_pattern option.',
# ci: Case insensitive comparison (default: false)',
# ip: A regular expression that determines which characters in the output should be
#    ignored. If no pattern is specified, verbatim comparison, ignoring leading
#    and trailing whitespaces, is made.', default = None)

diff_file = os.path.join(corrector.submission_directory(), '.regex_corrector')

MAXLINES = 10000

def show_diff():
    return not os.path.exists(diff_file)

def main(diff=False, verbatim=True, ci=False, ip=None, strip_lines=True, **kwargs):
    options = type("", (), {'verbatim': verbatim, 'ignore_pattern': ip,
        'case_insensitive': ci, 'strip_lines': strip_lines})

    try:
        res = corrector.Result()
        res.html_header = "<h4>Output comparer</h4>"

        orig_expected = corrector.expected()
        orig_obtained = corrector.obtained()
        expected, obtained = "", ""

        if options.strip_lines:
            orig_expected = '\n'.join(map(lambda l: l.strip(), orig_expected.splitlines()))
            orig_obtained = '\n'.join(map(lambda l: l.strip(), orig_obtained.splitlines()))
    
        if options.verbatim or options.ignore_pattern is None:
            expected = orig_expected
            obtained = orig_obtained
        else:
            ignore = re.compile(options.ignore_pattern)

            expected = re.sub(ignore, '', orig_expected)
            obtained = re.sub(ignore, '', orig_obtained)


        expected = expected.replace('\n', '')
        obtained = obtained.replace('\n', '')

        if options.case_insensitive:
            expected = expected.lower()
            obtained = obtained.lower()

        if expected.strip() == obtained.strip():
            print "Correct answer"
            if kwargs['has_error']:
                res.corrector_result = corrector.CORR_OK
                res.classification = corrector.ACCEPTED_WITH_ERRORS
            else:
                res.corrector_result = corrector.CORR_OK
                res.classification = corrector.ACCEPTED
        else:
            if not diff:
                print "Output was not correct"
            res.corrector_result = corrector.CORR_ERROR
            res.classification = corrector.WRONG_ANSWER

            if diff:
                if show_diff():
                    differ = difflib.HtmlDiff(tabsize=4)
                    res.html_body = '''<div style="background: white; margin: 2mm; padding: 3mm">
                    <p style="font-family: monospace; font-size: 0.81em; color: red">Output was not correct</p>
                    <h4>Difference between obtained and expected output</h4>'''
                    res.html_body += differ.make_table(
                            orig_obtained.splitlines()[:MAXLINES],
                            orig_expected.splitlines()[:MAXLINES],
                            'Obtained output', 'Expected output')
                    res.html_body += '</div>'
                    if len(orig_expected.splitlines()) > MAXLINES or len(orig_obtained.splitlines()) > MAXLINES:
                        res.html_body += "<p>Output truncated..</p>"
                    corrector.touch(diff_file)
                else:
                    print "Output was not correct"
            
        return res

    except Exception, ex:
        print(ex)
        res.corrector_result = corrector.CORR_OK 
        res.classification = corrector.REQUIRES_REEVALUATION

