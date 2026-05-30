# <span class="keep-together">Appendix E. </span>Quick Reference

Here <span id="app05.xhtml_D3method21"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="methods quick reference"></span><span id="app05.xhtml_Mquick21"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="methods"
secondary="quick reference"></span>is a list of the most commonly used
D3 methods covered in this book, plus a brief summary of its use, and
one example for each. (Methods that require a bit more explanation—such
as line and area generators, geographic projections, layouts, and
scale-specific methods—have been omitted.)

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Selections">

<div id="app05.xhtml_idm140093176337024" class="dedication">

# Selections

<a href="http://bit.ly/2t1FJhC"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.select()</code></a>  
<span id="app05.xhtml_idm140093176333648"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.select()"></span>Returns a
<span id="app05.xhtml_idm140093176332816"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="D3 methods for making"></span>reference to the first element
found:

``` calibre39
// Selects an SVG element and stores a reference to it in 'svg'
var svg = d3.select("svg");
```

<a href="http://bit.ly/2t1EJtU"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.selectAll()</code></a>  
<span id="app05.xhtml_idm140093176323904"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.selectAll()"></span>Returns references
to all found elements:

``` calibre39
// Selects all circle elements and stores references to them in 'circles'
var circles = d3.selectAll("circle");
```

<a href="http://bit.ly/2t1EGye"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.append()</code></a>  
<span id="app05.xhtml_idm140093176308272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="selection.append()"></span><span id="app05.xhtml_idm140093176307536"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="append()"></span>Takes a selection,
creates a new element inside of it, then returns a reference to the
newly created element:

``` calibre39
// Creates a new circle inside of the 'svg' selection established earlier
d3.select("svg").append("circle");

// This would accomplish the same thing…
svg.append("circle");

// …but it's often useful to store a reference to the new element
var newCircle = svg.append("circle");
```

<a href="http://bit.ly/2t1FMtO"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.remove()</code></a>  
<span id="app05.xhtml_idm140093176227792"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.remove()"></span>Takes a
selection, removes it from the DOM, and returns a reference to the
deleted selection:

``` calibre39
// Removes the first rect element
d3.select("rect").remove();
```

<a href="http://bit.ly/2t1FPpu"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.text()</code></a>  
<span id="app05.xhtml_idm140093176286272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.text()"></span>Takes a
selection, sets its text content, and returns a reference to the
acted-upon selection:

``` calibre39
// Sets the text content of #tooltip to "15%"
d3.select("#tooltip").text("15%");
```

<a href="http://bit.ly/2t1Q3X6"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.attr()</code></a>  
<span id="app05.xhtml_idm140093176268208"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.attr()"></span>Takes a
selection, sets an attribute value, and returns a reference to the
acted-upon selection:

``` calibre39
// Assigns a radius value of 10 to all circle elements
d3.selectAll("circle").attr("r", 10);
```

<a href="http://bit.ly/2t1HThk"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.style()</code></a>  
<span id="app05.xhtml_idm140093176262880"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.style()"></span>Takes a
selection, sets an inline CSS style, and returns a reference to the
acted-upon selection:

``` calibre39
// Assigns a CSS fill of "teal" to all circle elements
d3.selectAll("circle").style("fill", "teal");
```

<a href="http://bit.ly/2t1p0eh"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.classed()</code></a>  
<span id="app05.xhtml_idm140093176064320"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.classed()"></span>Takes a
selection, adds or removes a class, and returns a reference to the
acted-upon selection; `true` adds the specified class, `false` removes
it:

``` calibre39
// Adds a class of "highlight" to the first circle element
d3.select("circle").classed("highlight", true);

// Removes the class of "active" from all circle elements
d3.selectAll("circle").classed("active", false);
```

<a href="http://bit.ly/2t1DoU6"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.each()</code></a>  
<span id="app05.xhtml_idm140093176142400"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.each()"></span>Takes a
selection, and runs an arbitrary function once for each element in the
selection, with the `this` context set to the element being acted upon:

``` calibre39
d3.selectAll("circle")
  .each(zoomAndEnhance);
  // Assumes a function named 'zoomAndEnhance' already defined
```

</div>

</div>

<div class="section calibre2" data-type="sect1" pdf-bookmark="Data">

<div id="app05.xhtml_idm140093176137408" class="dedication">

# Data

<a href="http://bit.ly/2t1qkOe"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.data()</code></a>  
<span id="app05.xhtml_idm140093176038288"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.data()"></span>Takes a
selection, calculates the difference between the number of elements and
number of data values, and binds the array of data values to any
existing elements (or not-yet-existing placeholder elements):

``` calibre39
d3.selectAll("circle")
    .data(dataset)  // Binds data to all circles (or placeholders)
    .enter()
    .append("circle");
```

<a href="http://bit.ly/2t1JCU1"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.datum()</code></a>  
<span id="app05.xhtml_idm140093176001472"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.datum()"></span>Takes a
selection, and binds a single data value to a single element (or
not-yet-existing placeholder element):

``` calibre39
svg.append("path")
    .datum(dataset)
    .attr("d", line);
```

<a href="http://bit.ly/2t1JDHz"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.enter()</code></a>  
<span id="app05.xhtml_idm140093175957488"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.enter()"></span>Takes a
selection and returns a subselection of “new” placeholder elements:

``` calibre39
d3.selectAll("circle")
  .data(dataset)
  .enter()  // Returns the placeholders for circles to-be-created
  .append("circle");  // Creates a circle for each placeholder
```

<a href="http://bit.ly/2t1oFsh"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.merge()</code></a>  
<span id="app05.xhtml_idm140093175828816"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.merge()"></span>Takes a
selection and merges it with another specified selection, returning a
newly merged selection:

``` calibre39
bars.enter()  // Get the enter subselection
    .append("rect")
    …  // Set attributes for new elements…
    .merge(bars)  // Merge enter subselection with existing bars selection
    …  // Set attributes for all elements…
```

<a href="http://bit.ly/2t1pelD"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.exit()</code></a>  
<span id="app05.xhtml_idm140093175808640"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.exit()"></span>Takes a
selection and returns a subselection of “exiting” elements:

``` calibre39
bars.exit()     // Get the exit subselection
    .transition()
    …  // Set attributes for exiting elements, e.g. dial down opacity…
```

<a href="http://bit.ly/2t1FMtO"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.remove()</code></a>  
<span id="app05.xhtml_idm140093175764000"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.remove()"></span>Takes a
selection and removes associated elements from the DOM:

``` calibre39
bars.exit()     // Get the exit subselection
    .remove();  // Delete exiting elements immediately
```

`function(d) { … }`  
Use anonymous functions to access data values bound to elements via `d`:

``` calibre39
d3.selectAll("rect")
  .attr("height", function(d) {
      return d.value;  // Set each rect's height to 'value'
  });
```

`function(d, i) { … }`  
Include `i` to get the index value of each element in the selection:

``` calibre39
d3.selectAll("rect")
  .attr("x", function(d, i) {
      return i * 10;  // Move each successive rect more to the right
  });
```

<a href="http://bit.ly/2t1G7N6"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.filter()</code></a>  
<span id="app05.xhtml_idm140093175683728"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.filter()"></span>Takes a
selection and returns a new (sub)selection:

``` calibre39
d3.selectAll("circle")
  .filter(function(d) {
       return d > 15;  // If 'true', element is included
  })
  .style("color", "red");
```

<a href="http://bit.ly/2t1KTtZ"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.csv()</code></a>  
<span id="app05.xhtml_idm140093175559808"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.csv()"></span>Loads an external CSV
file, parses the contents into JSON, then hands off the results to a
callback function:

``` calibre39
d3.csv("food.csv", function(data) {
    console.log(data);
});
```

<a href="http://bit.ly/2t1BbYL"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.json()</code></a>  
<span id="app05.xhtml_idm140093175517856"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.json()"></span>Loads an external JSON
file, parses the contents into JSON, then hands off the results to a
callback function:

``` calibre39
d3.json("waterfallVelocities.json", function(json) {
    console.log(json);
});
```

<a href="http://bit.ly/2t1FAe7"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.request()</code></a>  
<span id="app05.xhtml_idm140093175499104"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.request()"></span>Loads an arbitrary
external file, then hands off the results to a callback function:

``` calibre39
d3.request("interesting_data.txt")
  .get(function(response) {
      // Do something with the response string
});
```

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Transitions">

<div id="app05.xhtml_idm140093176039648" class="dedication">

# Transitions

<a href="http://bit.ly/2t1qCVk"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.transition()</code></a>  
<span id="app05.xhtml_idm140093175461312"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.transition()"></span>Takes a
<span id="app05.xhtml_idm140093175460480"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transitions"
secondary="methods quick reference"></span>selection, and initiates a
new transition, so values specified after this point will be
interpolated over time (rather than set immediately):

``` calibre39
d3.selectAll("circle")
  .attr("cx", 0)     // Initial value for 'cx' is set
  .transition()      // Transition is initiated
  .attr("cx", 100);  // 'cx' will be interpolated to 100
```

<a href="http://bit.ly/2t1imEZ"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">transition</code></em><code
class="calibre23">.delay()</code></a>  
<span id="app05.xhtml_idm140093175665296"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transition.delay()"></span>Takes a
transition, and sets the delay, in milliseconds:

``` calibre39
d3.selectAll("circle")
  .attr("cx", 0)
  .transition()
  .delay(1000)  // Wait 1 second before starting
  .attr("cx", 100);
```

<a href="http://bit.ly/2t1IkrY"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">transition</code></em><code
class="calibre23">.duration()</code></a>  
<span id="app05.xhtml_idm140093175383584"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transition.duration()"></span>Takes a
transition, and sets the duration, in milliseconds:

``` calibre39
d3.selectAll("circle")
  .attr("cx", 0)
  .transition()
  .duration(2000)  // Transition will occur over 2 seconds
  .attr("cx", 100);
```

<a href="http://bit.ly/2t1FyTw"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">transition</code></em><code
class="calibre23">.ease()</code></a>  
<span id="app05.xhtml_idm140093175338624"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transition.ease()"></span>Takes a
transition, and sets the easing to be used:

``` calibre39
d3.selectAll("circle")
  .attr("cx", 0)
  .transition()
  .ease(d3.easeLinear)  // Transition will be linear
  .attr("cx", 100);
```

<a href="http://bit.ly/2t1FyTw"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">transition</code></em><code
class="calibre23">.on()</code></a>  
<span id="app05.xhtml_idm140093175314784"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transition.on()"></span>Takes a
transition, and binds a function to be executed at either the `"start"`
or `"end"`:

``` calibre39
d3.selectAll("circle")
  .attr("cx", 0)
  .transition()
  .attr("cx", 100)
  .on("end", function() {  // <-- Executes after transition
      console.log("All done!")
  });
```

</div>

</div>

<div class="section calibre2" data-type="sect1" pdf-bookmark="Scales">

<div id="app05.xhtml_idm140093175312512" class="dedication">

# Scales

<a href="http://bit.ly/2t1rKbw"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.scaleLinear()</code></a>  
Creates a <span id="app05.xhtml_idm140093175212848"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scales"
secondary="handy methods for"></span><span id="app05.xhtml_idm140093175211840"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.scaleLinear()"></span>new linear scale
function:

``` calibre39
var xScale = d3.scaleLinear();
```

<a href="http://bit.ly/2t1oVXZ"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">scaleLinear</code></em><code
class="calibre23">.domain()</code></a>  
<span id="app05.xhtml_idm140093175205056"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scaleLinear.domain()"></span>Sets a
linear scale’s input domain:

``` calibre39
xScale.domain([ 0, 2000 ]);
```

<a href="http://bit.ly/2t1GTd1"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">scaleLinear</code></em><code
class="calibre23">.range()</code></a>  
<span id="app05.xhtml_idm140093175160272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scaleLinear.range()"></span>Sets a linear
scale’s output range:

``` calibre39
xScale.range([ 0, width ]);
```

<a href="http://bit.ly/2t1rSb0"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">scaleLinear</code></em><code
class="calibre23">.rangeRound()</code></a>  
<span id="app05.xhtml_idm140093175148240"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scaleLinear.rangeRound()"></span>Sets a
linear scale’s output range, and has all values output by the scale
rounded to the nearest whole number:

``` calibre39
xScale.rangeRound([ 0, width ]);
```

<a href="http://bit.ly/2t1LkVr"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">scaleLinear</code></em><code
class="calibre23">.nice()</code></a>  
<span id="app05.xhtml_idm140093175094016"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scaleLinear.nice()"></span>Expands a
linear scale’s domain to the nearest round values:

``` calibre39
xScale.nice();
```

<a href="http://bit.ly/2t1Hnje"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">scaleLinear</code></em><code
class="calibre23">.clamp()</code></a>  
<span id="app05.xhtml_idm140093174996272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="scaleLinear.clamp()"></span>Forces any
values output by this scale to be constrained (rounded to be) within the
specified range:

``` calibre39
xScale.clamp(true);
```

<div class="calibre27 note" data-type="note">

###### Note

Other scale types—such as `scaleSqrt`, `scalePow`, and
`scaleOrdinal`—may share similar methods or have unique methods of their
own. Double-check the documentation for each type of scale.

</div>

<a href="http://bit.ly/2t1jYP3"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.min()</code></a>  
<span id="app05.xhtml_idm140093175090752"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.min()"></span>Returns the smallest
value in an array:

``` calibre39
d3.min([ 10, 20, 70, 35 ]);  // Returns 10
```

<a href="http://bit.ly/2t1HueI"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.max()</code></a>  
<span id="app05.xhtml_idm140093174973680"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.max()"></span>Returns the largest
value in an array:

``` calibre39
d3.max([ 10, 20, 70, 35 ]);  // Returns 70
```

</div>

</div>

<div class="section calibre2" data-type="sect1" pdf-bookmark="Axes">

<div id="app05.xhtml_idm140093174954336" class="dedication">

# Axes

<a href="http://bit.ly/2t1s4ae"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.axisTop</code></a>, <a href="http://bit.ly/2t1H8EX"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.axisRight</code></a>, <a href="http://bit.ly/2t1qrJX"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><span
class="keep-together"><code
class="calibre23">d3.axisBottom</code></span></a>, and <a href="http://bit.ly/2t1Hw6g"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.axisLeft</code></a>  
<span id="app05.xhtml_idm140093174962768"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.axisTop"></span><span id="app05.xhtml_idm140093174962064"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.axisRight"></span><span id="app05.xhtml_idm140093174961392"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.axisBottom"></span><span id="app05.xhtml_idm140093174960720"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.axisLeft"></span>Creates a
<span id="app05.xhtml_idm140093174959920"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="axes"
secondary="methods quick reference"></span>new axis generator function,
with the specified orientation:

``` calibre39
var xAxis = d3.svg.axisBottom();
```

<a href="http://bit.ly/2t1qZ2d"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">axis</code></em><code
class="calibre23">.scale()</code></a>  
<span id="app05.xhtml_idm140093174852624"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="axis.scale()"></span>Takes an axis, and
specifies the scale to be used:

``` calibre39
xAxis.scale(xScale);
```

<a href="http://bit.ly/2t1vt97"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">axis</code></em><code
class="calibre23">.ticks()</code></a>  
<span id="app05.xhtml_idm140093174814272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="axis.ticks()"></span>Takes an axis, and
specifies a target number of ticks to be used:

``` calibre39
xAxis.ticks(5);
```

<a href="http://bit.ly/2t1qgOy"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">axis</code></em><code
class="calibre23">.tickValues()</code></a>  
<span id="app05.xhtml_idm140093174759776"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="axis.tickValues()"></span>Takes an axis,
and specifies the values to be labeled with ticks:

``` calibre39
xAxis.tickValues([0, 100, 250, 600]);
```

<a href="http://bit.ly/2t1MUq3"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.call()</code></a>  
<span id="app05.xhtml_idm140093174783840"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.call()"></span>Takes a
selection, and calls an arbitrary method to act upon the selection;
commonly used to generate an axis:

``` calibre39
// Calls xAxis(), generating axis elements inside 'g'
svg.append("g").call(xAxis);
```

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Interactivity">

<div id="app05.xhtml_idm140093174866096" class="dedication">

# Interactivity

<a href="http://bit.ly/2t1ppxh"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">selection</code></em><code
class="calibre23">.on()</code></a>  
<span id="app05.xhtml_idm140093174893280"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selection.on()"></span>Takes a
<span id="app05.xhtml_idm140093174892448"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="interactivity"
secondary="methods quick reference"></span>selection, and binds an event
listener:

``` calibre39
// Binds click functionality to #button
d3.select("#button")
  .on("click", function() { … });
```

<a href="http://bit.ly/2t1FJhC"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.select(this)</code></a>  
<span id="app05.xhtml_idm140093174882480"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.select(this)"></span>Within an
anonymous function, `this` refers to “the element being acted upon”:

``` calibre39
d3.selectAll("rect")
  .on("mouseover", function() {
      // The 'this' below refers to the rect underneath the mouse
      d3.select(this).classed("highlight", true);
  });
```

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Numbers, Dates, and Times">

<div id="app05.xhtml_idm140093174677872" class="dedication">

# Numbers, Dates, and Times

<a href="http://bit.ly/2t1rg5f"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.range()</code></a>  
<span id="app05.xhtml_idm140093174569152"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.range()"></span>Generates an array of
sequential numbers:

``` calibre39
d3.range(5);
//Returns [0, 1, 2, 3, 4]
```

<a href="http://bit.ly/2t1Ftzo"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.format</code></a>  
<span id="app05.xhtml_idm140093174564016"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.format"></span>Creates a new number
formatter, for converting numbers to strings:

``` calibre39
var formatAsPercentage = d3.format(".1%");
formatAsPercentage(1.2);
//Returns "120.0%"
```

<div class="calibre27 note" data-type="note">

###### Note

See the <a href="http://bit.ly/2t1HPhu"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">API reference
for number formatting values</a>.

</div>

<a href="http://bit.ly/2t1Defp"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.timeParse</code></a>  
<span id="app05.xhtml_idm140093174551872"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.timeParse"></span>Creates a new time
parser, for converting strings to Date objects:

``` calibre39
var parseTime = d3.timeParse("%m/%d/%y");
parseTime("02/20/17");
//Could return: Mon Feb 20 2017 00:00:00 GMT-0800 (PST)
```

<a href="http://bit.ly/2t1undC"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">d3.timeFormat</code></a>  
<span id="app05.xhtml_idm140093174647056"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.timeFormat"></span>Creates a new time
formatter, for converting Date objects to strings:

``` calibre39
var formatTime = d3.timeFormat("%b %e");
formatTime(new Date);
//Returns today's date, e.g.: "Apr 28"
```

<div class="calibre27 note" data-type="note">

###### Note

See the <a href="http://bit.ly/2t1svRU"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">API reference
for time formatting values</a>.

