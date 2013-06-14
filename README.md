android-helper
==============

Helper script to do common task

clogcat.py
----------
colored logcat with tag filtering, modified from Jeff Sharkey's code

![clogcat screenshot][1]

### sample

    clogcat.py 
    clogcat.py -s MainActivity // filter log by one tag
    clogcat.py -x E // filter log by log level (E,W,V,D,I)
    clogcat.py -w white_list.txt // filter log by a list of tags, one tag per line in the txt file
    clogcat.py -s MainActivity -t 1 // also print time

### sample white_list.txt
    dalvikvm
    MainActivity
    BaseFragment
    CustomView



to9patch.py
-----------
create 9patch with simple options.

usage: to9patch.py infile -t top_offset -l left_offset -b bottom_offset -r right_offset -o outfile

offset can be ?% or ?px, default is 20%

### sample

    ./to9patch sample/sample_normal.png 
    ./to9patch sample/sample_normal.png -t 20%
    ./to9patch sample/sample_normal.png -t 20% -l 30%
    ./to9patch sample/sample_normal.png -t 20% -l 30% -o sample/a.9.png

button_xml.py
-------------
generate the xml for a 2 state button

usage: button_xml.py slug -n NORMAL_FS -a ACTIVE_FS

default drawable name formats are %s_normal and %s_active

screencap.py
------------
android screen cap using monkeyrunner
### usage

    monkeyrunner screencap.py


 [1]: https://raw.github.com/billynyh/android-helper/master/static/clogcat-1.jpg
