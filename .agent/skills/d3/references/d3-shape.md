# D3 - D3-Shape

**Pages:** 12

---

## Areas | D3 by Observable

**URL:** https://d3js.org/d3-shape/area

**Contents:**
- Areas ​
- area(x, y0, y1) ​
- area(data) ​
- area.x(x) ​
- area.x0(x) ​
- area.x1(x) ​
- area.y(y) ​
- area.y0(y) ​
- area.y1(y) ​
- area.defined(defined) ​

Examples · The area generator produces an area defined by a topline and a baseline as in an area chart. Typically, the two lines share the same x-values (x0 = x1), differing only in y-value (y0 and y1); most commonly, y0 is defined as a constant representing zero (the y scale’s output for zero). The topline is defined by x1 and y1 and is rendered first; the baseline is defined by x0 and y0 and is rendered second with the points in reverse order. With a curveLinear curve, this produces a clockwise polygon. See also radial areas.

Source · Constructs a new area generator with the given x, y0, and y1 accessors or numbers.

If x, y0 or y1 are not specified, the respective defaults will be used. The above can be expressed more explicitly as:

Source · Generates an area for the given array of data.

If the area generator has a context, then the area is rendered to this context as a sequence of path method calls and this function returns void. Otherwise, a path data string is returned.

Depending on this area generator’s associated curve, the given input data may need to be sorted by x-value before being passed to the area generator.

Source · If x is specified, sets x0 to x and x1 to null and returns this area generator.

If x is not specified, returns the current x0 accessor.

This method is intended for vertically-oriented areas, as when time goes down↓ rather than right→; for the more common horizontally-oriented areas, use area.x instead.

Source · If x is specified, sets the x0 accessor to the specified function or number and returns this area generator.

When an area is generated, the x0 accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments.

If x is not specified, returns the current x0 accessor.

The x0 accessor defaults to:

The default x0 accessor assumes that the input data are two-element arrays of numbers [[x0, y0], [x1, y1], …]. If your data are in a different format, or if you wish to transform the data before rendering, then you should specify a custom accessor as shown above.

This method is intended for vertically-oriented areas, as when time goes down↓ rather than right→; for the more common horizontally-oriented areas, use area.x instead.

Source · If x is specified, sets the x1 accessor to the specified function or number and returns this area generator.

When an area is generated, the x1 accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments.

If x is not specified, returns the current x1 accessor.

The x1 accessor defaults to null, indicating that the previously-computed x0 value should be reused for the x1 value; this default is intended for horizontally-oriented areas.

This method is intended for vertically-oriented areas, as when time goes down↓ rather than right→; for the more common horizontally-oriented areas, use area.y0 and area.y1 instead.

Source · If y is specified, sets y0 to y and y1 to null and returns this area generator.

If y is not specified, returns the current y0 accessor.

Source · If y is specified, sets the y0 accessor to the specified function or number and returns this area generator.

When an area is generated, the y0 accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments. For a horizontally-oriented area with a constant baseline (i.e., an area that is not stacked, and not a ribbon or band), y0 is typically set to the output of the y scale for zero.

If y is not specified, returns the current y0 accessor.

The y0 accessor defaults to:

In the default SVG coordinate system, note that the default zero represents the top of the chart rather than the bottom, producing a flipped (or “hanging”) area.

Source · If y is specified, sets the y1 accessor to the specified function or number and returns this area generator.

When an area is generated, the y1 accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments.

If y is not specified, returns the current y1 accessor.

The y1 accessor defaults to:

The default y1 accessor assumes that the input data are two-element arrays of numbers [[x0, y0], [x1, y1], …]. If your data are in a different format, or if you wish to transform the data before rendering, then you should specify a custom accessor as shown above. A null accessor is also allowed, indicating that the previously-computed y0 value should be reused for the y1 value; this can be used for a vertically-oriented area, as when time goes down↓ instead of right→.

Examples · Source · If defined is specified, sets the defined accessor to the specified function or boolean and returns this area generator.

When an area is generated, the defined accessor will be invoked for each element in the input data array, being passed the element d, the index i, and the array data as three arguments. If the given element is defined (i.e., if the defined accessor returns a truthy value for this element), the x0, x1, y0 and y1 accessors will subsequently be evaluated and the point will be added to the current area segment. Otherwise, the element will be skipped, the current area segment will be ended, and a new area segment will be generated for the next defined point. As a result, the generated area may have several discrete segments.

If defined is not specified, returns the current defined accessor.

The defined accessor defaults to the constant true, and assumes that the input data is always defined:

Note that if an area segment consists of only a single point, it may appear invisible unless rendered with rounded or square line caps. In addition, some curves such as curveCardinalOpen only render a visible segment if it contains multiple points.

Source · If curve is specified, sets the curve factory and returns this area generator.

If curve is not specified, returns the current curve factory, which defaults to curveLinear.

Source · If context is specified, sets the context and returns this area generator.

If context is not specified, returns the current context.

The context defaults to null. If the context is not null, then the generated area is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated area is returned.

Source · If digits is specified, sets the maximum number of digits after the decimal separator and returns this area generator.

If digits is not specified, returns the current maximum fraction digits, which defaults to 3.

This option only applies when the associated context is null, as when this area generator is used to produce path data.

An alias for area.lineY0.

Source · Returns a new line generator that has this area generator’s current defined accessor, curve and context. The line’s x-accessor is this area’s x0-accessor, and the line’s y-accessor is this area’s y0-accessor.

Source · Returns a new line generator that has this area generator’s current defined accessor, curve and context. The line’s x-accessor is this area’s x1-accessor, and the line’s y-accessor is this area’s y0-accessor.

Source · Returns a new line generator that has this area generator’s current defined accessor, curve and context. The line’s x-accessor is this area’s x0-accessor, and the line’s y-accessor is this area’s y1-accessor.

**Examples:**

Example 1 (javascript):
```javascript
const area = d3.area((d) => x(d.Date), y(0), (d) => y(d.Close));
```

Example 2 (javascript):
```javascript
const area = d3.area()
    .x((d) => x(d.Date))
    .y0(y(0))
    .y1((d) => y(d.Close));
```

Example 3 (unknown):
```unknown
svg.append("path").attr("d", area(data));
```

Example 4 (javascript):
```javascript
const area = d3.area().x((d) => x(d.Date));
```

