## d3-color | D3 by Observable

**URL:** https://d3js.org/d3-color

**Contents:**
- d3-color ​
- color(specifier) ​
- color.opacity ​
- color.rgb() ​
- color.copy(values) ​
- color.brighter(k) ​
- color.darker(k) ​
- color.displayable() ​
- color.formatHex() ​
- color.formatHex8() ​

Even though your browser understands a lot about colors, it doesn’t offer much help in manipulating colors through JavaScript. The d3-color module therefore provides representations for various color spaces, allowing specification, conversion and manipulation. (Also see d3-interpolate for color interpolation.)

For example, take the named color steelblue, which is rgb(70, 130, 180) in RGB:

To convert to HSL hsl(207.3, 44%, 49%):

To then rotate the hue by 90° hsl(297.3, 44%, 49%), increase the saturation by 20% hsl(297.3, 64%, 49%), and format as an RGB string rgb(198, 45, 205):

To fade the color slightly rgba(198, 45, 205, 0.8):

In addition to the ubiquitous and machine-friendly RGB and HSL color space, d3-color supports color spaces that are designed for humans:

Cubehelix features monotonic lightness, while CIELAB and its polar form CIELChab are perceptually uniform.

For additional color spaces, see:

To measure color differences, see:

Source · Parses the specified CSS Color Module Level 3 specifier string, returning an RGB or HSL color, along with CSS Color Module Level 4 hex specifier strings. If the specifier was not valid, null is returned. Some examples:

The list of supported named colors is specified by CSS.

Note: this function may also be used with instanceof to test if an object is a color instance. The same is true of color subclasses, allowing you to test whether a color is in a particular color space.

This color’s opacity, typically in the range [0, 1].

Source · Returns the RGB equivalent of this color. For RGB colors, that’s this.

Source · Returns a copy of this color. If values is specified, any enumerable own properties of values are assigned to the new returned color.

Source · Returns a brighter copy of this color. For example, if k is 1, steelblue in RGB color space becomes rgb(100, 186, 255). The parameter k controls how much brighter the returned color should be (in arbitrary units); if k is not specified, it defaults to 1. The behavior of this method is dependent on the implementing color space.

Source · Returns a darker copy of this color. For example, if k is 1, steelblue in RGB color space becomes rgb(49, 91, 126). The parameter k controls how much darker the returned color should be (in arbitrary units); if k is not specified, it defaults to 1. The behavior of this method is dependent on the implementing color space.

Source · Returns true if and only if the color is displayable on standard hardware. For example, this returns false for an RGB color if any channel value is less than zero or greater than 255 when rounded, or if the opacity is not in the range [0, 1].

Source · Returns a hexadecimal string representing this color in RGB space, such as #4682b4. If this color is not displayable, a suitable displayable color is returned instead. For example, RGB channel values greater than 255 are clamped to 255.

Source · Returns a hexadecimal string representing this color in RGBA space, such as #4682b4cc. If this color is not displayable, a suitable displayable color is returned instead. For example, RGB channel values greater than 255 are clamped to 255.

Source · Returns a string representing this color according to the CSS Color Module Level 3 specification, such as hsl(257, 50%, 80%) or hsla(257, 50%, 80%, 0.2). If this color is not displayable, a suitable displayable color is returned instead by clamping S and L channel values to the interval [0, 100].

Source · Returns a string representing this color according to the CSS Object Model specification, such as rgb(247, 234, 186) or rgba(247, 234, 186, 0.2). If this color is not displayable, a suitable displayable color is returned instead by clamping RGB channel values to the interval [0, 255].

Source · An alias for color.formatRgb.

Source · Constructs a new RGB color. The channel values are exposed as r, g and b properties on the returned instance. Use the RGB color picker to explore this color space.

If r, g and b are specified, these represent the channel values of the returned color; an opacity may also be specified. If a CSS Color Module Level 3 specifier string is specified, it is parsed and then converted to the RGB color space. See color for examples. If a color instance is specified, it is converted to the RGB color space using color.rgb. Note that unlike color.rgb this method always returns a new instance, even if color is already an RGB color.

Source · Returns a new RGB color where the r, g, and b channels are clamped to the range [0, 255] and rounded to the nearest integer value, and the opacity is clamped to the range [0, 1].

Source · Constructs a new HSL color. The channel values are exposed as h, s and l properties on the returned instance. Use the HSL color picker to explore this color space.

If h, s and l are specified, these represent the channel values of the returned color; an opacity may also be specified. If a CSS Color Module Level 3 specifier string is specified, it is parsed and then converted to the HSL color space. See color for examples. If a color instance is specified, it is converted to the RGB color space using color.rgb and then converted to HSL. (Colors already in the HSL color space skip the conversion to RGB.)

Source · Returns a new HSL color where the h channel is clamped to the range [0, 360), and the s, l, and opacity channels are clamped to the range [0, 1].

Source · Constructs a new CIELAB color. The channel values are exposed as l, a and b properties on the returned instance. Use the CIELAB color picker to explore this color space. The value of l is typically in the range [0, 100], while a and b are typically in [-160, +160].

If l, a and b are specified, these represent the channel values of the returned color; an opacity may also be specified. If a CSS Color Module Level 3 specifier string is specified, it is parsed and then converted to the CIELAB color space. See color for examples. If a color instance is specified, it is converted to the RGB color space using color.rgb and then converted to CIELAB. (Colors already in the CIELAB color space skip the conversion to RGB, and colors in the HCL color space are converted directly to CIELAB.)

Source · Constructs a new CIELAB color with the specified l value and a = b = 0.

Source · Equivalent to d3.lch, but with reversed argument order.

Source · Constructs a new CIELChab color. The channel values are exposed as l, c and h properties on the returned instance. Use the CIELChab color picker to explore this color space. The value of l is typically in the range [0, 100], c is typically in [0, 230], and h is typically in [0, 360).

If l, c, and h are specified, these represent the channel values of the returned color; an opacity may also be specified. If a CSS Color Module Level 3 specifier string is specified, it is parsed and then converted to CIELChab color space. See color for examples. If a color instance is specified, it is converted to the RGB color space using color.rgb and then converted to CIELChab. (Colors already in CIELChab color space skip the conversion to RGB, and colors in CIELAB color space are converted directly to CIELChab.)

Source · Constructs a new Cubehelix color. The channel values are exposed as h, s and l properties on the returned instance.

If h, s and l are specified, these represent the channel values of the returned color; an opacity may also be specified. If a CSS Color Module Level 3 specifier string is specified, it is parsed and then converted to the Cubehelix color space. See color for examples. If a color instance is specified, it is converted to the RGB color space using color.rgb and then converted to Cubehelix. (Colors already in the Cubehelix color space skip the conversion to RGB.)

**Examples:**

Example 1 (css):
```css
let c = d3.color("steelblue"); // {r: 70, g: 130, b: 180, opacity: 1}
```

Example 2 (css):
```css
c = d3.hsl(c); // {h: 207.27…, s: 0.44, l: 0.4902…, opacity: 1}
```

Example 3 (unknown):
```unknown
c.h += 90;
c.s += 0.2;
c + ""; // rgb(198, 45, 205)
```

Example 4 (unknown):
```unknown
c.opacity = 0.8;
c + ""; // rgba(198, 45, 205, 0.8)
```
