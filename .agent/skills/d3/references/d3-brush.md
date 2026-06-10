## d3-brush | D3 by Observable

**URL:** https://d3js.org/d3-brush

**Contents:**
- d3-brush ​
- brush() ​
- brushX() ​
- brushY() ​
- brush(group) ​
- brush.move(group, selection, event) ​
- brush.clear(group, event) ​
- brush.extent(extent) ​
- brush.filter(filter) ​
- brush.touchable(touchable) ​

Brushing is the interactive specification a one- or two-dimensional selected region using a pointing gesture, such as by clicking and dragging the mouse. Brushing is often used to select discrete elements, such as dots in a scatterplot or files on a desktop. It can also be used to zoom-in to a region of interest, or to select continuous regions for cross-filtering data or live histograms:

The d3-brush module implements brushing for mouse and touch events using SVG. Click and drag on the brush selection to translate the selection. Click and drag on one of the selection handles to move the corresponding edge (or edges) of the selection. Click and drag on the invisible overlay to define a new brush selection, or click anywhere within the brushable region while holding down the META (⌘) key. Holding down the ALT (⌥) key while moving the brush causes it to reposition around its center, while holding down SPACE locks the current brush size, allowing only translation.

Brushes also support programmatic control. For example, you can listen to end events, and then initiate a transition with brush.move to snap the brush selection to semantic boundaries:

Or you can have the brush recenter when you click outside the current selection:

Examples · Source · Creates a new two-dimensional brush.

Examples · Source · Creates a new one-dimensional brush along the x-dimension.

Source · Creates a new one-dimensional brush along the y-dimension.

Examples · Source · Applies the brush to the specified group, which must be a selection of SVG G elements. This function is typically not invoked directly, and is instead invoked via selection.call. For example, to render a brush:

Internally, the brush uses selection.on to bind the necessary event listeners for dragging. The listeners use the name .brush, so you can subsequently unbind the brush event listeners as follows:

The brush also creates the SVG elements necessary to display the brush selection and to receive input events for interaction. You can add, remove or modify these elements as desired to change the brush appearance; you can also apply stylesheets to modify the brush appearance. The structure of a two-dimensional brush is as follows:

The overlay rect covers the brushable area defined by brush.extent. The selection rect covers the area defined by the current brush selection. The handle rects cover the edges and corners of the brush selection, allowing the corresponding value in the brush selection to be modified interactively. To modify the brush selection programmatically, use brush.move.

Examples · Source · Sets the active selection of the brush on the specified group, which must be a selection or a transition of SVG G elements. The selection must be defined as an array of numbers, or null to clear the brush selection. For a two-dimensional brush, it must be defined as [[x0, y0], [x1, y1]], where x0 is the minimum x-value, y0 is the minimum y-value, x1 is the maximum x-value, and y1 is the maximum y-value. For an x-brush, it must be defined as [x0, x1]; for a y-brush, it must be defined as [y0, y1]. The selection may also be specified as a function which returns such an array; if a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element. The returned array defines the brush selection for that element.

Examples · Source · An alias for brush.move with the null selection.

Examples · Source · If extent is specified, sets the brushable extent to the specified array of points [[x0, y0], [x1, y1]], where [x0, y0] is the top-left corner and [x1, y1] is the bottom-right corner, and returns this brush. The extent may also be specified as a function which returns such an array; if a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element. If extent is not specified, returns the current extent accessor, which defaults to:

This default implementation requires that the owner SVG element have a defined viewBox, or width and height attributes. Alternatively, consider using element.getBoundingClientRect. (In Firefox, element.clientWidth and element.clientHeight is zero for SVG elements!)

The brush extent determines the size of the invisible overlay and also constrains the brush selection; the brush selection cannot go outside the brush extent.

Examples · Source · If filter is specified, sets the filter to the specified function and returns the brush. If filter is not specified, returns the current filter, which defaults to:

If the filter returns falsey, the initiating event is ignored and no brush gesture is started. Thus, the filter determines which input events are ignored. The default filter ignores mousedown events on secondary buttons, since those buttons are typically intended for other purposes, such as the context menu.

