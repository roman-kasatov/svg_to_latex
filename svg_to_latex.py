from xml.dom import minidom
from svgpathtools import *
import numpy as np
from tqdm import tqdm # Progress bar

from coloring_script import * # Browser console script

filename = 'nkshkn.svg'
precision = 4 # decimal places
path_seg_partition = 3 # 2 or more
types = ['line', 'circle', 'ellipse']
#types = ['line', 'circle', 'ellipse', 'rect']
colors = {'red' : '#FEFEFE', 'black' : '#000000'}

res_forms = open('result.txt', 'w')
res_colors = open('coloring.txt', 'w')
colors_array = []
current_color = '#000000'
styles = {}
doc = minidom.parse(filename)
doc.normalize() # why did i write this?

info = doc.getElementsByTagName('svg')[0]
(sizeX, sizeY) = map(float, info.attributes['viewBox'].value.split(' ')[2:])

def main():
	load_styles()
	print("Parsing simple figures...")
	for type in types:
		parse(type)
	print("Parsing paths...")
	paths = doc.getElementsByTagName('path')
	pbar = tqdm(total=paths.length, desc="paths processing", ascii="*█")
	for svg_path in paths:
		proceed_path(svg_path)
		pbar.update(1)
	pbar.close()
	res_colors.write("colors_array = " + str(colors_array) + coloring_script)
	res_forms.close()
	res_colors.close()

def proceed_path(svg_path):
	path = [x.value for x in svg_path.attributes.values()][-1]
	path_parsed = parse_path(path)
	for seg_nmb in tqdm(range(len(path_parsed)), desc="path", ascii="*█", leave=True):
		seg = path_parsed[seg_nmb]
		poly = seg.poly()

		out_x, out_y = "", str(sizeY) + "-\\left("
		for nmb in range(len(poly) + 1):
			out_x += f_pow('t', nmb) + f_dot() + str(round(np.real(poly[nmb]), precision)) + '+'
			out_y += f_pow('t', nmb) + f_dot() + str(round(np.imag(poly[nmb]), precision)) + '+'
		out_x = out_x[:-1] # remove last '+'
		out_y = out_y[:-1] # remove last '+'
		out_y += "\\right)"

		out = "\\left(" + out_x + ', ' + out_y + "\\right)\\left\\{0\\le t\\le1\\right\\}"
		res_forms.write(out + '\n')
		colors_array.append(current_color)

		# OLD METHOD. COULD BE USED AS SPECIAL MODE
		#points = [seg.point(x) for x in np.linspace(0, 1, path_seg_partition)]
		#for nmb in range(len(points) - 1):
		#	draw_line(np.real(points[nmb]), sizeY-np.imag(points[nmb]), np.real(points[nmb+1]), sizeY-np.imag(points[nmb+1]))

def load_styles():
	# i really hate this way to proceed styles
	stl = doc.getElementsByTagName('style')
	if len(stl) == 0:
		return
	style_string = stl[0].childNodes[1].nodeValue
	style_string = style_string.replace(' ', '')
	style_string = style_string.replace('\t', '')
	raw_styles = style_string[1:-1].split('\n')
	for s in raw_styles:
		br_pos = s.find('{')
		name = s[1:br_pos]
		body = s[br_pos + 1:-1].split(';')
		st_params = {}
		for param in body:
			pair = param.split(':')
			st_params[pair[0]] = pair[1]
		styles[name] = st_params

def parse(type):
	itemList = doc.getElementsByTagName(type)
	if itemList.length == 0:
		return
	pbar = tqdm(total=itemList.length, desc=type, ascii="*█")
	if type == 'line':
		for item in itemList:
			(x1, y1, x2, y2) = get_features(item)
			y1 = sizeY - y1
			y2 = sizeY - y2
			draw_line(x1, y1, x2, y2)
			pbar.update(1)
	elif type == 'rect':
		for item in itemList:
			(x, y, width, height) = get_features(item)
			y = sizeY - y
			draw_rect(x, y, width, height)
			pbar.update(1)
	elif type == 'circle':
		for item in itemList:	
			(cx, cy, r) = get_features(item)
			cy = sizeY - cy
			draw_circle(cx, cy, r)
			pbar.update(1)
	elif type == 'ellipse':
		for item in itemList:	
			(cx, cy, rx, ry) = get_features(item)
			cy = sizeY - cy
			draw_ellipse(cx, cy, rx, ry)
			pbar.update(1)
	pbar.close()

def get_features(item):
	global current_color
	features = [x.value for x in item.attributes.values()]
	style = features[0].split(' ')
	line_color = styles[style[1]]['stroke']
	if line_color[0] == '#':
		current_color = line_color
	elif line_color in colors:
		current_color = colors[line_color]
	else:
		raise SystemExit("\nERROR! COLOR NOT FOUND: " + str(line_color))

	return map(float, features[1:])

def segment(a, b, var):
	a = rn(a)
	b = rn(b)
	return "\\left\\{" + str(min(a, b)) + "\\le " + var + "\\le" + str(max(a,b)) + "\\right\\}"

def f_sqrt(x):
	return "\\sqrt{" + str(x) + "}"
def f_pow(var, pow):
	if pow == 0:
		return "1"
	if pow == 1:
		return var
	if len(var) == 1:
		return var + "^{" + str(pow) + "}"
	return "\\left(" + var + "\\right)^{" + str(pow) + "}"
def f_dot():
	return "\\cdot"
def f_div(a, b):
	return "\\frac{" + a + "}{" + b + "}"

def rn(x): # round with precision
	return round(x, precision)
def rnstr(x): # round and turn to str
	return str(round(x, precision))

def draw_line(x1, y1, x2, y2):
	if y1 == y2:
		out = "y=" + rnstr(y1) + segment(x1, x2, 'x')
	elif x1 == x2:
		out = "x=" + rnstr(x1) + segment(y1, y2, 'y')
	else:
		k = (y2 - y1) / (x2 - x1)
		b = y1 - k * x1
		out = out = "y=x" + f_dot() + rnstr(k) + "+" + rnstr(b) + segment(x1, x2, 'x')
	res_forms.write(out + '\n')
	colors_array.append(current_color)

def draw_rect(x, y, width, height):
	draw_line(x, y, x + width, y)
	draw_line(x + width, y, x + width, y - height)
	draw_line(x + width, y - height, x, y - height)
	draw_line(x, y - height, x, y)

def draw_circle(cx, cy, r):
	out = f_pow("x-" + rnstr(abs(cx)), 2) + "+" + f_pow("y-" + rnstr(abs(cy)), 2) + "=" + rnstr(r*r)
	res_forms.write(out + '\n')
	colors_array.append(current_color)

def draw_ellipse(cx, cy, rx, ry):
	out = f_div(f_pow("x-" + rnstr(abs(cx)), 2), rnstr(rx*rx)) + "+" + f_div(f_pow("y-" + rnstr(abs(cy)), 2), rnstr(ry*ry)) + "=1"
	res_forms.write(out + '\n')
	colors_array.append(current_color)

main()