---

## Radial links | D3 by Observable

**URL:** https://d3js.org/d3-shape/radial-link

**Contents:**
- Radial links ​
- linkRadial() ​
- linkRadial.angle(angle) ​
- linkRadial.radius(radius) ​

A radial link generator is like the Cartesian link generator except the x and y accessors are replaced with angle and radius accessors. Radial links are positioned relative to the origin; use a transform to change the origin.

Source · Returns a new link generator with radial tangents. For example, to visualize links in a tree diagram rooted in the center of the display, you might say:

Source · Equivalent to link.x, except the accessor returns the angle in radians, with 0 at -y (12 o’clock).

Source · Equivalent to link.y, except the accessor returns the radius: the distance from the origin.

**Examples:**

Example 1 (javascript):
```javascript
const link = d3.linkRadial()
    .angle((d) => d.x)
    .radius((d) => d.y);
```

---

## Pies | D3 by Observable

**URL:** https://d3js.org/d3-shape/pie

**Contents:**
- Pies ​
- pie() ​
- pie(data, ...arguments) ​
- pie.value(value) ​
- pie.sort(compare) ​
- pie.sortValues(compare) ​
- pie.startAngle(angle) ​
- pie.endAngle(angle) ​
- pie.padAngle(angle) ​

Examples · The pie generator computes the necessary angles to represent a tabular dataset as a pie or donut chart; these angles can then be passed to an arc generator. (The pie generator does not produce a shape directly.)

Source · Constructs a new pie generator with the default settings.

Source · Generates a pie for the given array of data, returning an array of objects representing each datum’s arc angles. For example, given a set of numbers, here is how to compute the angles for a pie chart:

The resulting arcs is an array of objects:

Each object in the returned array has the following properties:

This representation is designed to work with the arc generator’s default startAngle, endAngle and padAngle accessors. Angles are in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise.

The length of the returned array is the same as data, and each element i in the returned array corresponds to the element i in the input data. The returned array of arcs is in the same order as the data, even when the pie chart is sorted.

Any additional arguments are arbitrary; they are propagated to the pie generator’s accessor functions along with the this object.

Source · If value is specified, sets the value accessor to the specified function or number and returns this pie generator.

When a pie is generated, the value accessor will be invoked for each element in the input data array, being passed the element d, the index i, and the array data as three arguments.

If value is not specified, returns the current value accessor.

The value accessor defaults to:

The default value accessor assumes that the input data are numbers, or that they are coercible to numbers using valueOf. If your data are not numbers, then you should specify an accessor that returns the corresponding numeric value for a given datum. For example, given a CSV file with number and name fields:

This is similar to mapping your data to values before invoking the pie generator:

The benefit of an accessor is that the input data remains associated with the returned objects, thereby making it easier to access other fields of the data, for example to set the color or to add text labels.

Source · If compare is specified, sets the data comparator to the specified function and returns this pie generator.

The data comparator takes two arguments a and b, each elements from the input data array. If the arc for a should be before the arc for b, then the comparator must return a number less than zero; if the arc for a should be after the arc for b, then the comparator must return a number greater than zero; returning zero means that the relative order of a and b is unspecified.

If compare is not specified, returns the current data comparator.

The data comparator defaults to null. If both the data comparator and the value comparator are null, then arcs are positioned in the original input order. Setting the data comparator implicitly sets the value comparator to null.

Sorting does not affect the order of the generated arc array which is always in the same order as the input data array; it only affects the computed angles of each arc. The first arc starts at the start angle and the last arc ends at the end angle.

Source · If compare is specified, sets the value comparator to the specified function and returns this pie generator.

The value comparator is similar to the data comparator, except the two arguments a and b are values derived from the input data array using the value accessor rather than the data elements. If the arc for a should be before the arc for b, then the comparator must return a number less than zero; if the arc for a should be after the arc for b, then the comparator must return a number greater than zero; returning zero means that the relative order of a and b is unspecified.

If compare is not specified, returns the current value comparator.

The value comparator defaults to descending. If both the data comparator and the value comparator are null, then arcs are positioned in the original input order. Setting the value comparator implicitly sets the data comparator to null.

Sorting does not affect the order of the generated arc array which is always in the same order as the input data array; it merely affects the computed angles of each arc. The first arc starts at the start angle and the last arc ends at the end angle.

Source · If angle is specified, sets the overall start angle of the pie to the specified function or number and returns this pie generator.

The start angle is the overall start angle of the pie, i.e., the start angle of the first arc. It is typically expressed as a constant number but can also be expressed as a function of data. When a function, the start angle accessor is invoked once, being passed the same arguments and this context as the pie generator.

If angle is not specified, returns the current start angle accessor.

The start angle accessor defaults to:

Angles are in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise.

Source · If angle is specified, sets the overall end angle of the pie to the specified function or number and returns this pie generator.

The end angle here means the overall end angle of the pie, i.e., the end angle of the last arc. It is typically expressed as a constant number but can also be expressed as a function of data. When a function, the end angle accessor is invoked once, being passed the same arguments and this context as the pie generator.

If angle is not specified, returns the current end angle accessor.

The end angle accessor defaults to:

Angles are in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise. The value of the end angle is constrained to startAngle ± τ, such that |endAngle - startAngle| ≤ τ.

Examples · Source · If angle is specified, sets the pad angle to the specified function or number and returns this pie generator.

The pad angle specifies the angular separation in radians between adjacent arcs. The total amount of padding is the specified angle times the number of elements in the input data array, and at most |endAngle - startAngle|; the remaining space is divided proportionally by value such that the relative area of each arc is preserved.

The pad angle is typically expressed as a constant number but can also be expressed as a function of data. When a function, the pad angle accessor is invoked once, being passed the same arguments and this context as the pie generator.

If angle is not specified, returns the current pad angle accessor.

The pad angle accessor defaults to:

**Examples:**

Example 1 (javascript):
```javascript
const pie = d3.pie();
```

Example 2 (javascript):
```javascript
const data = [1, 1, 2, 3, 5, 8, 13, 21];
const pie = d3.pie();
const arcs = pie(data);
```

