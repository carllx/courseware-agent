# D3 - D3-Scale

**Pages:** 19

---

## Band scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/band

**Contents:**
- Band scales ​
- scaleBand(domain, range) ​
- band(value) ​
- band.domain(domain) ​
- band.range(range) ​
- band.rangeRound(range) ​
- band.round(round) ​
- band.paddingInner(padding) ​
- band.paddingOuter(padding) ​
- band.padding(padding) ​

Band scales are like ordinal scales except the output range is continuous and numeric. The scale divides the continuous range into uniform bands. Band scales are typically used for bar charts with an ordinal or categorical dimension.

Examples · Source · Constructs a new band scale with the specified domain and range, no padding, no rounding and center alignment.

If a single argument is specified, it is interpreted as the range. If domain is not specified, it defaults to the empty domain. If range is not specified, it defaults to the unit range [0, 1].

Examples · Source · Given a value in the input domain, returns the start of the corresponding band derived from the output range.

If the given value is not in the scale’s domain, returns undefined.

Examples · Source · If domain is specified, sets the domain to the specified array of values and returns this scale.

The first element in domain will be mapped to the first band, the second domain value to the second band, and so on. Domain values are stored internally in an InternMap from primitive value to index; the resulting index is then used to determine the band. Thus, a band scale’s values must be coercible to a primitive value, and the primitive domain value uniquely identifies the corresponding band. If domain is not specified, this method returns the current domain.

Examples · Source · If range is specified, sets the scale’s range to the specified two-element array of numbers and returns this scale.

If the elements in the given array are not numbers, they will be coerced to numbers. If range is not specified, returns the scale’s current range, which defaults to [0, 1].

Examples · Source · Sets the scale’s range to the specified two-element array of numbers while also enabling rounding; returns this scale.

This is a convenience method equivalent to:

Rounding is sometimes useful for avoiding antialiasing artifacts, though also consider the shape-rendering “crispEdges” styles.

Examples · Source · If round is specified, enables or disables rounding accordingly and returns this scale.

If round is not specified, returns whether rounding is enabled.

If rounding is enabled, the start and stop of each band will be integers. Rounding is sometimes useful for avoiding antialiasing artifacts, though also consider the shape-rendering “crispEdges” styles. Note that if the width of the domain is not a multiple of the cardinality of the range, there may be leftover unused space, even without padding! Use band.align to specify how the leftover space is distributed.

Examples · Source · If padding is specified, sets the inner padding to the specified number which must be less than or equal to 1 and returns this scale.

If padding is not specified, returns the current inner padding which defaults to 0.

The inner padding specifies the proportion of the range that is reserved for blank space between bands; a value of 0 means no blank space between bands, and a value of 1 means a bandwidth of zero.

Examples · Source · If padding is specified, sets the outer padding to the specified number which is typically in the range [0, 1] and returns this scale.

If padding is not specified, returns the current outer padding which defaults to 0.

The outer padding specifies the amount of blank space, in terms of multiples of the step, to reserve before the first band and after the last band.

Examples · Source · A convenience method for setting the inner and outer padding to the same padding value.

If padding is not specified, returns the inner padding.

Examples · Source · If align is specified, sets the alignment to the specified value which must be in the range [0, 1], and returns this scale.

If align is not specified, returns the current alignment which defaults to 0.5.

The alignment specifies how outer padding is distributed in the range. A value of 0.5 indicates that the outer padding should be equally distributed before the first band and after the last band; i.e., the bands should be centered within the range. A value of 0 or 1 may be used to shift the bands to one side, say to position them adjacent to an axis. For more, see this explainer.

Examples · Source · Returns the width of each band.

Examples · Source · Returns the distance between the starts of adjacent bands.

Examples · Source · Returns an exact copy of this scale.

