## Voronoi diagrams | D3 by Observable

**URL:** https://d3js.org/d3-delaunay/voronoi

**Contents:**
- Voronoi diagrams ​
- delaunay.voronoi(bounds) ​
  - voronoi.delaunay ​
  - voronoi.circumcenters ​
  - voronoi.vectors ​
  - voronoi.xminvoronoi.yminvoronoi.xmaxvoronoi.ymax ​
- voronoi.contains(i, x, y) ​
- voronoi.neighbors(i) ​
- voronoi.render(context) ​
- voronoi.renderBounds(context) ​

Given a set of points, the Voronoi diagram partitions the plane into cells representing the region of the plane that is closest to the corresponding point. The Voronoi diagram is the dual of the Delaunay triangulation.

Source · Returns the Voronoi diagram for the given Delaunay triangulation. When rendering, the diagram will be clipped to the specified bounds = [xmin, ymin, xmax, ymax].

If bounds is not specified, it defaults to [0, 0, 960, 500]. The Voronoi diagram is returned even in degenerate cases where no triangulation exists — namely 0, 1 or 2 points, and collinear points.

The Voronoi diagram’s associated Delaunay triangulation.

The circumcenters of the Delaunay triangles as a Float64Array [cx0, cy0, cx1, cy1, …]. Each contiguous pair of coordinates cx, cy is the circumcenter for the corresponding triangle. These circumcenters form the coordinates of the Voronoi cell polygons.

A Float64Array [vx0, vy0, wx0, wy0, …] where each non-zero quadruple describes an open (infinite) cell on the outer hull, giving the directions of two open half-lines.

The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram. These values only affect the rendering methods (voronoi.render, voronoi.renderBounds, voronoi.renderCell).

Source · Returns true if the cell with the specified index i contains the specified point ⟨x, y⟩; i.e., whether the point i is the closest point in the diagram to the specified point. (This method is not affected by the associated Voronoi diagram’s viewport bounds.)

Source · Returns an iterable over the indexes of the cells that share a common edge with the specified cell i. Voronoi neighbors are always neighbors on the Delaunay graph, but the converse is false when the common edge has been clipped out by the Voronoi diagram’s viewport.

Source · Renders the mesh of Voronoi cells to the specified context. The specified context must implement the context.moveTo and context.lineTo methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Renders the viewport extent to the specified context. The specified context must implement the context.rect method from the CanvasPathMethods API. Equivalent to context.rect(voronoi.xmin, voronoi.ymin, voronoi.xmax - voronoi.xmin, voronoi.ymax - voronoi.ymin). If a context is not specified, an SVG path string is returned instead.

Source · Renders the cell with the specified index i to the specified context. The specified context must implement the context.moveTo , context.lineTo and context.closePath methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Returns an iterable over the non-empty polygons for each cell, with the cell index as property. See also voronoi.renderCell.

Source · Returns the convex, closed polygon [[x0, y0], [x1, y1], …, [x0, y0]] representing the cell for the specified point i. See also voronoi.renderCell.

Source · Updates the Voronoi diagram and underlying triangulation after the points have been modified in-place — useful for Lloyd’s relaxation. Calls delaunay.update on the underlying Delaunay triangulation.

**Examples:**

Example 1 (javascript):
```javascript
const delaunay = d3.Delaunay.from([[0, 0], [0, 100], [100, 0], [100, 100]]);
const voronoi = delaunay.voronoi([0, 0, 640, 480]);
```

Example 2 (unknown):
```unknown
voronoi.neighbors(-1) // []
```

---

## d3-delaunay | D3 by Observable

**URL:** https://d3js.org/d3-delaunay

**Contents:**
- d3-delaunay ​

This is a fast library for computing the Voronoi diagram of a set of two-dimensional points. It is based on Delaunator, a fast library for computing the Delaunay triangulation using sweep algorithms. The Voronoi diagram is constructed by connecting the circumcenters of adjacent triangles in the Delaunay triangulation.

For an interactive explanation of how this library works, see The Delaunay’s Dual.

---

## Delaunay triangulations | D3 by Observable

**URL:** https://d3js.org/d3-delaunay/delaunay

**Contents:**
- Delaunay triangulations ​
- new Delaunay(points) ​
  - delaunay.points ​
  - delaunay.halfedges ​
  - delaunay.hull ​
  - delaunay.triangles ​
  - delaunay.inedges ​
- Delaunay.from(points, fx, fy, that) ​
- delaunay.find(x, y, i) ​
- delaunay.neighbors(i) ​

The Delaunay triangulation is a triangular mesh formed from a set of points in x and y. No point is inside the circumcircle of any triangle, which is a nice geometric property for certain applications, and tends to avoid “sliver” triangles. The Delaunay triangulation is the dual of the Voronoi diagram.

Source · Returns the Delaunay triangulation for the given flat array [x0, y0, x1, y1, …] of points.

The given points may be any array-like type, but is typically a Float64Array.