Example 3 (json):
```json
[
  {"data":  1, "value":  1, "index": 6, "startAngle": 6.050474740247008, "endAngle": 6.166830023713296, "padAngle": 0},
  {"data":  1, "value":  1, "index": 7, "startAngle": 6.166830023713296, "endAngle": 6.283185307179584, "padAngle": 0},
  {"data":  2, "value":  2, "index": 5, "startAngle": 5.817764173314431, "endAngle": 6.050474740247008, "padAngle": 0},
  {"data":  3, "value":  3, "index": 4, "startAngle": 5.468698322915565, "endAngle": 5.817764173314431, "padAngle": 0},
  {"data":  5, "value":  5, "index": 3, "startAngle": 4.886921905584122, "endAngle": 5.468698322915565, "padAngle": 0},
  {"data":  8, "value":  8, "index": 2, "startAngle": 3.956079637853813, "endAngle": 4.886921905584122, "padAngle": 0},
  {"data": 13, "value": 13, "index": 1, "startAngle": 2.443460952792061, "endAngle": 3.956079637853813, "padAngle": 0},
  {"data": 21, "value": 21, "index": 0, "startAngle": 0.000000000000000, "endAngle": 2.443460952792061, "padAngle": 0}
]
```

Example 4 (javascript):
```javascript
const pie = d3.pie().value((d) => d.value);
```

---

## Radial areas | D3 by Observable

**URL:** https://d3js.org/d3-shape/radial-area

**Contents:**
- Radial areas ​
- areaRadial() ​
- areaRadial(data) ​
- areaRadial.angle(angle) ​
- areaRadial.startAngle(angle) ​
- areaRadial.endAngle(angle) ​
- areaRadial.radius(radius) ​
- areaRadial.innerRadius(radius) ​
- areaRadial.outerRadius(radius) ​
- areaRadial.defined(defined) ​

Examples · A radial area generator is like the Cartesian area generator except the x and y accessors are replaced with angle and radius accessors. Radial areas are positioned relative to the origin; use a transform to change the origin.

Source · Constructs a new radial area generator with the default settings.

Source · Equivalent to area.

Source · Equivalent to area.x, except the accessor returns the angle in radians, with 0 at -y (12 o’clock).

Source · Equivalent to area.x0, except the accessor returns the angle in radians, with 0 at -y (12 o’clock). Note: typically angle is used instead of setting separate start and end angles.

Source · Equivalent to area.x1, except the accessor returns the angle in radians, with 0 at -y (12 o’clock). Note: typically angle is used instead of setting separate start and end angles.

Source · Equivalent to area.y, except the accessor returns the radius: the distance from the origin.

Source · Equivalent to area.y0, except the accessor returns the radius: the distance from the origin.

Source · Equivalent to area.y1, except the accessor returns the radius: the distance from the origin.

Source · Equivalent to area.defined.

Source · Equivalent to area.curve. Note that curveMonotoneX or curveMonotoneY are not recommended for radial areas because they assume that the data is monotonic in x or y, which is typically untrue of radial areas.

Source · Equivalent to area.context.

An alias for areaRadial.lineStartAngle.

Source · Returns a new radial line generator that has this radial area generator’s current defined accessor, curve and context. The line’s angle accessor is this area’s start angle accessor, and the line’s radius accessor is this area’s inner radius accessor.

Source · Returns a new radial line generator that has this radial area generator’s current defined accessor, curve and context. The line’s angle accessor is this area’s end angle accessor, and the line’s radius accessor is this area’s inner radius accessor.

Source · Returns a new radial line generator that has this radial area generator’s current defined accessor, curve and context. The line’s angle accessor is this area’s start angle accessor, and the line’s radius accessor is this area’s outer radius accessor.

**Examples:**

Example 1 (javascript):
```javascript
const area = d3.areaRadial();
```

Example 2 (unknown):
```unknown
svg.append("path").attr("d", area(data));
```

Example 3 (javascript):
```javascript
const area = d3.areaRadial().angle((d) => a(d.Date));
```

Example 4 (javascript):
```javascript
const area = d3.areaRadial().radius((d) => r(d.temperature));
```

---

## Curves | D3 by Observable

**URL:** https://d3js.org/d3-shape/curve

**Contents:**
- Curves ​
- curveBasis(context) ​
- curveBasisClosed(context) ​
- curveBasisOpen(context) ​
- curveBumpX(context) ​
- curveBumpY(context) ​
- curveBundle(context) ​
- curveBundle.beta(beta) ​
- curveCardinal(context) ​
- curveCardinalClosed(context) ​

Curves turn a discrete (pointwise) representation of a line or area into a continuous shape: curves specify how to interpolate between two-dimensional [x, y] points.

Curves are typically not constructed or used directly. Instead, one of the built-in curves is being passed to line.curve or area.curve.

If desired, you can implement a custom curve. For an example of using a curve directly, see Context to Curve.

Source · Produces a cubic basis spline using the specified control points. The first and last points are triplicated such that the spline starts at the first point and ends at the last point, and is tangent to the line between the first and second points, and to the line between the penultimate and last points.

Source · Produces a closed cubic basis spline using the specified control points. When a line segment ends, the first three control points are repeated, producing a closed loop with C2 continuity.

Source · Produces a cubic basis spline using the specified control points. Unlike basis, the first and last points are not repeated, and thus the curve typically does not intersect these points.

Source · Produces a Bézier curve between each pair of points, with horizontal tangents at each point.

Source · Produces a Bézier curve between each pair of points, with vertical tangents at each point.

Source · Produces a straightened cubic basis spline using the specified control points, with the spline straightened according to the curve’s beta, which defaults to 0.85. This curve is typically used in hierarchical edge bundling to disambiguate connections, as proposed by Danny Holten in Hierarchical Edge Bundles: Visualization of Adjacency Relations in Hierarchical Data. This curve does not implement curve.areaStart and curve.areaEnd; it is intended to work with d3.line, not d3.area.

Source · Returns a bundle curve with the specified beta in the range [0, 1], representing the bundle strength. If beta equals zero, a straight line between the first and last point is produced; if beta equals one, a standard basis spline is produced. For example:

Source · Produces a cubic cardinal spline using the specified control points, with one-sided differences used for the first and last piece. The default tension is 0.

Source · Produces a closed cubic cardinal spline using the specified control points. When a line segment ends, the first three control points are repeated, producing a closed loop. The default tension is 0.