Changes to this scale will not affect the returned scale, and vice versa.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scaleBand(["a", "b", "c"], [0, 960]);
```

Example 2 (javascript):
```javascript
const x = d3.scaleBand(["a", "b", "c"], [0, 960]);
x("a"); // 0
x("b"); // 320
x("c"); // 640
x("d"); // undefined
```

Example 3 (javascript):
```javascript
const x = d3.scaleBand([0, 960]).domain(["a", "b", "c", "d", "e", "f"]);
```

Example 4 (javascript):
```javascript
const x = d3.scaleBand().range([0, 960]);
```

---

## Time scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/time

**Contents:**
- Time scales ​
- scaleTime(domain, range) ​
- scaleUtc(domain, range) ​
- time.ticks(count) ​
- time.tickFormat(count, specifier) ​
- time.nice(count) ​

Time scales are a variant of linear scales that have a temporal domain: domain values are coerced to dates rather than numbers, and invert likewise returns a date. Time scales implement ticks based on calendar intervals, taking the pain out of generating axes for temporal domains.

Examples · Source · Constructs a new time scale with the specified domain and range, the default interpolator and clamping disabled. For example, to create a position encoding:

If domain is not specified, it defaults to [2000-01-01, 2000-01-02] in local time. If range is not specified, it defaults to [0, 1].

Examples · Source · Equivalent to scaleTime, but the returned time scale operates in Coordinated Universal Time rather than local time. For example, to create a position encoding:

If domain is not specified, it defaults to [2000-01-01, 2000-01-02] in UTC time. If range is not specified, it defaults to [0, 1].

A UTC scale should be preferred when possible as it behaves more predictably: days are always twenty-four hours and the scale does not depend on the browser’s time zone.

Examples · Source · Returns representative dates from the scale’s domain.

The returned tick values are uniformly-spaced (mostly), have sensible values (such as every day at midnight), and are guaranteed to be within the extent of the domain. Ticks are often used to display reference lines, or tick marks, in conjunction with the visualized data.

An optional count may be specified to affect how many ticks are generated. If count is not specified, it defaults to 10. The specified count is only a hint; the scale may return more or fewer values depending on the domain.

The following time intervals are considered for automatic ticks:

In lieu of a count, a time interval may be explicitly specified. To prune the generated ticks for a given time interval, use interval.every. For example, to generate ticks at 15-minute intervals:

Note: in some cases, such as with day ticks, specifying a step can result in irregular spacing of ticks because time intervals have varying length.

Examples · Source · Returns a time format function suitable for displaying tick values.

The specified count is currently ignored, but is accepted for consistency with other scales such as linear.tickFormat. If a format specifier is specified, this method is equivalent to format. If specifier is not specified, the default time format is returned. The default multi-scale time format chooses a human-readable representation based on the specified date as follows:

Although somewhat unusual, this default behavior has the benefit of providing both local and global context: for example, formatting a sequence of ticks as [11 PM, Mon 07, 01 AM] reveals information about hours, dates, and day simultaneously, rather than just the hours [11 PM, 12 AM, 01 AM]. See d3-time-format if you’d like to roll your own conditional time format.

Examples · Source · Extends the domain so that it starts and ends on nice round values.

This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. See linear.nice for more.

An optional tick count argument allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain. Alternatively, a time interval may be specified to explicitly set the ticks. If an interval is specified, an optional step may also be specified to skip some ticks. For example, time.nice(d3.utcSecond.every(10)) will extend the domain to an even ten seconds (0, 10, 20, etc.). See time.ticks and interval.every for further detail.

Nicing is useful if the domain is computed from data, say using extent, and may be irregular. For example, for a domain of [2009-07-13T00:02, 2009-07-13T23:48], the nice domain is [2009-07-13, 2009-07-14]. If the domain has more than two values, nicing the domain only affects the first and last value.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scaleTime([new Date(2000, 0, 1), new Date(2000, 0, 2)], [0, 960]);
x(new Date(2000, 0, 1, 5)); // 200
x(new Date(2000, 0, 1, 16)); // 640
x.invert(200); // Sat Jan 01 2000 05:00:00 GMT-0800 (PST)
x.invert(640); // Sat Jan 01 2000 16:00:00 GMT-0800 (PST)
```

Example 2 (javascript):
```javascript
const x = d3.scaleUtc([new Date("2000-01-01"), new Date("2000-01-02")], [0, 960]);
x(new Date("2000-01-01T05:00Z")); // 200
x(new Date("2000-01-01T16:00Z")); // 640
x.invert(200); // 2000-01-01T05:00Z
x.invert(640); // 2000-01-01T16:00Z
```

Example 3 (javascript):
```javascript
const x = d3.scaleTime();
x.ticks(10);
// [Sat Jan 01 2000 00:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 03:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 06:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 09:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 12:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 15:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 18:00:00 GMT-0800 (PST),
//  Sat Jan 01 2000 21:00:00 GMT-0800 (PST),
//  Sun Jan 02 2000 00:00:00 GMT-0800 (PST)]
```

Example 4 (javascript):
```javascript
const x = d3.scaleUtc().domain([new Date("2000-01-01T00:00Z"), new Date("2000-01-01T02:00Z")]);
x.ticks(d3.utcMinute.every(15));
// [2000-01-01T00:00Z,
//  2000-01-01T00:15Z,
//  2000-01-01T00:30Z,
//  2000-01-01T00:45Z,
//  2000-01-01T01:00Z,
//  2000-01-01T01:15Z,
//  2000-01-01T01:30Z,
//  2000-01-01T01:45Z,
//  2000-01-01T02:00Z]
```

---

## Quantize scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/quantize

**Contents:**
- Quantize scales ​
- scaleQuantize(domain, range) ​
- quantize(value) ​
- quantize.invertExtent(value) ​
- quantize.domain(domain) ​
- quantize.range(range) ​
- quantize.thresholds() ​
- quantize.copy() ​

Quantize scales are similar to linear scales, except they use a discrete rather than continuous range. The continuous input domain is divided into uniform segments based on the number of values in (i.e., the cardinality of) the output range. Each range value y can be expressed as a quantized linear function of the domain value x: y = m round(x) + b. See the quantized choropleth for an example.

Examples · Source · Constructs a new quantize scale with the specified domain and range.

If either domain or range is not specified, each defaults to [0, 1].

Examples · Source · Given a value in the input domain, returns the corresponding value in the output range. For example, to apply a color encoding:

Or dividing the domain into three equally-sized parts with different range values to compute an appropriate stroke width:

Examples · Source · Returns the extent of values in the domain [x0, x1] for the corresponding value in the range: the inverse of quantize. This method is useful for interaction, say to determine the value in the domain that corresponds to the pixel location under the mouse.

Examples · Source · If domain is specified, sets the scale’s domain to the specified two-element array of numbers.

If the elements in the given array are not numbers, they will be coerced to numbers. The numbers must be in ascending order or the behavior of the scale is undefined.

If domain is not specified, returns the scale’s current domain.

Examples · Source · If range is specified, sets the scale’s range to the specified array of values.

The array may contain any number of discrete values. The elements in the given array need not be numbers; any value or type will work.

If range is not specified, returns the scale’s current range.

Examples · Source · Returns the array of computed thresholds within the domain.

