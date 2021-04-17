import cv2
import gi

gi.require_version("Gdk", "3.0")
from gi.repository import Gdk

def fit_to_screen_size(image, screen_height):
	current_width = image.shape[1]
	current_height = image.shape[0]
	max_width, max_height = __get_screen_size(Gdk.Display.get_default())

	if current_height > max_height or current_width > max_width:
		dimensions = (int(current_width/current_height * screen_height), screen_height)
		return cv2.resize(image, dimensions)

	return image

def scale_to_height(image, target_height):
	current_width = image.shape[1]
	current_height = image.shape[0]
	dimensions = (int(current_width/current_height * target_height), target_height)
	return cv2.resize(image, dimensions)

def scale_to_width(image, target_width):
	current_width = image.shape[1]
	current_height = image.shape[0]
	dimensions = (target_width, int(current_height/current_width * target_width))
	return cv2.resize(image, dimensions)

def __get_screen_size(display):
	mon_geoms = [
		display.get_monitor(i).get_geometry()
		for i in range(display.get_n_monitors())
	]

	x0 = min(r.x			for r in mon_geoms)
	y0 = min(r.y			for r in mon_geoms)
	x1 = max(r.x + r.width  for r in mon_geoms)
	y1 = max(r.y + r.height for r in mon_geoms)

	return x1 - x0, y1 - y0

def calc_area(base, height):
	return base * height