Source · Produces a cubic cardinal spline using the specified control points. Unlike curveCardinal, one-sided differences are not used for the first and last piece, and thus the curve starts at the second point and ends at the penultimate point. The default tension is 0.

Source · Returns a cardinal curve with the specified tension in the range [0, 1]. The tension determines the length of the tangents: a tension of one yields all zero tangents, equivalent to curveLinear; a tension of zero produces a uniform Catmull–Rom spline. For example:

Source · Produces a cubic Catmull–Rom spline using the specified control points and the parameter alpha, which defaults to 0.5, as proposed by Yuksel et al. in On the Parameterization of Catmull–Rom Curves, with one-sided differences used for the first and last piece.

Source · Produces a closed cubic Catmull–Rom spline using the specified control points and the parameter alpha, which defaults to 0.5, as proposed by Yuksel et al. When a line segment ends, the first three control points are repeated, producing a closed loop.

Source · Produces a cubic Catmull–Rom spline using the specified control points and the parameter alpha, which defaults to 0.5, as proposed by Yuksel et al. Unlike curveCatmullRom, one-sided differences are not used for the first and last piece, and thus the curve starts at the second point and ends at the penultimate point.

Source · Returns a cubic Catmull–Rom curve with the specified alpha in the range [0, 1]. If alpha is zero, produces a uniform spline, equivalent to curveCardinal with a tension of zero; if alpha is one, produces a chordal spline; if alpha is 0.5, produces a centripetal spline. Centripetal splines are recommended to avoid self-intersections and overshoot. For example:

Source · Produces a polyline through the specified points.

Source · Produces a closed polyline through the specified points by repeating the first point when the line segment ends.

Source · Produces a cubic spline that preserves monotonicity in y, assuming monotonicity in x, as proposed by Steffen in A simple method for monotonic interpolation in one dimension: “a smooth curve with continuous first-order derivatives that passes through any given set of data points without spurious oscillations. Local extrema can occur only at grid points where they are given by the data, but not in between two adjacent grid points.”

Source · Produces a cubic spline that preserves monotonicity in x, assuming monotonicity in y, as proposed by Steffen in A simple method for monotonic interpolation in one dimension: “a smooth curve with continuous first-order derivatives that passes through any given set of data points without spurious oscillations. Local extrema can occur only at grid points where they are given by the data, but not in between two adjacent grid points.”

Source · Produces a natural cubic spline with the second derivative of the spline set to zero at the endpoints.

Source · Produces a piecewise constant function (a step function) consisting of alternating horizontal and vertical lines. The y-value changes at the midpoint of each pair of adjacent x-values.

Source · Produces a piecewise constant function (a step function) consisting of alternating horizontal and vertical lines. The y-value changes after the x-value.

Source · Produces a piecewise constant function (a step function) consisting of alternating horizontal and vertical lines. The y-value changes before the x-value.

Curves are typically not used directly, instead being passed to line.curve and area.curve. However, you can define your own curve implementation should none of the built-in curves satisfy your needs using the following interface; see the curveLinear source for an example implementation. You can also use this low-level interface with a built-in curve type as an alternative to the line and area generators.

Indicates the start of a new area segment. Each area segment consists of exactly two line segments: the topline, followed by the baseline, with the baseline points in reverse order.

Indicates the end of the current area segment.

Indicates the start of a new line segment. Zero or more points will follow.

Indicates the end of the current line segment.

Indicates a new point in the current line segment with the given x- and y-values.

**Examples:**

Example 1 (javascript):
```javascript
const line = d3.line()
    .x((d) => x(d.date))
    .y((d) => y(d.value))
    .curve(d3.curveCatmullRom.alpha(0.5));
```

Example 2 (javascript):
```javascript
const line = d3.line().curve(d3.curveBundle.beta(0.5));
```

Example 3 (javascript):
```javascript
const line = d3.line().curve(d3.curveCardinal.tension(0.5));
```

Example 4 (javascript):
```javascript
const line = d3.line().curve(d3.curveCatmullRom.alpha(0.5));
```

---

## Arcs | D3 by Observable

**URL:** https://d3js.org/d3-shape/arc

**Contents:**
- Arcs ​
- arc() ​
- arc(...arguments) ​
- arc.centroid(...arguments) ​
- arc.innerRadius(radius) ​
- arc.outerRadius(radius) ​
- arc.cornerRadius(radius) ​
- arc.startAngle(angle) ​
- arc.endAngle(angle) ​
- arc.padAngle(angle) ​

The arc generator produces a circular or annular sector, as in a pie or donut chart. Arcs are centered at the origin; use a transform to move the arc to a different position.

If the absolute difference between the start and end angles (the angular span) is greater than 2π, the arc generator will produce a complete circle or annulus. If it is less than 2π, the arc’s angular length will be equal to the absolute difference between the two angles (going clockwise if the signed difference is positive and anticlockwise if it is negative). If the absolute difference is less than 2π, the arc may have rounded corners and angular padding.

See also the pie generator, which computes the necessary angles to represent an array of data as a pie or donut chart; these angles can then be passed to an arc generator.

Source · Constructs a new arc generator with the default settings. With default settings:

Or, with the radii and angles configured as constants:

Source · Generates an arc for the given arguments. The arguments are arbitrary; they are propagated to the arc generator’s accessor functions along with the this object. For example, with the default settings, an object with radii and angles is expected:

If the radii and angles are instead defined as constants, you can generate an arc without any arguments:

If the arc generator has a context, then the arc is rendered to this context as a sequence of path method calls and this function returns void. Otherwise, a path data string is returned.

Examples · Source · Computes the midpoint [x, y] of the center line of the arc that would be generated by the given arguments.

The arguments are arbitrary; they are propagated to the arc generator’s accessor functions along with the this object. To be consistent with the generated arc, the accessors must be deterministic, i.e., return the same value given the same arguments. The midpoint is defined as (startAngle + endAngle) / 2 and (innerRadius + outerRadius) / 2. For example:

Note that this is not the geometric center of the arc, which may be outside the arc; this method is merely a convenience for positioning labels.

Source · If radius is specified, sets the inner radius to the specified function or number and returns this arc generator.

If radius is not specified, returns the current inner radius accessor.

The inner radius accessor defaults to:

Specifying the inner radius as a function is useful for constructing a stacked polar bar chart, often in conjunction with a sqrt scale. More commonly, a constant inner radius is used for a donut or pie chart. If the outer radius is smaller than the inner radius, the inner and outer radii are swapped. A negative value is treated as zero.

