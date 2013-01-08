android-helper
==============

Helper script to do common task

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
