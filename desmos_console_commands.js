
// PAINT ALL ONE COLOR
state = Calc.getState()
var item;
for (item = 0; item < state["expressions"]["list"].length; item++) {
  state["expressions"]["list"][item].color = "#C0BC20"
  //console.log(item);
}
Calc.setState(state)

// PAINT WITH colors_array
colors_array = ['#7E71B1', '#009846', '#FFED00', '#000000', '#EF7F1A', '#EF7F1A', '#EF7F1A', '#EF7F1A', '#86776F', '#86776F', '#86776F', '#86776F']
state = Calc.getState()
var item;
for (item = 0; item < colors_array.length; item++) {
  state["expressions"]["list"][item].color = colors_array[item]
}
Calc.setState(state)

// RAINBOW COLORING
step = 5;
saturation = 100;
lightness = 50;
alpha = 0.7;
state = Calc.getState();
var item;
for (item = 0; item < state["expressions"]["list"].length; item++) {
  color = `hsla(${(step * item) % 360},${saturation}%,${lightness}%,${alpha})`;
  state["expressions"]["list"][item].color = color;
}
Calc.setState(state);