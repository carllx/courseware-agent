## d3-axis | D3 by Observable

**URL:** https://d3js.org/d3-axis

**Contents:**
- d3-axis ​
- axisTop(scale) ​
- axisRight(scale) ​
- axisBottom(scale) ​
- axisLeft(scale) ​
- axis(context) ​
- axis.scale(scale) ​
- axis.ticks(...arguments) ​
- axis.tickArguments(arguments) ​
- axis.tickValues(values) ​

The axis component renders human-readable reference marks for position scales. It works with most scale types, including linear, log, band, and time scales as shown above.

Calling the axis component on a selection of SVG containers (usually a single G element) populates the axes. Axes are rendered at the origin. To change the position of the axis with respect to the chart, specify a transform attribute on the containing element.

If the scale has changed, call the axis component a second time to update. For smooth animations, you can call it on a transition.

The elements created by the axis are considered part of its public API. You can apply external stylesheets or modify the generated axis elements to customize the axis appearance. An axis consists of a path element of class “domain” representing the extent of the scale’s domain, followed by transformed g elements of class “tick” representing each of the scale’s ticks. Each tick has a line element to draw the tick line, and a text element for the tick label. For example, here is a typical bottom-oriented axis:

The orientation of an axis is fixed; to change the orientation, remove the old axis and create a new axis.

Source · Constructs a new top-oriented axis generator for the given scale, with empty tick arguments, a tick size of 6 and padding of 3. In this orientation, ticks are drawn above the horizontal domain path.

Source · Constructs a new right-oriented axis generator for the given scale, with empty tick arguments, a tick size of 6 and padding of 3. In this orientation, ticks are drawn to the right of the vertical domain path.

Source · Constructs a new bottom-oriented axis generator for the given scale, with empty tick arguments, a tick size of 6 and padding of 3. In this orientation, ticks are drawn below the horizontal domain path.

Source · Constructs a new left-oriented axis generator for the given scale, with empty tick arguments, a tick size of 6 and padding of 3. In this orientation, ticks are drawn to the left of the vertical domain path.

Source · Render the axis to the given context, which may be either a selection of SVG containers (either SVG or G elements) or a corresponding transition.

Source · If scale is specified, sets the scale and returns the axis. If scale is not specified, returns the current scale.

Sets the arguments that will be passed to scale.ticks and scale.tickFormat when the axis is rendered, and returns the axis generator.

The meaning of the arguments depends on the axis’ scale type: most commonly, the arguments are a suggested count for the number of ticks (or a time interval for time scales), and an optional format specifier to customize how the tick values are formatted. For example, to generate twenty ticks with SI-prefix formatting on a linear scale, say:

To generate ticks every fifteen minutes with a time scale, say:

This method is a convenience function for axis.tickArguments. For example, this:

This method has no effect if the scale does not implement scale.ticks, as with band and point scales. To set the tick values explicitly, use axis.tickValues. To set the tick format explicitly, use axis.tickFormat. To generate tick values directly, use scale.ticks.

Source · If arguments is specified, sets the arguments that will be passed to scale.ticks and scale.tickFormat when the axis is rendered, and returns the axis generator. See also axis.ticks, which is used more commonly.

The meaning of the arguments depends on the axis’ scale type: most commonly, the arguments are a suggested count for the number of ticks (or a time interval for time scales), and an optional format specifier to customize how the tick values are formatted. For example, to generate twenty ticks with SI-prefix formatting on a linear scale, say:

To generate ticks every fifteen minutes with a time scale, say:

If arguments is not specified, returns the current tick arguments, which defaults to the empty array. If arguments is specified, this method has no effect if the scale does not implement scale.ticks, as with band and point scales. To set the tick values explicitly, use axis.tickValues. To set the tick format explicitly, use axis.tickFormat.

Source · If a values iterable is specified, the specified values are used for ticks rather than the scale’s automatic tick generator. For example, to generate ticks at specific values:

The explicit tick values take precedence over the tick arguments set by axis.tickArguments. However, any tick arguments will still be passed to the scale’s tickFormat function if a tick format is not also set.

If values is null, clears any previously-set explicit tick values and reverts back to the scale’s tick generator. If values is not specified, returns the current tick values, which defaults to null.

Source · If format is specified, sets the tick format function and returns the axis. For example, to display integers with comma-grouping for thousands:

More commonly, a format specifier is passed to axis.ticks, which has the advantage of setting the format precision automatically based on the tick interval:

See d3-format and d3-time-format for help creating formatters.

If format is not specified, returns the current format function, which defaults to null. A null format indicates that the scale’s default formatter should be used, which is generated by calling scale.tickFormat. In this case, the arguments specified by axis.tickArguments are likewise passed to scale.tickFormat.

Source · If size is specified, sets the inner and outer tick size to the specified value and returns the axis.

If size is not specified, returns the current inner tick size, which defaults to 6.

Source · If size is specified, sets the inner tick size to the specified value and returns the axis.

If size is not specified, returns the current inner tick size, which defaults to 6.

The inner tick size controls the length of the tick lines, offset from the native position of the axis.

Source · If size is specified, sets the outer tick size to the specified value and returns the axis.

If size is not specified, returns the current outer tick size, which defaults to 6.

The outer tick size controls the length of the square ends of the domain path, offset from the native position of the axis. Thus, the “outer ticks” are not actually ticks but part of the domain path, and their position is determined by the associated scale’s domain extent. Thus, outer ticks may overlap with the first or last inner tick. An outer tick size of 0 suppresses the square ends of the domain path, instead producing a straight line.

Source · If padding is specified, sets the padding to the specified value in pixels and returns the axis.

If padding is not specified, returns the current padding which defaults to 3 pixels.

Source · If offset is specified, sets the pixel offset to the specified value in pixels and returns the axis.

If offset is not specified, returns the current pixel offset.

The pixel offset defaults to 0 on devices with a devicePixelRatio greater than 1, and 0.5 otherwise. This default pixel offset ensures crisp edges on low-resolution devices.

**Examples:**

Example 1 (csharp):
```csharp
const gx = svg.append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x));
```

Example 2 (swift):
```swift
gx.transition()
    .duration(750)
    .call(d3.axisBottom(x));
```

Example 3 (csharp):
```csharp
<g fill="none" font-size="10" font-family="sans-serif" text-anchor="middle">
  <path class="domain" stroke="currentColor" d="M0.5,6V0.5H880.5V6"></path>
  <g class="tick" opacity="1" transform="translate(0.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">0.0</text>
  </g>
  <g class="tick" opacity="1" transform="translate(176.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">0.2</text>
  </g>
  <g class="tick" opacity="1" transform="translate(352.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">0.4</text>
  </g>
  <g class="tick" opacity="1" transform="translate(528.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">0.6</text>
  </g>
  <g class="tick" opacity="1" transform="translate(704.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">0.8</text>
  </g>
  <g class="tick" opacity="1" transform="translate(880.5,0)">
    <line stroke="currentColor" y2="6"></line>
    <text fill="currentColor" y="9" dy="0.71em">1.0</text>
  </g>
</g>
```

Example 4 (csharp):
```csharp
svg.append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x));
```

---