Source · If radius is specified, sets the outer radius to the specified function or number and returns this arc generator.

If radius is not specified, returns the current outer radius accessor.

The outer radius accessor defaults to:

Specifying the outer radius as a function is useful for constructing a coxcomb or polar bar chart, often in conjunction with a sqrt scale. More commonly, a constant outer radius is used for a pie or donut chart. If the outer radius is smaller than the inner radius, the inner and outer radii are swapped. A negative value is treated as zero.

Examples · Source · If radius is specified, sets the corner radius to the specified function or number and returns this arc generator.

If radius is not specified, returns the current corner radius accessor.

The corner radius accessor defaults to:

If the corner radius is greater than zero, the corners of the arc are rounded using circles of the given radius. For a circular sector, the two outer corners are rounded; for an annular sector, all four corners are rounded.

The corner radius may not be larger than (outerRadius - innerRadius) / 2. In addition, for arcs whose angular span is less than π, the corner radius may be reduced as two adjacent rounded corners intersect. This occurs more often with the inner corners. See the arc corners animation for illustration.

Source · If angle is specified, sets the start angle to the specified function or number and returns this arc generator.

If angle is not specified, returns the current start angle accessor.

The start angle accessor defaults to:

The angle is specified in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise. If |endAngle - startAngle| ≥ 2π, a complete circle or annulus is generated rather than a sector.

Source · If angle is specified, sets the end angle to the specified function or number and returns this arc generator.

If angle is not specified, returns the current end angle accessor.

The end angle accessor defaults to:

The angle is specified in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise. If |endAngle - startAngle| ≥ 2π, a complete circle or annulus is generated rather than a sector.

Examples · Source · If angle is specified, sets the pad angle to the specified function or number and returns this arc generator.

If angle is not specified, returns the current pad angle accessor.

The pad angle accessor defaults to:

The pad angle is converted to a fixed linear distance separating adjacent arcs, defined as padRadius × padAngle. This distance is subtracted equally from the start and end of the arc. If the arc forms a complete circle or annulus, as when |endAngle - startAngle| ≥ 2π, the pad angle is ignored.

If the inner radius or angular span is small relative to the pad angle, it may not be possible to maintain parallel edges between adjacent arcs. In this case, the inner edge of the arc may collapse to a point, similar to a circular sector. For this reason, padding is typically only applied to annular sectors (i.e., when innerRadius is positive), as shown in this diagram:

The recommended minimum inner radius when using padding is outerRadius * padAngle / sin(θ), where θ is the angular span of the smallest arc before padding. For example, if the outer radius is 200 pixels and the pad angle is 0.02 radians, a reasonable θ is 0.04 radians, and a reasonable inner radius is 100 pixels. See the arc padding animation for illustration.

Often, the pad angle is not set directly on the arc generator, but is instead computed by the pie generator so as to ensure that the area of padded arcs is proportional to their value; see pie.padAngle. See the pie padding animation for illustration. If you apply a constant pad angle to the arc generator directly, it tends to subtract disproportionately from smaller arcs, introducing distortion.

Source · If radius is specified, sets the pad radius to the specified function or number and returns this arc generator. If radius is not specified, returns the current pad radius accessor, which defaults to null, indicating that the pad radius should be automatically computed as sqrt(innerRadius × innerRadius + outerRadius × outerRadius). The pad radius determines the fixed linear distance separating adjacent arcs, defined as padRadius × padAngle.

Source · If context is specified, sets the context and returns this arc generator.

If context is not specified, returns the current context, which defaults to null.

If the context is not null, then the generated arc is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated arc is returned.

Source · If digits is specified, sets the maximum number of digits after the decimal separator and returns this arc generator.

If digits is not specified, returns the current maximum fraction digits, which defaults to 3.

This option only applies when the associated context is null, as when this arc generator is used to produce path data.

**Examples:**

Example 1 (csharp):
```csharp
svg.append("path")
    .attr("transform", "translate(100,100)")
    .attr("d", d3.arc()({
      innerRadius: 100,
      outerRadius: 200,
      startAngle: -Math.PI / 2,
      endAngle: Math.PI / 2
    }));
```

Example 2 (javascript):
```javascript
const arc = d3.arc();
```

Example 3 (javascript):
```javascript
const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(100)
    .startAngle(0)
    .endAngle(Math.PI / 2);
```

Example 4 (css):
```css
const arc = d3.arc();

arc({
  innerRadius: 0,
  outerRadius: 100,
  startAngle: 0,
  endAngle: Math.PI / 2
}); // "M0,-100A100,100,0,0,1,100,0L0,0Z"
```

---

## Links | D3 by Observable

**URL:** https://d3js.org/d3-shape/link

**Contents:**
- Links ​
- link(curve) ​
- linkVertical() ​
- linkHorizontal() ​
- link(...arguments) ​
- link.source(source) ​
- link.target(target) ​
- link.x(x) ​
- link.y(y) ​
- link.context(context) ​

Examples · The link shape generates a smooth cubic Bézier curve from a source point to a target point. The tangents of the curve at the start and end are either vertical or horizontal. See also radial links.

Source · Returns a new link generator using the specified curve. For example, to visualize links in a tree diagram rooted on the top edge of the display, you might say:

Source · Shorthand for link with curveBumpY; suitable for visualizing links in a tree diagram rooted on the top edge of the display. Equivalent to:

Source · Shorthand for link with curveBumpX; suitable for visualizing links in a tree diagram rooted on the left edge of the display. Equivalent to:

Source · Generates a link for the given arguments. The arguments are arbitrary; they are propagated to the link generator’s accessor functions along with the this object. With the default settings, an object with source and target properties is expected.

Source · If source is specified, sets the source accessor to the specified function and returns this link generator.

If source is not specified, returns the current source accessor.

The source accessor defaults to:

Source · If target is specified, sets the target accessor to the specified function and returns this link generator.

If target is not specified, returns the current target accessor.

The target accessor defaults to:

Source · If x is specified, sets the x-accessor to the specified function or number and returns this link generator.

If x is not specified, returns the current x accessor.

The x accessor defaults to:

Source · If y is specified, sets the y-accessor to the specified function or number and returns this link generator.

If y is not specified, returns the current y accessor.

