from xml.dom import minidom

filename = 'AESC.svg'
precision = 4 # decimal places
#types = ['line', 'rect', 'circle', 'ellipse']
types = ['circle', 'ellipse', 'line']

doc = minidom.parse(filename)
doc.normalize() # why did i write this?

info = doc.getElementsByTagName('svg')[0]
(sizeX, sizeY) = map(float, info.attributes['viewBox'].value.split(' ')[2:])

def main():
	for type in types:
		parse(type)

def parse(type):
	itemList = doc.getElementsByTagName(type)
	if type == 'line':
		for item in itemList:
			(x1, y1, x2, y2) = get_features(item)
			y1 = sizeY - y1
			y2 = sizeY - y2
			draw_line(x1, y1, x2, y2)
	elif type == 'rect':
		for item in itemList:
			(x, y, width, height) = get_features(item)
			y = sizeY - y
			draw_rect(x, y, width, height)
	elif type == 'circle':
		for item in itemList:	
			(cx, cy, r) = get_features(item)
			cy = sizeY - cy
			draw_circle(cx, cy, r)
	elif type == 'ellipse':
		for item in itemList:	
			(cx, cy, rx, ry) = get_features(item)
			cy = sizeY - cy
			draw_ellipse(cx, cy, rx, ry)

def get_features(item):
	return map(float, [x.value for x in item.attributes.values()][1:])

def segment(a, b, var):
	a = rn(a)
	b = rn(b)
	return "\\left\\{" + str(min(a, b)) + "\\le " + var + "\\le" + str(max(a,b)) + "\\right\\}"

def f_sqrt(x):
	return "\\sqrt{" + str(x) + "}"
def f_sqr(var):
	return "\\left(" + var + "\\right)^{2}"
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
	print(out)

def draw_rect(x, y, width, height):
	draw_line(x, y, x + width, y)
	draw_line(x + width, y, x + width, y - height)
	draw_line(x + width, y - height, x, y - height)
	draw_line(x, y - height, x, y)

def draw_circle(cx, cy, r):
	out = f_sqr("x-" + rnstr(abs(cx))) + "+" + f_sqr("y-" + rnstr(abs(cy))) + "=" + rnstr(r*r)
	print(out)

def draw_ellipse(cx, cy, rx, ry):
	out = f_div(f_sqr("x-" + rnstr(abs(cx))), rnstr(rx*rx)) + "+" + f_div(f_sqr("y-" + rnstr(abs(cy))), rnstr(ry*ry)) + "=1"
	print(out)
#	<ellipse class="fil0 str0" cx="157.1083" cy="65.4486" rx="14.0689" ry="20.3856"/>

# \frac{\left(x-10\right)^{2}}{10}+\frac{\left(y-20\right)^{2}}{40}=1

main()
# y=\sqrt{x} \left\{x<10\right\}