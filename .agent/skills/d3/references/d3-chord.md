## Ribbons | D3 by Observable

**URL:** https://d3js.org/d3-chord/ribbon

**Contents:**
- Ribbons ​
- ribbon() ​
- ribbon(...arguments) ​
- ribbon.source(source) ​
- ribbon.target(target) ​
- ribbon.radius(radius) ​
- ribbon.sourceRadius(radius) ​
- ribbon.targetRadius(radius) ​
- ribbon.startAngle(angle) ​
- ribbon.endAngle(angle) ​

A ribbon visually represents the volume of flow between two nodes in a chord diagram. Ribbons come in two varieties: ribbon represents a bidirectional flow, while ribbonArrow represents a unidirectional flow. The latter is suitable for chordDirected.

Source · Creates a new ribbon generator with the default settings.

Source · Generates a ribbon for the given arguments. The arguments are arbitrary; they are propagated to the ribbon generator’s accessor functions along with the this object. For example, with the default settings, a chord object is expected:

If the ribbon generator has a context, then the ribbon is rendered to this context as a sequence of path method calls and this function returns void. Otherwise, a path data string is returned.

Source · If source is specified, sets the source accessor to the specified function and returns this ribbon generator. If source is not specified, returns the current source accessor, which defaults to:

Source · If target is specified, sets the target accessor to the specified function and returns this ribbon generator. If target is not specified, returns the current target accessor, which defaults to:

Source · If radius is specified, sets the source and target radius accessor to the specified function and returns this ribbon generator. For example to set a fixed radius of 240 pixels:

Now the arguments you pass to ribbon do not need to specify a radius property on the source and target.

If radius is not specified, returns the current source radius accessor, which defaults to:

Source · If radius is specified, sets the source radius accessor to the specified function and returns this ribbon generator. If radius is not specified, returns the current source radius accessor, which defaults to:

Source · If radius is specified, sets the target radius accessor to the specified function and returns this ribbon generator. If radius is not specified, returns the current target radius accessor, which defaults to:

By convention, the target radius in asymmetric chord diagrams is typically inset from the source radius, resulting in a gap between the end of the directed link and its associated group arc.

Source · If angle is specified, sets the start angle accessor to the specified function and returns this ribbon generator. If angle is not specified, returns the current start angle accessor, which defaults to:

The angle is specified in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise.

Source · If angle is specified, sets the end angle accessor to the specified function and returns this ribbon generator. If angle is not specified, returns the current end angle accessor, which defaults to:

The angle is specified in radians, with 0 at -y (12 o’clock) and positive angles proceeding clockwise.

Source · If angle is specified, sets the pad angle accessor to the specified function and returns this ribbon generator. If angle is not specified, returns the current pad angle accessor, which defaults to:

The pad angle specifies the angular gap between adjacent ribbons.

Source · If context is specified, sets the context and returns this ribbon generator. If context is not specified, returns the current context, which defaults to null. If the context is not null, then the generated ribbon is rendered to this context as a sequence of path method calls. Otherwise, a path data string representing the generated ribbon is returned. See also d3-path.

Source · Creates a new arrow ribbon generator with the default settings. See also chordDirected.

Source · If radius is specified, sets the arrowhead radius accessor to the specified function and returns this ribbon generator. If radius is not specified, returns the current arrowhead radius accessor, which defaults to:

**Examples:**

Example 1 (javascript):
```javascript
const ribbon = d3.ribbon();
```

Example 2 (css):
```css
ribbon({
  source: {startAngle: 0.7524114, endAngle: 1.1212972, radius: 240},
  target: {startAngle: 1.8617078, endAngle: 1.9842927, radius: 240}
}) // "M164.0162810494058,-175.21032946354026A240,240,0,0,1,216.1595644740915,-104.28347273835429Q0,0,229.9158815306728,68.8381247563705A240,240,0,0,1,219.77316791012538,96.43523560788266Q0,0,164.0162810494058,-175.21032946354026Z"
```

Example 3 (javascript):
```javascript
function source(d) {
  return d.source;
}
```

Example 4 (javascript):
```javascript
function target(d) {
  return d.target;
}
```

---

## Chords | D3 by Observable

