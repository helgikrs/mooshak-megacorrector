#!/usr/bin/python2
import cStringIO
import contextlib
import optparse
import os
import re
import sys

import emailer
import corrector

default_priority = [5, 2, 15, 13, 14, 3, 4, 6, 7, 8, 9, 10, 11, 12, 1, 0]

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


@contextlib.contextmanager
def withIO():
    stdout, stderr = sys.stdout, sys.stderr
    try:
        ret = [cStringIO.StringIO(), cStringIO.StringIO()]
        sys.stdout = ret[0]
        sys.stderr = ret[1]
        yield ret
    finally:
        sys.stdout = stdout
        sys.stderr = stderr

        ret[0] = ret[0].getvalue()
        ret[1] = ret[1].getvalue()


def exit(code):
    if corrector.is_error(code):
        print """<h3 style="color: red">%s</h3>""" % corrector.classifications[code]

    sys.exit(code)


def print_format(output, exit_code, print_header=True):
    if output.strip() == "" and print_header:
        return
    
    body = output
    if print_header:
        out = output.split('\n')
        header = out[0]
        body = "\n".join(out[1:]).strip()

        print "<h4>"
        print header
        print "</h4>"
    
    if exit_code == corrector.CORR_ERROR:
        color = "red"
    else:
        color = "green"
    
    if not body:
        if exit_code == corrector.CORR_ERROR:
            body = "Error Found"
        else:
            body = "OK"

    body = """<pre style="color: %s">%s</pre>""" % (color, body)

    print body

def print_result(output, res):
    header = bool(res.html_header)
    if header:
        print res.html_header
    if res.html_before:
        print res.html_before
    if not res.html_body:
        print_format(output, res.corrector_result, not header)
    else:
        print res.html_body
    if res.html_after:
        print res.html_after

def highest_priority(exit_codes, priority):
    exit = -1
    idx = 10000000

    for i in exit_codes:
        try:
            idxx = priority.index(i)
            if idxx < idx:
                idx = idxx
                exit = i
        except:
            pass

    if exit == -1:
        return 0
    return exit

def parse_arguments():
    parser = optparse.OptionParser(description='A Mooshak Mega Corrector(TM)')

    parser.add_option('-f', '--file',
            help='File containing the correctors', type="string", action='store', default="")

    parser.add_option('-t', '--type',
            help='Type of corrector', choices=['priority', 'overwrite', 'firsterr',], type="choice", action='store', default="priority")

    parser.add_option('-p', '--priority',
            help='Priority of exit statuses', type="string", action='store', default=', '.join(map(str, default_priority)))

    options, args = parser.parse_args()

    try:
        options.priority = map(lambda n: int(n), options.priority.split(',')) + default_priority
    except:
        parser.print_usage() 
        print "-p --priority Must be comma seperated integer values"
        exit(1)

    return options, args

def error(p, ex, out):
    print out[0]
    print """<p>There was an error in corrector %s: %r </br>
System admin has been notified</p>"""%(p, ex)
    emailer.send_bug_report(ex, p, corrector.submission_directory())
    
def run_corrector(options, pipeline):
    res = []
    has_error = False

    for prog in pipeline:
	if prog.startswith("!"):
            continue

        try:
            with withIO() as out:
                v = validate(prog.strip(), has_error)
            
            if v:
                if isinstance(v, corrector.Result):
                    print_result(out[0], v)
                    res.append( (v.corrector_result, v.classification) )
                    has_error |= bool(v.corrector_result)
                else:
                    print_format(out[0], v[0])
                    res.append(v)
                    has_error |= bool(v[0])
            else:
                print_format(out[0], False)
        except Exception, e:
            import traceback
            tb = traceback.format_exc()
            error(prog, tb, out)

    """
    if options.type == "overwrite":
        if exitc == -1:
            exitc = 0
        exit(exitc)
    elif options.type == "priority":
        exit(highest_priority(corrector.get_all_classifications(), options.priority))
    """

    exit(highest_priority(map(lambda n: n[1], res), options.priority))


def validate(prog, has_error):
    if prog.endswith(")"):
        prog = prog[:-1]
        module_name, args = prog.split("(", 1)
        module_name = module_name.strip()
        args = list(eval('(%s,)' % args))
    else:
        module_name = prog
        args = []

    module = __import__(module_name)

    return module.main(*args, has_error=has_error)

def parse_file(fd):
    return filter(lambda n: n.strip() != "", open(fd).read().split('\n'))

if __name__ == "__main__":
    this = '/'.join(os.path.realpath(__file__).split('/')[:-1])

    sys.path.append(this)
    sys.path.append(os.path.join(this, "user_correctors"))

    options, args = parse_arguments()

    if options.file:
        pipeline = parse_file(options.file)
    else:
        pipeline = args

    run_corrector(options, pipeline)
