# certGen.py

This is a simple python command line script to generate a certificate. It was
created for the SEES NASA program but can be easily modified to display other
content.

Usage:
./certGen.py -h --help --user [name] --level [level] --theme [theme] --file [fileName]

Themes follow the matplotlib naming scheme
[here](https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html). The
default is plasma.

Please format files with `[name] [level] [theme]` per line. The theme parameter
is optional and will default to plasma if left blank. Names are assumed to be
2 words long

`# ./certGen.py --user "jane doe" --level advanced`

![janeDoeCert](JaneDoeAdvanced.png)
