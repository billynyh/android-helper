#!/usr/bin/python
import sys, os, getopt

CURR = os.path.abspath( __file__ )
CURR_DIR = os.path.dirname(CURR)
OUTDIR = CURR_DIR + "/gen"
NORMAL_FS = "%s_normal"
ACTIVE_FS = "%s_active"

DEBUG = True

def print_usage():
    print 'usage: button_xml.py slug -n NORMAL_FS -a ACTIVE_FS'
    sys.exit(2)
    

def main(argv):
    global NORMAL_FS
    global ACTIVE_FS
    
    if len(argv) == 0:
        print_usage()
    if len(argv) > 1:
        try:
           opts, args = getopt.getopt(argv[1:],"n:a:")
        except getopt.GetoptError:
            print_usage()
        if DEBUG:
            print opts
        for opt, arg in opts:
            if opt == '-n':
                if arg.find("%s")==-1:
                    arg = "%s" + arg
                NORMAL_FS = arg
            elif opt == '-a':
                if arg.find("%s")==-1:
                    arg = "%s" + arg
                ACTIVE_FS = arg

    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    name = argv[0]
    f = open("assets/button.xml", "r")
    s = f.read()
    active_name = ACTIVE_FS % name
    normal_name = NORMAL_FS % name
    out = s % (active_name, normal_name)
    outfile = "%s/%s.xml" % (OUTDIR, name)

    if DEBUG:
        print out

    fout = open(outfile, "w+")
    fout.write(out)
    fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])