The number of returned thresholds is one less than the length of the range: values less than the first threshold are assigned the first element in the range, whereas values greater than or equal to the last threshold are assigned the last element in the range.

Examples · Source · Returns an exact copy of this scale.

Changes to this scale will not affect the returned scale, and vice versa.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleQuantize([0, 100], d3.schemeBlues[9]);
```

Example 2 (javascript):
```javascript
const color = d3.scaleQuantize(d3.schemeBlues[9]);
```

Example 3 (javascript):
```javascript
const color = d3.scaleQuantize([0, 1], ["brown", "steelblue"]);
color(0.49); // "brown"
color(0.51); // "steelblue"
```

Example 4 (javascript):
```javascript
const width = d3.scaleQuantize([10, 100], [1, 2, 4]);
width(20); // 1
width(50); // 2
width(80); // 4
```

---

## Sequential scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/sequential

**Contents:**
- Sequential scales ​
- scaleSequential(domain, interpolator) ​
- sequential.interpolator(interpolator) ​
- sequential.range(range) ​
- sequential.rangeRound(range) ​
- scaleSequentialLog(domain, range) ​
- scaleSequentialPow(domain, range) ​
- scaleSequentialSqrt(domain, range) ​
- scaleSequentialSymlog(domain, range) ​
- scaleSequentialQuantile(domain, range) ​

Sequential scales are similar to linear scales in that they map a continuous, numeric input domain to a continuous output range. Unlike linear scales, the input domain and output range of a sequential scale always have exactly two elements, and the output range is typically specified as an interpolator rather than an array of values. Sequential scales are typically used for a color encoding; see also d3-scale-chromatic. These scales do not expose invert and interpolate methods. There are also log, pow, symlog, and quantile variants of sequential scales.

Examples · Source · Constructs a new sequential scale with the specified domain and interpolator function or array.

If domain is not specified, it defaults to [0, 1].

If interpolator is not specified, it defaults to the identity function.

When the scale is applied, the interpolator will be invoked with a value typically in the range [0, 1], where 0 represents the minimum value and 1 represents the maximum value. For example, to implement the ill-advised angry rainbow scale (please use interpolateRainbow instead):

If interpolator is an array, it represents the scale’s two-element output range and is converted to an interpolator function using interpolate.

A sequential scale’s domain must be numeric and must contain exactly two values.

If interpolator is specified, sets the scale’s interpolator to the specified function.

If interpolator is not specified, returns the scale’s current interpolator.

See linear.range. If range is specified, the given two-element array is converted to an interpolator function using interpolate.

The above is equivalent to:

See linear.rangeRound. If range is specified, implicitly uses interpolateRound as the interpolator.

Returns a new sequential scale with a logarithmic transform, analogous to a log scale.

Returns a new sequential scale with an exponential transform, analogous to a power scale.

Returns a new sequential scale with a square-root transform, analogous to a sqrt scale.

Returns a new sequential scale with a symmetric logarithmic transform, analogous to a symlog scale.

Source · Returns a new sequential scale with a p-quantile transform, analogous to a quantile scale.

Source · Returns an array of n + 1 quantiles.

For example, if n = 4, returns an array of five numbers: the minimum value, the first quartile, the median, the third quartile, and the maximum.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleSequential([0, 100], d3.interpolateBlues);
```

Example 2 (javascript):
```javascript
const color = d3.scaleSequential(d3.interpolateBlues);
```

Example 3 (javascript):
```javascript
const identity = d3.scaleSequential();
```

Example 4 (javascript):
```javascript
const rainbow = d3.scaleSequential((t) => d3.hsl(t * 360, 1, 0.5) + "");
```

---

## Threshold scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/threshold

**Contents:**
- Threshold scales ​
- scaleThreshold(domain, range) ​
- threshold(value) ​
- threshold.invertExtent(value) ​
- threshold.domain(domain) ​
- threshold.range(range) ​
- threshold.copy() ​

Threshold scales are similar to quantize scales, except they allow you to map arbitrary subsets of the domain to discrete values in the range. The input domain is still continuous, and divided into slices based on a set of threshold values. See this choropleth for an example.

Examples · Source · Constructs a new threshold scale with the specified domain and range.

If domain is not specified, it defaults to [0.5].

If range is not specified, it defaults to [0, 1].

Examples · Source · Given a value in the input domain, returns the corresponding value in the output range. For example:

Source · Returns the extent of values in the domain [x0, x1] for the corresponding value in the range, representing the inverse mapping from range to domain.

This method is useful for interaction, say to determine the value in the domain that corresponds to the pixel location under the mouse. The extent below the lowest threshold is undefined (unbounded), as is the extent above the highest threshold.

Examples · Source · If domain is specified, sets the scale’s domain to the specified array of values.

The values must be in ascending order or the behavior of the scale is undefined. The values are typically numbers, but any naturally ordered values (such as strings) will work; a threshold scale can be used to encode any type that is ordered. If the number of values in the scale’s range is n + 1, the number of values in the scale’s domain must be n. If there are fewer than n elements in the domain, the additional values in the range are ignored. If there are more than n elements in the domain, the scale may return undefined for some inputs.

If domain is not specified, returns the scale’s current domain.

Examples · Source · If range is specified, sets the scale’s range to the specified array of values.

If the number of values in the scale’s domain is n, the number of values in the scale’s range must be n + 1. If there are fewer than n + 1 elements in the range, the scale may return undefined for some inputs. If there are more than n + 1 elements in the range, the additional values are ignored. The elements in the given array need not be numbers; any value or type will work.

