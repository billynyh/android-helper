android-helper
==============

Helper script to do common task

to9patch.py
-----------
create 9patch with simple options.
usage: to9patch.py infile -x x_offset -y y_offset -o outfile
offset can be ?% or ?px, default is 20%

sample:
    ./to9patch sample/sample_normal.png 
    ./to9patch sample/sample_normal.png -x 20%
    ./to9patch sample/sample_normal.png -x 20% -y 30%
    ./to9patch sample/sample_normal.png -x 20% -y 30% -o sample/a.9.png