</div>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Other Useful JavaScript">

<div id="app05.xhtml_idm140093174402736" class="dedication">

# Other Useful JavaScript

<a href="https://mzl.la/2t1NjJ5"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">parseInt()</code></a>  
Converts a <span id="app05.xhtml_idm140093174399408"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="JavaScript"
secondary="quick reference"></span><span id="app05.xhtml_idm140093174398400"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="parseInt()"></span>string (typically) to
an integer:

``` calibre39
parseInt("123")  // Returns 123
```

<a href="https://mzl.la/2t1JuDG"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">parseFloat()</code></a>  
<span id="app05.xhtml_idm140093174393664"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="parseFloat()"></span>Converts a string
(typically) to a floating-point (decimal) number:

``` calibre39
parseFloat("456.789")  // Returns 456.789
```

<a href="https://mzl.la/2t1w7na"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">+</code></a>  
The unary plus operator attempts to convert what follows it into a
number (like shorthand for `parseInt()` or `parseFloat()`):

``` calibre39
+"123"      // Returns 123
+"456.789"  // Returns 456.789
```

<a href="http://mzl.la/1nwbDYh"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">Math.random()</code></a>  
<span id="app05.xhtml_idm140093174463456"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Math.random()"></span>Returns a random
value between 0.0 (inclusive) and 1.0 (exclusive):

``` calibre39
Math.random() * 100  // Could return 61.87844036612…
```

<a href="https://mzl.la/2t1EeA9"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">Math.round()</code></a>  
<span id="app05.xhtml_idm140093174492368"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Math.round()"></span>Rounds a value to
the nearest integer (or, in the case of 0.5, to the nearest greater
integer value):

``` calibre39
Math.round(1.012)  // Returns 1
Math.round(1.5)    // Returns 2
Math.round(-1.5)   // Returns -1
```

<a href="https://mzl.la/2t1sttz"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">Math.ceil()</code></a>  
<span id="app05.xhtml_idm140093174354592"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Math.ceil()"></span>Rounds a value up to
the nearest integer:

``` calibre39
Math.ceil(23.011231444)  // Returns 24
```

<a href="https://mzl.la/2t1ksVy"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">Math.floor()</code></a>  
<span id="app05.xhtml_idm140093174330096"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Math.floor()"></span>Rounds a value down
to the nearest integer:

``` calibre39
Math.floor(61.87844036612)  // Returns 61
```

<a href="https://mzl.la/2t1EiQp"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">array</code></em><code
class="calibre23">.push()</code></a>  
<span id="app05.xhtml_idm140093174346992"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="array.push()"></span>Appends a new value
to an existing array:

``` calibre39
var numbers = [ 2, 3, 4, 5 ];
numbers.push(6);  // Now numbers is [ 2, 3, 4, 5, 6 ]
```

<a href="https://mzl.la/2t1wfTG"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em><code
class="calibre26">array</code></em><code
class="calibre23">.shift()</code></a>  
Removes the<span id="app05.xhtml_idm140093174194752"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Mquick21"></span><span id="app05.xhtml_idm140093174193744"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="D3method21"></span><span id="app05.xhtml_idm140093174192800"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="array.shift()"></span> first value from
an existing array, and returns that value:

``` calibre39
var animals = [ "dog", "cat", "bird" ];
animals.shift();  //Returns "dog"
//Now animals is [ "cat", "bird" ]
```

</div>

</div>

</div>

</div>

</div>

<span id="ix01.xhtml"></span>

<div id="ix01.xhtml_sbo-rt-content" class="calibre1">

<div class="section calibre2 index" data-type="index">

<div id="ix01.xhtml_idm140093174176800" class="dedication">

# Index

<div class="dedication" data-type="index">

<div class="dedication" data-type="indexdiv">

### <span class="keep-together" gentext="indexsymbols">Symbols</span>

- <span class="keep-together" data-type="index-term">+ (append
  operator)</span>, <a href="#ch06.xhtml_idm140093199239856"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Labels</a>
- <span class="keep-together" data-type="index-term">3D drawing</span>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208296896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Three-Dimensional</a>
  - <span class="keep-together"
    data-type="index-term">projections</span>,
    <a href="#ch14.xhtml_idm140093182528704"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Projections</a>
- <span class="keep-together" data-type="index-term">= (assignment
  operator)</span>, <a href="#ch03.xhtml_idm140093208305840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Variables</a>,
  <a href="#ch03.xhtml_idm140093206749088"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">if() only</a>
- <span class="keep-together" data-type="index-term">== (comparison
  operator)</span>, <a href="#ch03.xhtml_idm140093206940080"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Comparison Operators</a>,
  <a href="#ch03.xhtml_idm140093206643648"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">if() only</a>,
  <a href="#ch03.xhtml_idm140093205951616"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>

</div>

<div class="dedication" data-type="indexdiv">

### A

- <span class="keep-together"
  data-type="index-term">accessibility</span>,
  <a href="#ch10.xhtml_idm140093188684224"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Consideration for Touch Devices</a>
- <span class="keep-together" data-type="index-term">accessor
  functions</span>, <a href="#ch07.xhtml_idm140093198703040"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">d3.min() and d3.max()</a>,
  <a href="#ch09.xhtml_idm140093191411264"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Updating all references</a>
- <span class="keep-together"
  data-type="index-term">acknowledgments</span>,
  <a href="#preface01.xhtml_idm140093207895840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Acknowledgments</a>
- <span class="keep-together" data-type="index-term">active
  selection</span>, <a href="#ch12.xhtml_idm140093187296016"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Getting More Specific</a>
- <span class="keep-together" data-type="index-term">Adobe Flash
  Player</span>, <a href="#ch02.xhtml_idm140093208171904"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">alternate
  mappings</span>, <a href="#ch01_split_000.xhtml_idm140093208066240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why Write Code?</a>
- <span class="keep-together" data-type="index-term">ancestor
  elements</span>, <a href="#ch03.xhtml_idm140093210906560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">DOM</a>
- <span class="keep-together" data-type="index-term">anonymous
  functions</span>, <a href="#ch05.xhtml_idm140093203414416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">High-Functioning</a>,
  <a href="#ch09.xhtml_idm140093195050976"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interaction via Event Listeners</a>
- <span class="keep-together"
  data-type="index-term">antialiasing</span>,
  <a href="#ch08.xhtml_idm140093196415888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">Apache server
  software</span>, <a href="#ch03.xhtml_idm140093208195920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">append operators
  (+)</span>, <a href="#ch06.xhtml_idm140093199240592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Labels</a>
- <span class="keep-together" data-type="index-term">append()</span>,
  <a href="#ch05.xhtml_idm140093204272128"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">One Link at a Time</a>,
  <a href="#ch06.xhtml_idm140093201834336"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing SVGs</a>,
  <a href="#ch12.xhtml_idm140093186867760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Getting More Specific</a>,
  <a href="#app05.xhtml_idm140093176307536"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together" data-type="index-term">arbitrary order,
  overriding</span>, <a href="#ch09.xhtml_idm140093195579184"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Ordinal Scales, Explained</a>
- <span class="keep-together" data-type="index-term">area charts</span>,
  <a href="#ch11.xhtml_idm140093187867104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Area Charts</a>
- <span class="keep-together" data-type="index-term">arguments (input
  values)</span>, <a href="#ch03.xhtml_idm140093206535552"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Functions</a>,
  <a href="#ch05.xhtml_idm140093203309456"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">High-Functioning</a>
- <span class="keep-together"
  data-type="index-term">array.length</span>,
  <a href="#ch12.xhtml_idm140093186419488"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Merging Selections</a>
- <span class="keep-together"
  data-type="index-term">array.push()</span>,
  <a href="#app05.xhtml_idm140093174346992"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together"
  data-type="index-term">array.shift()</span>,
  <a href="#ch09.xhtml_idm140093191771200"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Making a smooth exit</a>,
  <a href="#app05.xhtml_idm140093174192800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together" data-type="index-term">arrays</span>,
  <a href="#ch03.xhtml_idm140093210086032"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Arrays</a>,
  <a href="#ch03.xhtml_idm140093207486624"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Objects and Arrays</a>,
  <a href="#ch03.xhtml_idm140093206485888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What arrays are made for</a>,
  <a href="#ch05.xhtml_idm140093204309520"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together" data-type="index-term">ascending order
  sort</span>, <a href="#ch10.xhtml_idm140093189619328"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">assignment operator
  (=)</span>, <a href="#ch03.xhtml_idm140093209713280"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Variables</a>,
  <a href="#ch03.xhtml_idm140093206749792"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">if() only</a>
- <span class="keep-together" data-type="index-term">asynchronous
  methods</span>, <a href="#ch05.xhtml_idm140093204183280"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">attr()</span>,
  <a href="#ch05.xhtml_idm140093203115296"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Beyond Text</a>,
  <a href="#ch06.xhtml_idm140093202996608"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Attributes</a>,
  <a href="#ch06.xhtml_idm140093201982352"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing SVGs</a>,
  <a href="#ch07.xhtml_idm140093198795760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Creating a Scale</a>,
  <a href="#ch08.xhtml_idm140093196618592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">attributes</span>
  - <span class="keep-together" data-type="index-term">assigning to HTML
    elements</span>, <a href="#ch03.xhtml_idm140093211182352"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Attributes</a>
  - <span class="keep-together" data-type="index-term">setting</span>,
    <a href="#ch06.xhtml_idm140093202997584"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Attributes</a>
  - <span class="keep-together" data-type="index-term">in SVG
    elements</span>, <a href="#ch06.xhtml_idm140093201993376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Drawing SVGs</a>
- <span class="keep-together" data-type="index-term">axes</span>
  - <span class="keep-together" data-type="index-term">creating
    generic</span>, <a href="#ch08.xhtml_idm140093196891408"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up an Axis</a>
  - <span class="keep-together" data-type="index-term">customizing tick
    number and value</span>, <a href="#ch08.xhtml_idm140093196374048"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Check for Ticks</a>
  - <span class="keep-together" data-type="index-term">dynamic and
    scalable</span>, <a href="#ch08.xhtml_idm140093196260880"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Final Touches</a>
  - <span class="keep-together" data-type="index-term">labeling</span>,
    <a href="#ch08.xhtml_idm140093195999264"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Formatting Tick Labels</a>
  - <span class="keep-together" data-type="index-term">methods quick
    reference</span>, <a href="#app05.xhtml_idm140093174959920"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Axes</a>
  - <span class="keep-together"
    data-type="index-term">positioning</span>,
    <a href="#ch08.xhtml_idm140093196661952"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
  - <span class="keep-together" data-type="index-term">vs.
    scales</span>, <a href="#ch07.xhtml_idm140093199049056"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scales</a>
  - <span class="keep-together" data-type="index-term">styling with
    CSS</span>, <a href="#ch08.xhtml_idm140093196461184"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
  - <span class="keep-together"
    data-type="index-term">time-based</span>,
    <a href="#ch08.xhtml_idm140093195961248"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Time-Based Axes</a>
  - <span class="keep-together" data-type="index-term">updating</span>,
    <a href="#ch09.xhtml_idm140093193555664"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating Axes</a>
  - <span class="keep-together" data-type="index-term">version 4.0
    changes</span>, <a href="#app02.xhtml_idm140093176617680"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Axes</a>
- <span class="keep-together" data-type="index-term">axis
  functions</span>, <a href="#ch08.xhtml_idm140093196907632"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Introducing Axes</a>
- <span class="keep-together"
  data-type="index-term">axis.scale()</span>,
  <a href="#app05.xhtml_idm140093174852624"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together"
  data-type="index-term">axis.ticks()</span>,
  <a href="#app05.xhtml_idm140093174814272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together"
  data-type="index-term">axis.tickValues()</span>,
  <a href="#app05.xhtml_idm140093174759776"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>

</div>

<div class="dedication" data-type="indexdiv">

### B

- <span class="keep-together" data-type="index-term">band scales</span>,
  <a href="#ch09.xhtml_idm140093195188288"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Referencing the Band Scale</a>
- <span class="keep-together" data-type="index-term">bar charts</span>
  (<span class="keep-together" gentext="see">see</span> also charts)
  - <span class="keep-together" data-type="index-term">adding color
    to</span>, <a href="#ch06.xhtml_idm140093200444928"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Color</a>
  - <span class="keep-together" data-type="index-term">adding labels
    to</span>, <a href="#ch06.xhtml_idm140093200339712"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Labels</a>
  - <span class="keep-together" data-type="index-term">scalable and
    flexible</span>, <a href="#ch09.xhtml_BCscal09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Modernizing the Bar Chart</a>-<a href="#ch09.xhtml_idm140093195114768"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Updates</a>
  - <span class="keep-together" data-type="index-term">simple</span>,
    <a href="#ch06.xhtml_idm140093202881728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Drawing divs</a>,
    <a href="#ch06.xhtml_BCcreate06"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Making a Bar Chart</a>-<a href="#ch06.xhtml_idm140093200450944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The New Chart</a>
  - <span class="keep-together" data-type="index-term">stacked</span>,
    <a href="#ch13.xhtml_BCstack13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stack Layout</a>-<a href="#ch13.xhtml_idm140093184057936"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stacked Areas</a>
  - <span class="keep-together" data-type="index-term">updating color
    of</span>, <a href="#ch09.xhtml_idm140093194647808"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating the Visuals</a>
  - <span class="keep-together" data-type="index-term">updating labels
    for</span>, <a href="#ch09.xhtml_idm140093194644384"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating the Visuals</a>
- <span class="keep-together" data-type="index-term">behaviors</span>
  - <span class="keep-together" data-type="index-term">binding to
    multiple elements with</span>,
    <a href="#ch10.xhtml_idm140093190633440"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing Behaviors</a>
  - <span class="keep-together" data-type="index-term">click to
    sort</span>, <a href="#ch10.xhtml_idm140093190022336"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Click to Sort</a>
  - <span class="keep-together" data-type="index-term">grouping SVG
    elements</span>, <a href="#ch10.xhtml_idm140093190031696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Grouping SVG Elements</a>
  - <span class="keep-together" data-type="index-term">hover to
    highlight</span>, <a href="#ch10.xhtml_idm140093190578736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">overlapping
    elements and</span>, <a href="#ch10.xhtml_idm140093190114048"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
- <span class="keep-together" data-type="index-term">bitmap map
  tiles</span>, <a href="#ch02.xhtml_idm140093207923840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">Bloch, Matt</span>,
  <a href="#ch14.xhtml_idm140093179639760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">MapShaper</a>
- <span class="keep-together" data-type="index-term">block-level
  elements</span>, <a href="#ch03.xhtml_idm140093210853760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">block-level
  scope</span>, <a href="#ch03.xhtml_idm140093205727920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Function-level scope</a>
- <span class="keep-together" data-type="index-term">blocks
  service</span>, <a href="#app04.xhtml_block20"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">bl.ocks.org</a>-<a href="#app04.xhtml_idm140093176343040"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">A Normal Web Server</a>
- <span class="keep-together" data-type="index-term">Bostock,
  Michael</span>, <a href="#preface01.xhtml_idm140093207803936"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What’s New in the Second Edition</a>,
  <a href="#preface01.xhtml_idm140093207884272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Acknowledgments</a>,
  <a href="#ch02.xhtml_idm140093207954800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Introducing D3</a>,
  <a href="#ch02.xhtml_idm140093208169600"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">box model</span>,
  <a href="#ch03.xhtml_idm140093210871440"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">browsers</span>
  - <span class="keep-together" data-type="index-term">development of
    interactivity</span>, <a href="#ch02.xhtml_idm140093207906720"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together" data-type="index-term">fundamentals
    of</span>, <a href="#ch03.xhtml_idm140093208194512"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Web</a>
  - <span class="keep-together" data-type="index-term">rendering</span>,
    <a href="#ch03.xhtml_idm140093210870768"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Rendering and the Box Model</a>
  - <span class="keep-together" data-type="index-term">support
    for</span>, <a href="#ch02.xhtml_idm140093207927168"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">SVG
    compatibility</span>, <a href="#ch03.xhtml_idm140093204732784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Compatibility</a>

</div>

<div class="dedication" data-type="indexdiv">

### C

- <span class="keep-together" data-type="index-term">callback
  functions</span>, <a href="#ch05.xhtml_idm140093204114816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>,
  <a href="#ch05.xhtml_idm140093203942560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">camelCase</span>,
  <a href="#app02.xhtml_idm140093176833712"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Namespace and camelCase</a>
- <span class="keep-together" data-type="index-term">Card,
  Stuart</span>, <a href="#ch02.xhtml_idm140093208177712"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">cartographic
  detail</span>, <a href="#ch14.xhtml_idm140093179666592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choose a Resolution</a>
- <span class="keep-together" data-type="index-term">cascading
  styles</span>, <a href="#ch03.xhtml_idm140093210199856"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Inheritance, Cascading, and Specificity</a>
  - (<span class="keep-together" gentext="see">see also</span> CSS
    (Cascading Style Sheets))
- <span class="keep-together" data-type="index-term">case
  studies</span>, <a href="#app01.xhtml_case17"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Case Studies</a>-<a href="#app01.xhtml_idm140093176888096"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">“Data Sketches” Series</a>
  - <span class="keep-together" data-type="index-term">“Close
    Votes”</span>, <a href="#app01.xhtml_idm140093177414944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Case Studies</a>
  - <span class="keep-together" data-type="index-term">“Data Sketches”
    series</span>, <a href="#app01.xhtml_idm140093176955296"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“Weather Circles”</a>
  - <span class="keep-together" data-type="index-term">“Explained
    Visually” series</span>, <a href="#app01.xhtml_idm140093177171664"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“What Size Am I?”</a>
  - <span class="keep-together" data-type="index-term">“Farmers'
    Markets” series</span>, <a href="#app01.xhtml_idm140093177063968"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“Workers’ Comp Benefits: How Much Is a Limb
    Worth?”</a>
  - <span class="keep-together" data-type="index-term">“Weather
    Circles”</span>, <a href="#app01.xhtml_idm140093177025104"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“Farmers’ Markets” Series</a>
  - <span class="keep-together" data-type="index-term">“What Size Am
    I?”</span>, <a href="#app01.xhtml_idm140093177228656"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“Close Votes”</a>
  - <span class="keep-together" data-type="index-term">“Worker's Comp
    Benefits”</span>, <a href="#app01.xhtml_idm140093177114896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">“Explained Visually” Series</a>
