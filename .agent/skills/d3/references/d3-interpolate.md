# D3 - D3-Interpolate

**Pages:** 5

---

## Zoom interpolation | D3 by Observable

**URL:** https://d3js.org/d3-interpolate/zoom

**Contents:**
- Zoom interpolation ​
- interpolateZoom(a, b) ​
- interpolateZoom.rho(rho) ​

An interpolator for zooming smoothly between two views of a two-dimensional plane based on “Smooth and efficient zooming and panning” by Jarke J. van Wijk and Wim A.A. Nuij.

Examples · Source · Returns an interpolator between the two views a and b. Each view is defined as an array of three numbers: cx, cy and width. The first two coordinates cx, cy represent the center of the viewport; the last coordinate width represents the size of the viewport.

The returned interpolator exposes a interpolate.duration property which encodes the recommended transition duration in milliseconds. This duration is based on the path length of the curved trajectory through xy space. If you want a slower or faster transition, multiply this by an arbitrary scale factor (V as described in the original paper).

Source · Given a zoom interpolator, returns a new zoom interpolator using the specified curvature rho. When rho is close to 0, the interpolator is almost linear. The default curvature is sqrt(2).

**Examples:**

Example 1 (unknown):
```unknown
d3.interpolateZoom([30, 30, 40], [135, 85, 60])(0.5) // [72, 52, 126.04761005270991]
```

Example 2 (unknown):
```unknown
d3.interpolateZoom.rho(0.5)([30, 30, 40], [135, 85, 60])(0.5) // [72, 52, 51.09549882328188]
```

---

## Value interpolation | D3 by Observable

**URL:** https://d3js.org/d3-interpolate/value

**Contents:**
- Value interpolation ​
- interpolate(a, b) ​
- interpolateNumber(a, b) ​
- interpolateRound(a, b) ​
- interpolateString(a, b) ​
- interpolateDate(a, b) ​
- interpolateArray(a, b) ​
- interpolateNumberArray(a, b) ​
- interpolateObject(a, b) ​
- interpolateBasis(values) ​

These are the most general interpolators, suitable for most values.

Examples · Source · Returns an interpolator between the two arbitrary values a and b.

The interpolator implementation is based on the type of the end value b, using the following algorithm:

Based on the chosen interpolator, a is coerced to the suitable corresponding type.

Examples · Source · Returns an interpolator between the two numbers a and b.

The returned interpolator is equivalent to:

Avoid interpolating to or from the number zero when the interpolator is used to generate a string. When very small values are stringified, they may be converted to scientific notation, which is an invalid attribute or style property value in older browsers. For example, the number 0.0000001 is converted to the string "1e-7". This is particularly noticeable with interpolating opacity. To avoid scientific notation, start or end the transition at 1e-6: the smallest value that is not stringified in scientific notation.

Examples · Source · Returns an interpolator between the two numbers a and b.

The interpolator is similar to interpolateNumber except it will round the resulting value to the nearest integer.

Examples · Source · Returns an interpolator between the two strings a and b.

The string interpolator finds numbers embedded in a and b, where each number is of the form understood by JavaScript. A few examples of numbers that will be detected within a string: -1, 42, 3.14159, and 6.0221413e+23.

For each number embedded in b, the interpolator will attempt to find a corresponding number in a. If a corresponding number is found, a numeric interpolator is created using interpolateNumber. The remaining parts of the string b are used as a template: the static parts of the string b remain constant for the interpolation, with the interpolated numeric values embedded in the template.

For example, if a is "300 12px sans-serif", and b is "500 36px Comic-Sans", two embedded numbers are found. The remaining static parts (of string b) are a space between the two numbers (" "), and the suffix ("px Comic-Sans"). The result of the interpolator at t = 0.5 is "400 24px Comic-Sans".

Examples · Source · Returns an interpolator between the two dates a and b.

No defensive copy of the returned date is created; the same Date instance is returned for every evaluation of the interpolator. No copy is made for performance reasons, as interpolators are often part of the inner loop of animated transitions.

Examples · Source · Returns an interpolator between the two arrays a and b.

If b is a typed array (e.g., Float64Array), interpolateNumberArray is called instead.

Internally, an array template is created that is the same length as b. For each element in b, if there exists a corresponding element in a, a generic interpolator is created for the two elements using interpolate. If there is no such element, the static value from b is used in the template. Then, for the given parameter t, the template’s embedded interpolators are evaluated. The updated array template is then returned.

For example, if a is the array [0, 1] and b is the array [1, 10, 100], then the result of the interpolator for t = 0.5 is the array [0.5, 5.5, 100].

No defensive copy of the template array is created; modifications of the returned array may adversely affect subsequent evaluation of the interpolator. No copy is made for performance reasons; interpolators are often part of the inner loop of animated transitions.

Examples · Source · Returns an interpolator between the two arrays of numbers a and b.

Internally, an array template is created that is the same type and length as b. For each element in b, if there exists a corresponding element in a, the values are directly interpolated in the array template. If there is no such element, the static value from b is copied. The updated array template is then returned.

