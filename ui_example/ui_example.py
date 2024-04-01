#! /usr/bin/python

from gimpfu import *
import gtk
import gimpui
import gobject

def example_plugin_entry(_image, _drawable):
    window = gtk.Window()
    window.set_title("UI Example")
    window.connect('destroy',  close_plugin_window)
    window_box = gtk.VBox()
    window.add(window_box)
    window.show_all()
    gtk.main()

def close_plugin_window(ret):
    gtk.main_quit()

register(
          "python-fu-ui-example",
          "Description",
          "Description",
          "Author name",
          "Apache 2 license",
          "2022",
          "UI Example",
          "*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
          ],
          [],
          example_plugin_entry, 
          menu="<Image>/Filters/Tutorial"
        )
main()