- <span class="keep-together" data-type="index-term">centroids</span>,
  <a href="#ch13.xhtml_idm140093184876544"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">chaining
  methods</span>
  - <span class="keep-together" data-type="index-term">alternatives
    to</span>, <a href="#ch05.xhtml_idm140093204251712"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Going Chainless</a>
  - <span class="keep-together" data-type="index-term">chain
    syntax</span>, <a href="#ch05.xhtml_idm140093204479280"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Chaining Methods</a>
  - <span class="keep-together" data-type="index-term">examining the
    links</span>, <a href="#ch05.xhtml_idm140093204436688"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">One Link at a Time</a>
  - <span class="keep-together" data-type="index-term">input/output
    matching</span>, <a href="#ch05.xhtml_idm140093204258432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Handoff</a>
- <span class="keep-together" data-type="index-term">charts</span>
  (<span class="keep-together" gentext="see">see</span> also bar charts)
  - <span class="keep-together" data-type="index-term">adding headlines
    and frames</span>, <a href="#ch16.xhtml_idm140093177454048"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Provide Context</a>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208151312"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Easy Charts</a>
  - <span class="keep-together" data-type="index-term">area
    charts</span>, <a href="#ch11.xhtml_idm140093187866368"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Area Charts</a>
  - <span class="keep-together" data-type="index-term">column
    charts</span>, <a href="#ch06.xhtml_idm140093202880784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Drawing divs</a>
  - <span class="keep-together" data-type="index-term">doughnut
    charts</span>, <a href="#ch13.xhtml_idm140093184871344"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
  - <span class="keep-together" data-type="index-term">general-use
    libraries for</span>, <a href="#ch02.xhtml_idm140093208285056"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">General-use charting libraries</a>
  - <span class="keep-together" data-type="index-term">line
    charts</span>, <a href="#ch11.xhtml_Cline11"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Line Charts</a>-<a href="#ch11.xhtml_idm140093187870848"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Visuals</a>
  - <span class="keep-together" data-type="index-term">multiple on one
    page</span>, <a href="#ch16.xhtml_idm140093177325888"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Provide Context</a>
  - <span class="keep-together" data-type="index-term">pie
    charts</span>, <a href="#ch13.xhtml_Cpie13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
  - <span class="keep-together" data-type="index-term">ring
    charts</span>, <a href="#ch13.xhtml_idm140093184772976"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">child
  elements</span>, <a href="#ch03.xhtml_idm140093210907904"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">DOM</a>
- <span class="keep-together" data-type="index-term">choropleth
  maps</span>, <a href="#ch14.xhtml_idm140093182397088"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choropleth</a>
- <span class="keep-together" data-type="index-term">circles,
  drawing</span>, <a href="#ch06.xhtml_idm140093201651376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data-Driven Shapes</a>
- <span class="keep-together" data-type="index-term">cities, adding to
  maps</span>, <a href="#ch14.xhtml_idm140093181846544"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">class
  selectors</span>, <a href="#ch03.xhtml_idm140093210475920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selectors</a>
- <span class="keep-together" data-type="index-term">classed()</span>,
  <a href="#ch06.xhtml_idm140093202745264"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">A Note on Classes</a>
- <span class="keep-together" data-type="index-term">classes</span>
  - <span class="keep-together" data-type="index-term">adding to
    elements</span>, <a href="#ch06.xhtml_idm140093202779440"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Classes</a>
  - <span class="keep-together" data-type="index-term">identifying
    elements with</span>, <a href="#ch03.xhtml_idm140093211132608"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Classes and IDs</a>
  - <span class="keep-together" data-type="index-term">vs.
    styles</span>, <a href="#ch06.xhtml_idm140093202756224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Classes</a>
- <span class="keep-together" data-type="index-term">click
  events</span>, <a href="#ch09.xhtml_idm140093195045744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interaction via Event Listeners</a>,
  <a href="#ch10.xhtml_idm140093190487504"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Binding Event Listeners</a>,
  <a href="#ch10.xhtml_idm140093188644448"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Consideration for Touch Devices</a>
- <span class="keep-together" data-type="index-term">click to
  sort</span>, <a href="#ch10.xhtml_idm140093190021328"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">clipping
  paths</span>, <a href="#ch09.xhtml_idm140093192681008"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Containing visual elements with clipping
  paths</a>, <a href="#ch11.xhtml_idm140093187438944"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Area Charts</a>
- <span class="keep-together" data-type="index-term">code examples,
  obtaining and using</span>,
  <a href="#ch01_split_002.xhtml_idm140093208042816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Using Sample Code</a>,
  <a href="#ch04.xhtml_idm140093204793360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Referencing D3</a>,
  <a href="#app04.xhtml_idm140093176473920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Sharing Your Code</a>
- <span class="keep-together" data-type="index-term">code
  sharing</span>, <a href="#app04.xhtml_idm140093176473168"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Sharing Your Code</a>
- <span class="keep-together" data-type="index-term">coding tips</span>
  - <span class="keep-together" data-type="index-term">chaining
    methods</span>, <a href="#ch05.xhtml_idm140093204257424"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Handoff</a>
  - <span class="keep-together" data-type="index-term">D3 chained
    syntax</span>, <a href="#ch12.xhtml_idm140093186945488"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Getting More Specific</a>
  - <span class="keep-together" data-type="index-term">deconstructing
    code</span>, <a href="#ch05.xhtml_idm140093204422448"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">One Link at a Time</a>
  - <span class="keep-together" data-type="index-term">increasing
    legibility</span>, <a href="#ch05.xhtml_idm140093204454720"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Chaining Methods</a>
  - <span class="keep-together" data-type="index-term">integrated design
    and development</span>, <a href="#ch16.xhtml_idm140093177263952"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Dancing Versus Gardening</a>
  - <span class="keep-together" data-type="index-term">limit to active
    transitions</span>, <a href="#ch09.xhtml_idm140093193039904"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Warning: Start carefully</a>
  - <span class="keep-together" data-type="index-term">styling SVG
    elements</span>, <a href="#ch08.xhtml_idm140093196528288"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
  - <span class="keep-together" data-type="index-term">using functions
    to hold data</span>, <a href="#ch05.xhtml_idm140093203185840"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Wants to Be Held</a>
- <span class="keep-together" data-type="index-term">color
  property</span>, <a href="#ch08.xhtml_idm140093196526912"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">colors</span>
  - <span class="keep-together" data-type="index-term">adding to bar
    charts</span>, <a href="#ch06.xhtml_idm140093200445936"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Color</a>
  - <span class="keep-together" data-type="index-term">adding to
    SVG</span>, <a href="#ch06.xhtml_idm140093201322208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pretty Colors, Oooh!</a>
  - <span class="keep-together"
    data-type="index-term">categorical</span>,
    <a href="#ch13.xhtml_idm140093184979264"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">column
  charts</span>, <a href="#ch06.xhtml_idm140093202882464"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing divs</a>
- <span class="keep-together" data-type="index-term">comments</span>
  - <span class="keep-together" data-type="index-term">CSS</span>,
    <a href="#ch03.xhtml_idm140093210370304"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Properties and Values</a>
  - <span class="keep-together" data-type="index-term">HTML</span>,
    <a href="#ch03.xhtml_idm140093210913840"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Comments</a>
  - <span class="keep-together"
    data-type="index-term">JavaScript</span>,
    <a href="#ch03.xhtml_idm140093206420384"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Functions</a>
- <span class="keep-together" data-type="index-term">comments and
  questions</span>, <a href="#preface01.xhtml_idm140093214391808"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">How to Contact Us</a>
- <span class="keep-together" data-type="index-term">communication
  protocols</span>, <a href="#ch03.xhtml_idm140093208186672"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">comparator
  functions</span>, <a href="#ch10.xhtml_idm140093189913456"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">comparison operator
  (==)</span>, <a href="#ch03.xhtml_idm140093206939440"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Comparison Operators</a>,
  <a href="#ch03.xhtml_idm140093206748416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">if() only</a>,
  <a href="#ch03.xhtml_idm140093205952320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>
- <span class="keep-together" data-type="index-term">console.log</span>,
  <a href="#ch11.xhtml_idm140093188434048"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data Preparation</a>,
  <a href="#ch12.xhtml_idm140093186749184"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Enter, Merge, and Exit</a>
- <span class="keep-together"
  data-type="index-term">console.table()</span>,
  <a href="#ch11.xhtml_idm140093188551424"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data Preparation</a>
- <span class="keep-together" data-type="index-term">contact
  information</span>, <a href="#preface01.xhtml_idm140093214392544"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">How to Contact Us</a>
- <span class="keep-together" data-type="index-term">containers</span>,
  <a href="#ch03.xhtml_idm140093211024720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Classes and IDs</a>,
  <a href="#ch03.xhtml_idm140093209957936"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Variables</a>
- <span class="keep-together" data-type="index-term">continuous
  ranges</span>, <a href="#ch09.xhtml_idm140093195519424"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Starting Your Own Band</a>
- <span class="keep-together" data-type="index-term">control
  structures</span>, <a href="#ch03.xhtml_idm140093206781376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Control Structures</a>
- <span class="keep-together" data-type="index-term">coordinate values,
  locating</span>, <a href="#ch14.xhtml_idm140093182889408"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">JSON, Meet GeoJSON</a>,
  <a href="#ch14.xhtml_idm140093181840368"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">CSS (Cascading
  Style Sheets)</span>
  - <span class="keep-together" data-type="index-term">applying to
    axes</span>, <a href="#ch08.xhtml_idm140093196460176"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
  - <span class="keep-together" data-type="index-term">cascading</span>,
    <a href="#ch03.xhtml_idm140093210200832"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Inheritance, Cascading, and Specificity</a>
  - <span class="keep-together" data-type="index-term">comments</span>,
    <a href="#ch03.xhtml_idm140093210371216"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Properties and Values</a>
  - <span class="keep-together" data-type="index-term">CSS rules</span>,
    <a href="#ch03.xhtml_idm140093210739920"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">CSS</a>
  - <span class="keep-together" data-type="index-term">hover
    effect</span>, <a href="#ch10.xhtml_idm140093190574944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together"
    data-type="index-term">inheritance</span>,
    <a href="#ch03.xhtml_idm140093210161216"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Inheritance, Cascading, and Specificity</a>
  - <span class="keep-together" data-type="index-term">properties and
    values</span>, <a href="#ch03.xhtml_idm140093210516720"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Properties and Values</a>,
    <a href="#ch05.xhtml_idm140093203113216"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Beyond Text</a>
  - <span class="keep-together" data-type="index-term">purpose
    of</span>, <a href="#ch03.xhtml_idm140093210849920"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">CSS</a>
  - <span class="keep-together" data-type="index-term">referencing
    styles</span>, <a href="#ch03.xhtml_idm140093210365296"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Referencing Styles</a>
  - <span class="keep-together" data-type="index-term">selectors and
    properties</span>, <a href="#ch03.xhtml_idm140093210799360"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">CSS</a>
  - <span class="keep-together"
    data-type="index-term">specificity</span>,
    <a href="#ch03.xhtml_idm140093209976864"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Inheritance, Cascading, and Specificity</a>
  - <span class="keep-together" data-type="index-term">styling SVG
    elements with</span>, <a href="#ch03.xhtml_idm140093205203008"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Styling SVG Elements</a>
- <span class="keep-together" data-type="index-term">CSV
  (comma-separated value files)</span>,
  <a href="#ch05.xhtml_idm140093204546720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>,
  <a href="#ch05.xhtml_idm140093204308848"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>

</div>

<div class="dedication" data-type="indexdiv">

### D

- <span class="keep-together" data-type="index-term">D3</span>
  - <span class="keep-together" data-type="index-term">additional
    resources for learning</span>, <a href="#app03.xhtml_D3resou19"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Further Study</a>-<a href="#app03.xhtml_idm140093176481792"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">D3-Related</a>
  - <span class="keep-together" data-type="index-term">alternative
    tools</span>, <a href="#ch02.xhtml_D3alt02"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Alternatives</a>-<a href="#ch02.xhtml_idm140093208218512"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">More specialized tools</a>
  - <span class="keep-together" data-type="index-term">browser
    support</span>, <a href="#ch02.xhtml_idm140093207928176"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">community
    support</span>, <a href="#app04.xhtml_idm140093176471952"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Sharing Your Code</a>
  - <span class="keep-together" data-type="index-term">core concepts
    of</span>, <a href="#ch06.xhtml_idm140093199063504"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Next Steps</a>
  - <span class="keep-together" data-type="index-term">data sharing
    in</span>, <a href="#ch02.xhtml_idm140093207915376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">development
    of</span>, <a href="#ch02.xhtml_idm140093207909856"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together"
    data-type="index-term">downloading</span>,
    <a href="#ch02.xhtml_idm140093207954064"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing D3</a>,
    <a href="#ch04.xhtml_idm140093204721120"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Downloading D3</a>
  - <span class="keep-together" data-type="index-term">explanatory
    visualizations with</span>, <a href="#ch02.xhtml_idm140093207932736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">geomapping
    in</span>, <a href="#ch02.xhtml_idm140093207920144"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">increased demand
    for D3 skills</span>, <a href="#preface01.xhtml_idm140093207815728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preface</a>
  - <span class="keep-together" data-type="index-term">meaning of
    name</span>, <a href="#ch02.xhtml_idm140093207959648"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing D3</a>
  - <span class="keep-together" data-type="index-term">methods quick
    reference</span>, <a href="#app05.xhtml_D3method21"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Quick Reference</a>-<a href="#app05.xhtml_idm140093174193744"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Useful JavaScript</a>
  - <span class="keep-together"
    data-type="index-term">microlibraries</span>,
    <a href="#app02.xhtml_idm140093176879520"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Modularity</a>
  - <span class="keep-together" data-type="index-term">philosophy
    underlying</span>, <a href="#ch02.xhtml_idm140093208162784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together" data-type="index-term">prerequisites to
    learning</span>, <a href="#ch01_split_001.xhtml_idm140093221163728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What This Book Is</a>
  - <span class="keep-together" data-type="index-term">project template
    creation</span>, <a href="#ch04.xhtml_idm140093204647424"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Referencing D3</a>
  - <span class="keep-together"
    data-type="index-term">referencing</span>,
    <a href="#ch04.xhtml_idm140093204799200"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Referencing D3</a>
  - <span class="keep-together" data-type="index-term">tools built
    with</span>, <a href="#ch02.xhtml_D3tools02"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">General-use charting libraries</a>-<a href="#ch02.xhtml_idm140093208217568"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">More specialized tools</a>
  - <span class="keep-together" data-type="index-term">tutorials</span>,
    <a href="#preface01.xhtml_idm140093207813744"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preface</a>
  - <span class="keep-together" data-type="index-term">underlying
    processes</span>, <a href="#ch02.xhtml_idm140093207946976"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Does</a>
  - <span class="keep-together" data-type="index-term">version 4.0
    changes</span>, <a href="#preface01.xhtml_idm140093207804944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What’s New in the Second Edition</a>,
    <a href="#ch01_split_002.xhtml_idm140093208039632"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Using Sample Code</a>,
    <a href="#app02.xhtml_D3change18"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What’s New in 4.0</a>-<a href="#app02.xhtml_idm140093176599536"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Zooming</a>
  - <span class="keep-together" data-type="index-term">web server set
    up</span>, <a href="#ch04.xhtml_D3webserv04"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up a Web Server</a>-<a href="#ch04.xhtml_idm140093204559472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Diving In</a>
- <span class="keep-together" data-type="index-term">d3.arc()</span>,
  <a href="#ch13.xhtml_idm140093185367616"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">d3.area()</span>,
  <a href="#ch11.xhtml_idm140093187861600"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Area Charts</a>
- <span class="keep-together"
  data-type="index-term">d3.axisBottom</span>,
  <a href="#ch08.xhtml_idm140093196898064"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>,
  <a href="#app05.xhtml_idm140093174961392"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together" data-type="index-term">d3.axisLeft</span>,
  <a href="#ch08.xhtml_idm140093196897392"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>,
  <a href="#app05.xhtml_idm140093174960720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together"
  data-type="index-term">d3.axisRight</span>,
  <a href="#ch08.xhtml_idm140093196896720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>,
  <a href="#app05.xhtml_idm140093174962064"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together" data-type="index-term">d3.axisTop</span>,
  <a href="#ch08.xhtml_idm140093196896048"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>,
  <a href="#app05.xhtml_idm140093174962768"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together" data-type="index-term">d3.csv()</span>,
  <a href="#ch05.xhtml_idm140093204143584"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>,
  <a href="#ch05.xhtml_idm140093204073040"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>,
  <a href="#ch16.xhtml_idm140093179300800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Load and Parse the Data</a>,
  <a href="#app05.xhtml_idm140093175559808"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">d3.csvParseRows()</span>,
  <a href="#ch16.xhtml_idm140093179276864"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Load and Parse the Data</a>
- <span class="keep-together" data-type="index-term">d3.drag()</span>,
  <a href="#ch13.xhtml_idm140093183321280"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Draggable Nodes</a>
- <span class="keep-together"
  data-type="index-term">d3.easeBounceOut</span>,
  <a href="#ch09.xhtml_idm140093193911696"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">ease()-y Does It</a>
- <span class="keep-together"
  data-type="index-term">d3.easeCubicInOut</span>,
  <a href="#ch09.xhtml_idm140093193910960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">ease()-y Does It</a>
- <span class="keep-together"
  data-type="index-term">d3.forceSimulation()</span>,
  <a href="#ch13.xhtml_idm140093183899376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Defining the Force Simulation</a>
- <span class="keep-together" data-type="index-term">d3.format</span>,
  <a href="#app05.xhtml_idm140093174564016"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Numbers, Dates, and Times</a>
- <span class="keep-together" data-type="index-term">d3.js</span>
  (<span class="keep-together" gentext="see">see</span> D3)
- <span class="keep-together" data-type="index-term">d3.json()</span>,
  <a href="#ch05.xhtml_idm140093203783136"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading JSON data</a>,
  <a href="#ch14.xhtml_idm140093182870704"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Paths</a>,
  <a href="#app05.xhtml_idm140093175517856"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together" data-type="index-term">d3.line()</span>,
  <a href="#ch11.xhtml_idm140093188344320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Line ’em Up</a>
- <span class="keep-together" data-type="index-term">d3.max()</span>,
  <a href="#ch07.xhtml_idm140093198888160"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">d3.min() and d3.max()</a>,
  <a href="#app05.xhtml_idm140093174973680"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together" data-type="index-term">d3.min()</span>,
  <a href="#ch07.xhtml_idm140093198888896"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">d3.min() and d3.max()</a>,
  <a href="#app05.xhtml_idm140093175090752"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together" data-type="index-term">d3.pie()</span>,
  <a href="#ch13.xhtml_idm140093185477760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">d3.range()</span>,
  <a href="#ch09.xhtml_idm140093195532128"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Ordinal Scales, Explained</a>,
  <a href="#app05.xhtml_idm140093174569152"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Numbers, Dates, and Times</a>