No defensive copy is made of the template array and the arguments a and b; modifications of these arrays may affect subsequent evaluation of the interpolator.

Examples · Source · Returns an interpolator between the two objects a and b.

Internally, an object template is created that has the same properties as b. For each property in b, if there exists a corresponding property in a, a generic interpolator is created for the two elements using interpolate. If there is no such property, the static value from b is used in the template. Then, for the given parameter t, the template's embedded interpolators are evaluated and the updated object template is then returned.

For example, if a is the object {x: 0, y: 1} and b is the object {x: 1, y: 10, z: 100}, the result of the interpolator for t = 0.5 is the object {x: 0.5, y: 5.5, z: 100}.

Object interpolation is particularly useful for dataspace interpolation, where data is interpolated rather than attribute values. For example, you can interpolate an object which describes an arc in a pie chart, and then use arc to compute the new SVG path data.

No defensive copy of the template object is created; modifications of the returned object may adversely affect subsequent evaluation of the interpolator. No copy is made for performance reasons; interpolators are often part of the inner loop of animated transitions.

Examples · Source · Returns a uniform nonrational B-spline interpolator through the specified array of values, which must be numbers.

Implicit control points are generated such that the interpolator returns values[0] at t = 0 and values[values.length - 1] at t = 1. See also curveBasis and interpolateRgbBasis.

Examples · Source · Returns a uniform nonrational B-spline interpolator through the specified array of values, which must be numbers.

The control points are implicitly repeated such that the resulting one-dimensional spline has cyclical C² continuity when repeated around t in [0,1]. See also curveBasisClosed and interpolateRgbBasisClosed.

Examples · Source · Returns a discrete interpolator for the given array of values.

The returned interpolator maps t in [0, 1 / n) to values[0], t in [1 / n, 2 / n) to values[1], and so on, where n = values.length. In effect, this is a lightweight quantize scale with a fixed domain of [0, 1].

Examples · Source · Returns n uniformly-spaced samples from the specified interpolator, where n is an integer greater than one.

The first sample is always at t = 0, and the last sample is always at t = 1. This can be useful in generating a fixed number of samples from a given interpolator, such as to derive the range of a quantize scale from a continuous interpolator.

This method will not work with interpolators that do not return defensive copies of their output, such as interpolateArray, interpolateDate and interpolateObject. For those interpolators, you must wrap the interpolator and create a copy for each returned value.

Examples · Source · Returns a piecewise interpolator, composing interpolators for each adjacent pair of values.

If interpolate is not specified, defaults to interpolate.

The returned interpolator maps t in [0, 1 / (n - 1)] to interpolate(values[0], values[1]), t in [1 / (n - 1), 2 / (n - 1)] to interpolate(values[1], values[2]), and so on, where n = values.length. In effect, this is a lightweight linear scale.

**Examples:**

Example 1 (unknown):
```unknown
d3.interpolate("red", "blue")(0.5) // "rgb(128, 0, 128)"
```

Example 2 (unknown):
```unknown
d3.interpolateNumber(20, 620)(0.8) // 500
```

Example 3 (javascript):
```javascript
function interpolator(t) {
  return a * (1 - t) + b * t;
}
```

Example 4 (unknown):
```unknown
d3.interpolateRound(20, 620)(0.821) // 513
```

---

## Transform interpolation | D3 by Observable

**URL:** https://d3js.org/d3-interpolate/transform

**Contents:**
- Transform interpolation ​
- interpolateTransformCss(a, b) ​
- interpolateTransformSvg(a, b) ​

Interpolators for CSS and SVG transforms. The interpolation method is standardized by CSS: see matrix decomposition for animation.

Examples · Source · Returns an interpolator between the two 2D CSS transforms represented by a and b. Each transform is decomposed to a standard representation of translate, rotate, x-skew and scale; these component transformations are then interpolated.

Examples · Source · Returns an interpolator between the two 2D SVG transforms represented by a and b. Each transform is decomposed to a standard representation of translate, rotate, x-skew and scale; these component transformations are then interpolated.

**Examples:**

Example 1 (unknown):
```unknown
d3.interpolateTransformCss("translateY(12px) scale(2)", "translateX(30px) rotate(5deg)")(0.5) // "translate(15px,6px) rotate(2.5deg) scale(1.5,1.5)"
```

Example 2 (unknown):
```unknown
d3.interpolateTransformSvg("skewX(-60)", "skewX(60) translate(280,0)") // "translate(140,0) skewX(0)"
```

---

## d3-interpolate | D3 by Observable

**URL:** https://d3js.org/d3-interpolate

**Contents:**
- d3-interpolate ​

This module provides a variety of interpolation methods for blending between two values. Values may be numbers, colors, strings, arrays, or even deeply-nested objects. For example:

The returned function i is an interpolator. Given a starting value a and an ending value b, it takes a parameter t typically in [0, 1] and returns the corresponding interpolated value. An interpolator typically returns a value equivalent to a at t = 0 and a value equivalent to b at t = 1.

You can interpolate more than just numbers. To find the perceptual midpoint between steelblue and brown:

Or, as a color ramp from t = 0 to t = 1:

