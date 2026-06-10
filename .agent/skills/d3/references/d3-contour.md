## Contour polygons | D3 by Observable

**URL:** https://d3js.org/d3-contour/contour

**Contents:**
- Contour polygons ​
- contours() ​
- contours(values) ​
- contours.contour(values, threshold) ​
- contours.size(size) ​
- contours.smooth(smooth) ​
- contours.thresholds(thresholds) ​

For each threshold value, the contour generator constructs a GeoJSON MultiPolygon geometry object representing the area where the input values are greater than or equal to the threshold value. The geometry is in planar coordinates, where ⟨i + 0.5, j + 0.5⟩ corresponds to element i + jn in the input values array.

Here is an example that loads a GeoTIFF of surface temperatures, and another that blurs a noisy monochrome PNG to produce smooth contours of cloud fraction:

Since the contour polygons are GeoJSON, you can transform and display them using standard tools; see geoPath, geoProject and geoStitch, for example. Here the above contours of surface temperature are displayed in the Natural Earth projection:

Contour plots can also visualize continuous functions by sampling. Here is the Goldstein–Price function (a test function for global optimization) and a trippy animation of sin(x + y)sin(x - y):

Examples · Source · Constructs a new contour generator with the default settings.

Source · Computes the contours for the given array of values, returning an array of GeoJSON MultiPolygon geometry objects.

Each geometry object represents the area where the input values are greater than or equal to the corresponding threshold value; the threshold value for each geometry object is exposed as geometry.value.

The input values must be an array of length n×m where [n, m] is the contour generator’s size; furthermore, each values[i + jn] must represent the value at the position ⟨i, j⟩. For example, to construct a 256×256 grid for the Goldstein–Price function where -2 ≤ x ≤ 2 and -2 ≤ y ≤ 1:

The returned geometry objects are typically passed to geoPath to display, using null or geoIdentity as the associated projection.

Source · Computes a single contour, returning a GeoJSON MultiPolygon geometry object representing the area where the input values are greater than or equal to the given threshold value; the threshold value for each geometry object is exposed as geometry.value.

The input values must be an array of length n×m where [n, m] is the contour generator’s size; furthermore, each values[i + jn] must represent the value at the position ⟨i, j⟩. See contours for an example.

Source · If size is specified, sets the expected size of the input values grid to the contour generator and returns the contour generator. The size is specified as an array [n, m] where n is the number of columns in the grid and m is the number of rows; n and m must be positive integers. If size is not specified, returns the current size which defaults to [1, 1].

Examples · Source · If smooth is specified, sets whether or not the generated contour polygons are smoothed using linear interpolation. If smooth is not specified, returns the current smoothing flag, which defaults to true.

Source · If thresholds is specified, sets the threshold generator to the specified function or array and returns this contour generator. If thresholds is not specified, returns the current threshold generator, which by default implements Sturges’ formula.

Thresholds are defined as an array of values [x0, x1, …]. The first generated contour corresponds to the area where the input values are greater than or equal to x0; the second contour corresponds to the area where the input values are greater than or equal to x1, and so on. Thus, there is exactly one generated MultiPolygon geometry object for each specified threshold value; the threshold value is exposed as geometry.value.

If a count is specified instead of an array of thresholds, then the input values’ extent will be uniformly divided into approximately count bins; see ticks.

**Examples:**

Example 1 (javascript):
```javascript
const contours = d3.contours()
    .size([width, height])
    .thresholds([0, 1, 2, 3, 4]);
```

Example 2 (javascript):
```javascript
const polygons = contours(grid);
```

Example 3 (sass):
```sass
var n = 256, m = 256, values = new Array(n * m);
for (var j = 0.5, k = 0; j < m; ++j) {
  for (var i = 0.5; i < n; ++i, ++k) {
    values[k] = goldsteinPrice(i / n * 4 - 2, 1 - j / m * 3);
  }
}
```

Example 4 (javascript):
```javascript
function goldsteinPrice(x, y) {
  return (1 + Math.pow(x + y + 1, 2) * (19 - 14 * x + 3 * x * x - 14 * y + 6 * x * x + 3 * y * y))
      * (30 + Math.pow(2 * x - 3 * y, 2) * (18 - 32 * x + 12 * x * x + 48 * y - 36 * x * y + 27 * y * y));
}
```