If range is not specified, returns the scale’s current range.

Examples · Source · Returns an exact copy of this scale.

Changes to this scale will not affect the returned scale, and vice versa.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleThreshold([0, 1], ["red", "white", "blue"]);
```

Example 2 (javascript):
```javascript
const color = d3.scaleThreshold(["red", "blue"]);
color(0); // "red"
color(1); // "blue"
```

Example 3 (javascript):
```javascript
const color = d3.scaleThreshold([0, 1], ["red", "white", "green"]);
color(-1); // "red"
color(0); // "white"
color(0.5); // "white"
color(1); // "green"
color(1000); // "green"
```

Example 4 (javascript):
```javascript
const color = d3.scaleThreshold([0, 1], ["red", "white", "green"]);
color.invertExtent("red"); // [undefined, 0]
color.invertExtent("white"); // [0, 1]
color.invertExtent("green"); // [1, undefined]
```

---

## Power scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/pow

**Contents:**
- Power scales ​
  - scalePow(domain, range) ​
  - scaleSqrt(domain, range) ​
  - pow.exponent(exponent) ​

Power (“pow”) scales are similar to linear scales, except an exponential transform is applied to the input domain value before the output range value is computed. Each range value y can be expressed as a function of the domain value x: y = mx^k + b, where k is the exponent value. Power scales also support negative domain values, in which case the input value and the resulting output value are multiplied by -1.

Examples · Source · Constructs a new pow scale with the specified domain and range, the exponent 1, the default interpolator and clamping disabled.

If either domain or range are not specified, each defaults to [0, 1].

Examples · Source · Constructs a new pow scale with the specified domain and range, the exponent 0.5, the default interpolator and clamping disabled.

If either domain or range are not specified, each defaults to [0, 1]. This is a convenience method equivalent to d3.scalePow(…).exponent(0.5).

Examples · Source · If exponent is specified, sets the current exponent to the given numeric value and returns this scale.

If exponent is not specified, returns the current exponent, which defaults to 1.

If the exponent is 1, the pow scale is effectively a linear scale.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scalePow([0, 100], ["red", "blue"]).exponent(2);
```

Example 2 (javascript):
```javascript
const x = d3.scaleSqrt([0, 100], ["red", "blue"]);
```

Example 3 (javascript):
```javascript
const x = d3.scalePow([0, 100], ["red", "blue"]).exponent(2);
```

Example 4 (unknown):
```unknown
x.exponent() // 2
```

---

## Quantile scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/quantile

**Contents:**
- Quantile scales ​
- scaleQuantile(domain, range) ​
- quantile(value) ​
- quantile.invertExtent(value) ​
- quantile.domain(domain) ​
- quantile.range(range) ​
- quantile.quantiles() ​
- quantile.copy() ​

Quantile scales map a sampled input domain to a discrete range. The domain is considered continuous and thus the scale will accept any reasonable input value; however, the domain is specified as a discrete set of sample values. The number of values in (the cardinality of) the output range determines the number of quantiles that will be computed from the domain. To compute the quantiles, the domain is sorted, and treated as a population of discrete values; see quantile. See this quantile choropleth for an example.

Examples · Source · Constructs a new quantile scale with the specified domain and range.

If either domain or range is not specified, each defaults to the empty array. The quantile scale is invalid until both a domain and range are specified.

Examples · Source · Given a value in the input domain, returns the corresponding value in the output range.

Examples · Source · Returns the extent of values in the domain [x0, x1] for the corresponding value in the range: the inverse of quantile.

This method is useful for interaction, say to determine the value in the domain that corresponds to the pixel location under the mouse.

Examples · Source · If domain is specified, sets the domain of the quantile scale to the specified set of discrete numeric values and returns this scale.

The array must not be empty, and must contain at least one numeric value; NaN, null and undefined values are ignored and not considered part of the sample population. If the elements in the given array are not numbers, they will be coerced to numbers. A copy of the input array is sorted and stored internally.

If domain is not specified, returns the scale’s current domain (the set of observed values).

Examples · Source · If range is specified, sets the discrete values in the range.

The array must not be empty, and may contain any type of value. The number of values in (the cardinality, or length, of) the range array determines the number of quantiles that are computed. For example, to compute quartiles, range must be an array of four elements such as [0, 1, 2, 3].

If range is not specified, returns the current range.

Examples · Source · Returns the quantile thresholds.

If the range contains n discrete values, the returned array will contain n - 1 thresholds. Values less than the first threshold are considered in the first quantile; values greater than or equal to the first threshold but less than the second threshold are in the second quantile, and so on. Internally, the thresholds array is used with bisect to find the output quantile associated with the given input value.

Examples · Source · Returns an exact copy of this scale.