The y accessor defaults to:

Source · If context is specified, sets the context and returns this link generator.

If context is not specified, returns the current context.

The context defaults to null. If the context is not null, then the generated link is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated link is returned. See also d3-path.

Source · If digits is specified, sets the maximum number of digits after the decimal separator and returns this link generator.

If digits is not specified, returns the current maximum fraction digits, which defaults to 3.

This option only applies when the associated context is null, as when this link generator is used to produce path data.

**Examples:**

Example 1 (javascript):
```javascript
const link = d3.link(d3.curveBumpY)
    .x((d) => d.x)
    .y((d) => d.y);
```

Example 2 (swift):
```swift
const link = d3.link(d3.curveBumpY);
```

Example 3 (swift):
```swift
const link = d3.link(d3.curveBumpX);
```

Example 4 (swift):
```swift
link({source: [100, 100], target: [300, 300]}) // "M100,100C200,100,200,300,300,300"
```

---

## Lines | D3 by Observable

**URL:** https://d3js.org/d3-shape/line

**Contents:**
- Lines ​
- line(x, y) ​
- line(data) ​
- line.x(x) ​
- line.y(y) ​
- line.defined(defined) ​
- line.curve(curve) ​
- line.context(context) ​
- line.digits(digits) ​

Examples · The line generator produces a spline or polyline as in a line chart. Lines also appear in many other visualization types, such as the links in hierarchical edge bundling. See also radial lines.

Source · Constructs a new line generator with the given x and y accessor.

If x or y are not specified, the respective defaults will be used. The above can be expressed more explicitly as:

Source · Generates a line for the given array of data.

If the line generator has a context, then the line is rendered to this context as a sequence of path method calls and this function returns void. Otherwise, a path data string is returned.

Depending on this line generator’s associated curve, the given input data may need to be sorted by x-value before being passed to the line generator.

Source · If x is specified, sets the x accessor to the specified function or number and returns this line generator.

If x is not specified, returns the current x accessor.

The x accessor defaults to:

When a line is generated, the x accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments.

The default x accessor assumes that the input data are two-element arrays of numbers. If your data are in a different format, or if you wish to transform the data before rendering, then you should specify a custom accessor.

Source · If y is specified, sets the y accessor to the specified function or number and returns this line generator.

When a line is generated, the y accessor will be invoked for each defined element in the input data array, being passed the element d, the index i, and the array data as three arguments.

If y is not specified, returns the current y accessor.

The y accessor defaults to:

The default y accessor assumes that the input data are two-element arrays of numbers. See line.x for more information.

Examples · Source · If defined is specified, sets the defined accessor to the specified function or boolean and returns this line generator.

When a line is generated, the defined accessor will be invoked for each element in the input data array, being passed the element d, the index i, and the array data as three arguments. If the given element is defined (i.e., if the defined accessor returns a truthy value for this element), the x and y accessors will subsequently be evaluated and the point will be added to the current line segment. Otherwise, the element will be skipped, the current line segment will be ended, and a new line segment will be generated for the next defined point.

If defined is not specified, returns the current defined accessor.

The defined accessor defaults to the constant true, and assumes that the input data is always defined:

Note that if a line segment consists of only a single point, it may appear invisible unless rendered with rounded or square line caps. In addition, some curves such as curveCardinalOpen only render a visible segment if it contains multiple points.

Source · If curve is specified, sets the curve factory and returns this line generator.

If curve is not specified, returns the current curve factory, which defaults to curveLinear.

Source · If context is specified, sets the context and returns this line generator.

If context is not specified, returns the current context.

The context defaults to null. If the context is not null, then the generated line is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated line is returned.

Source · If digits is specified, sets the maximum number of digits after the decimal separator and returns this line generator.

If digits is not specified, returns the current maximum fraction digits, which defaults to 3.

This option only applies when the associated context is null, as when this line generator is used to produce path data.

**Examples:**

Example 1 (javascript):
```javascript
const line = d3.line((d) => x(d.Date), (d) => y(d.Close));
```

Example 2 (javascript):
```javascript
const line = d3.line()
    .x((d) => x(d.Date))
    .y((d) => y(d.Close));
```

Example 3 (unknown):
```unknown
svg.append("path").attr("d", line(data)).attr("stroke", "currentColor");
```

Example 4 (javascript):
```javascript
const line = d3.line().x((d) => x(d.Date));
```

---

## Radial lines | D3 by Observable

**URL:** https://d3js.org/d3-shape/radial-line

**Contents:**
- Radial lines ​
- lineRadial() ​
- lineRadial(data) ​
- lineRadial.angle(angle) ​
- lineRadial.radius(radius) ​
- lineRadial.defined(defined) ​
- lineRadial.curve(curve) ​
- lineRadial.context(context) ​

Examples · A radial line generator is like the Cartesian line generator except the x and y accessors are replaced with angle and radius accessors. Radial lines are positioned relative to the origin; use a transform to change the origin.

Source · Constructs a new radial line generator with the default settings.

Source · Equivalent to line.

Source · Equivalent to line.x, except the accessor returns the angle in radians, with 0 at -y (12 o’clock).

Source · Equivalent to line.y, except the accessor returns the radius: the distance from the origin.

Source · Equivalent to line.defined.

Source · Equivalent to line.curve. Note that curveMonotoneX or curveMonotoneY are not recommended for radial lines because they assume that the data is monotonic in x or y, which is typically untrue of radial lines.

Source · Equivalent to line.context.

**Examples:**

Example 1 (javascript):
```javascript
const line = d3.lineRadial();
```

Example 2 (unknown):
```unknown
svg.append("path").attr("d", line(data)).attr("stroke", "currentColor");
```

Example 3 (javascript):
```javascript
const line = d3.lineRadial().angle((d) => a(d.Date));
```

Example 4 (javascript):
```javascript
const line = d3.lineRadial().radius((d) => r(d.temperature));
```

---

## Symbols | D3 by Observable

**URL:** https://d3js.org/d3-shape/symbol

**Contents:**
- Symbols ​
- symbol(type, size) ​
- symbol(...arguments) ​
- symbol.type(type) ​
- symbol.size(size) ​
- symbol.context(context) ​
- symbol.digits(digits) ​
- symbolsFill ​
- symbolsStroke ​
- symbolAsterisk ​

