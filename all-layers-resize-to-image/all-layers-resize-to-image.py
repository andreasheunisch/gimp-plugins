#!/usr/bin/env python2
from gimpfu import *
import time

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def resize_all_layers(img):
    gimp.context_push()
    img.undo_group_start()

    for layer in img.layers:
        pdb.gimp_layer_resize_to_image_size(layer)

    img.undo_group_end()
    gimp.context_pop()


register(
    "python-fu-all-layers-resize-to-image",
    N_("Resize all layers to image size"),
    "Layers to image size",
    "",
    "",
    "",
    N_("All layers to image size"),
    "RGB*, GRAY*",
    [
            (PF_IMAGE, "image",       "Input image", None)
    ],
    [],
    resize_all_layers,
    menu="<Image>/Layer",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()