Changes to this scale will not affect the returned scale, and vice versa.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleQuantile(penguins.map((d) => d.body_mass_g), d3.schemeBlues[5]);
```

Example 2 (unknown):
```unknown
color(3000); // "#eff3ff"
color(4000); // "#6baed6"
color(5000); // "#08519c"
```

Example 3 (unknown):
```unknown
color.invertExtent("#eff3ff"); // [2700, 3475]
color.invertExtent("#6baed6"); // [3800, 4300]
color.invertExtent("#08519c"); // [4950, 6300]
```

Example 4 (javascript):
```javascript
const color = d3.scaleQuantile(d3.schemeBlues[5]);
color.domain(penguins.map((d) => d.body_mass_g));
```

---

## Linear scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/linear

**Contents:**
- Linear scales ​
- scaleLinear(domain, range) ​
- linear(value) ​
- linear.invert(value) ​
- linear.domain(domain) ​
- linear.range(range) ​
- linear.rangeRound(range) ​
- linear.clamp(clamp) ​
- linear.unknown(value) ​
- linear.interpolate(interpolate) ​

Linear scales map a continuous, quantitative input domain to a continuous output range using a linear transformation (translate and scale). If the range is also numeric, the mapping may be inverted. Linear scales are a good default choice for continuous quantitative data because they preserve proportional differences. Each range value y can be expressed as a function of the domain value x: y = mx + b.

Examples · Source · Constructs a new linear scale with the specified domain and range, the default interpolator, and clamping disabled.

If a single argument is specified, it is interpreted as the range. If either domain or range are not specified, each defaults to [0, 1].

Examples · Source · Given a value from the domain, returns the corresponding value from the range. For example, to apply a position encoding:

To apply a color encoding:

If the given value is outside the domain, and clamping is not enabled, the mapping will be extrapolated such that the returned value is outside the range.

Examples · Source · Given a value from the range, returns the corresponding value from the domain. Inversion is useful for interaction, say to determine the data value corresponding to the position of the mouse. For example, to invert a position encoding:

If the given value is outside the range, and clamping is not enabled, the mapping may be extrapolated such that the returned value is outside the domain. This method is only supported if the range is numeric. If the range is not numeric, returns NaN.

For a valid value y in the range, linear(linear.invert(y)) approximately equals y; similarly, for a valid value x in the domain, linear.invert(linear(x)) approximately equals x. The scale and its inverse may not be exact due to the limitations of floating point precision.

Examples · Source · If domain is specified, sets the scale’s domain to the specified array of numbers and returns this scale.

The array must contain two or more elements. If the elements in the given array are not numbers, they will be coerced to numbers.

Although continuous scales typically have two values each in their domain and range, specifying more than two values produces a piecewise scale. For example, to create a diverging color scale that interpolates between white and red for negative values, and white and green for positive values, say:

Internally, a piecewise scale performs a binary search for the range interpolator corresponding to the given domain value. Thus, the domain must be in ascending or descending order. If the domain and range have different lengths N and M, only the first min(N,M) elements in each are observed.

If domain is not specified, returns a copy of the scale’s current domain.

Examples · Source · If range is specified, sets the scale’s range to the specified array of values and returns this scale.

The array must contain two or more elements. Unlike the domain, elements in the given array need not be numbers; any value that is supported by the underlying interpolator will work, though note that numeric ranges are required for invert.

If range is not specified, returns a copy of the scale’s current range.

See linear.interpolate for more examples.

Examples · Source · Sets the scale’s range to the specified array of values while also setting the scale’s interpolator to interpolateRound; returns this scale.

This is a convenience method equivalent to:

The rounding interpolator is sometimes useful for avoiding antialiasing artifacts, though also consider the shape-rendering “crispEdges” styles. Note that this interpolator can only be used with numeric ranges.

Examples · Source · If clamp is specified, enables or disables clamping accordingly; returns this scale.

If clamping is disabled and the scale is passed a value outside the domain, the scale may return a value outside the range through extrapolation. If clamping is enabled, the return value of the scale is always within the scale’s range. Clamping similarly applies to linear.invert. For example:

If clamp is not specified, returns whether or not the scale currently clamps values to within the range.

Examples · Source · If value is specified, sets the output value of the scale for undefined or NaN input values and returns this scale. This is useful for specifying how missing or invalid data is displayed.

If value is not specified, returns the current unknown value, which defaults to undefined.

Examples · Source · If interpolate is specified, sets the scale’s range interpolator factory.

The scale’s interpolator factory is used to create interpolators for each adjacent pair of values from the range; these interpolators then map a normalized domain parameter t in [0, 1] to the corresponding value in the range. If factory is not specified, returns the scale’s current interpolator factory, which defaults to d3.interpolate. See d3-interpolate for more interpolators.

For example, consider a diverging color scale with three colors in the range:

Two interpolators are created internally by the scale, equivalent to:

A common reason to specify a custom interpolator is to change the color space of interpolation. For example, to use HCL:

Or for Cubehelix with a custom gamma:

The default interpolator may reuse return values. For example, if the range values are objects, then the value interpolator always returns the same object, modifying it in-place. If the scale is used to set an attribute or style, this is typically acceptable (and desirable for performance); however, if you need to store the scale’s return value, you must specify your own interpolator or make a copy as appropriate.

Examples · Source · Returns approximately count representative values from the scale’s domain.

If count is not specified, it defaults to 10. The returned tick values are uniformly spaced, have human-readable values (such as multiples of powers of 10), and are guaranteed to be within the extent of the domain. Ticks are often used to display reference lines, or tick marks, in conjunction with the visualized data. The specified count is only a hint; the scale may return more or fewer values depending on the domain. See also d3-array’s ticks.

Examples · Source · Returns a number format function suitable for displaying a tick value, automatically computing the appropriate precision based on the fixed interval between tick values. The specified count should have the same value as the count that is used to generate the tick values.

An optional specifier allows a custom format where the precision of the format is automatically set by the scale as appropriate for the tick interval. For example, to format percentage change, you might say:

If specifier uses the format type s, the scale will return a SI-prefix format based on the largest value in the domain. If the specifier already specifies a precision, this method is equivalent to locale.format.

See also d3.tickFormat.

Examples · Source · Extends the domain so that it starts and ends on nice round values.

This method typically modifies the scale’s domain, and may only extend the bounds to the nearest round value. Nicing is useful if the domain is computed from data, say using extent, and may be irregular. If the domain has more than two values, nicing the domain only affects the first and last value.

An optional tick count argument allows greater control over the step size used to extend the bounds, guaranteeing that the returned ticks will exactly cover the domain.

Nicing a scale only modifies the current domain; it does not automatically nice domains that are subsequently set using linear.domain. You must re-nice the scale after setting the new domain, if desired.

Examples · Source · Returns an exact copy of this scale.

Changes to this scale will not affect the returned scale, and vice versa.

Examples · Source · Returns a number format function suitable for displaying a tick value, automatically computing the appropriate precision based on the fixed interval between tick values, as determined by d3.tickStep.

An optional specifier allows a custom format where the precision of the format is automatically set by the scale as appropriate for the tick interval. For example, to format percentage change, you might say:

If specifier uses the format type s, the scale will return a SI-prefix format based on the larger absolute value of start and stop. If the specifier already specifies a precision, this method is equivalent to locale.format.

Examples · Source · Constructs a new identity scale with the specified range (and by extension, domain).

Identity scales are a special case of linear scales where the domain and range are identical; the scale and its invert method are thus the identity function. These scales are occasionally useful when working with pixel coordinates, say in conjunction with an axis. Identity scales do not support rangeRound, clamp or interpolate.

If range is not specified, it defaults to [0, 1].

Examples · Source · Constructs a new radial scale with the specified domain and range.

Radial scales are a variant of linear scales where the range is internally squared so that an input value corresponds linearly to the squared output value. These scales are useful when you want the input value to correspond to the area of a graphical mark and the mark is specified by radius, as in a radial bar chart. Radial scales do not support interpolate.

If domain or range is not specified, each defaults to [0, 1].

**Examples:**

Example 1 (unknown):
```unknown
d3.scaleLinear([0, 100], ["red", "blue"])
```

Example 2 (unknown):
```unknown
d3.scaleLinear(["red", "blue"]) // default domain of [0, 1]
```

Example 3 (javascript):
```javascript
const x = d3.scaleLinear([10, 130], [0, 960]);
x(20); // 80
x(50); // 320
```

Example 4 (javascript):
```javascript
const color = d3.scaleLinear([10, 100], ["brown", "steelblue"]);
color(20); // "rgb(154, 52, 57)"
color(50); // "rgb(123, 81, 103)"
```

---

## Symlog scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/symlog

**Contents:**
- Symlog scales ​
- scaleSymlog(domain, range) ​
- symlog.constant(constant) ​

See A bi-symmetric log transformation for wide-range data by Webber for details. Unlike a log scale, a symlog scale domain can include zero.

Examples · Source · Constructs a new continuous scale with the specified domain and range, the constant 1, the default interpolator and clamping disabled.

If a single argument is specified, it is interpreted as the range. If either domain or range are not specified, each defaults to [0, 1].

Examples · Source · If constant is specified, sets the symlog constant to the specified number and returns this scale. The constant defaults to 1.

If constant is not specified, returns the current value of the symlog constant.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scaleSymlog([0, 100], [0, 960]);
```