The coordinates of the points as an array [x0, y0, x1, y1, …].

The halfedge indexes as an Int32Array [j0, j1, …]. For each index 0 ≤ i < halfedges.length, there is a halfedge from triangle vertex j = halfedges[i] to triangle vertex i. Equivalently, this means that triangle ⌊i / 3⌋ is adjacent to triangle ⌊j / 3⌋. If j is negative, then triangle ⌊i / 3⌋ is an exterior triangle on the convex hull. For example, to render the internal edges of the Delaunay triangulation:

See also delaunay.render.

An Int32Array of point indexes that form the convex hull in counterclockwise order. If the points are collinear, returns them ordered.

See also delaunay.renderHull.

The triangle vertex indexes as an Uint32Array [i0, j0, k0, i1, j1, k1, …]. Each contiguous triplet of indexes i, j, k forms a counterclockwise triangle. The coordinates of the triangle’s points can be found by going through delaunay.points. For example, to render triangle i:

See also delaunay.renderTriangle.

The incoming halfedge indexes as a Int32Array [e0, e1, e2, …]. For each point i, inedges[i] is the halfedge index e of an incoming halfedge. For coincident points, the halfedge index is -1; for points on the convex hull, the incoming halfedge is on the convex hull; for other points, the choice of incoming halfedge is arbitrary. The inedges table can be used to traverse the Delaunay triangulation; see also delaunay.neighbors.

Delaunay.from is typically slower than new Delaunay because it requires materializing a new flat array of xy coordinates.

Source · Returns the Delaunay triangulation for the given array or iterable of points. If fx and fy are not specified, then points is assumed to be an array of two-element arrays of numbers: [[x0, y0], [x1, y1], …].

Otherwise, fx and fy are functions that are invoked for each element in the points array in order, and must return the respective x and y coordinate for each point.

If that is specified, the functions fx and fy are invoked with that as this. (See Array.from for reference.)

Examples · Source · Returns the index of the input point that is closest to the specified point ⟨x, y⟩. The search is started at the specified point i. If i is not specified, it defaults to zero.

Source · Returns an iterable over the indexes of the neighboring points to the specified point i. The iterable is empty if i is a coincident point.

Source · Renders the edges of the Delaunay triangulation to the specified context. The specified context must implement the context.moveTo and context.lineTo methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Renders the convex hull of the Delaunay triangulation to the specified context. The specified context must implement the context.moveTo and context.lineTo methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Renders triangle i of the Delaunay triangulation to the specified context. The specified context must implement the context.moveTo, context.lineTo and context.closePath methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Renders the input points of the Delaunay triangulation to the specified context as circles with the specified radius. If radius is not specified, it defaults to 2. The specified context must implement the context.moveTo and context.arc methods from the CanvasPathMethods API. If a context is not specified, an SVG path string is returned instead.

Source · Returns the closed polygon [[x0, y0], [x1, y1], …, [x0, y0]] representing the convex hull. See also delaunay.renderHull.

Source · Returns an iterable over the polygons for each triangle, in order. See also delaunay.renderTriangle.

Source · Returns the closed polygon [[x0, y0], [x1, y1], [x2, y2], [x0, y0]] representing the triangle i. See also delaunay.renderTriangle.

Source · Recomputes the triangulation after the points have been modified in-place.

Source · Returns the Voronoi diagram for the given Delaunay triangulation. When rendering, the diagram will be clipped to the specified bounds = [xmin, ymin, xmax, ymax].

If bounds is not specified, it defaults to [0, 0, 960, 500]. The Voronoi diagram is returned even in degenerate cases where no triangulation exists — namely 0, 1 or 2 points, and collinear points.

**Examples:**

Example 1 (javascript):
```javascript
const delaunay = new d3.Delaunay(Float64Array.of(0, 0, 0, 1, 1, 0, 1, 1));
```

Example 2 (sass):
```sass
const {points, halfedges, triangles} = delaunay;
for (let i = 0, n = halfedges.length; i < n; ++i) {
  const j = halfedges[i];
  if (j < i) continue;
  const ti = triangles[i];
  const tj = triangles[j];
  context.moveTo(points[ti * 2], points[ti * 2 + 1]);
  context.lineTo(points[tj * 2], points[tj * 2 + 1]);
}
```

Example 3 (javascript):
```javascript
const {points, triangles} = delaunay;
const t0 = triangles[i * 3 + 0];
const t1 = triangles[i * 3 + 1];
const t2 = triangles[i * 3 + 2];
context.moveTo(points[t0 * 2], points[t0 * 2 + 1]);
context.lineTo(points[t1 * 2], points[t1 * 2 + 1]);
context.lineTo(points[t2 * 2], points[t2 * 2 + 1]);
context.closePath();
```

Example 4 (javascript):
```javascript
const delaunay = d3.Delaunay.from([[0, 0], [0, 1], [1, 0], [1, 1]]);
```