Examples · Symbols provide a categorical shape encoding as in a scatterplot. Symbols are centered at the origin; use a transform to move the symbol to a different position.

Source · Constructs a new symbol generator of the specified type and size. If not specified, type defaults to a circle, and size defaults to 64.

Source · Generates a symbol for the given arguments. The arguments are arbitrary; they are propagated to the symbol generator’s accessor functions along with the this object. With the default settings, invoking the symbol generator produces a circle of 64 square pixels.

If the symbol generator has a context, then the symbol is rendered to this context as a sequence of path method calls and this function returns void. Otherwise, a path data string is returned.

Source · If type is specified, sets the symbol type to the specified function or symbol type and returns this symbol generator.

If type is a function, the symbol generator’s arguments and this are passed through. This is convenient for use with selection.attr, say in conjunction with an ordinal scale to produce a categorical symbol encoding.

If type is not specified, returns the current symbol type accessor.

The symbol type accessor defaults to:

See symbolsFill and symbolsStroke for built-in symbol types. To implement a custom symbol type, pass an object that implements symbolType.draw.

Source · If size is specified, sets the size to the specified function or number and returns this symbol generator.

If size is a function, the symbol generator’s arguments and this are passed through. This is convenient for use with selection.attr, say in conjunction with a linear scale to produce a quantitative size encoding.

If size is not specified, returns the current size accessor.

The size accessor defaults to:

Source · If context is specified, sets the context and returns this symbol generator.

If context is not specified, returns the current context.

The context defaults to null. If the context is not null, then the generated symbol is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated symbol is returned.

Source · If digits is specified, sets the maximum number of digits after the decimal separator and returns this symbol generator.

If digits is not specified, returns the current maximum fraction digits, which defaults to 3.

This option only applies when the associated context is null, as when this symbol generator is used to produce path data.

Source · An array containing a set of symbol types designed for filling: circle, cross, diamond, square, star, triangle, and wye. Useful for a categorical shape encoding with an ordinal scale.

Source · An array containing a set of symbol types designed for stroking: circle, plus, times, triangle2, asterisk, square2, and diamond2. Useful for a categorical shape encoding with an ordinal scale.

Source · The asterisk symbol type; intended for stroking.

Source · The circle symbol type; intended for either filling or stroking.

Source · The Greek cross symbol type, with arms of equal length; intended for filling.

Source · The rhombus symbol type; intended for filling.

Source · The rotated square symbol type; intended for stroking.

Source · The plus symbol type; intended for stroking.

Source · The square symbol type; intended for filling.

Source · The square2 symbol type; intended for stroking.

Source · The pentagonal star (pentagram) symbol type; intended for filling.

Source · The up-pointing triangle symbol type; intended for filling.

Source · The up-pointing triangle symbol type; intended for stroking.

Source · The Y-shape symbol type; intended for filling.

Source · The X-shape symbol type; intended for stroking.

Symbol types are typically not used directly, instead being passed to symbol.type. However, you can define your own symbol type implementation should none of the built-in types satisfy your needs using the following interface. You can also use this low-level interface with a built-in symbol type as an alternative to the symbol generator.

Renders this symbol type to the specified context with the specified size in square pixels. The context implements the CanvasPathMethods interface. (Note that this is a subset of the CanvasRenderingContext2D interface!) See also d3-path.

Examples · Source · Returns the point [x, y] for the given angle in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise, and the given radius.

**Examples:**

Example 1 (unknown):
```unknown
svg.append("path").attr("d", d3.symbol(d3.symbolCross));
```

Example 2 (unknown):
```unknown
d3.symbol()() // "M4.514,0A4.514,4.514,0,1,1,-4.514,0A4.514,4.514,0,1,1,4.514,0"
```

Example 3 (javascript):
```javascript
const symbol = d3.symbol().type(d3.symbolCross);
```

Example 4 (javascript):
```javascript
const symbolType = d3.scaleOrdinal(d3.symbolsFill);
const symbol = d3.symbol().type((d) => symbolType(d.category));
```

---

## Stacks | D3 by Observable

**URL:** https://d3js.org/d3-shape/stack

**Contents:**
- Stacks ​
- stack() ​
- stack(data, ...arguments) ​
- stack.keys(keys) ​
- stack.value(value) ​
- stack.order(order) ​
- stack.offset(offset) ​
- Stack orders ​
  - stackOrderAppearance(series) ​
  - stackOrderAscending(series) ​

Examples · Stacking converts lengths into contiguous position intervals. For example, a bar chart of monthly sales might be broken down into a multi-series bar chart by category, stacking bars vertically and applying a categorical color encoding. Stacked charts can show overall value and per-category value simultaneously; however, it is typically harder to compare across categories as only the bottom layer of the stack is aligned. So, chose the stack order carefully, and consider a streamgraph. (See also grouped charts.)

Like the pie generator, the stack generator does not produce a shape directly. Instead it computes positions which you can then pass to an area generator or use directly, say to position bars.

Source · Constructs a new stack generator with the default settings. See stack for usage.

Source · Generates a stack for the given array of data and returns an array representing each series. Any additional arguments are arbitrary; they are propagated to accessors along with the this object.

For example, consider this tidy table of monthly fruit sales:

This could be represented in JavaScript as an array of objects, perhaps parsed from CSV:

To compute the stacked series (a series, or layer, for each fruit; and a stack, or column, for each date), we can index the data by date and then fruit, compute the distinct fruit names across the data set, and lastly get the sales value for each date and fruit.

See union and index from d3-array.

The resulting array has one element per series. Each series has one point per month, and each point has a lower and upper value defining the baseline and topline:

Each series in then typically passed to an area generator to render an area chart, or used to construct rectangles for a bar chart.

The series are determined by the keys accessor; each series i in the returned array corresponds to the ith key. Each series is an array of points, where each point j corresponds to the jth element in the input data. Lastly, each point is represented as an array [y0, y1] where y0 is the lower value (baseline) and y1 is the upper value (topline); the difference between y0 and y1 corresponds to the computed value for this point. The key for each series is available as series.key, and the index as series.index. The input data element for each point is available as point.data.

Source · If keys is specified, sets the keys accessor to the specified function or array and returns this stack generator.

If keys is not specified, returns the current keys accessor.