Example 2 (javascript):
```javascript
const color = d3.scaleSymlog(["red", "blue"]) // default domain of [0, 1]
```

Example 3 (javascript):
```javascript
const x = d3.scaleSymlog([0, 100], [0, 960]).constant(2);
```

Example 4 (unknown):
```unknown
x.constant() // 2
```

---

## Ordinal scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/ordinal

**Contents:**
- Ordinal scales ​
- scaleOrdinal(domain, range) ​
- ordinal(value) ​
- ordinal.domain(domain) ​
- ordinal.range(range) ​
- ordinal.unknown(value) ​
- ordinal.copy() ​
- scaleImplicit ​

Unlike continuous scales, ordinal scales have a discrete domain and range. For example, an ordinal scale might map a set of named categories to a set of colors, or determine the horizontal positions of columns in a column chart.

Examples · Source · Constructs a new ordinal scale with the specified domain and range.

If domain is not specified, it defaults to the empty array. If range is not specified, it defaults to the empty array; an ordinal scale always returns undefined until a non-empty range is defined.

Examples · Source · Given a value in the input domain, returns the corresponding value in the output range.

If the given value is not in the scale’s domain, returns the unknown value; or, if the unknown value is implicit (the default), then the value is implicitly added to the domain and the next-available value in the range is assigned to value, such that this and subsequent invocations of the scale given the same input value return the same output value.

Examples · Source · If domain is specified, sets the domain to the specified array of values.

The first element in domain will be mapped to the first element in the range, the second domain value to the second range value, and so on. Domain values are stored internally in an InternMap from primitive value to index; the resulting index is then used to retrieve a value from the range. Thus, an ordinal scale’s values must be coercible to a primitive value, and the primitive domain value uniquely identifies the corresponding range value.

If domain is not specified, this method returns the current domain.

Setting the domain on an ordinal scale is optional if the unknown value is implicit (the default). In this case, the domain will be inferred implicitly from usage by assigning each unique value passed to the scale a new value from the range.

An explicit domain is recommended for deterministic behavior; inferring the domain from usage is dependent on ordering.

Examples · Source · If range is specified, sets the range of the ordinal scale to the specified array of values.

The first element in the domain will be mapped to the first element in range, the second domain value to the second range value, and so on. If there are fewer elements in the range than in the domain, the scale will reuse values from the start of the range. If range is not specified, this method returns the current range.

