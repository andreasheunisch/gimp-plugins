#!/usr/bin/env python2
from gimpfu import *
import time
import math

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)


def exit_invalid_path():
    gimp.message("path with exactly 2 achor points is required")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def rotate(self, angle):
        a,d = self.polar()
        return Vector(d * math.cos(a + angle), d * math.sin(a + angle))
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def direction(self):
        return math.atan2(self.y, self.x)

    def polar(self):
        return self.direction(), self.length()
    
def intersect(x0, p1, p2):
    delta = p2 - p1
    a = p1.x - x0
    b = delta.y / delta.x * a
    return Vector(p1.x + a, p1.y + b)


def intersect2(a_1, a_2, b_1, b_2):
    n = (a_2.y - a_1.y)*(b_2.x - b_1.x) - (b_2.y - b_1.y)*(a_2.x - a_1.x)
    z = (b_2.y - b_1.y)*(a_1.x - b_2.x) - (a_1.y - b_2.y)*(b_2.x - b_1.x)
    d = z/n
    return Vector(
        a_1.x + d * (a_2.x - a_1.x),
        a_1.y + d * (a_2.y - a_1.y)
    )


def rotation_angle_from_path(p1, p2):
    line = p1 - p2
    line.y *= -1
    angle = line.direction()
    if angle > 0.75*math.pi:
        angle -= math.pi
    elif angle > 0.25*math.pi:
        angle -= math.pi/2.0
    elif angle < -0.75*math.pi:
        angle += math.pi
    elif angle < -0.25*math.pi:
        angle += math.pi/2.0
    return angle


def crop_rotated_rectangle(width, height, angle):
    center = Vector(width / 2.0, height / 2.0)
    r_A = center + Vector(- width / 2.0, height / 2.0).rotate(angle)
    r_B = center + Vector(width / 2.0, height / 2.0).rotate(angle)
    r_C = center + Vector(width / 2.0, - height / 2.0).rotate(angle)
    r_D = center + Vector(- width / 2.0, - height / 2.0).rotate(angle)

    i_A = r_A
    i_B = r_B
    i_C = r_C
    i_D = r_D

    if r_D.x > r_A.x:
        i_C = intersect2(r_B, r_B + Vector(0,1), r_D, r_C)
        i_D = Vector(r_D.x, i_C.y)
        i_A = intersect2(r_D, r_D + Vector(0,-1), r_A, r_B)
    else:
        i_C = intersect2(r_C, r_C + Vector(0,1), r_D, r_C)
        i_D = Vector(r_A.x, i_C.y)
        i_A = intersect2(r_A, r_A + Vector(0,-1), r_A, r_B)
    
    crop_offset = i_A
    crop_width = abs(i_C.x - i_D.x)
    crop_height = abs(i_C.y - i_A.y)
    return crop_offset,crop_width,crop_height


def correct_image(img, layer):
    gimp.context_push()
    img.undo_group_start()

    path = None
    try:
        path = pdb.gimp_path_get_current(img)
    except Exception as ex:
        exit_invalid_path()

    if path is None:
        exit_invalid_path()

    else:
        path_id = pdb.gimp_path_get_current(img)
        path_type, path_closed, num_path_point_details, points_pairs = \
            pdb.gimp_path_get_points(img, path)
        pdb.gimp_path_delete(img, path_id)

        points = []
        for i in range(int(len(points_pairs) / 3)):
            x = points_pairs[3*i]
            y = points_pairs[3*i+1]
            t = points_pairs[3*i+2]
            if t == 1:
                points.append(Vector(x,y))
        print(str(points))

        if len(points) != 2:
            exit_invalid_path()

        else:
            try:
                angle = rotation_angle_from_path(points[0], points[1])
                rotated = pdb.gimp_item_transform_rotate(layer, angle, True, 0,0)
                # pdb.gimp_floating_sel_anchor(rotated)

                crop_offset, crop_width, crop_height = \
                crop_rotated_rectangle(img.width, img.height, angle)

                pdb.gimp_image_crop(img, crop_width, crop_height, crop_offset.x, crop_offset.y)
            
            except Exception as ex:
                gimp.message(getattr(ex, 'message', repr(ex)))


    img.undo_group_end()
    gimp.context_pop()




register(
    "python-fu-rotate-keep-size",
    N_("Adjust horizon while preserving image size"),
    "Adjust horizon",
    "",
    "",
    "",
    N_("Adjust horizon"),
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
