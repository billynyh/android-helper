#!/usr/bin/python

'''
    Copyright 2009, The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License. 
    You may obtain a copy of the License at 

        http://www.apache.org/licenses/LICENSE-2.0 

    Unless required by applicable law or agreed to in writing, software 
    distributed under the License is distributed on an "AS IS" BASIS, 
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
    See the License for the specific language governing permissions and 
    limitations under the License.
'''
# customized by billynyh 
# script to highlight adb logcat output for console
# written by jeff sharkey, http://jsharkey.org/
# piping detection and popen() added by other android team members


import os, sys, re, StringIO, getopt
import fcntl, termios, struct

# unpack the current terminal width/height
data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234')
HEIGHT, WIDTH = struct.unpack('hh',data)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

BLUE = CYAN
def format(fg=None, bg=None, bright=False, bold=False, dim=False, reset=False):
    # manually derived from http://en.wikipedia.org/wiki/ANSI_escape_code#Codes
    codes = []
    if reset: codes.append("0")
    else:
        if not fg is None: codes.append("3%d" % (fg))
        if not bg is None:
            if not bright: codes.append("4%d" % (bg))
            else: codes.append("10%d" % (bg))
        if bold: codes.append("1")
        elif dim: codes.append("2")
        else: codes.append("22")
    return "\033[%sm" % (";".join(codes))


def indent_wrap(message, indent=0, width=80):
    wrap_area = width - indent
    messagebuf = StringIO.StringIO()
    current = 0
    while current < len(message):
        next = min(current + wrap_area, len(message))
        messagebuf.write(message[current:next])
        if next < len(message):
            messagebuf.write("\n%s" % (" " * indent))
        current = next
    return messagebuf.getvalue()


LAST_USED = [RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE]
KNOWN_TAGS = {
    "dalvikvm": BLUE,
    "Process": BLUE,
    "ActivityManager": CYAN,
    "ActivityThread": CYAN,
}

def allocate_color(tag):
    # this will allocate a unique format for the given tag
    # since we dont have very many colors, we always keep track of the LRU
    if not tag in KNOWN_TAGS:
        KNOWN_TAGS[tag] = LAST_USED[0]
    color = KNOWN_TAGS[tag]
    LAST_USED.remove(color)
    LAST_USED.append(color)
    return color


RULES = {
    #re.compile(r"([\w\.@]+)=([\w\.@]+)"): r"%s\1%s=%s\2%s" % (format(fg=BLUE), format(fg=GREEN), format(fg=BLUE), format(reset=True)),
}

TAGTYPE_WIDTH = 3
TAG_WIDTH = 26
PROCESS_WIDTH = -1 # 8 or -1
HEADER_SIZE = TAGTYPE_WIDTH + 1 + TAG_WIDTH + 1 + PROCESS_WIDTH + 1

TAGTYPES = {
    "V": "%s%s%s " % (format(fg=WHITE, bg=BLACK), "V".center(TAGTYPE_WIDTH), format(reset=True)),
    "D": "%s%s%s " % (format(fg=BLACK, bg=BLUE), "D".center(TAGTYPE_WIDTH), format(reset=True)),
    "I": "%s%s%s " % (format(fg=BLACK, bg=GREEN), "I".center(TAGTYPE_WIDTH), format(reset=True)),
    "W": "%s%s%s " % (format(fg=BLACK, bg=YELLOW), "W".center(TAGTYPE_WIDTH), format(reset=True)),
    "E": "%s%s%s " % (format(fg=BLACK, bg=RED), "E".center(TAGTYPE_WIDTH), format(reset=True)),
    "S": "%s%s%s " % (format(fg=BLACK, bg=GREEN), "I".center(TAGTYPE_WIDTH), format(reset=True)),
}
TAG_MESSAGE_COLORS = {
    "V": format(fg=WHITE),
    "D": format(fg=BLUE),
    "I": format(fg=GREEN),
    "W": format(fg=YELLOW),
    "E": format(fg=RED),
    "S": format(fg=WHITE)
}

retag = re.compile("^(.*)([A-Z])/([^\(]+)\(([^\)]+)\): (.*)$")

white_list = None
black_list = None
show_time = False
level_filter = None

def read_list(fname):
    f = open(fname, "r")
    list = []
    while True:
        s = f.readline()
        if s:
            list.append(s[:-1])
        else:
            break
    return list

# to pick up -d or -e
#adb_args = ' '.join(sys.argv[1:])

# read white list / black list
try:
    opts, args = getopt.getopt(sys.argv[1:],"w:b:t:s:x:")
except getopt.GetoptError:
    pass
print opts
for opt, arg in opts:
    if opt == "-w":
        white_list = read_list(arg)
    elif opt == "-b":
        black_list = read_list(arg)
    elif opt == "-s":
        white_list = [arg]
    if opt == "-x":
        level_filter = arg
    if opt == "-t":
        show_time = arg == "1"
print "-- black list --"
print black_list
print "-- white list --"
print white_list
print show_time 
print level_filter


# if someone is piping in to us, use stdin as input.  if not, invoke adb logcat
if os.isatty(sys.stdin.fileno()):
    input = os.popen("adb logcat -v time")
else:
    input = sys.stdin


while True:
    try:
        line = input.readline()
    except KeyboardInterrupt:
        break

    match = retag.match(line)
    if not match is None:
        time, tagtype, tag, owner, message = match.groups()
        linebuf = StringIO.StringIO()
        tag = tag.strip()
        if not tagtype in TAGTYPES: 
            tagtype = "W"

        if not level_filter is None:
            if level_filter != tagtype:
                continue

        display = False
        if black_list and not tag in black_list:
            display = True
        if white_list and tag in white_list:
            display = True
        if white_list is None and black_list is None:
            display = True
    
        #print tag + " " + ",".join(black_list) + " " + str(tag in black_list)
        if not display:
            continue

        # center process info
        if PROCESS_WIDTH > 0:
            owner = owner.strip().center(PROCESS_WIDTH)
            #linebuf.write("%s%s%s " % (format(fg=BLACK, bg=BLACK, bright=True), owner, format(reset=True)))
            linebuf.write("%s%s%s " % (TAG_MESSAGE_COLORS[tagtype], owner, format(reset=True)))

        if show_time:
            linebuf.write("%s%s %s" % (TAG_MESSAGE_COLORS[tagtype], time, format(reset=True)))

        # right-align tag title and allocate color if needed
        tag = tag[-TAG_WIDTH:].rjust(TAG_WIDTH)
        linebuf.write("%s%s %s" % (TAG_MESSAGE_COLORS[tagtype], tag, format(reset=True)))

        # write out tagtype colored edge
        linebuf.write(TAGTYPES[tagtype])

        # insert line wrapping as needed
        message = indent_wrap(message, HEADER_SIZE, WIDTH)

        # format tag message using rules
        for matcher in RULES:
            replace = RULES[matcher]
            message = matcher.sub(replace, message)

        linebuf.write("%s%s%s" % (TAG_MESSAGE_COLORS[tagtype], message, format(reset=True)))
        line = linebuf.getvalue()

    print line
    if len(line) == 0: break