- <span class="keep-together"
  data-type="index-term">d3.request()</span>,
  <a href="#ch16.xhtml_idm140093179297072"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Load and Parse the Data</a>,
  <a href="#app05.xhtml_idm140093175499104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together" data-type="index-term">d3.scale()</span>,
  <a href="#ch14.xhtml_idm140093182834560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Projections</a>
- <span class="keep-together"
  data-type="index-term">d3.scaleLinear()</span>,
  <a href="#ch07.xhtml_idm140093197662128"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Methods</a>,
  <a href="#app05.xhtml_idm140093175211840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together" data-type="index-term">d3.select()</span>,
  <a href="#ch05.xhtml_idm140093204432320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">One Link at a Time</a>,
  <a href="#ch05.xhtml_idm140093203895632"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Please Make Your Selection</a>,
  <a href="#ch12.xhtml_idm140093187505760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">A Closer Look at Selections</a>,
  <a href="#ch12.xhtml_idm140093187026464"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Getting More Specific</a>,
  <a href="#app05.xhtml_idm140093176333648"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">d3.select(this)</span>,
  <a href="#app05.xhtml_idm140093174882480"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interactivity</a>
- <span class="keep-together"
  data-type="index-term">d3.selectAll()</span>,
  <a href="#app05.xhtml_idm140093176323904"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together" data-type="index-term">d3.stack()</span>,
  <a href="#ch13.xhtml_idm140093184858608"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Stack Layout</a>
- <span class="keep-together" data-type="index-term">d3.style()</span>,
  <a href="#ch05.xhtml_idm140093203113888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Beyond Text</a>,
  <a href="#ch06.xhtml_idm140093202545952"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Styles</a>,
  <a href="#ch12.xhtml_idm140093186232336"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Filtering Selections Based on Data</a>
- <span class="keep-together" data-type="index-term">d3.text()</span>,
  <a href="#ch05.xhtml_idm140093204264208"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">One Link at a Time</a>,
  <a href="#ch06.xhtml_idm140093200306416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Labels</a>
- <span class="keep-together"
  data-type="index-term">d3.timeFormat</span>,
  <a href="#app05.xhtml_idm140093174647056"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Numbers, Dates, and Times</a>
- <span class="keep-together"
  data-type="index-term">d3.timeParse</span>,
  <a href="#ch07.xhtml_idm140093197429376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Converting strings to dates</a>,
  <a href="#app05.xhtml_idm140093174551872"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Numbers, Dates, and Times</a>
- <span class="keep-together" data-type="index-term">d3.tsv()</span>,
  <a href="#ch05.xhtml_idm140093203850784"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">data</span>
  - <span class="keep-together" data-type="index-term">binding to
    elements</span>, <a href="#ch05.xhtml_Dbind05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Data</a>-<a href="#ch05.xhtml_idm140093202911184"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Beyond Text</a>,
    <a href="#ch09.xhtml_Dbind09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Joins with Keys</a>-<a href="#ch09.xhtml_idm140093190965472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exit transition</a>
  - <span class="keep-together" data-type="index-term">dealing with
    missing data</span>, <a href="#ch11.xhtml_idm140093188217072"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Dealing with Missing Data</a>
  - <span class="keep-together" data-type="index-term">definition of
    term</span>, <a href="#ch05.xhtml_idm140093204553920"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data</a>
  - <span class="keep-together" data-type="index-term">generating page
    elements for</span>, <a href="#ch05.xhtml_Dpage05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Generating Page Elements</a>-<a href="#ch05.xhtml_idm140093204333680"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Going Chainless</a>
  - <span class="keep-together" data-type="index-term">generating
    random</span>, <a href="#ch06.xhtml_idm140093202063312"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Random Data</a>
  - <span class="keep-together" data-type="index-term">holding with
    functions</span>, <a href="#ch05.xhtml_idm140093203184864"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Wants to Be Held</a>
  - <span class="keep-together" data-type="index-term">sorting</span>,
    <a href="#ch10.xhtml_idm140093190019040"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Click to Sort</a>
  - <span class="keep-together" data-type="index-term">storage
    forms</span>, <a href="#ch05.xhtml_idm140093204552320"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data</a>
  - <span class="keep-together" data-type="index-term">supported file
    types</span>, <a href="#ch05.xhtml_idm140093204548304"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data</a>,
    <a href="#ch05.xhtml_idm140093204310528"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data</a>
  - <span class="keep-together" data-type="index-term">updating
    of</span> (<span class="keep-together" gentext="see">see</span>
    updates)
  - <span class="keep-together" data-type="index-term">using bound
    data</span>, <a href="#ch05.xhtml_idm140093203472016"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Using Your Data</a>
  - <span class="keep-together" data-type="index-term">verifying</span>,
    <a href="#ch05.xhtml_idm140093203960640"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">data arrays</span>,
  <a href="#ch05.xhtml_idm140093204130080"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">data binding</span>
  - <span class="keep-together" data-type="index-term">CSV files</span>,
    <a href="#ch05.xhtml_idm140093204218544"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>
  - <span class="keep-together" data-type="index-term">data()
    method</span>, <a href="#ch05.xhtml_idm140093204318208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">In a Bind</a>
  - <span class="keep-together" data-type="index-term">handling loading
    errors</span>, <a href="#ch05.xhtml_idm140093204184224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>
  - <span class="keep-together" data-type="index-term">inspecting bound
    data</span>, <a href="#ch05.xhtml_idm140093203586864"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Bound and Determined</a>
  - <span class="keep-together" data-type="index-term">JSON
    files</span>, <a href="#ch05.xhtml_idm140093203782464"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading JSON data</a>
  - <span class="keep-together" data-type="index-term">purpose
    of</span>, <a href="#ch05.xhtml_idm140093204323472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Data</a>
  - <span class="keep-together" data-type="index-term">selecting
    elements</span>, <a href="#ch05.xhtml_idm140093203887584"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Please Make Your Selection</a>
    - (<span class="keep-together" gentext="see">see also</span>
      selections)
  - <span class="keep-together" data-type="index-term">using bound
    data</span>, <a href="#ch05.xhtml_idm140093203474240"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Using Your Data</a>
- <span class="keep-together" data-type="index-term">data joins</span>
  - <span class="keep-together" data-type="index-term">controlling order
    of</span>, <a href="#ch09.xhtml_idm140093191752704"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Joins with Keys</a>
  - <span class="keep-together" data-type="index-term">defining key
    functions</span>, <a href="#ch09.xhtml_idm140093191073632"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Key functions</a>
  - <span class="keep-together" data-type="index-term">enter, merge, and
    exit selections</span>, <a href="#ch12.xhtml_DJenter12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Enter, Merge, and Exit</a>-<a href="#ch12.xhtml_idm140093186243728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Exit Selection</a>
  - <span class="keep-together" data-type="index-term">exit
    transition</span>, <a href="#ch09.xhtml_idm140093191314432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exit transition</a>
  - <span class="keep-together" data-type="index-term">preparing data
    for</span>, <a href="#ch09.xhtml_idm140093191743568"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preparing the data</a>
  - <span class="keep-together" data-type="index-term">updating
    references</span>, <a href="#ch09.xhtml_idm140093191418992"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating all references</a>
- <span class="keep-together" data-type="index-term">data loading</span>
  - <span class="keep-together" data-type="index-term">error
    handling</span>, <a href="#ch05.xhtml_idm140093204185232"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>
  - <span class="keep-together" data-type="index-term">project
    walk-through example</span>,
    <a href="#ch16.xhtml_idm140093179306688"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Load and Parse the Data</a>
- <span class="keep-together" data-type="index-term">data mapping</span>
  - <span class="keep-together" data-type="index-term">benefits of
    computation</span>,
    <a href="#ch01_split_000.xhtml_idm140093208067696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why Write Code?</a>
  - <span class="keep-together" data-type="index-term">binding data
    for</span>, <a href="#ch05.xhtml_DMbind05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Data</a>-<a href="#ch05.xhtml_idm140093202909264"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Beyond Text</a>
  - <span class="keep-together" data-type="index-term">design
    application in</span>, <a href="#ch02.xhtml_idm140093207936992"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Does</a>
- <span class="keep-together" data-type="index-term">data
  sharing</span>, <a href="#ch02.xhtml_idm140093207914080"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">data
  strings</span>, <a href="#ch05.xhtml_idm140093204076816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading CSV data</a>
- <span class="keep-together" data-type="index-term">data values,
  encoding as color</span>, <a href="#ch06.xhtml_idm140093200436256"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Color</a>
- <span class="keep-together" data-type="index-term">data
  visualization</span>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_DValt02"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Alternatives</a>-<a href="#ch02.xhtml_idm140093208219488"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">More specialized tools</a>
  - <span class="keep-together" data-type="index-term">benefits of
    interactivity</span>,
    <a href="#ch01_split_000.xhtml_idm140093221177456"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why Interactive?</a>
  - <span class="keep-together" data-type="index-term">definition
    of</span>, <a href="#ch01_split_000.xhtml_idm140093208077856"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why Data Visualization?</a>
  - <span class="keep-together" data-type="index-term">early
    applications for</span>, <a href="#ch02.xhtml_idm140093208176368"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together" data-type="index-term">exporting to
    other file types</span>, <a href="#ch15.xhtml_DVexport15"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exporting</a>-<a href="#ch15.xhtml_idm140093179340928"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>
  - <span class="keep-together" data-type="index-term">posting and
    finding jobs in</span>,
    <a href="#preface01.xhtml_idm140093207814704"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preface</a>,
    <a href="#app03.xhtml_idm140093176478736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Getting a Job and Geeking Out</a>
  - <span class="keep-together" data-type="index-term">rewards
    of</span>, <a href="#ch01_split_000.xhtml_idm140093208060896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why Write Code?</a>
  - <span class="keep-together" data-type="index-term">rhetoric-design
    decisions</span>, <a href="#ch11.xhtml_idm140093188105792"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Visuals</a>
  - <span class="keep-together" data-type="index-term">web-standard
    technologies and</span>,
    <a href="#ch01_split_000.xhtml_idm140093221169840"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why on the Web?</a>
- <span class="keep-together" data-type="index-term">data()</span>,
  <a href="#ch03.xhtml_idm140093206483088"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What arrays are made for</a>,
  <a href="#ch05.xhtml_idm140093204318944"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">In a Bind</a>,
  <a href="#ch05.xhtml_idm140093203429744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Using Your Data</a>,
  <a href="#ch06.xhtml_idm140093202477920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Power of data()</a>,
  <a href="#ch09.xhtml_idm140093195024416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Changing the Data</a>,
  <a href="#ch11.xhtml_idm140093188232720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Line ’em Up</a>
- <span class="keep-together" data-type="index-term">Data-Driven
  Documents</span> (<span class="keep-together" gentext="see">see</span>
  D3)
- <span class="keep-together" data-type="index-term">data-driven
  shapes</span>, <a href="#ch06.xhtml_idm140093201664320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data-Driven Shapes</a>
- <span class="keep-together" data-type="index-term">datum()</span>,
  <a href="#ch11.xhtml_idm140093188232016"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Line ’em Up</a>
- <span class="keep-together" data-type="index-term">Davies,
  Jason</span>, <a href="#ch14.xhtml_idm140093182403504"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Projections</a>
- <span class="keep-together" data-type="index-term">defined()</span>,
  <a href="#ch11.xhtml_idm140093188157792"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dealing with Missing Data</a>
- <span class="keep-together" data-type="index-term">degrees vs.
  radians</span>, <a href="#ch13.xhtml_idm140093185468256"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">descendant
  elements</span>, <a href="#ch03.xhtml_idm140093210905072"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">DOM</a>
- <span class="keep-together" data-type="index-term">descendant
  selectors</span>, <a href="#ch03.xhtml_idm140093210651104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selectors</a>
- <span class="keep-together" data-type="index-term">descending order
  sort</span>, <a href="#ch10.xhtml_idm140093189618720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">design
  systems</span>, <a href="#ch01_split_000.xhtml_idm140093208063728"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why Write Code?</a>
- <span class="keep-together" data-type="index-term">developer
  tools</span>, <a href="#ch03.xhtml_devtool03"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Developer Tools</a>-<a href="#ch03.xhtml_idm140093210876816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Developer Tools</a>
- <span class="keep-together" data-type="index-term">div element</span>,
  <a href="#ch03.xhtml_idm140093211026240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Classes and IDs</a>,
  <a href="#ch06.xhtml_idm140093202890224"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing divs</a>,
  <a href="#ch10.xhtml_idm140093189136032"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">HTML div Tooltips</a>
- <span class="keep-together" data-type="index-term">DOM (Document
  Object Model)</span>
  - <span class="keep-together" data-type="index-term">appending SVG
    elements with axis function</span>,
    <a href="#ch08.xhtml_idm140093196810000"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up an Axis</a>
  - <span class="keep-together" data-type="index-term">examining current
    state of</span>, <a href="#ch03.xhtml_idm140093210884224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Developer Tools</a>
  - <span class="keep-together" data-type="index-term">hierarchical
    structure</span>, <a href="#ch03.xhtml_idm140093210911072"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">DOM</a>
  - <span class="keep-together" data-type="index-term">interacting with
    event listeners</span>, <a href="#ch09.xhtml_idm140093195279696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Interaction via Event Listeners</a>
  - <span class="keep-together" data-type="index-term">styling with
    CSS</span>, <a href="#ch03.xhtml_idm140093210848944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">CSS</a>
- <span class="keep-together" data-type="index-term">domain
  names</span>, <a href="#ch03.xhtml_idm140093208183312"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">domain()</span>,
  <a href="#ch07.xhtml_idm140093197658128"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Methods</a>
- <span class="keep-together" data-type="index-term">doughnut
  charts</span>, <a href="#ch13.xhtml_idm140093184872080"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">drawing</span>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208113088"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Almost from Scratch</a>
  - <span class="keep-together" data-type="index-term">circles</span>,
    <a href="#ch06.xhtml_idm140093201650880"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data-Driven Shapes</a>
  - <span class="keep-together" data-type="index-term">irregular
    forms</span>, <a href="#ch11.xhtml_idm140093188674528"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Using Paths</a>,
    <a href="#ch13.xhtml_idm140093184875808"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
    - (<span class="keep-together" gentext="see">see also</span> paths)
  - <span class="keep-together"
    data-type="index-term">rectangles</span>,
    <a href="#ch06.xhtml_idm140093202888816"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Drawing divs</a>
  - <span class="keep-together" data-type="index-term">SVG overlapping
    shapes</span>, <a href="#ch03.xhtml_idm140093205262528"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Layering and Drawing Order</a>,
    <a href="#ch10.xhtml_idm140093190112144"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">3D
    drawing</span>, <a href="#ch02.xhtml_idm140093208294672"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Three-Dimensional</a>
- <span class="keep-together" data-type="index-term">drawing order, in
  SVG</span>, <a href="#ch03.xhtml_idm140093205267440"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Layering and Drawing Order</a>
- <span class="keep-together" data-type="index-term">dual
  encoding</span>, <a href="#ch06.xhtml_idm140093200434912"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Color</a>
- <span class="keep-together" data-type="index-term">duration()</span>,
  <a href="#ch09.xhtml_idm140093194555648"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">duration(), or How Long Is This Going to
  Take?</a>
- <span class="keep-together" data-type="index-term">dynamic
  axes</span>, <a href="#ch08.xhtml_idm140093196259872"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Final Touches</a>
- <span class="keep-together" data-type="index-term">dynamic
  paragraphs</span>, <a href="#ch05.xhtml_idm140093203713488"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Please Make Your Selection</a>,
  <a href="#ch05.xhtml_idm140093202913008"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Beyond Text</a>
- <span class="keep-together" data-type="index-term">dynamic
  scales</span>, <a href="#ch07.xhtml_idm140093198365872"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up Dynamic Scales</a>
- <span class="keep-together" data-type="index-term">dynamic
  typing</span>, <a href="#ch03.xhtml_idm140093206184720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>

</div>

<div class="dedication" data-type="indexdiv">

### E

- <span class="keep-together" data-type="index-term">each()</span>,
  <a href="#ch12.xhtml_idm140093185724960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">To each() Their Own</a>
- <span class="keep-together" data-type="index-term">easing</span>,
  <a href="#ch09.xhtml_idm140093194005776"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">ease()-y Does It</a>
- <span class="keep-together" data-type="index-term">edges</span>,
  <a href="#ch13.xhtml_idm140093184168832"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Force Layout</a>
- <span class="keep-together" data-type="index-term">elements</span>
  - <span class="keep-together" data-type="index-term">adding</span>,
    <a href="#ch09.xhtml_Eadd09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Kinds of Data Updates</a>-<a href="#ch09.xhtml_idm140093191888352"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Update</a>
  - <span class="keep-together" data-type="index-term">adding a class
    to</span>, <a href="#ch06.xhtml_idm140093202757168"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Classes</a>
  - <span class="keep-together" data-type="index-term">adding structure
    with</span>, <a href="#ch03.xhtml_idm140093211735744"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Structure with Elements</a>
  - <span class="keep-together" data-type="index-term">block-level
    elements</span>, <a href="#ch03.xhtml_idm140093210853024"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Rendering and the Box Model</a>
  - <span class="keep-together" data-type="index-term">common
    elements</span>, <a href="#ch03.xhtml_idm140093211302432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Common Elements</a>
  - <span class="keep-together" data-type="index-term">description
    of</span>, <a href="#ch03.xhtml_idm140093210909552"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">DOM</a>
  - <span class="keep-together" data-type="index-term">div
    element</span>, <a href="#ch03.xhtml_idm140093211025632"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Classes and IDs</a>,
    <a href="#ch10.xhtml_idm140093189135360"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">HTML div Tooltips</a>
  - <span class="keep-together" data-type="index-term">exiting
    elements</span>, <a href="#ch09.xhtml_idm140093191786912"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exit</a>
  - <span class="keep-together" data-type="index-term">generating page
    elements</span>, <a href="#ch05.xhtml_Egener05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Generating Page Elements</a>-<a href="#ch05.xhtml_idm140093204332800"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Going Chainless</a>
  - <span class="keep-together" data-type="index-term">inline
    elements</span>, <a href="#ch03.xhtml_idm140093210857728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Rendering and the Box Model</a>
  - <span class="keep-together" data-type="index-term">removing</span>,
    <a href="#ch09.xhtml_Eremov09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Removing Values (and Elements)</a>-<a href="#ch09.xhtml_idm140093191762112"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Making a smooth exit</a>
- <span class="keep-together" data-type="index-term">elements
  (SVG)</span>, <a href="#ch03.xhtml_idm140093205662496"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The SVG Element</a>,
  <a href="#ch06.xhtml_idm140093201990752"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing SVGs</a>,
  <a href="#ch08.xhtml_idm140093196740864"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>,
  <a href="#ch10.xhtml_idm140093190116512"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>,
  <a href="#ch11.xhtml_idm140093188673312"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Using Paths</a> (<span class="keep-together"
  gentext="see">see</span> also SVG (Scalable Vector Graphics))
