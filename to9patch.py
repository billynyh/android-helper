#!/usr/bin/python
import sys, os, getopt
import Image, ImageDraw

DEBUG = True

def get_9patch_name(fname):
    SUFFIX = ".9.png"
    if fname.endswith(SUFFIX):
        return fname
    if fname.endswith(".png"):
        return fname[0:-4] + SUFFIX
    return fname + SUFFIX

def get_offset(offset, l):
    offset_px = 0
    size = None
    default = (int)(l * 0.2)

    if offset is None:
        return default

    if offset.endswith("px"):
        offset_px = int(offset[0:-2])
        return offset_px
        
    elif offset.endswith("%"):
        p = float(offset[0:-1]) * 0.01
        return (int)(p * l)
    return default


def process_file(fname, offsets, outfile):
    ori = Image.open(fname)
    result = to9patch_from_offsets(ori, offsets)
    result.save(outfile, "PNG")

def to9patch_from_offsets(ori, offsets):
    (w,h) = ori.size

    o_t = get_offset(offsets[0], h)
    o_b = get_offset(offsets[2], h)
    o_l = get_offset(offsets[1], w)
    o_r = get_offset(offsets[3], w)


    lines = [
        (0, 1+o_l, 0, h-o_l),
        (w+1, 1+o_r, w+1, h-o_r),
        (1+o_t, 0, w-o_t, 0),
        (1+o_b, h+1, w-o_b, h+1)
    ]

    result = to9patch_from_lines(ori, lines)
    return result
    

def to9patch_from_lines(ori, lines):
    COLOR = (0,0,0,255)

    (w,h) = ori.size
    size = (w+2, h+2)

    result = Image.new('RGBA', size)
    result.paste(ori, (1,1))
    draw = ImageDraw.Draw(result)
    for line in lines:
        draw.line(line, fill=COLOR, width=1)
    del draw
    return result

def print_usage():
    print 'usage: to9patch.py infile -t top_offset -l left_offset -b bottom_offset -r right_offset -o outfile'
    print 'offset can be ?% or ?px, default is 20%'
    sys.exit(2)
    

def main(argv):
    arg_len = len(argv)
    if arg_len < 2:
        print_usage()
        
    fname = argv[1]
    outfile = None

    o_t = None
    o_l = None
    o_b = None
    o_r = None

    if arg_len > 2:
        try:
            opts, args = getopt.getopt(argv[2:],"o:t:l:b:r:")
        except getopt.GetoptError:
            print_usage()

        if DEBUG:
            print opts

        for opt, arg in opts:
            if opt == "-o":
                outfile = arg
            elif opt == "-t":
                o_t = arg
            elif opt == "-l":
                o_l = arg
            elif opt == "-b":
                o_b = arg
            elif opt == "-r":
                o_r = arg

    if outfile is None:
        outfile = get_9patch_name(fname)
   
    if o_t is None:
        o_t = o_b
    if o_b is None:
        o_b = o_t
    if o_l is None:
        o_l = o_r
    if o_r is None:
        o_r = o_l

    offsets = (o_t, o_l, o_b, o_r)
    process_file(fname, offsets, outfile)

if __name__=="__main__":
    main(sys.argv)
