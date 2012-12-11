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


def to9patch(fname, offset_x, offset_y, outfile):
    COLOR = (0,0,0,255)

    ori = Image.open(fname)
    (w,h) = ori.size

    ox = get_offset(offset_x, w)
    oy = get_offset(offset_y, h)

    size = (w+2, h+2)
    result = Image.new('RGBA', size)
    result.paste(ori, (1,1))
    draw = ImageDraw.Draw(result)
    draw.line( (0, 1+oy, 0, h-oy), fill=COLOR, width=1 )
    draw.line( (w+1, 1+oy, w+1, h-oy), fill=COLOR, width=1 )
    draw.line( (1+ox, 0, w-ox, 0), fill=COLOR, width=1 )
    draw.line( (1+ox, h+1, w-ox, h+1), fill=COLOR, width=1 )
    del draw

    result.save(outfile, "PNG")

def print_usage():
    print 'usage: to9patch.py infile -x x_offset -y y_offset -o outfile'
    print 'offset can be ?% or ?px, default is 20%'
    sys.exit(2)
    

def main(argv):
    arg_len = len(argv)
    if arg_len < 2:
        print_usage()
        
    fname = argv[1]
    offset_x = None
    offset_y = None
    outfile = None

    if arg_len > 2:
        try:
            opts, args = getopt.getopt(argv[2:],"x:y:o:")
        except getopt.GetoptError:
            print_usage()

        if DEBUG:
            print opts

        for opt, arg in opts:
            if opt == "-x":
                offset_x = arg
            elif opt == "-y":
                offset_y = arg
            elif opt == "-o":
                outfile = arg

    if offset_y is None:
        offset_y = offset_x
    if offset_x is None:
        offset_x = offset_y
    if outfile is None:
        outfile = get_9patch_name(fname)
   
    to9patch(fname, offset_x, offset_y, outfile)

if __name__=="__main__":
    main(sys.argv)
