#!/usr/bin/env python2
from gimpfu import *
import time
import math


def correct_image(img, layer):
    gimp.context_push()
    img.undo_group_start()

    try:
        orig_width = img.width
        orig_height = img.height
        orig_ratio = orig_width/orig_height

        non_empty, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
        crop_width = x2-x1
        crop_height = y2-y1
        crop_ratio = crop_width / crop_height

        w = crop_width
        h = crop_height
        if crop_ratio > orig_ratio:
            w = orig_ratio * crop_height
        elif crop_ratio < orig_ratio:
            h = crop_width / orig_ratio

        offs_x = (orig_width - w) / 2.0
        offs_y = (orig_height - h) / 2.0
        pdb.gimp_image_crop(img, w, h, offs_x, offs_y)

        pdb.gimp_image_scale(img, orig_width, orig_height)


    except Exception as ex:
        gimp.message(getattr(ex, 'message', repr(ex)))

    img.undo_group_end()
    gimp.context_pop()




register(
    "python-fu-crop-keep-size",
    N_("Crop while preserving image size"),
    "Crop keep size",
    "",
    "",
    "",
    N_("Crop keep size"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    correct_image,
    menu="<Image>/MyTools",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