The keys accessor defaults to the empty array. A series (layer) is generated for each key. Keys are typically strings, but they may be arbitrary values; see InternMap. The series’ key is passed to the value accessor, along with each data point, to compute the point’s value.

Source · If value is specified, sets the value accessor to the specified function or number and returns this stack generator.

If value is not specified, returns the current value accessor.

The value accessor defaults to:

The default value accessor assumes that the input data is an array of objects exposing named properties with numeric values. This is a “wide” rather than “tidy” representation of data and is no longer recommended. See stack for an example using tidy data.

Source · If order is specified, sets the order accessor to the specified function or array and returns this stack generator.

If order is a function, it is passed the generated series array and must return an array of numeric indexes representing the stack order. For example, to use reverse key order:

The stack order is computed prior to the offset; thus, the lower value for all points is zero at the time the order is computed. The index attribute for each series is also not set until after the order is computed.

If order is not specified, returns the current order accessor.

The order accessor defaults to stackOrderNone; this uses the order given by the key accessor. See stack orders for the built-in orders.

Source · If offset is specified, sets the offset accessor to the specified function and returns this stack generator.

The offset function is passed the generated series array and the order index array; it is then responsible for updating the lower and upper values in the series array. See the built-in offsets for a reference implementation.

If offset is not specified, returns the current offset acccesor.

The offset accessor defaults to stackOffsetNone; this uses a zero baseline. See stack offsets for the built-in offsets.

Stack orders are typically not used directly, but are instead passed to stack.order.

Source · Returns a series order such that the earliest series (according to the maximum value) is at the bottom.

Source · Returns a series order such that the smallest series (according to the sum of values) is at the bottom.

Source · Returns a series order such that the largest series (according to the sum of values) is at the bottom.

Source · Returns a series order such that the earliest series (according to the maximum value) are on the inside and the later series are on the outside. This order is recommended for streamgraphs in conjunction with the wiggle offset. See Stacked Graphs — Geometry & Aesthetics by Byron & Wattenberg for more information.

Source · Returns the given series order [0, 1, … n - 1] where n is the number of elements in series. Thus, the stack order is given by the key accessor.

Source · Returns the reverse of the given series order [n - 1, n - 2, … 0] where n is the number of elements in series. Thus, the stack order is given by the reverse of the key accessor.

Stack offsets are typically not used directly, but are instead passed to stack.offset.

Source · Applies a zero baseline and normalizes the values for each point such that the topline is always one.

Source · Positive values are stacked above zero, negative values are stacked below zero, and zero values are stacked at zero.

Source · Applies a zero baseline.

Source · Shifts the baseline down such that the center of the streamgraph is always at zero.

Source · Shifts the baseline so as to minimize the weighted wiggle of layers. This offset is recommended for streamgraphs in conjunction with the inside-out order. See Stacked Graphs — Geometry & Aesthetics by Bryon & Wattenberg for more information.

**Examples:**

Example 1 (json):
```json
const data = [
  {date: new Date("2015-01-01"), fruit: "apples", sales: 3840},
  {date: new Date("2015-01-01"), fruit: "bananas", sales: 1920},
  {date: new Date("2015-01-01"), fruit: "cherries", sales: 960},
  {date: new Date("2015-01-01"), fruit: "durians", sales: 400},
  {date: new Date("2015-02-01"), fruit: "apples", sales: 1600},
  {date: new Date("2015-02-01"), fruit: "bananas", sales: 1440},
  {date: new Date("2015-02-01"), fruit: "cherries", sales: 960},
  {date: new Date("2015-02-01"), fruit: "durians", sales: 400},
  {date: new Date("2015-03-01"), fruit: "apples", sales: 640},
  {date: new Date("2015-03-01"), fruit: "bananas", sales: 960},
  {date: new Date("2015-03-01"), fruit: "cherries", sales: 640},
  {date: new Date("2015-03-01"), fruit: "durians", sales: 400},
  {date: new Date("2015-04-01"), fruit: "apples", sales: 320},
  {date: new Date("2015-04-01"), fruit: "bananas", sales: 480},
  {date: new Date("2015-04-01"), fruit: "cherries", sales: 640},
  {date: new Date("2015-04-01"), fruit: "durians", sales: 400}
];
```

Example 2 (javascript):
```javascript
const series = d3.stack()
    .keys(d3.union(data.map(d => d.fruit))) // apples, bananas, cherries, …
    .value(([, group], key) => group.get(key).sales)
  (d3.index(data, d => d.date, d => d.fruit));
```

Example 3 (json):
```json
[
  [[   0, 3840], [   0, 1600], [   0,  640], [   0,  320]], // apples
  [[3840, 5760], [1600, 3040], [ 640, 1600], [ 320,  800]], // bananas
  [[5760, 6720], [3040, 4000], [1600, 2240], [ 800, 1440]], // cherries
  [[6720, 7120], [4000, 4400], [2240, 2640], [1440, 1840]]  // durians
]
```

Example 4 (dart):
```dart
svg.append("g")
  .selectAll("g")
  .data(series)
  .join("g")
    .attr("fill", d => color(d.key))
  .selectAll("rect")
  .data(D => D)
  .join("rect")
    .attr("x", d => x(d.data[0]))
    .attr("y", d => y(d[1]))
    .attr("height", d => y(d[0]) - y(d[1]))
    .attr("width", x.bandwidth());
```

---

## d3-shape | D3 by Observable

**URL:** https://d3js.org/d3-shape

**Contents:**
- d3-shape ​

Visualizations can be represented by discrete graphical marks such as symbols, arcs, lines, and areas. While the rectangles of a bar chart may sometimes be simple, other shapes are complex, such as rounded annular sectors and Catmull–Rom splines. The d3-shape module provides a variety of shape generators for your convenience.

As with other aspects of D3, these shapes are driven by data: each shape generator exposes accessors that control how the input data are mapped to a visual representation. For example, you might define a line generator for a time series by scaling fields of your data to fit the chart:

This line generator can then be used to compute the d attribute of an SVG path element:

Or you can use it to render to a Canvas 2D context:

**Examples:**

Example 1 (javascript):
```javascript
const line = d3.line()
    .x((d) => x(d.date))
    .y((d) => y(d.value));
```

Example 2 (unknown):
```unknown
path.datum(data).attr("d", line);
```

Example 3 (unknown):
```unknown
line.context(context)(data);
```

---