Examples · Source · If value is specified, sets the output value of the scale for unknown input values and returns this scale.

If value is not specified, returns the current unknown value, which defaults to implicit. The implicit value enables implicit domain construction; see ordinal.domain.

Examples · Source · Returns an exact copy of this ordinal scale.

Changes to this scale will not affect the returned scale, and vice versa.

Examples · Source · A special value for ordinal.unknown that enables implicit domain construction: unknown values are implicitly added to the domain.

An explicit domain is recommended for deterministic behavior; inferring the domain from usage is dependent on ordering.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleOrdinal(["a", "b", "c"], ["red", "green", "blue"]);
```

Example 2 (unknown):
```unknown
color("a") // "red"
```

Example 3 (javascript):
```javascript
const color = d3.scaleOrdinal(["red", "green", "blue"]).domain(["a", "b", "c"]);
color("a"); // "red"
color("b"); // "green"
color("c"); // "blue"
```

Example 4 (unknown):
```unknown
color.domain() // ["a", "b", "c"]
```

---

## Logarithmic scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/log

**Contents:**
- Logarithmic scales ​
- scaleLog(domain, range) ​
- log.base(base) ​
- log.ticks(count) ​
- log.tickFormat(count, specifier) ​
- log.nice() ​

Logarithmic (“log”) scales are like linear scales except that a logarithmic transform is applied to the input domain value before the output range value is computed. The mapping to the range value y can be expressed as a function of the domain value x: y = m log(x) + b.

As log(0) = -∞, a log scale domain must be strictly-positive or strictly-negative; the domain must not include or cross zero. A log scale with a positive domain has a well-defined behavior for positive values, and a log scale with a negative domain has a well-defined behavior for negative values. (For a negative domain, input and output values are implicitly multiplied by -1.) The behavior of the scale is undefined if you pass a negative value to a log scale with a positive domain or vice versa.

Examples · Source · Constructs a new log scale with the specified domain and range, the base 10, the default interpolator and clamping disabled.

If domain is not specified, it defaults to [1, 10]. If range is not specified, it defaults to [0, 1].

Examples · Source · If base is specified, sets the base for this logarithmic scale to the specified value.

If base is not specified, returns the current base, which defaults to 10. Note that due to the nature of a logarithmic transform, the base does not affect the encoding of the scale; it only affects which ticks are chosen.

Examples · Source · Like linear.ticks, but customized for a log scale.

If the base is an integer, the returned ticks are uniformly spaced within each integer power of base; otherwise, one tick per power of base is returned. The returned ticks are guaranteed to be within the extent of the domain. If the orders of magnitude in the domain is greater than count, then at most one tick per power is returned. Otherwise, the tick values are unfiltered, but note that you can use log.tickFormat to filter the display of tick labels. If count is not specified, it defaults to 10.

Examples · Source · Like linear.tickFormat, but customized for a log scale. The specified count typically has the same value as the count that is used to generate the tick values.

If there are too many ticks, the formatter may return the empty string for some of the tick labels; however, note that the ticks are still shown to convey the logarithmic transform accurately. To disable filtering, specify a count of Infinity.

When specifying a count, you may also provide a format specifier or format function. For example, to get a tick formatter that will display 20 ticks of a currency, say log.tickFormat(20, "$,f"). If the specifier does not have a defined precision, the precision will be set automatically by the scale, returning the appropriate format. This provides a convenient way of specifying a format whose precision will be automatically set by the scale.

Examples · Source · Like linear.nice, except extends the domain to integer powers of base.

If the domain has more than two values, nicing the domain only affects the first and last value. Nicing a scale only modifies the current domain; it does not automatically nice domains that are subsequently set using log.domain. You must re-nice the scale after setting the new domain, if desired.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scaleLog([1, 10], [0, 960]);
```

Example 2 (javascript):
```javascript
const x = d3.scaleLog([1, 1024], [0, 960]).base(2);
```

Example 3 (javascript):
```javascript
const x = d3.scaleLog([1, 100], [0, 960]);
const T = x.ticks(); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
```

Example 4 (javascript):
```javascript
const x = d3.scaleLog([1, 100], [0, 960]);
const T = x.ticks(); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, …]
const f = x.tickFormat();
T.map(f); // ["1", "2", "3", "4", "5", "", "", "", "", "10", …]
```

---

## d3-scale | D3 by Observable

**URL:** https://d3js.org/d3-scale

**Contents:**
- d3-scale ​

Scales map a dimension of abstract data to a visual representation. Although most often used for encoding data as position, say to map time and temperature to a horizontal and vertical position in a scatterplot, scales can represent virtually any visual encoding, such as color, stroke width, or symbol size. Scales can also be used with virtually any type of data, such as named categorical data or discrete data that requires sensible breaks.

For visualizing the scale’s encoding, see d3-axis, as well as scale.ticks and scale.tickFormat. For color schemes, see d3-scale-chromatic.

---

## Point scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/point

**Contents:**
- Point scales ​
- scalePoint(domain, range) ​
- point(value) ​
- point.domain(domain) ​
- point.range(range) ​
- point.rangeRound(range) ​
- point.round(round) ​
- point.padding(padding) ​
- point.align(align) ​
- point.bandwidth() ​

Point scales are a variant of band scales with the bandwidth fixed to zero. Point scales are typically used for scatterplots with an ordinal or categorical dimension.

Examples · Source · Constructs a new point scale with the specified domain and range, no padding, no rounding and center alignment. If domain is not specified, it defaults to the empty domain. If range is not specified, it defaults to the unit range [0, 1].