- <span class="keep-together" data-type="index-term">encoding
  values</span>, <a href="#ch06.xhtml_idm140093200435584"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Color</a>
- <span class="keep-together" data-type="index-term">enter
  selections</span>, <a href="#ch12.xhtml_entsel12"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Enter Selection</a>-<a href="#ch12.xhtml_idm140093186438352"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Enter Selection</a>
- <span class="keep-together" data-type="index-term">enter()</span>,
  <a href="#ch05.xhtml_idm140093203711888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Please Make Your Selection</a>
- <span class="keep-together" data-type="index-term">errata</span>,
  <a href="#preface01.xhtml_idm140093214386432"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">How to Contact Us</a>,
  <a href="#ch01_split_002.xhtml_idm140093208031840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Using Sample Code</a>
- <span class="keep-together" data-type="index-term">event
  listeners</span>, <a href="#ch09.xhtml_idm140093195280368"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interaction via Event Listeners</a>,
  <a href="#ch10.xhtml_idm140093190668352"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Binding Event Listeners</a>,
  <a href="#ch10.xhtml_idm140093190627280"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Introducing Behaviors</a>
- <span class="keep-together" data-type="index-term">event model</span>,
  <a href="#ch10.xhtml_idm140093190666464"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Binding Event Listeners</a>
- <span class="keep-together" data-type="index-term">exit
  selection</span>, <a href="#ch09.xhtml_idm140093191879008"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Removing Values (and Elements)</a>,
  <a href="#ch12.xhtml_idm140093186253104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Exit Selection</a>
- <span class="keep-together" data-type="index-term">exiting
  elements</span>, <a href="#ch09.xhtml_idm140093191684000"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Exit</a>
- <span class="keep-together" data-type="index-term">exploratory vs.
  explanatory visualizations</span>,
  <a href="#ch02.xhtml_idm140093207931744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">exporting D3
  visualizations</span>
  - <span class="keep-together" data-type="index-term">bitmaps</span>,
    <a href="#ch15.xhtml_idm140093179386816"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Bitmaps</a>
  - <span class="keep-together" data-type="index-term">PDFs</span>,
    <a href="#ch15.xhtml_idm140093179377984"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">PDF</a>
  - <span class="keep-together" data-type="index-term">SVG
    format</span>, <a href="#ch15.xhtml_EXsvg1"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>-<a href="#ch15.xhtml_idm140093179339952"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>
- <span class="keep-together" data-type="index-term">external style
  sheets</span>, <a href="#ch03.xhtml_idm140093210316432"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Reference an external stylesheet from the
  HTML</a>

</div>

<div class="dedication" data-type="indexdiv">

### F

- <span class="keep-together" data-type="index-term">Flare</span>,
  <a href="#ch02.xhtml_idm140093208172640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">for loops</span>,
  <a href="#ch03.xhtml_idm140093206634224"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">for() now</a>,
  <a href="#ch06.xhtml_idm140093202169120"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Random Data</a>
- <span class="keep-together" data-type="index-term">force-directed
  layouts</span>
  - <span class="keep-together" data-type="index-term">creating visual
    elements</span>, <a href="#ch13.xhtml_idm140093183828832"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Creating the Visual Elements</a>
  - <span class="keep-together" data-type="index-term">draggable
    nodes</span>, <a href="#ch13.xhtml_idm140093183349456"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Draggable Nodes</a>
  - <span class="keep-together"
    data-type="index-term">initializing</span>,
    <a href="#ch13.xhtml_idm140093183900384"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Defining the Force Simulation</a>
  - <span class="keep-together" data-type="index-term">list of forces
    and options</span>, <a href="#ch13.xhtml_idm140093183841696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Defining the Force Simulation</a>
  - <span class="keep-together" data-type="index-term">network data
    preparation</span>, <a href="#ch13.xhtml_idm140093184160176"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preparing the Network Data</a>
  - <span class="keep-together" data-type="index-term">updating visuals
    over time</span>, <a href="#ch13.xhtml_idm140093183463040"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating Visuals over Time</a>
  - <span class="keep-together" data-type="index-term">uses for</span>,
    <a href="#ch13.xhtml_idm140093184054800"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Force Layout</a>
- <span class="keep-together" data-type="index-term">formatting
  functions, testing</span>, <a href="#ch08.xhtml_idm140093195967152"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Formatting Tick Labels</a>
- <span class="keep-together" data-type="index-term">frames</span>,
  <a href="#ch16.xhtml_idm140093177455392"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Provide Context</a>
- <span class="keep-together" data-type="index-term">function-level
  scope</span>, <a href="#ch03.xhtml_idm140093205732576"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Function-level scope</a>
- <span class="keep-together" data-type="index-term">functions</span>
  - <span class="keep-together" data-type="index-term">accessor
    functions</span>, <a href="#ch07.xhtml_idm140093198702544"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">d3.min() and d3.max()</a>,
    <a href="#ch09.xhtml_idm140093191235472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating all references</a>
  - <span class="keep-together" data-type="index-term">anonymous
    functions</span>, <a href="#ch05.xhtml_idm140093203413136"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">High-Functioning</a>,
    <a href="#ch09.xhtml_idm140093195051872"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Interaction via Event Listeners</a>
  - <span class="keep-together" data-type="index-term">axis
    functions</span>, <a href="#ch08.xhtml_idm140093196906896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing Axes</a>
  - <span class="keep-together" data-type="index-term">basic code
    structure of</span>, <a href="#ch05.xhtml_idm140093203423024"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">High-Functioning</a>
  - <span class="keep-together" data-type="index-term">callback
    function</span>, <a href="#ch05.xhtml_idm140093204114208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>,
    <a href="#ch05.xhtml_idm140093203989184"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Loading CSV data</a>
  - <span class="keep-together" data-type="index-term">comparator
    functions</span>, <a href="#ch10.xhtml_idm140093189912720"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Click to Sort</a>
  - <span class="keep-together" data-type="index-term">D3 scales
    as</span>, <a href="#ch07.xhtml_idm140093199052864"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scales</a>
  - <span class="keep-together" data-type="index-term">event
    listeners</span>, <a href="#ch09.xhtml_idm140093195050304"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Interaction via Event Listeners</a>
  - <span class="keep-together" data-type="index-term">key
    functions</span>, <a href="#ch09.xhtml_idm140093191747312"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Joins with Keys</a>,
    <a href="#ch09.xhtml_idm140093191074576"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Key functions</a>
  - <span class="keep-together" data-type="index-term">line generator
    functions</span>, <a href="#ch11.xhtml_idm140093188341968"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Line ’em Up</a>
  - <span class="keep-together" data-type="index-term">vs.
    methods</span>, <a href="#ch05.xhtml_idm140093204476176"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Chaining Methods</a>
  - <span class="keep-together" data-type="index-term">named
    functions</span>, <a href="#ch05.xhtml_idm140093203412192"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">High-Functioning</a>
  - <span class="keep-together" data-type="index-term">passing arguments
    to</span>, <a href="#ch03.xhtml_idm140093206537008"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Functions</a>
  - <span class="keep-together" data-type="index-term">testing
    formatting functions</span>,
    <a href="#ch08.xhtml_idm140093195966480"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Formatting Tick Labels</a>
  - <span class="keep-together" data-type="index-term">used as
    arguments</span>, <a href="#ch05.xhtml_idm140093203134352"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Wants to Be Held</a>

</div>

<div class="dedication" data-type="indexdiv">

### G

- <span class="keep-together" data-type="index-term">geocoding
  services</span>, <a href="#ch14.xhtml_idm140093181838960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">Geographic
  Information Systems (GIS) software</span>,
  <a href="#ch14.xhtml_idm140093179678176"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Find Shapefiles</a>
- <span class="keep-together" data-type="index-term">GeoJSON</span>,
  <a href="#ch03.xhtml_idm140093207074848"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">GeoJSON</a>,
  <a href="#ch14.xhtml_idm140093183075888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">JSON, Meet GeoJSON</a>,
  <a href="#ch14.xhtml_idm140093179607632"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Convert to GeoJSON</a>
- <span class="keep-together" data-type="index-term">geomapping</span>
  - <span class="keep-together" data-type="index-term">acquiring/parsing
    raw geodata</span>, <a href="#ch14.xhtml_GEOpars14"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Acquiring and Preparing Raw Geodata</a>-<a href="#ch14.xhtml_idm140093179393040"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Choose a Projection</a>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208126784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Geomapping</a>
  - <span class="keep-together" data-type="index-term">choropleth
    maps</span>, <a href="#ch14.xhtml_idm140093182398096"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Choropleth</a>
  - <span class="keep-together" data-type="index-term">D3 support
    for</span>, <a href="#ch02.xhtml_idm140093207919200"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">defining path
    generators</span>, <a href="#ch14.xhtml_idm140093182886512"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Paths</a>
  - <span class="keep-together" data-type="index-term">geocoding
    services</span>, <a href="#ch14.xhtml_idm140093181838224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Points</a>
  - <span class="keep-together" data-type="index-term">GeoJSON</span>,
    <a href="#ch14.xhtml_idm140093183076896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">JSON, Meet GeoJSON</a>
  - <span class="keep-together"
    data-type="index-term">longitude/latitude pairs</span>,
    <a href="#ch14.xhtml_idm140093182898160"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">JSON, Meet GeoJSON</a>
  - <span class="keep-together" data-type="index-term">map
    points</span>, <a href="#ch14.xhtml_idm140093181849168"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Points</a>
  - <span class="keep-together" data-type="index-term">modifying
    projections</span>, <a href="#ch14.xhtml_idm140093182553568"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Projections</a>
  - <span class="keep-together" data-type="index-term">panning</span>,
    <a href="#ch14.xhtml_Gpan14"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Panning</a>-<a href="#ch14.xhtml_idm140093180502560"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Border Problems</a>
  - <span class="keep-together" data-type="index-term">value
    labels</span>, <a href="#ch14.xhtml_idm140093179878880"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Value Labels</a>
  - <span class="keep-together" data-type="index-term">zooming</span>,
    <a href="#ch14.xhtml_Gzoom14"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Zooming</a>-<a href="#ch14.xhtml_idm140093179897072"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Preset Views</a>
- <span class="keep-together" data-type="index-term">global
  namespace</span>, <a href="#ch03.xhtml_idm140093205720016"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Global namespace</a>
- <span class="keep-together" data-type="index-term">Google Maps</span>,
  <a href="#ch02.xhtml_idm140093207922432"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">granularity</span>,
  <a href="#ch14.xhtml_idm140093179663440"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choose a Resolution</a>
- <span class="keep-together" data-type="index-term">graphs</span>
  (<span class="keep-together" gentext="see">see</span> also charts)
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208136064"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Graph Visualizations</a>
  - <span class="keep-together" data-type="index-term">creating with
    force-directed layouts</span>, <a href="#ch13.xhtml_Gforce13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Force Layout</a>-<a href="#ch13.xhtml_idm140093183081760"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Draggable Nodes</a>
- <span class="keep-together" data-type="index-term">group
  elements</span>, <a href="#ch08.xhtml_idm140093196740160"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>

</div>

<div class="dedication" data-type="indexdiv">

### H

- <span class="keep-together" data-type="index-term">headlines</span>,
  <a href="#ch16.xhtml_idm140093177454720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Provide Context</a>
- <span class="keep-together" data-type="index-term">Heer,
  Jeffrey</span>, <a href="#ch02.xhtml_idm140093207902416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">horizontal
  axis</span>, <a href="#ch08.xhtml_idm140093196795232"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">hover to
  highlight</span>, <a href="#ch10.xhtml_idm140093190577792"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>
- <span class="keep-together" data-type="index-term">HTML (Hypertext
  Markup Language)</span> (<span class="keep-together"
  gentext="see">see</span> also elements)
  - <span class="keep-together"
    data-type="index-term">attributes</span>,
    <a href="#ch03.xhtml_idm140093211183376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Attributes</a>,
    <a href="#ch05.xhtml_idm140093203112304"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Beyond Text</a>
  - <span class="keep-together" data-type="index-term">classes and
    IDs</span>, <a href="#ch03.xhtml_idm140093211139232"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Classes and IDs</a>
  - <span class="keep-together" data-type="index-term">comments</span>,
    <a href="#ch03.xhtml_idm140093210914816"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Comments</a>
  - <span class="keep-together" data-type="index-term">common
    elements</span>, <a href="#ch03.xhtml_idm140093211303408"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Common Elements</a>
  - <span class="keep-together" data-type="index-term">div
    tooltips</span>, <a href="#ch10.xhtml_idm140093189136944"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">HTML div Tooltips</a>
  - <span class="keep-together" data-type="index-term">serving web pages
    with</span>, <a href="#ch03.xhtml_idm140093214278192"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Web</a>
  - <span class="keep-together" data-type="index-term">specifying
    structure with</span>, <a href="#ch03.xhtml_idm140093214269360"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">HTML</a>
  - <span class="keep-together" data-type="index-term">tags and
    elements</span>, <a href="#ch03.xhtml_idm140093212467264"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Structure with Elements</a>
- <span class="keep-together" data-type="index-term">HTTP (Hypertext
  Transfer Protocol)</span>, <a href="#ch03.xhtml_idm140093208185936"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">HTTPS (Hypertext
  Transfer Protocol Secure)</span>,
  <a href="#ch03.xhtml_idm140093214287232"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>

</div>

<div class="dedication" data-type="indexdiv">

### I

- <span class="keep-together" data-type="index-term">ID
  selectors</span>, <a href="#ch03.xhtml_idm140093210453360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selectors</a>
- <span class="keep-together" data-type="index-term">IDs, HTML
  elements</span>, <a href="#ch03.xhtml_idm140093211131696"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Classes and IDs</a>
- <span class="keep-together" data-type="index-term">if
  statements</span>, <a href="#ch03.xhtml_idm140093206777392"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">if() only</a>
- <span class="keep-together" data-type="index-term">immediate
  transformations</span>, <a href="#ch09.xhtml_idm140093192751376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">End gracefully</a>
- <span class="keep-together" data-type="index-term">indentation
  convention</span>, <a href="#ch12.xhtml_idm140093186944128"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Getting More Specific</a>
- <span class="keep-together" data-type="index-term">index order</span>,
  <a href="#ch09.xhtml_idm140093191754560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data Joins with Keys</a>
- <span class="keep-together" data-type="index-term">inheritance</span>,
  <a href="#ch03.xhtml_idm140093210160240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Inheritance, Cascading, and Specificity</a>
- <span class="keep-together" data-type="index-term">inline
  elements</span>, <a href="#ch03.xhtml_idm140093210858464"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">inline style
  rules</span>, <a href="#ch03.xhtml_idm140093210138400"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Attach inline styles</a>
- <span class="keep-together" data-type="index-term">input
  domain</span>, <a href="#ch07.xhtml_idm140093199134640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Domains and Ranges</a>
- <span class="keep-together"
  data-type="index-term">interactivity</span>
  - <span class="keep-together" data-type="index-term">behaviors</span>,
    <a href="#ch10.xhtml_Ibehav10"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing Behaviors</a>-<a href="#ch10.xhtml_idm140093190087904"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
    - <span class="keep-together" data-type="index-term">hover to
      highlight</span>, <a href="#ch10.xhtml_idm140093190577120"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">benefits
    of</span>, <a href="#ch01_split_000.xhtml_idm140093221176432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Why Interactive?</a>
  - <span class="keep-together" data-type="index-term">browser
    development and</span>, <a href="#ch02.xhtml_idm140093207905696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together" data-type="index-term">click to
    sort</span>, <a href="#ch10.xhtml_idm140093190019984"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Click to Sort</a>
  - <span class="keep-together" data-type="index-term">event listeners
    and</span>, <a href="#ch10.xhtml_idm140093190669360"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Event Listeners</a>
  - <span class="keep-together" data-type="index-term">grouping SVG
    elements</span>, <a href="#ch10.xhtml_idm140093190033616"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Grouping SVG Elements</a>
  - <span class="keep-together" data-type="index-term">methods quick
    reference</span>, <a href="#app05.xhtml_idm140093174892448"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Interactivity</a>
  - <span class="keep-together" data-type="index-term">pointer
    events</span>, <a href="#ch10.xhtml_idm140093190113088"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">project
    walk-through example</span>, <a href="#ch16.xhtml_Iproj16"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Add Interactivity</a>-<a href="#ch16.xhtml_idm140093177617728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Add Interactivity</a>
  - <span class="keep-together" data-type="index-term">tooltips</span>,
    <a href="#ch10.xhtml_Itool10"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Tooltips</a>-<a href="#ch10.xhtml_idm140093188648704"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">HTML div Tooltips</a>
  - <span class="keep-together" data-type="index-term">touch
    devices</span>, <a href="#ch10.xhtml_idm140093188646128"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Consideration for Touch Devices</a>
- <span class="keep-together" data-type="index-term">Internet
  Explorer</span>, <a href="#ch03.xhtml_idm140093204734480"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">A Note on Compatibility</a>

</div>

<div class="dedication" data-type="indexdiv">

### J