Here’s a more elaborate example demonstrating type inference used by interpolate:

Note that the generic value interpolator detects not only nested objects and arrays, but also color strings and numbers embedded in strings!

**Examples:**

Example 1 (javascript):
```javascript
const i = d3.interpolateNumber(10, 20);
i(0.0); // 10
i(0.2); // 12
i(0.5); // 15
i(1.0); // 20
```

Example 2 (unknown):
```unknown
d3.interpolateLab("steelblue", "brown")(0.5); // "rgb(142, 92, 109)"
```

Example 3 (css):
```css
const i = d3.interpolate({colors: ["red", "blue"]}, {colors: ["white", "black"]});
i(0.0); // {colors: ["rgb(255, 0, 0)", "rgb(0, 0, 255)"]}
i(0.5); // {colors: ["rgb(255, 128, 128)", "rgb(0, 0, 128)"]}
i(1.0); // {colors: ["rgb(255, 255, 255)", "rgb(0, 0, 0)"]}
```

---

## Color interpolation | D3 by Observable

**URL:** https://d3js.org/d3-interpolate/color

**Contents:**
- Color interpolation ​
- interpolateRgb(a, b) ​
- interpolateRgbBasis(colors) ​
- interpolateRgbBasisClosed(colors) ​
- interpolateHsl(a, b) ​
- interpolateHslLong(a, b) ​
- interpolateLab(a, b) ​
- interpolateHcl(a, b) ​
- interpolateHclLong(a, b) ​
- interpolateCubehelix(a, b) ​

Interpolators for colors in various color spaces.

Examples · Source · Returns an RGB color space interpolator between the two colors a and b with a configurable gamma. If the gamma is not specified, it defaults to 1.0. The colors a and b need not be in RGB; they will be converted to RGB using d3.rgb. The return value of the interpolator is an RGB string.

Examples · Source · Returns a uniform nonrational B-spline interpolator through the specified array of colors, which are converted to RGB color space. Implicit control points are generated such that the interpolator returns colors[0] at t = 0 and colors[colors.length - 1] at t = 1. Opacity interpolation is not currently supported. See also d3.interpolateBasis, and see d3-scale-chromatic for examples.

Examples · Source · Returns a uniform nonrational B-spline interpolator through the specified array of colors, which are converted to RGB color space. The control points are implicitly repeated such that the resulting spline has cyclical C² continuity when repeated around t in [0,1]; this is useful, for example, to create cyclical color scales. Opacity interpolation is not currently supported. See also d3.interpolateBasisClosed, and see d3-scale-chromatic for examples.

Examples · Source · Returns an HSL color space interpolator between the two colors a and b. The colors a and b need not be in HSL; they will be converted to HSL using d3.hsl. If either color’s hue or saturation is NaN, the opposing color’s channel value is used. The shortest path between hues is used. The return value of the interpolator is an RGB string.

Examples · Source · Like interpolateHsl, but does not use the shortest path between hues.

Examples · Source · Returns a CIELAB color space interpolator between the two colors a and b. The colors a and b need not be in CIELAB; they will be converted to CIELAB using d3.lab. The return value of the interpolator is an RGB string.

Examples · Source · Returns a CIELChab color space interpolator between the two colors a and b. The colors a and b need not be in CIELChab; they will be converted to CIELChab using d3.hcl. If either color’s hue or chroma is NaN, the opposing color’s channel value is used. The shortest path between hues is used. The return value of the interpolator is an RGB string.

Examples · Source · Like interpolateHcl, but does not use the shortest path between hues.

Examples · Source · Returns a Cubehelix color space interpolator between the two colors a and b using a configurable gamma. If the gamma is not specified, it defaults to 1.0. The colors a and b need not be in Cubehelix; they will be converted to Cubehelix using d3.cubehelix. If either color’s hue or saturation is NaN, the opposing color’s channel value is used. The shortest path between hues is used. The return value of the interpolator is an RGB string.

Examples · Source · Like interpolateCubehelix, but does not use the shortest path between hues.

Given that interpolate is one of interpolateRgb, interpolateCubehelix or interpolateCubehelixLong, returns a new interpolator factory of the same type using the specified gamma. See Eric Brasseur’s article, Gamma error in picture scaling, for more on gamma correction.

Examples · Source · Returns an interpolator between the two hue angles a and b. If either hue is NaN, the opposing value is used. The shortest path between hues is used. The return value of the interpolator is a number in [0, 360).

Whereas standard interpolators blend from a starting value a at t = 0 to an ending value b at t = 1, spline interpolators smoothly blend multiple input values for t in [0,1] using piecewise polynomial functions. Only cubic uniform nonrational B-splines are currently supported, also known as basis splines.

**Examples:**

Example 1 (unknown):
```unknown
d3.interpolateRgb("purple", "orange")
```

Example 2 (unknown):
```unknown
d3.interpolateRgbBasis(["purple", "green", "orange"])
```

Example 3 (unknown):
```unknown
d3.interpolateRgbBasisClosed(["purple", "green", "orange"])
```

Example 4 (unknown):
```unknown
d3.interpolateHsl("purple", "orange")
```

---