Source · If touchable is specified, sets the touch support detector to the specified function and returns the brush. If touchable is not specified, returns the current touch support detector, which defaults to:

Touch event listeners are only registered if the detector returns truthy for the corresponding element when the brush is applied. The default detector works well for most browsers that are capable of touch input, but not all; Chrome’s mobile device emulator, for example, fails detection.

Source · If modifiers is specified, sets whether the brush listens to key events during brushing and returns the brush. If modifiers is not specified, returns the current behavior, which defaults to true.

Source · If size is specified, sets the size of the brush handles to the specified number and returns the brush. If size is not specified, returns the current handle size, which defaults to six. This method must be called before applying the brush to a selection; changing the handle size does not affect brushes that were previously rendered.

Source · If listener is specified, sets the event listener for the specified typenames and returns the brush. If an event listener was already registered for the same type and name, the existing listener is removed before the new listener is added. If listener is null, removes the current event listeners for the specified typenames, if any. If listener is not specified, returns the first currently-assigned listener matching the specified typenames, if any. When a specified event is dispatched, each listener will be invoked with the same context and arguments as selection.on listeners: the current event event and datum d, with the this context as the current DOM element.

The typenames is a string containing one or more typename separated by whitespace. Each typename is a type, optionally followed by a period (.) and a name, such as brush.foo and brush.bar; the name allows multiple listeners to be registered for the same type. The type must be one of the following:

See dispatch.on and brush events for more.

Examples · Source · Returns the current brush selection for the specified node. Internally, an element’s brush state is stored as element.__brush; however, you should use this method rather than accessing it directly. If the given node has no selection, returns null. Otherwise, the selection is defined as an array of numbers. For a two-dimensional brush, it is [[x0, y0], [x1, y1]], where x0 is the minimum x-value, y0 is the minimum y-value, x1 is the maximum x-value, and y1 is the maximum y-value. For an x-brush, it is [x0, x1]; for a y-brush, it is [y0, y1].

When a brush event listener is invoked, it receives the current brush event. The event object exposes several fields:

**Examples:**

Example 1 (unknown):
```unknown
svg.append("g")
    .attr("class", "brush")
    .call(d3.brush().on("brush", brushed));
```

Example 2 (unknown):
```unknown
group.on(".brush", null);
```

Example 3 (jsx):
```jsx
<g class="brush" fill="none" pointer-events="all" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);">
  <rect class="overlay" pointer-events="all" cursor="crosshair" x="0" y="0" width="960" height="500"></rect>
  <rect class="selection" cursor="move" fill="#777" fill-opacity="0.3" stroke="#fff" shape-rendering="crispEdges" x="112" y="194" width="182" height="83"></rect>
  <rect class="handle handle--n" cursor="ns-resize" x="107" y="189" width="192" height="10"></rect>
  <rect class="handle handle--e" cursor="ew-resize" x="289" y="189" width="10" height="93"></rect>
  <rect class="handle handle--s" cursor="ns-resize" x="107" y="272" width="192" height="10"></rect>
  <rect class="handle handle--w" cursor="ew-resize" x="107" y="189" width="10" height="93"></rect>
  <rect class="handle handle--nw" cursor="nwse-resize" x="107" y="189" width="10" height="10"></rect>
  <rect class="handle handle--ne" cursor="nesw-resize" x="289" y="189" width="10" height="10"></rect>
  <rect class="handle handle--se" cursor="nwse-resize" x="289" y="272" width="10" height="10"></rect>
  <rect class="handle handle--sw" cursor="nesw-resize" x="107" y="272" width="10" height="10"></rect>
</g>
```

Example 4 (javascript):
```javascript
function defaultExtent() {
  var svg = this.ownerSVGElement || this;
  if (svg.hasAttribute("viewBox")) {
    svg = svg.viewBox.baseVal;
    return [[svg.x, svg.y], [svg.x + svg.width, svg.y + svg.height]];
  }
  return [[0, 0], [svg.width.baseVal.value, svg.height.baseVal.value]];
}
```