**URL:** https://d3js.org/d3-chord/chord

**Contents:**
- Chords ​
- chord() ​
- chord(matrix) ​
- chord.padAngle(angle) ​
- chord.sortGroups(compare) ​
- chord.sortSubgroups(compare) ​
- chord.sortChords(compare) ​
- chordDirected() ​
- chordTranspose() ​

The chord layout computes angles to generate a chord diagram.

Source · Constructs a new chord layout with the default settings.

Source · Computes the chord layout for the specified square matrix of size n×n, where the matrix represents the directed flow amongst a network (a complete digraph) of n nodes.

The return value of chord(matrix) is an array of chords, where each chord represents the combined bidirectional flow between two nodes i and j (where i may be equal to j) and is an object with the following properties:

Each source and target subgroup is also an object with the following properties:

The chords are typically passed to ribbon to display the network relationships.

The returned array includes only chord objects for which the value matrix[i][j] or matrix[j][i] is non-zero. Furthermore, the returned array only contains unique chords: a given chord ij represents the bidirectional flow from i to j and from j to i, and does not contain a duplicate chord ji; i and j are chosen such that the chord’s source always represents the larger of matrix[i][j] and matrix[j][i].

The chords array also defines a secondary array of length n, chords.groups, where each group represents the combined outflow for node i, corresponding to the elements matrix[i][0 … n - 1], and is an object with the following properties:

The groups are typically passed to arc to produce a donut chart around the circumference of the chord layout.

Source · If angle is specified, sets the pad angle between adjacent groups to the specified number in radians and returns this chord layout. If angle is not specified, returns the current pad angle, which defaults to zero.

Source · If compare is specified, sets the group comparator to the specified function or null and returns this chord layout. If compare is not specified, returns the current group comparator, which defaults to null. If the group comparator is non-null, it is used to sort the groups by their total outflow. See also ascending and descending.

Source · If compare is specified, sets the subgroup comparator to the specified function or null and returns this chord layout. If compare is not specified, returns the current subgroup comparator, which defaults to null. If the subgroup comparator is non-null, it is used to sort the subgroups corresponding to matrix[i][0 … n - 1] for a given group i by their total outflow. See also ascending and descending.

Source · If compare is specified, sets the chord comparator to the specified function or null and returns this chord layout. If compare is not specified, returns the current chord comparator, which defaults to null. If the chord comparator is non-null, it is used to sort the chords by their combined flow; this only affects the z-order of the chords. See also ascending and descending.

Examples · Source · A chord layout for unidirectional flows. The chord from i to j is generated from the value in matrix[i][j] only.

Source · A transposed chord layout. Useful to highlight outgoing (rather than incoming) flows.

**Examples:**

Example 1 (javascript):
```javascript
const chord = d3.chord();
```

---

## d3-chord | D3 by Observable

**URL:** https://d3js.org/d3-chord

**Contents:**
- d3-chord ​

Chord diagrams visualize flow between a set of nodes in a graph, such as transition probabilities between finite states. The diagram above shows a fake dataset from Circos of people who dyed their hair.

D3’s chord layout represents flow using a square matrix of size n×n, where n is the number of nodes in the graph. Each value matrix[i][j] represents the flow from the ith node to the jth node. (Each number matrix[i][j] must be nonnegative, though it can be zero if there is no flow from node i to node j.)

Above, each row and column represents a hair color (black, blond, brown, red); each value represents a number of people who dyed their hair from one color to another color. For example, 5,871 people had black hair and dyed it blond, while 1,951 people had blond hair and dyed it black. The matrix diagonal represents people who kept the same color.

A chord diagram visualizes these transitions by arranging the population by starting color along the circumference of a circle and drawing ribbons between each color. The starting and ending width of the ribbon is proportional to the number of people that had the respective starting and ending color. The color of the ribbon, arbitrarily, is the color with the larger of the two values.

**Examples:**

Example 1 (sql):
```sql
const matrix = [
  // to black, blond, brown, red
  [11975,  5871, 8916, 2868], // from black
  [ 1951, 10048, 2060, 6171], // from blond
  [ 8010, 16145, 8090, 8045], // from brown
  [ 1013,   990,  940, 6907]  // from red
];
```