- <span class="keep-together" data-type="index-term">JavaScript</span>
  - <span class="keep-together"
    data-type="index-term">array.length</span>,
    <a href="#ch12.xhtml_idm140093186418752"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Merging Selections</a>
  - <span class="keep-together" data-type="index-term">arrays</span>,
    <a href="#ch03.xhtml_idm140093210087040"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Arrays</a>,
    <a href="#ch03.xhtml_idm140093207493968"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Objects and Arrays</a>,
    <a href="#ch03.xhtml_idm140093206486896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What arrays are made for</a>
  - <span class="keep-together" data-type="index-term">as basis for
    D3</span>, <a href="#ch01_split_001.xhtml_idm140093221159712"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What This Book Is</a>
  - <span class="keep-together" data-type="index-term">comments</span>,
    <a href="#ch03.xhtml_idm140093206421328"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Functions</a>
  - <span class="keep-together" data-type="index-term">comparison
    operators</span>, <a href="#ch03.xhtml_idm140093206941088"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Comparison Operators</a>
  - <span class="keep-together" data-type="index-term">control
    structures</span>, <a href="#ch03.xhtml_idm140093206782384"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Control Structures</a>
  - <span class="keep-together" data-type="index-term">dynamic
    typing</span>, <a href="#ch03.xhtml_idm140093206185728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Dynamic typing</a>
  - <span class="keep-together" data-type="index-term">event
    model</span>, <a href="#ch10.xhtml_idm140093190665728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Event Listeners</a>
  - <span class="keep-together" data-type="index-term">function-level
    scope</span>, <a href="#ch03.xhtml_idm140093205733584"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Function-level scope</a>
  - <span class="keep-together" data-type="index-term">functions</span>,
    <a href="#ch03.xhtml_idm140093206538016"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Functions</a>
  - <span class="keep-together" data-type="index-term">GeoJSON</span>,
    <a href="#ch03.xhtml_idm140093207075856"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">GeoJSON</a>
  - <span class="keep-together" data-type="index-term">global
    namespace</span>, <a href="#ch03.xhtml_idm140093205721024"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Global namespace</a>
  - <span class="keep-together" data-type="index-term">introduction
    of</span>, <a href="#ch02.xhtml_idm140093207908720"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Origins and Context</a>
  - <span class="keep-together" data-type="index-term">JSON</span>,
    <a href="#ch03.xhtml_idm140093207264192"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">JSON</a>
  - <span class="keep-together" data-type="index-term">logical
    operators</span>, <a href="#ch03.xhtml_idm140093206895040"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Logical Operators</a>
  - <span class="keep-together" data-type="index-term">mathematical
    operators</span>, <a href="#ch03.xhtml_idm140093207204880"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Mathematical Operators</a>
  - <span class="keep-together" data-type="index-term">objects</span>,
    <a href="#ch03.xhtml_idm140093208567536"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Objects</a>
  - <span class="keep-together" data-type="index-term">quick
    reference</span>, <a href="#app05.xhtml_idm140093174399408"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Useful JavaScript</a>
  - <span class="keep-together" data-type="index-term">referencing
    scripts</span>, <a href="#ch03.xhtml_idm140093206319760"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Referencing Scripts</a>
  - <span class="keep-together" data-type="index-term">this
    keyword</span>, <a href="#ch10.xhtml_idm140093190299280"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">using the JS
    console</span>, <a href="#ch03.xhtml_idm140093209969216"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hello, Console</a>
  - <span class="keep-together" data-type="index-term">variable
    hoisting</span>, <a href="#ch03.xhtml_idm140093205899280"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Variable hoisting</a>
  - <span class="keep-together" data-type="index-term">variables</span>,
    <a href="#ch03.xhtml_idm140093209959616"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Variables</a>
- <span class="keep-together" data-type="index-term">jQuery</span>
  - <span class="keep-together" data-type="index-term">chain
    syntax</span>, <a href="#ch05.xhtml_idm140093204478336"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Chaining Methods</a>
  - <span class="keep-together" data-type="index-term">libraries and
    plug-ins for</span>, <a href="#ch02.xhtml_idm140093208148080"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Easy Charts</a>
  - <span class="keep-together" data-type="index-term">transitions
    using</span>, <a href="#ch09.xhtml_idm140093192818000"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Warning: Start carefully</a>
- <span class="keep-together" data-type="index-term">JSON (JavaScript
  Object Notation)</span>, <a href="#ch03.xhtml_idm140093207263184"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">JSON</a>,
  <a href="#ch05.xhtml_idm140093204547360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>,
  <a href="#ch05.xhtml_idm140093203783936"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading JSON data</a>

</div>

<div class="dedication" data-type="indexdiv">

### K

- <span class="keep-together" data-type="index-term">key
  functions</span>, <a href="#ch09.xhtml_idm140093191748048"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data Joins with Keys</a>,
  <a href="#ch09.xhtml_idm140093191075312"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Key functions</a>

</div>

<div class="dedication" data-type="indexdiv">

### L

- <span class="keep-together" data-type="index-term">labels</span>
  - <span class="keep-together" data-type="index-term">for axes</span>,
    <a href="#ch08.xhtml_idm140093196899392"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up an Axis</a>,
    <a href="#ch08.xhtml_idm140093195998256"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Formatting Tick Labels</a>
  - <span class="keep-together" data-type="index-term">for bar
    charts</span>, <a href="#ch09.xhtml_idm140093194643648"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating the Visuals</a>
  - <span class="keep-together" data-type="index-term">for maps</span>,
    <a href="#ch14.xhtml_idm140093179880832"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Value Labels</a>
- <span class="keep-together" data-type="index-term">Landay,
  James</span>, <a href="#ch02.xhtml_idm140093208177040"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">layering, in
  SVG</span>, <a href="#ch03.xhtml_idm140093205266768"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Layering and Drawing Order</a>
- <span class="keep-together" data-type="index-term">layouts</span>
  - <span class="keep-together" data-type="index-term">force-directed
    layout</span>, <a href="#ch13.xhtml_Lforce13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Force Layout</a>-<a href="#ch13.xhtml_idm140093183082736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Draggable Nodes</a>
  - <span class="keep-together" data-type="index-term">list of</span>,
    <a href="#ch13.xhtml_idm140093185493424"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Layouts</a>
  - <span class="keep-together" data-type="index-term">pie
    layout</span>, <a href="#ch13.xhtml_Lpie13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>-<a href="#ch13.xhtml_idm140093184861728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pie Layout</a>
  - <span class="keep-together" data-type="index-term">role of</span>,
    <a href="#ch13.xhtml_idm140093185496576"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Layouts</a>
  - <span class="keep-together" data-type="index-term">stack
    layout</span>, <a href="#ch13.xhtml_Lstack13"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stack Layout</a>-<a href="#ch13.xhtml_idm140093184058912"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stacked Areas</a>
- <span class="keep-together" data-type="index-term">line charts</span>
  - <span class="keep-together" data-type="index-term">data
    preparation</span>, <a href="#ch11.xhtml_idm140093188874272"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Line Charts</a>
  - <span class="keep-together" data-type="index-term">dealing with
    missing data</span>, <a href="#ch11.xhtml_idm140093188218768"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Dealing with Missing Data</a>
  - <span class="keep-together" data-type="index-term">line generator
    function</span>, <a href="#ch11.xhtml_idm140093188343616"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Line ’em Up</a>
  - <span class="keep-together" data-type="index-term">refining visual
    presentation</span>, <a href="#ch11.xhtml_idm140093188112272"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Visuals</a>
  - <span class="keep-together" data-type="index-term">scale
    setup</span>, <a href="#ch11.xhtml_idm140093188427344"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scale Setup</a>
- <span class="keep-together" data-type="index-term">line generator
  function</span>, <a href="#ch11.xhtml_idm140093188342640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Line ’em Up</a>
- <span class="keep-together" data-type="index-term">linear
  scales</span>, <a href="#ch07.xhtml_idm140093199045696"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
  - (<span class="keep-together" gentext="see">see also</span> scales)
- <span class="keep-together" data-type="index-term">local
  servers</span>, <a href="#ch03.xhtml_idm140093208199472"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">logical
  operators</span>, <a href="#ch03.xhtml_idm140093206894032"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Logical Operators</a>
- <span class="keep-together" data-type="index-term">longitude/latitude
  pairs</span>, <a href="#ch14.xhtml_idm140093182897216"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">JSON, Meet GeoJSON</a>
- <span class="keep-together" data-type="index-term">loosely typed
  languages</span>, <a href="#ch03.xhtml_idm140093206151728"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>

</div>

<div class="dedication" data-type="indexdiv">

### M

- <span class="keep-together" data-type="index-term">magic
  numbers</span>, <a href="#ch09.xhtml_idm140093193582336"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Updating Scales</a>
- <span class="keep-together" data-type="index-term">map tiles</span>,
  <a href="#ch02.xhtml_idm140093207923104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">Mapbox</span>,
  <a href="#ch02.xhtml_idm140093207920816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Doesn’t Do</a>
- <span class="keep-together" data-type="index-term">mapping
  data</span>, <a href="#ch05.xhtml_idm140093204325264"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Binding Data</a>
- <span class="keep-together" data-type="index-term">mapping
  rules</span>, <a href="#ch01_split_000.xhtml_idm140093208064464"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why Write Code?</a>
- <span class="keep-together" data-type="index-term">maps</span>
  (<span class="keep-together" gentext="see">see</span> also geomapping)
  - <span class="keep-together" data-type="index-term">choropleth
    maps</span>, <a href="#ch14.xhtml_idm140093182396416"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Choropleth</a>
  - <span class="keep-together" data-type="index-term">Google
    Maps</span>, <a href="#ch02.xhtml_idm140093207921760"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">What It Doesn’t Do</a>
  - <span class="keep-together" data-type="index-term">labeling</span>,
    <a href="#ch14.xhtml_idm140093179879824"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Value Labels</a>
  - <span class="keep-together" data-type="index-term">map
    points</span>, <a href="#ch14.xhtml_idm140093181847488"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Points</a>
  - <span class="keep-together" data-type="index-term">political
    maps</span>, <a href="#ch14.xhtml_idm140093182395472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Choropleth</a>
  - <span class="keep-together" data-type="index-term">population
    maps</span>, <a href="#ch14.xhtml_idm140093181828480"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">MapShaper</span>,
  <a href="#ch14.xhtml_idm140093179639024"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">MapShaper</a>
- <span class="keep-together" data-type="index-term">masks</span>,
  <a href="#ch09.xhtml_idm140093192676880"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Containing visual elements with clipping
  paths</a>
- <span class="keep-together" data-type="index-term">Math.ceil()</span>,
  <a href="#app05.xhtml_idm140093174354592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together"
  data-type="index-term">Math.floor()</span>,
  <a href="#app05.xhtml_idm140093174330096"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together"
  data-type="index-term">Math.random()</span>,
  <a href="#app05.xhtml_idm140093174463456"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together"
  data-type="index-term">Math.round()</span>,
  <a href="#app05.xhtml_idm140093174492368"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together" data-type="index-term">mathematical
  operators</span>, <a href="#ch03.xhtml_idm140093207203872"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Mathematical Operators</a>
- <span class="keep-together" data-type="index-term">maximum
  values</span>, <a href="#ch09.xhtml_idm140093193479808"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Updating Scales</a>
- <span class="keep-together" data-type="index-term">merge()</span>,
  <a href="#app02.xhtml_idm140093176825040"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together" data-type="index-term">merging
  selections</span>, <a href="#ch12.xhtml_mergsel12"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Merging Selections</a>-<a href="#ch12.xhtml_idm140093186256112"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Merging Selections</a>
- <span class="keep-together" data-type="index-term">methods</span>
  - <span class="keep-together" data-type="index-term">quick
    reference</span>, <a href="#app05.xhtml_Mquick21"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Quick Reference</a>-<a href="#app05.xhtml_idm140093174194752"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Useful JavaScript</a>
  - <span class="keep-together" data-type="index-term">vs.
    functions</span>, <a href="#ch05.xhtml_idm140093204463424"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Chaining Methods</a>
- <span class="keep-together"
  data-type="index-term">microlibraries</span>,
  <a href="#app02.xhtml_idm140093176878544"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Modularity</a>
- <span class="keep-together" data-type="index-term">Migurski,
  Mike</span>, <a href="#ch14.xhtml_idm140093179613536"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other simplification options</a>
- <span class="keep-together" data-type="index-term">missing
  data</span>, <a href="#ch11.xhtml_idm140093188217744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dealing with Missing Data</a>
- <span class="keep-together" data-type="index-term">mouseover
  events</span>, <a href="#ch10.xhtml_idm140093190579440"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>,
  <a href="#ch10.xhtml_idm140093190340640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>
- <span class="keep-together" data-type="index-term">Mr. Data
  Converter</span>, <a href="#ch05.xhtml_idm140093203892656"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Loading JSON data</a>
- <span class="keep-together" data-type="index-term">multitouch
  interactions</span>, <a href="#ch10.xhtml_idm140093188643776"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Consideration for Touch Devices</a>
- <span class="keep-together" data-type="index-term">multivalue
  maps</span>, <a href="#app02.xhtml_idm140093176820560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Multivalue Maps</a>

</div>

<div class="dedication" data-type="indexdiv">

### N

- <span class="keep-together" data-type="index-term">named
  functions</span>, <a href="#ch05.xhtml_idm140093203413808"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">High-Functioning</a>
- <span class="keep-together" data-type="index-term">namespace</span>,
  <a href="#app02.xhtml_idm140093176834416"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Namespace and camelCase</a>
- <span class="keep-together" data-type="index-term">nodes</span>,
  <a href="#ch13.xhtml_idm140093184169504"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Force Layout</a>,
  <a href="#ch13.xhtml_idm140093183348448"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Draggable Nodes</a>
- <span class="keep-together"
  data-type="index-term">normalization</span>,
  <a href="#ch07.xhtml_idm140093199028848"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Normalization</a>

</div>

<div class="dedication" data-type="indexdiv">

### O

- <span class="keep-together" data-type="index-term">object
  constancy</span>, <a href="#ch09.xhtml_idm140093191767920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Making a smooth exit</a>
- <span class="keep-together" data-type="index-term">objects</span>,
  <a href="#ch03.xhtml_idm140093208568272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Objects</a>
- <span class="keep-together" data-type="index-term">Ogievetsky,
  Vadim</span>, <a href="#ch02.xhtml_idm140093208165296"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">on()</span>,
  <a href="#ch09.xhtml_idm140093195048400"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interaction via Event Listeners</a>,
  <a href="#ch10.xhtml_idm140093190484384"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Binding Event Listeners</a>
- <span class="keep-together" data-type="index-term">open source
  software</span>, <a href="#ch01_split_000.xhtml_idm140093221167552"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why on the Web?</a>,
  <a href="#app04.xhtml_idm140093176472560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Sharing Your Code</a>
- <span class="keep-together" data-type="index-term">order()</span>,
  <a href="#ch16.xhtml_idm140093178446864"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Render the Initial View</a>
- <span class="keep-together" data-type="index-term">ordinal
  scales</span>, <a href="#ch09.xhtml_idm140093195761600"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Modernizing the Bar Chart</a>,
  <a href="#ch13.xhtml_idm140093184934928"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>,
  <a href="#app02.xhtml_idm140093176623376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Ordinal Scales</a>
- <span class="keep-together" data-type="index-term">output
  range</span>, <a href="#ch07.xhtml_idm140093199133968"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Domains and Ranges</a>
- <span class="keep-together" data-type="index-term">overlapping
  elements</span>, <a href="#ch10.xhtml_idm140093190117248"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>

</div>

<div class="dedication" data-type="indexdiv">

### P

- <span class="keep-together" data-type="index-term">padding</span>,
  <a href="#ch07.xhtml_idm140093197963360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Refining the Plot</a>,
  <a href="#ch08.xhtml_idm140093196112928"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Y Not?</a>,
  <a href="#ch09.xhtml_idm140093195503616"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Starting Your Own Band</a>
- <span class="keep-together" data-type="index-term">page
  elements</span> (<span class="keep-together" gentext="see">see</span>
  also data joining)
  - <span class="keep-together" data-type="index-term">binding data
    to</span>, <a href="#ch05.xhtml_PEbind05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Binding Data</a>-<a href="#ch05.xhtml_idm140093202910208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Beyond Text</a>
    - <span class="keep-together" data-type="index-term">CSV
      files</span>, <a href="#ch05.xhtml_idm140093204147408"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Loading CSV data</a>
    - <span class="keep-together" data-type="index-term">data()
      method</span>, <a href="#ch05.xhtml_idm140093204317264"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">In a Bind</a>
    - <span class="keep-together" data-type="index-term">handling
      loading errors</span>, <a href="#ch05.xhtml_idm140093204182608"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Loading CSV data</a>
    - <span class="keep-together" data-type="index-term">inspecting
      bound data</span>, <a href="#ch05.xhtml_idm140093203585856"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Bound and Determined</a>
    - <span class="keep-together" data-type="index-term">JSON
      files</span>, <a href="#ch05.xhtml_idm140093203781520"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Loading JSON data</a>
    - <span class="keep-together" data-type="index-term">purpose
      of</span>, <a href="#ch05.xhtml_idm140093204322464"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Binding Data</a>
    - <span class="keep-together" data-type="index-term">selecting
      elements</span>, <a href="#ch05.xhtml_idm140093203886304"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Please Make Your Selection</a>
    - <span class="keep-together" data-type="index-term">using bound
      data</span>, <a href="#ch05.xhtml_idm140093203473232"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Using Your Data</a>
  - <span class="keep-together"
    data-type="index-term">generating</span>,
    <a href="#ch05.xhtml_PEgener05"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Generating Page Elements</a>-<a href="#ch05.xhtml_idm140093204331856"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Going Chainless</a>
    - <span class="keep-together" data-type="index-term">alternatives to
      chaining</span>, <a href="#ch05.xhtml_idm140093204250704"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Going Chainless</a>
    - <span class="keep-together" data-type="index-term">chaining
      methods</span>, <a href="#ch05.xhtml_idm140093204480560"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">Chaining Methods</a>
    - <span class="keep-together" data-type="index-term">code
      deconstruction</span>, <a href="#ch05.xhtml_idm140093204423728"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">One Link at a Time</a>
    - <span class="keep-together" data-type="index-term">input/output
      matching</span>, <a href="#ch05.xhtml_idm140093204256480"
      class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
      data-type="index:locator">The Handoff</a>
- <span class="keep-together" data-type="index-term">panning
  (maps)</span>, <a href="#ch14.xhtml_pan14"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Panning</a>-<a href="#ch14.xhtml_idm140093180503504"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Border Problems</a>
- <span class="keep-together" data-type="index-term">paragraph
  elements</span>, <a href="#ch05.xhtml_idm140093204536352"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Generating Page Elements</a>
- <span class="keep-together" data-type="index-term">parent
  elements</span>, <a href="#ch03.xhtml_idm140093210908576"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">DOM</a>
- <span class="keep-together"
  data-type="index-term">parseFloat()</span>,
  <a href="#app05.xhtml_idm140093174393664"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together" data-type="index-term">parseInt()</span>,
  <a href="#app05.xhtml_idm140093174398400"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Other Useful JavaScript</a>
- <span class="keep-together" data-type="index-term">paths</span>,
  <a href="#ch11.xhtml_path11"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Using Paths</a>-<a href="#ch11.xhtml_idm140093187435984"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Area Charts</a>,
  <a href="#ch14.xhtml_idm140093182885488"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Paths</a>
  - <span class="keep-together" data-type="index-term">drawing line
    charts with</span>, <a href="#ch11.xhtml_Pline11"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Line Charts</a>-<a href="#ch11.xhtml_idm140093187869872"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Visuals</a>
  - <span class="keep-together" data-type="index-term">path
    syntax</span>, <a href="#ch11.xhtml_idm140093188670704"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Using Paths</a>
- <span class="keep-together" data-type="index-term">pie layout</span>,
  <a href="#ch13.xhtml_pie13"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>-<a href="#ch13.xhtml_idm140093184860784"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">pixel-based
  coordinates system</span>, <a href="#ch03.xhtml_idm140093205644896"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The SVG Element</a>
- <span class="keep-together" data-type="index-term">pixels</span>
  - <span class="keep-together" data-type="index-term">lining up
    to</span>, <a href="#ch09.xhtml_idm140093195415152"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Starting Your Own Band</a>
  - <span class="keep-together" data-type="index-term">smoothing</span>,
    <a href="#ch08.xhtml_idm140093196416832"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">pointer
  events</span>, <a href="#ch10.xhtml_idm140093190114960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>
  - (<span class="keep-together" gentext="see">see also</span> mouseover
    events; tooltips)
