coloring_script = '''
state = Calc.getState()
var item;
for (item = 0; item < colors_array.length; item++) {
  state["expressions"]["list"][item].color = colors_array[item]
}
Calc.setState(state)
'''