---

## Density estimation | D3 by Observable

**URL:** https://d3js.org/d3-contour/density

**Contents:**
- Density estimation ​
- contourDensity() ​
- density(data) ​
- density.x(x) ​
- density.y(y) ​
- density.weight(weight) ​
- density.size(size) ​
- density.cellSize(cellSize) ​
- density.thresholds(thresholds) ​
- density.bandwidth(bandwidth) ​

Contours can show the estimated density of point clouds, which is useful to avoid overplotting in large datasets. The contourDensity method implements fast two-dimensional kernel density estimation.

Here is a scatterplot showing the relationship between the idle duration and eruption duration for Old Faithful:

And here is a density contour plot showing the relationship between the weight and price of 53,940 diamonds:

Examples · Source · Constructs a new density estimator with the default settings.

Source · Estimates the density contours for the given array of data, returning an array of GeoJSON MultiPolygon geometry objects.

Each geometry object represents the area where the estimated number of points per square pixel is greater than or equal to the corresponding threshold value; the threshold value for each geometry object is exposed as geometry.value. The returned geometry objects are typically passed to geoPath to display, using null or geoIdentity as the associated projection. See also contours.

The x and y coordinate for each data point are computed using density.x and density.y. In addition, density.weight indicates the relative contribution of each data point (default 1). The generated contours are only accurate within the estimator’s defined size.

Source · If x is specified, sets the x-coordinate accessor. If x is not specified, returns the current x-coordinate accessor, which defaults to:

Source · If y is specified, sets the y-coordinate accessor. If y is not specified, returns the current y-coordinate accessor, which defaults to:

Source · If weight is specified, sets the accessor for point weights. If weight is not specified, returns the current point weight accessor, which defaults to:

Source · If size is specified, sets the size of the density estimator to the specified bounds and returns the estimator. The size is specified as an array [width, height], where width is the maximum x-value and height is the maximum y-value. If size is not specified, returns the current size which defaults to [960, 500]. The estimated density contours are only accurate within the defined size.

Source · If cellSize is specified, sets the size of individual cells in the underlying bin grid to the specified positive integer and returns the estimator. If cellSize is not specified, returns the current cell size, which defaults to 4. The cell size is rounded down to the nearest power of two. Smaller cells produce more detailed contour polygons, but are more expensive to compute.

Source · If thresholds is specified, sets the threshold generator to the specified function or array and returns this contour generator. If thresholds is not specified, returns the current threshold generator, which by default generates about twenty nicely-rounded density thresholds.

Thresholds are defined as an array of values [x0, x1, …]. The first generated density contour corresponds to the area where the estimated density is greater than or equal to x0; the second contour corresponds to the area where the estimated density is greater than or equal to x1, and so on. Thus, there is exactly one generated MultiPolygon geometry object for each specified threshold value; the threshold value is exposed as geometry.value. The first value x0 should typically be greater than zero.

If a count is specified instead of an array of thresholds, then approximately count uniformly-spaced nicely-rounded thresholds will be generated; see ticks.

Source · If bandwidth is specified, sets the bandwidth (the standard deviation) of the Gaussian kernel and returns the estimate. If bandwidth is not specified, returns the current bandwidth, which defaults to 20.4939…. The specified bandwidth is currently rounded to the nearest supported value by this implementation, and must be nonnegative.

Examples · Source · Return a contour(value) function that can be used to compute an arbitrary contour on the given data without needing to recompute the underlying grid. The returned contour function also exposes a contour.max value which represents the maximum density of the grid.

**Examples:**

Example 1 (javascript):
```javascript
function x(d) {
  return d[0];
}
```

Example 2 (javascript):
```javascript
function y(d) {
  return d[1];
}
```

Example 3 (javascript):
```javascript
function weight() {
  return 1;
}
```

---

## d3-contour | D3 by Observable

**URL:** https://d3js.org/d3-contour

**Contents:**
- d3-contour ​

This module computes contour polygons by applying marching squares to a rectangular grid of numeric values. For example, the contours above show the topography of Maungawhau.