- <span class="keep-together" data-type="index-term">points</span>,
  <a href="#ch14.xhtml_idm140093181848160"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">political
  maps</span>, <a href="#ch14.xhtml_idm140093182394528"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choropleth</a>
- <span class="keep-together" data-type="index-term">population
  maps</span>, <a href="#ch14.xhtml_idm140093181829216"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">port
  numbers</span>, <a href="#ch03.xhtml_idm140093208180880"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">prefuse
  toolkit</span>, <a href="#ch02.xhtml_idm140093207903152"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>
- <span class="keep-together" data-type="index-term">print-to-PDF
  functionality</span>, <a href="#ch15.xhtml_idm140093179373136"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">PDF</a>
- <span class="keep-together" data-type="index-term">project
  walk-through</span>, <a href="#ch16.xhtml_prowalk16"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Project Walk-Through</a>-<a href="#ch16.xhtml_idm140093177260176"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dancing Versus Gardening</a>
  - <span class="keep-together" data-type="index-term">adding
    interactivity</span>, <a href="#ch16.xhtml_idm140093178324224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Add Interactivity</a>
  - <span class="keep-together" data-type="index-term">data loading and
    parsing</span>, <a href="#ch16.xhtml_idm140093179307664"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Load and Parse the Data</a>
  - <span class="keep-together" data-type="index-term">data
    preparation</span>, <a href="#ch16.xhtml_idm140093179324608"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Prepare the Data</a>
  - <span class="keep-together" data-type="index-term">integrating
    charts for context</span>, <a href="#ch16.xhtml_idm140093177456368"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Provide Context</a>
  - <span class="keep-together" data-type="index-term">rendering initial
    view</span>, <a href="#ch16.xhtml_idm140093178648096"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Render the Initial View</a>
  - <span class="keep-together" data-type="index-term">visual
    refinements</span>, <a href="#ch16.xhtml_idm140093177615888"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refine Styling</a>
- <span class="keep-together" data-type="index-term">projections</span>,
  <a href="#ch14.xhtml_idm140093182530608"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Projections</a>,
  <a href="#ch14.xhtml_idm140093181773008"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">properties</span>,
  <a href="#ch03.xhtml_idm140093210797904"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">CSS</a>,
  <a href="#ch03.xhtml_idm140093210515744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Properties and Values</a>,
  <a href="#ch03.xhtml_idm140093208564912"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Objects</a>
- <span class="keep-together" data-type="index-term">Protovis
  visualization toolkit</span>, <a href="#ch02.xhtml_idm140093208168864"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Origins and Context</a>

</div>

<div class="dedication" data-type="indexdiv">

### Q

- <span class="keep-together" data-type="index-term">quantitative
  scales</span>, <a href="#ch08.xhtml_idm140093196902576"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Introducing Axes</a>
- <span class="keep-together" data-type="index-term">quantize
  scales</span>, <a href="#ch14.xhtml_idm140093182375696"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choropleth</a>
- <span class="keep-together" data-type="index-term">questions and
  comments</span>, <a href="#preface01.xhtml_idm140093214391136"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">How to Contact Us</a>
- <span class="keep-together" data-type="index-term">queued
  transitions</span>, <a href="#ch09.xhtml_idm140093192818640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Warning: Start carefully</a>

</div>

<div class="dedication" data-type="indexdiv">

### R

- <span class="keep-together" data-type="index-term">radians</span>,
  <a href="#ch13.xhtml_idm140093185467520"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">random data,
  generating</span>, <a href="#ch06.xhtml_idm140093202064048"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Random Data</a>
- <span class="keep-together" data-type="index-term">range
  banding</span>, <a href="#ch09.xhtml_idm140093195511120"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Starting Your Own Band</a>
- <span class="keep-together" data-type="index-term">rectangles,
  drawing</span>, <a href="#ch06.xhtml_idm140093202889488"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Drawing divs</a>
- <span class="keep-together" data-type="index-term">red state/blue
  state maps</span>, <a href="#ch14.xhtml_idm140093182393856"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choropleth</a>
- <span class="keep-together" data-type="index-term">remote
  servers</span>, <a href="#ch03.xhtml_idm140093208198800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">rendering</span>,
  <a href="#ch03.xhtml_idm140093210872848"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">requests</span>,
  <a href="#ch03.xhtml_idm140093208203360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">resolution</span>,
  <a href="#ch14.xhtml_idm140093179665856"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choose a Resolution</a>
- <span class="keep-together" data-type="index-term">rhetoric—design
  decisions</span>, <a href="#ch11.xhtml_idm140093188106592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Refining the Visuals</a>
- <span class="keep-together" data-type="index-term">ring charts</span>,
  <a href="#ch13.xhtml_idm140093184773712"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>

</div>

<div class="dedication" data-type="indexdiv">

### S

- <span class="keep-together" data-type="index-term">scale()</span>,
  <a href="#ch08.xhtml_idm140093196852032"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>
- <span class="keep-together"
  data-type="index-term">scaleLinear.clamp()</span>,
  <a href="#app05.xhtml_idm140093174996272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together"
  data-type="index-term">scaleLinear.domain()</span>,
  <a href="#app05.xhtml_idm140093175205056"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together"
  data-type="index-term">scaleLinear.nice()</span>,
  <a href="#app05.xhtml_idm140093175094016"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together"
  data-type="index-term">scaleLinear.range()</span>,
  <a href="#app05.xhtml_idm140093175160272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together"
  data-type="index-term">scaleLinear.rangeRound()</span>,
  <a href="#app05.xhtml_idm140093175148240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>
- <span class="keep-together" data-type="index-term">scales</span>,
  <a href="#ch07.xhtml_scale07"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Scales</a>-<a href="#ch07.xhtml_idm140093196944608"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Formatting dates and strings</a>
  - <span class="keep-together" data-type="index-term">additional
    types</span>, <a href="#ch07.xhtml_idm140093197630976"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Scales</a>
  - <span class="keep-together" data-type="index-term">vs. axes</span>,
    <a href="#ch07.xhtml_idm140093199050336"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scales</a>
  - <span class="keep-together" data-type="index-term">creating</span>,
    <a href="#ch07.xhtml_idm140093199024528"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Creating a Scale</a>
  - <span class="keep-together" data-type="index-term">d3.min() and
    d3.max()</span>, <a href="#ch07.xhtml_idm140093198887488"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">d3.min() and d3.max()</a>
  - <span class="keep-together" data-type="index-term">definition of
    term</span>, <a href="#ch07.xhtml_idm140093199054848"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scales</a>
  - <span class="keep-together" data-type="index-term">dynamic
    scales</span>, <a href="#ch07.xhtml_idm140093198366880"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up Dynamic Scales</a>
  - <span class="keep-together" data-type="index-term">handy methods
    for</span>, <a href="#ch07.xhtml_idm140093197661392"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Methods</a>,
    <a href="#app05.xhtml_idm140093175212848"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scales</a>
  - <span class="keep-together" data-type="index-term">incorporating
    scaled values</span>, <a href="#ch07.xhtml_idm140093198205136"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Incorporating Scaled Values</a>
  - <span class="keep-together" data-type="index-term">input
    domain/output range</span>, <a href="#ch07.xhtml_idm140093199035280"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Domains and Ranges</a>
  - <span class="keep-together" data-type="index-term">need for</span>,
    <a href="#ch07.xhtml_idm140093199041376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Apples and Pixels</a>
  - <span class="keep-together"
    data-type="index-term">normalization</span>,
    <a href="#ch07.xhtml_idm140093199029696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Normalization</a>
  - <span class="keep-together" data-type="index-term">plot
    refinements</span>, <a href="#ch07.xhtml_idm140093198109504"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Plot</a>
  - <span class="keep-together" data-type="index-term">scatterplot
    scaling example</span>, <a href="#ch07.xhtml_Sscatter07"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scaling the Scatterplot</a>-<a href="#ch07.xhtml_idm140093197667648"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Plot</a>
  - <span class="keep-together" data-type="index-term">square root
    scales</span>, <a href="#ch07.xhtml_idm140093197602784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Square Root Scales</a>
  - <span class="keep-together" data-type="index-term">time
    scales</span>, <a href="#ch07.xhtml_Stime07"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Time Scales</a>-<a href="#ch07.xhtml_idm140093196942752"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Formatting dates and strings</a>
- <span class="keep-together" data-type="index-term">scatterplots</span>
  - <span class="keep-together" data-type="index-term">adding x/y axes
    to</span>, <a href="#ch08.xhtml_idm140093196910320"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Axes</a>
  - <span class="keep-together" data-type="index-term">creating</span>,
    <a href="#ch06.xhtml_Screat06"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Making a Scatterplot</a>-<a href="#ch06.xhtml_idm140093199350464"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Labels</a>
  - <span class="keep-together" data-type="index-term">scaling</span>,
    <a href="#ch07.xhtml_SPscale07"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Scaling the Scatterplot</a>-<a href="#ch07.xhtml_idm140093197668592"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Refining the Plot</a>
- <span class="keep-together" data-type="index-term">scope</span>
  - <span class="keep-together"
    data-type="index-term">block-level</span>,
    <a href="#ch03.xhtml_idm140093205730288"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Function-level scope</a>
  - <span class="keep-together"
    data-type="index-term">function-level</span>,
    <a href="#ch03.xhtml_idm140093205731232"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Function-level scope</a>
- <span class="keep-together" data-type="index-term">screen coordinates
  vs. geo-coordinates</span>, <a href="#ch14.xhtml_idm140093182058000"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Points</a>
- <span class="keep-together" data-type="index-term">scripts</span>,
  <a href="#ch03.xhtml_idm140093206318752"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Referencing Scripts</a>
- <span class="keep-together" data-type="index-term">select()</span>,
  <a href="#ch05.xhtml_idm140093204277136"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">One Link at a Time</a>,
  <a href="#ch09.xhtml_idm140093192230912"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Select</a>
- <span class="keep-together" data-type="index-term">selectAll()</span>,
  <a href="#ch09.xhtml_idm140093192230176"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Select</a>
- <span class="keep-together"
  data-type="index-term">selection.append()</span>,
  <a href="#app05.xhtml_idm140093176308272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.attr()</span>,
  <a href="#app05.xhtml_idm140093176268208"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.call()</span>,
  <a href="#app05.xhtml_idm140093174783840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Axes</a>
- <span class="keep-together"
  data-type="index-term">selection.classed()</span>,
  <a href="#app05.xhtml_idm140093176064320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.data()</span>,
  <a href="#app05.xhtml_idm140093176038288"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.datum()</span>,
  <a href="#app05.xhtml_idm140093176001472"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.each()</span>,
  <a href="#app05.xhtml_idm140093176142400"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.enter()</span>,
  <a href="#app05.xhtml_idm140093175957488"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.exit()</span>,
  <a href="#app05.xhtml_idm140093175808640"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.filter()</span>,
  <a href="#app05.xhtml_idm140093175683728"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.merge()</span>,
  <a href="#app05.xhtml_idm140093175828816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.on()</span>,
  <a href="#app05.xhtml_idm140093174893280"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Interactivity</a>
- <span class="keep-together"
  data-type="index-term">selection.remove()</span>,
  <a href="#app05.xhtml_idm140093176227792"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>,
  <a href="#app05.xhtml_idm140093175764000"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together"
  data-type="index-term">selection.style()</span>,
  <a href="#app05.xhtml_idm140093176262880"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.text()</span>,
  <a href="#app05.xhtml_idm140093176286272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selections</a>
- <span class="keep-together"
  data-type="index-term">selection.transition()</span>,
  <a href="#app05.xhtml_idm140093175461312"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transitions</a>
- <span class="keep-together" data-type="index-term">selections</span>
  - <span class="keep-together" data-type="index-term">chained syntax
    for</span>, <a href="#ch12.xhtml_Schain12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Getting More Specific</a>-<a href="#ch12.xhtml_idm140093187150432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Getting More Specific</a>
  - <span class="keep-together" data-type="index-term">D3 methods for
    making</span>, <a href="#ch12.xhtml_idm140093187432816"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Selections</a>,
    <a href="#app05.xhtml_idm140093176332816"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Selections</a>
  - <span class="keep-together" data-type="index-term">enter
    selection</span>, <a href="#ch12.xhtml_Senter12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Enter Selection</a>-<a href="#ch12.xhtml_idm140093186439360"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Enter Selection</a>
  - <span class="keep-together" data-type="index-term">exit
    selection</span>, <a href="#ch12.xhtml_idm140093186254112"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Exit Selection</a>
  - <span class="keep-together" data-type="index-term">filtering based
    on data</span>, <a href="#ch12.xhtml_Sfilter12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Filtering Selections Based on Data</a>-<a href="#ch12.xhtml_idm140093185501856"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">To each() Their Own</a>
  - <span class="keep-together" data-type="index-term">inability to
    modify</span>, <a href="#app02.xhtml_idm140093176828592"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Selections</a>
  - <span class="keep-together" data-type="index-term">merging</span>,
    <a href="#ch12.xhtml_Smerg12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Merging Selections</a>-<a href="#ch12.xhtml_idm140093186257088"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Merging Selections</a>
  - <span class="keep-together" data-type="index-term">overview
    of</span>, <a href="#ch12.xhtml_Sover12"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Closer Look at Selections</a>-<a href="#ch12.xhtml_idm140093187396912"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Closer Look at Selections</a>
  - <span class="keep-together" data-type="index-term">storing</span>,
    <a href="#ch12.xhtml_idm140093187148208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Storing Selections</a>
- <span class="keep-together" data-type="index-term">selectors</span>,
  <a href="#ch03.xhtml_idm140093210798512"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">CSS</a>
- <span class="keep-together" data-type="index-term">semantic
  structure</span>, <a href="#ch03.xhtml_idm140093211591936"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Content Plus Structure</a>
- <span class="keep-together" data-type="index-term">sequential numbers,
  generating arrays of</span>, <a href="#ch09.xhtml_idm140093195535552"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Ordinal Scales, Explained</a>
- <span class="keep-together" data-type="index-term">servers</span>,
  <a href="#ch03.xhtml_idm140093208200144"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">shape-rendering
  property</span>, <a href="#ch08.xhtml_idm140093196391360"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together" data-type="index-term">shapefiles</span>,
  <a href="#ch14.xhtml_idm140093179679376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Find Shapefiles</a>
- <span class="keep-together" data-type="index-term">sibling
  elements</span>, <a href="#ch03.xhtml_idm140093210907232"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">DOM</a>
- <span class="keep-together" data-type="index-term">sort()</span>,
  <a href="#ch10.xhtml_idm140093189911264"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">sorting</span>,
  <a href="#ch10.xhtml_idm140093190020656"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Click to Sort</a>
- <span class="keep-together" data-type="index-term">source code,
  viewing</span>, <a href="#ch03.xhtml_idm140093211007920"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Developer Tools</a>
- <span class="keep-together" data-type="index-term">space-based
  indentation</span>, <a href="#ch12.xhtml_idm140093186944800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Getting More Specific</a>
- <span class="keep-together" data-type="index-term">specificity</span>,
  <a href="#ch03.xhtml_idm140093209975888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Inheritance, Cascading, and Specificity</a>
- <span class="keep-together" data-type="index-term">square root
  scales</span>, <a href="#ch07.xhtml_idm140093197601808"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Square Root Scales</a>
- <span class="keep-together" data-type="index-term">stack layout</span>
  - <span class="keep-together" data-type="index-term">anchoring
    bars</span>, <a href="#ch13.xhtml_idm140093184452528"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Anchoring Those Bars</a>
  - <span class="keep-together" data-type="index-term">creating</span>,
    <a href="#ch13.xhtml_idm140093184849696"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stack Layout</a>
  - <span class="keep-together" data-type="index-term">specifying
    order</span>, <a href="#ch13.xhtml_idm140093184473968"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A New Order</a>
  - <span class="keep-together" data-type="index-term">stacking
    areas</span>, <a href="#ch13.xhtml_idm140093184315680"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stacked Areas</a>
  - <span class="keep-together" data-type="index-term">version 4.0
    changes</span>, <a href="#app02.xhtml_idm140093176608896"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Stack Layout</a>
- <span class="keep-together" data-type="index-term">stack()</span>,
  <a href="#ch16.xhtml_idm140093178971056"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Load and Parse the Data</a>
- <span class="keep-together" data-type="index-term">staggered
  transitions</span>, <a href="#ch09.xhtml_idm140093193905728"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Please Do Not delay()</a>
- <span class="keep-together" data-type="index-term">strict equality
  operators</span>, <a href="#ch03.xhtml_idm140093205913952"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>
- <span class="keep-together" data-type="index-term">style()</span>,
  <a href="#ch05.xhtml_idm140093203114560"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Beyond Text</a>,
  <a href="#ch06.xhtml_idm140093202546656"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Styles</a>
- <span class="keep-together" data-type="index-term">styles</span>
  - <span class="keep-together" data-type="index-term">vs.
    classes</span>, <a href="#ch06.xhtml_idm140093202755008"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Classes</a>
  - <span class="keep-together" data-type="index-term">referencing
    CSS</span>, <a href="#ch03.xhtml_idm140093210364320"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Referencing Styles</a>
  - <span class="keep-together" data-type="index-term">setting</span>,
    <a href="#ch06.xhtml_idm140093202545152"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Styles</a>