Examples · Source · Given a value in the input domain, returns the corresponding point derived from the output range.

If the given value is not in the scale’s domain, returns undefined.

Examples · Source · If domain is specified, sets the domain to the specified array of values.

The first element in domain will be mapped to the first point, the second domain value to the second point, and so on. Domain values are stored internally in an InternMap from primitive value to index; the resulting index is then used to determine the point. Thus, a point scale’s values must be coercible to a primitive value, and the primitive domain value uniquely identifies the corresponding point. If domain is not specified, this method returns the current domain.

Examples · Source · If range is specified, sets the scale’s range to the specified two-element array of numbers and returns this scale.

If the elements in the given array are not numbers, they will be coerced to numbers. If range is not specified, returns the scale’s current range, which defaults to [0, 1].

Examples · Source · Sets the scale’s range to the specified two-element array of numbers while also enabling rounding; returns this scale.

This is a convenience method equivalent to:

Rounding is sometimes useful for avoiding antialiasing artifacts, though also consider the shape-rendering “crispEdges” styles.

Examples · Source · If round is specified, enables or disables rounding accordingly.

If round is not specified, returns whether rounding is enabled.

If rounding is enabled, the position of each point will be integers. Rounding is sometimes useful for avoiding antialiasing artifacts, though also consider the shape-rendering “crispEdges” styles. Note that if the width of the domain is not a multiple of the cardinality of the range, there may be leftover unused space, even without padding! Use point.align to specify how the leftover space is distributed.

Examples · Source · If padding is specified, sets the outer padding to the specified number which is typically in the range [0, 1].

If padding is not specified, returns the current outer padding which defaults to 0.

The outer padding specifies the amount of blank space, in terms of multiples of the step, to reserve before the first point and after the last point. Equivalent to band.paddingOuter.

Examples · Source · If align is specified, sets the alignment to the specified value which must be in the range [0, 1].

If align is not specified, returns the current alignment which defaults to 0.5.

The alignment specifies how any leftover unused space in the range is distributed. A value of 0.5 indicates that the leftover space should be equally distributed before the first point and after the last point; i.e., the points should be centered within the range. A value of 0 or 1 may be used to shift the points to one side, say to position them adjacent to an axis.

Examples · Source · Returns zero.

Examples · Source · Returns the distance between adjacent points.

Examples · Source · Returns an exact copy of this scale. Changes to this scale will not affect the returned scale, and vice versa.

**Examples:**

Example 1 (javascript):
```javascript
const x = d3.scalePoint(["a", "b", "c"], [0, 960]);
x("a"); // 0
x("b"); // 480
x("c"); // 960
x("d"); // undefined
```

Example 2 (javascript):
```javascript
const x = d3.scalePoint([0, 960]).domain(["a", "b", "c", "d", "e", "f"]);
```

Example 3 (javascript):
```javascript
const x = d3.scalePoint().range([0, 960]);
```

Example 4 (javascript):
```javascript
const x = d3.scalePoint().rangeRound([0, 960]);
```

---

## Diverging scales | D3 by Observable

**URL:** https://d3js.org/d3-scale/diverging

**Contents:**
- Diverging scales ​
- scaleDiverging(domain, interpolator) ​
- diverging.interpolator(interpolator) ​
- diverging.range(range) ​
- diverging.rangeRound(range) ​
- scaleDivergingLog(domain, range) ​
- scaleDivergingPow(domain, range) ​
- scaleDivergingSqrt(domain, range) ​
- scaleDivergingSymlog(domain, range) ​

Diverging scales are similar to linear scales in that they map a continuous, numeric input domain to a continuous output range. Unlike linear scales, the input domain and output range of a diverging scale always have exactly three elements, and the output range is typically specified as an interpolator rather than an array of values. Diverging scales are typically used for a color encoding; see also d3-scale-chromatic. These scales do not expose invert and interpolate methods. There are also log, pow, and symlog variants of diverging scales.

Examples · Source · Constructs a new diverging scale with the specified domain and interpolator function or array.

If domain is not specified, it defaults to [0, 0.5, 1].

If interpolator is not specified, it defaults to the identity function.

When the scale is applied, the interpolator will be invoked with a value typically in the range [0, 1], where 0 represents the extreme negative value, 0.5 represents the neutral value, and 1 represents the extreme positive value.

If interpolator is an array, it represents the scale’s three-element output range and is converted to an interpolator function using d3.interpolate and d3.piecewise.

A diverging scale’s domain must be numeric and must contain exactly three values.

If interpolator is specified, sets the scale’s interpolator to the specified function.

If interpolator is not specified, returns the scale’s current interpolator.

See linear.range. If range is specified, the given three-element array is converted to an interpolator function using piecewise.

The above is equivalent to:

See linear.range. If range is specified, implicitly uses interpolateRound as the interpolator.

Returns a new diverging scale with a logarithmic transform, analogous to a log scale.

Returns a new diverging scale with an exponential transform, analogous to a power scale.

Returns a new diverging scale with a square-root transform, analogous to a sqrt scale.

Returns a new diverging scale with a symmetric logarithmic transform, analogous to a symlog scale.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleDiverging([-1, 0, 1], d3.interpolateRdBu);
```

Example 2 (javascript):
```javascript
const color = d3.scaleDiverging(d3.interpolateRdBu);
```

Example 3 (javascript):
```javascript
const identity = d3.scaleDiverging();
```

Example 4 (javascript):
```javascript
const color = d3.scaleDiverging(["blue", "white", "red"]);
```

---
