#!/usr/bin/env python2
from gimpfu import *
import time

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def hello(img):
    gimp.message("Hello World!")

register(
    "python-fu-hello-world",
    N_("Display 'Hello World!' message"),
    "Display message",
    "",
    "",
    "",
    N_("Hello"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None)
    ],
    [],
    hello,
    menu="<Image>/Filters/Tutorial",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
