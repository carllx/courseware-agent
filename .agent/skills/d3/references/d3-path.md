> Source: [https://d3js.org/d3-path](https://d3js.org/d3-path)

# d3-path

[Examples](https://observablehq.com/@d3/d3-path) · Say you have some code that draws to a 2D canvas:

```js
function drawCircle(context, radius) {
  context.moveTo(radius, 0);
  context.arc(0, 0, radius, 0, 2 * Math.PI);
}
```

The d3-path module lets you take this exact code and additionally render to [SVG](http://www.w3.org/TR/SVG/paths.html). It works by [serializing](#path_toString) [CanvasPathMethods](http://www.w3.org/TR/2dcontext/#canvaspathmethods) calls to [SVG path data](http://www.w3.org/TR/SVG/paths.html#PathData). For example:

```js
const path = d3.path();
drawCircle(path, 40);
path.toString(); // "M40,0A40,40,0,1,1,-40,0A40,40,0,1,1,40,0"
```

Now code you write once can be used with both Canvas (for performance) and SVG (for convenience). For a practical example, see [d3-shape](./d3-shape.md).

## path() {#path}

[Source](https://github.com/d3/d3-path/blob/main/src/path.js) · Constructs a new path serializer that implements [CanvasPathMethods](http://www.w3.org/TR/2dcontext/#canvaspathmethods).

## *path*.moveTo(*x*, *y*) {#path_moveTo}

[Source](https://github.com/d3/d3-path/blob/main/src/path.js) · Move to the specified point ⟨*x*, *y*⟩. Equivalent to [*context*.moveTo](http://www.w3.org/TR/2dcontext/#dom-context-2d-moveto) and SVG’s [“moveto” command](http://www.w3.org/TR/SVG/paths.html#PathDataMovetoCommands).

```js
path.moveTo(100, 100);
```

## *path*.closePath() {#path_closePath}

[Source](https://github.com/d3/d3-path/blob/main/src/path.js) · Ends the current subpath and causes an automatic straight line to be drawn from the current point to the initial point of the current subpa