- <span class="keep-together" data-type="index-term">SVG (Scalable
  Vector Graphics)</span>
  - <span class="keep-together" data-type="index-term">adding colors
    to</span>, <a href="#ch06.xhtml_idm140093201321200"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Pretty Colors, Oooh!</a>
  - <span class="keep-together" data-type="index-term">applying styles
    to elements</span>, <a href="#ch03.xhtml_idm140093205388064"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Styling SVG Elements</a>
  - <span class="keep-together" data-type="index-term">applying
    transparency</span>, <a href="#ch03.xhtml_idm140093205043488"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transparency</a>
  - <span class="keep-together" data-type="index-term">axis functions
    and</span>, <a href="#ch08.xhtml_idm140093196903808"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Introducing Axes</a>
  - <span class="keep-together" data-type="index-term">benefits
    of</span>, <a href="#ch03.xhtml_idm140093205771376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>
  - <span class="keep-together" data-type="index-term">browser
    compatibility</span>, <a href="#ch03.xhtml_idm140093204733744"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">A Note on Compatibility</a>
  - <span class="keep-together" data-type="index-term">creating
    elements</span>, <a href="#ch03.xhtml_idm140093205612224"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The SVG Element</a>,
    <a href="#ch06.xhtml_idm140093201985712"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Create the SVG</a>
  - <span class="keep-together" data-type="index-term">creating
    shapes</span>, <a href="#ch03.xhtml_idm140093205648656"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Simple Shapes</a>,
    <a href="#ch06.xhtml_idm140093201663584"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data-Driven Shapes</a>
  - <span class="keep-together" data-type="index-term">creating
    tooltips</span>, <a href="#ch10.xhtml_idm140093189359424"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG Element Tooltips</a>
  - <span class="keep-together" data-type="index-term">drawing irregular
    forms</span> (<span class="keep-together" gentext="see">see</span>
    paths)
  - <span class="keep-together" data-type="index-term">drawing
    overlapping shapes</span>, <a href="#ch03.xhtml_idm140093205263376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Layering and Drawing Order</a>,
    <a href="#ch10.xhtml_idm140093190115840"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together" data-type="index-term">exporting D3
    visualizations as</span>, <a href="#ch15.xhtml_SVGexport15"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>-<a href="#ch15.xhtml_idm140093179339008"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG</a>
  - <span class="keep-together" data-type="index-term">grouping
    elements</span>, <a href="#ch10.xhtml_idm140093190032608"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Grouping SVG Elements</a>
  - <span class="keep-together" data-type="index-term">layering and
    drawing order</span>, <a href="#ch03.xhtml_idm140093205268384"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Layering and Drawing Order</a>
  - <span class="keep-together" data-type="index-term">property/value
    pairs</span>, <a href="#ch06.xhtml_idm140093201990016"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Drawing SVGs</a>
  - <span class="keep-together" data-type="index-term">styling with
    CSS</span>, <a href="#ch08.xhtml_idm140093196414688"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>
  - <span class="keep-together"
    data-type="index-term">transformations</span>,
    <a href="#ch08.xhtml_idm140093196649152"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Positioning Axes</a>

</div>

<div class="dedication" data-type="indexdiv">

### T

- <span class="keep-together" data-type="index-term">tags</span>,
  <a href="#ch03.xhtml_idm140093211926624"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Adding Structure with Elements</a>
- <span class="keep-together" data-type="index-term">text()</span>,
  <a href="#ch05.xhtml_idm140093204264912"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">One Link at a Time</a>
- <span class="keep-together" data-type="index-term">text-based
  data</span>, <a href="#ch05.xhtml_idm140093204550224"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
  - (<span class="keep-together" gentext="see">see also</span> data)
- <span class="keep-together" data-type="index-term">this
  keyword</span>, <a href="#ch10.xhtml_idm140093190298544"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Hover to Highlight</a>
- <span class="keep-together" data-type="index-term">3D drawing</span>
  - <span class="keep-together" data-type="index-term">alternative tools
    for</span>, <a href="#ch02.xhtml_idm140093208295888"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Three-Dimensional</a>
  - <span class="keep-together"
    data-type="index-term">projections</span>,
    <a href="#ch14.xhtml_idm140093182527728"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Projections</a>
- <span class="keep-together"
  data-type="index-term">tickFormat()</span>,
  <a href="#ch08.xhtml_idm140093195996960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Formatting Tick Labels</a>
- <span class="keep-together" data-type="index-term">ticks (time
  measurement)</span>, <a href="#ch13.xhtml_idm140093183462096"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Updating Visuals over Time</a>
- <span class="keep-together"
  data-type="index-term">tickValues()</span>,
  <a href="#ch08.xhtml_idm140093196294368"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Check for Ticks</a>
- <span class="keep-together" data-type="index-term">time scales</span>,
  <a href="#ch07.xhtml_time07"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Time Scales</a>-<a href="#ch07.xhtml_idm140093196943696"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Formatting dates and strings</a>
- <span class="keep-together" data-type="index-term">time-based
  axes</span>, <a href="#ch08.xhtml_idm140093195960240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Time-Based Axes</a>
- <span class="keep-together" data-type="index-term">tooltips</span>,
  <a href="#ch10.xhtml_tool10"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Tooltips</a>-<a href="#ch10.xhtml_idm140093188649648"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">HTML div Tooltips</a>
  - <span class="keep-together" data-type="index-term">default</span>,
    <a href="#ch10.xhtml_idm140093189635584"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Default Browser Tooltips</a>
  - <span class="keep-together" data-type="index-term">HTML div
    tooltips</span>, <a href="#ch10.xhtml_idm140093189137952"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">HTML div Tooltips</a>
  - <span class="keep-together" data-type="index-term">SVG
    elements</span>, <a href="#ch10.xhtml_idm140093189360432"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">SVG Element Tooltips</a>
- <span class="keep-together" data-type="index-term">touch-based
  interfaces</span>, <a href="#ch10.xhtml_idm140093188645120"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Consideration for Touch Devices</a>
- <span class="keep-together"
  data-type="index-term">transformations</span>,
  <a href="#ch02.xhtml_idm140093207938240"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">What It Does</a>,
  <a href="#ch08.xhtml_trans08"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Setting Up an Axis</a>-<a href="#ch08.xhtml_idm140093196466192"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>,
  <a href="#ch08.xhtml_idm140093196649888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together"
  data-type="index-term">transition.delay()</span>,
  <a href="#app05.xhtml_idm140093175665296"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transitions</a>
- <span class="keep-together"
  data-type="index-term">transition.duration()</span>,
  <a href="#app05.xhtml_idm140093175383584"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transitions</a>
- <span class="keep-together"
  data-type="index-term">transition.ease()</span>,
  <a href="#app05.xhtml_idm140093175338624"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transitions</a>
- <span class="keep-together"
  data-type="index-term">transition.on()</span>,
  <a href="#app05.xhtml_idm140093175314784"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transitions</a>
- <span class="keep-together" data-type="index-term">transitions</span>
  - <span class="keep-together" data-type="index-term">adding
    animated</span>, <a href="#ch09.xhtml_idm140093194308128"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transitions</a>
  - <span class="keep-together" data-type="index-term">chaining
    together</span>, <a href="#ch09.xhtml_idm140093192755648"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">End gracefully</a>
  - <span class="keep-together" data-type="index-term">clipping
    paths</span>, <a href="#ch09.xhtml_idm140093192682016"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Containing visual elements with clipping
    paths</a>, <a href="#ch11.xhtml_idm140093187438208"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Area Charts</a>
  - <span class="keep-together" data-type="index-term">controlling
    duration of</span>, <a href="#ch09.xhtml_idm140093194556656"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">duration(), or How Long Is This Going to
    Take?</a>
  - <span class="keep-together" data-type="index-term">definition of
    term</span>, <a href="#ch09.xhtml_idm140093195943456"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updates, Transitions, and Motion</a>
  - <span class="keep-together" data-type="index-term">delaying start
    of</span>, <a href="#ch09.xhtml_idm140093193906736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Please Do Not delay()</a>
  - <span class="keep-together" data-type="index-term">equalizing pace
    of</span>, <a href="#ch09.xhtml_idm140093194008784"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">ease()-y Does It</a>
  - <span class="keep-together" data-type="index-term">exit
    transition</span>, <a href="#ch09.xhtml_idm140093191315440"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exit transition</a>
  - <span class="keep-together" data-type="index-term">in mouseover
    events</span>, <a href="#ch10.xhtml_idm140093190434768"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Hover to Highlight</a>
  - <span class="keep-together"
    data-type="index-term">interrupted</span>,
    <a href="#ch10.xhtml_idm140093189799200"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Click to Sort</a>
  - <span class="keep-together" data-type="index-term">limit to active
    number</span>, <a href="#ch09.xhtml_idm140093193038912"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Warning: Start carefully</a>
  - <span class="keep-together" data-type="index-term">marking
    beginnings/endings of</span>,
    <a href="#ch09.xhtml_idm140093193268736"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">on() Transition Starts and Ends</a>
  - <span class="keep-together" data-type="index-term">methods quick
    reference</span>, <a href="#app05.xhtml_idm140093175460480"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transitions</a>
  - <span class="keep-together" data-type="index-term">randomizing
    data</span>, <a href="#ch09.xhtml_idm140093193879184"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Randomizing the Data</a>
  - <span class="keep-together" data-type="index-term">updating
    axes</span>, <a href="#ch09.xhtml_idm140093193556672"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating Axes</a>
  - <span class="keep-together" data-type="index-term">updating
    scales</span>, <a href="#ch09.xhtml_idm140093193635264"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating Scales</a>
  - <span class="keep-together" data-type="index-term">version 4.0
    changes</span>, <a href="#app02.xhtml_idm140093176661472"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transitions</a>
- <span class="keep-together" data-type="index-term">translation
  transforms</span>, <a href="#ch08.xhtml_idm140093196794496"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Positioning Axes</a>
- <span class="keep-together"
  data-type="index-term">transparency</span>,
  <a href="#ch03.xhtml_idm140093205042512"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Transparency</a>
- <span class="keep-together" data-type="index-term">tutorials</span>,
  <a href="#preface01.xhtml_idm140093207812800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Preface</a>
- <span class="keep-together" data-type="index-term">.txt (plain text
  files)</span>, <a href="#ch05.xhtml_idm140093204549216"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Data</a>
- <span class="keep-together" data-type="index-term">type
  converting</span>, <a href="#ch03.xhtml_idm140093205950976"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>
- <span class="keep-together" data-type="index-term">type
  selectors</span>, <a href="#ch03.xhtml_idm140093210659888"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Selectors</a>
- <span class="keep-together" data-type="index-term">typeof
  operator</span>, <a href="#ch03.xhtml_idm140093205998384"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Dynamic typing</a>
- <span class="keep-together" data-type="index-term">typographical
  conventions</span>, <a href="#preface01.xhtml_idm140093207761152"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Conventions Used in This Book</a>

</div>

<div class="dedication" data-type="indexdiv">

### U

- <span class="keep-together" data-type="index-term">ul (unordered
  list)</span>, <a href="#ch03.xhtml_idm140093210862384"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">updates</span>,
  <a href="#ch09.xhtml_update09"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Updates, Transitions, and Motion</a>-<a href="#ch09.xhtml_idm140093190674704"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Recap</a> (<span class="keep-together"
  gentext="see">see</span> also transitions)
  - <span class="keep-together" data-type="index-term">adding and
    removing data</span>, <a href="#ch09.xhtml_idm140093190960128"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Add and Remove: Combo Platter</a>
  - <span class="keep-together" data-type="index-term">adding
    values/elements</span>, <a href="#ch09.xhtml_Uvalue09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Kinds of Data Updates</a>-<a href="#ch09.xhtml_idm140093191890272"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Update</a>
  - <span class="keep-together" data-type="index-term">animation
    of</span>, <a href="#ch09.xhtml_idm140093194306176"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transitions</a>
  - <span class="keep-together" data-type="index-term">bar
    charts</span>, <a href="#ch09.xhtml_Ubar09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Modernizing the Bar Chart</a>-<a href="#ch09.xhtml_idm140093195115744"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Updates</a>
  - <span class="keep-together" data-type="index-term">basic steps
    to</span>, <a href="#ch09.xhtml_idm140093195250032"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Updating Data</a>,
    <a href="#ch09.xhtml_idm140093194938624"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Changing the Data</a>
  - <span class="keep-together" data-type="index-term">data
    joins</span>, <a href="#ch09.xhtml_Ujoin09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Data Joins with Keys</a>-<a href="#ch09.xhtml_idm140093190966448"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Exit transition</a>
  - <span class="keep-together" data-type="index-term">event listeners
    and</span>, <a href="#ch09.xhtml_idm140093195281376"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Interaction via Event Listeners</a>
  - <span class="keep-together" data-type="index-term">overview
    of</span>, <a href="#ch09.xhtml_idm140093190692096"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Recap</a>
  - <span class="keep-together" data-type="index-term">removing
    values/elements</span>, <a href="#ch09.xhtml_Uremove09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Removing Values (and Elements)</a>-<a href="#ch09.xhtml_idm140093191764032"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Making a smooth exit</a>
- <span class="keep-together" data-type="index-term">URLs (Uniform
  Resource Locators)</span>, <a href="#ch03.xhtml_idm140093208191680"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>

</div>

<div class="dedication" data-type="indexdiv">

### V

- <span class="keep-together" data-type="index-term">values</span>
  - <span class="keep-together" data-type="index-term">adding</span>,
    <a href="#ch09.xhtml_Vadd09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Other Kinds of Data Updates</a>-<a href="#ch09.xhtml_idm140093191889296"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Update</a>
  - <span class="keep-together" data-type="index-term">animating changes
    in</span>, <a href="#ch09.xhtml_idm140093194307120"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Transitions</a>
  - <span class="keep-together" data-type="index-term">in CSS</span>,
    <a href="#ch03.xhtml_idm140093210515072"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Properties and Values</a>
  - <span class="keep-together" data-type="index-term">in
    objects</span>, <a href="#ch03.xhtml_idm140093208566592"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Objects</a>
  - <span class="keep-together" data-type="index-term">removing</span>,
    <a href="#ch09.xhtml_Vremov09"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Removing Values (and Elements)</a>-<a href="#ch09.xhtml_idm140093191763056"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Making a smooth exit</a>
- <span class="keep-together" data-type="index-term">variable
  hoisting</span>, <a href="#ch03.xhtml_idm140093205898272"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Variable hoisting</a>
- <span class="keep-together" data-type="index-term">variable
  scope</span>, <a href="#ch03.xhtml_idm140093205731904"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Function-level scope</a>
- <span class="keep-together" data-type="index-term">variables</span>,
  <a href="#ch03.xhtml_idm140093209958608"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Variables</a>,
  <a href="#ch06.xhtml_idm140093201814096"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Create the SVG</a>
- <span class="keep-together" data-type="index-term">vector data</span>,
  <a href="#ch14.xhtml_idm140093179665184"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Choose a Resolution</a>
- <span class="keep-together" data-type="index-term">vertical
  axis</span>, <a href="#ch08.xhtml_idm140093196188800"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Y Not?</a>
- <span class="keep-together" data-type="index-term">visual
  rules</span>, <a href="#ch03.xhtml_idm140093210872112"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">visual
  structure</span>, <a href="#ch03.xhtml_idm140093212126336"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Content Plus Structure</a>
- <span class="keep-together" data-type="index-term">visualization,
  definition of</span>,
  <a href="#ch01_split_000.xhtml_idm140093208078832"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why Data Visualization?</a>
  - (<span class="keep-together" gentext="see">see also</span> data
    visualization)

</div>

<div class="dedication" data-type="indexdiv">

### W

- <span class="keep-together" data-type="index-term">Web development
  tools</span>, <a href="#ch03.xhtml_webdev03"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Developer Tools</a>-<a href="#ch03.xhtml_idm140093210875840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Developer Tools</a>
- <span class="keep-together" data-type="index-term">Web
  fundamentals</span>, <a href="#ch03.xhtml_webfund03"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>-<a href="#ch03.xhtml_idm140093214272032"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">The Web</a>
- <span class="keep-together" data-type="index-term">web
  inspector</span>, <a href="#ch03.xhtml_idm140093210866960"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Rendering and the Box Model</a>
- <span class="keep-together" data-type="index-term">Web servers</span>
  - <span class="keep-together" data-type="index-term">operation
    of</span>, <a href="#ch03.xhtml_idm140093208201152"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">The Web</a>
  - <span class="keep-together" data-type="index-term">setting
    up</span>, <a href="#ch04.xhtml_WSsetup04"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Setting Up a Web Server</a>-<a href="#ch04.xhtml_idm140093204558496"
    class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
    data-type="index:locator">Diving In</a>
- <span class="keep-together" data-type="index-term">web-standard
  technologies, benefits of</span>,
  <a href="#ch01_split_000.xhtml_idm140093221170592"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Why on the Web?</a>
- <span class="keep-together" data-type="index-term">wedges</span>,
  <a href="#ch13.xhtml_idm140093185366880"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Pie Layout</a>
- <span class="keep-together" data-type="index-term">whitespace,
  adding</span>, <a href="#ch09.xhtml_idm140093195502880"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Starting Your Own Band</a>
  - (<span class="keep-together" gentext="see">see also</span> padding)

</div>

<div class="dedication" data-type="indexdiv">

### Z

- <span class="keep-together" data-type="index-term">zoom
  behavior</span>, <a href="#app02.xhtml_idm140093176604320"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Zooming</a>
- <span class="keep-together" data-type="index-term">zooming
  (maps)</span>, <a href="#ch14.xhtml_zoom14"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Zooming</a>-<a href="#ch14.xhtml_idm140093179832720"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="index:locator">Preset Views</a>

</div>

</div>

</div>

</div>

</div>

<span id="colophon01.xhtml"></span>

<div id="colophon01.xhtml_sbo-rt-content" class="calibre1">

<div class="section calibre2 colophon" data-type="colophon"
pdf-bookmark="About the Author">

<div id="colophon01.xhtml_idm140093174176304" class="dedication">

# About the Author

**Scott Murray** is a designer who writes software to create data
visualizations and other interactive experiences. Scott is in the
Learning Group at O’Reilly Media, and has taught numerous courses and
workshops on data visualization and creative coding. He is also a Senior
Developer for <a href="http://processing.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Processing</a>,
and is working on his next book, <a href="http://p5book.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em>Creative
Coding and Data Visualization with p5.js: Drawing on the Web with
JavaScript</em></a>. Scott earned an AB from Vassar College and an MFA
from the Dynamic Media Institute at the Massachusetts College of Art and
Design. His work can be seen at <a href="http://alignedleft.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em>alignedleft.com</em></a>.

</div>

</div>

</div>

<span id="colophon02.xhtml"></span>

<div id="colophon02.xhtml_sbo-rt-content" class="calibre1">

<div class="section calibre2 colophon" data-type="colophon"
pdf-bookmark="Colophon">

<div id="colophon02.xhtml_colophon" class="dedication">

# Colophon

The animals on the cover of *Interactive Data Visualization for the Web*
are long-tailed tits or bushtits (*Aegithalos caudatus*). The bushtit is
a common species of bird found throughout Europe and Asia. The
*caudatus* group of the species has a pure white head.

These birds are known for their tiny size, measuring around only 13 to
15 cm in length, including their tail. The long-tailed tit is recognized
by its stubby bill, contrasted to its long, narrow tail. Females and
males are indistinguishable, both undergoing a full moult before their
first winter. Their adult plumage is primarily black and white with
accents of gray and pink.

The bushtit inhabits deciduous and mixed woodland, feeding on insects
with a preference for the eggs and larvae of moths and butterflies, and
favoring oak, ash, and sycamore trees. They tend to nest in scrub areas
usually closer to the ground.

The cover image is from a loose plate of Hungarian origin. The cover
font is Adobe ITC Garamond. The text font is Adobe Minion Pro; the
heading font is Adobe Myriad Condensed; and the code font is Dalton
Maag’s Ubuntu Mono.

</div>

</div>

</div>
