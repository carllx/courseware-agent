# <span class="keep-together">Chapter 13. </span>Layouts

Contrary <span id="ch13.xhtml_idm140093185496576"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="layouts" secondary="role of"></span>to
what the name implies, D3 *layouts* do not, in fact, lay anything out
for you on the screen. The layout methods have no direct *visual*
output. Rather, D3 layouts take data that you provide and remap or
otherwise transform it, thereby generating *new* data that is more
convenient for a specific visual task. It’s still up to you to take that
new data and generate visuals from it.

The <span id="ch13.xhtml_idm140093185493424"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="layouts" secondary="list of"></span>list
of D3 layouts includes:

- Chord

- Cluster

- Force

- Pack

- Partition

- Pie

- Stack

- Tree

- Treemap

In this chapter, I introduce three of the most common: pie, stack, and
force layouts. Each layout performs a different function, and each has
its own syntax and considerations.

If you are curious about the other D3 layouts, work your way through the
examples in this chapter first, to get familiar with D3’s general
approach. Then check out
<a href="https://github.com/mbostock/d3/wiki/Gallery"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">the many
examples on the D3 website</a>, and be sure to reference
<a href="https://github.com/d3/d3/blob/master/API.md"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">the official API
documentation</a>.

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Pie Layout">

<div id="ch13.xhtml_idm140093185480768" class="dedication">

# Pie Layout

`d3.pie()` <span id="ch13.xhtml_idm140093185477760"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.pie()"></span><span id="ch13.xhtml_Lpie13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="layouts"
secondary="pie layout"></span><span id="ch13.xhtml_pie13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="pie layout"></span><span id="ch13.xhtml_Cpie13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="pie charts"></span>might not be as delicious as it sounds,
but it’s still worthy of your attention. It is typically used to create
a doughnut or pie chart, like the example in
<a href="#ch13.xhtml_simple_pie_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-1</a>.

<figure class="calibre35">
<div id="ch13.xhtml_simple_pie_chart" class="figure">
<img
src="images/0bd5dd9c42880cdf2835e1bc867310353e9db837e117835fac406bc6930c0219.png"
class="calibre208" alt="dvw2 1301" />
<h6 class="calibre37"><span class="keep-together">Figure 13-1. </span>A
simple pie chart</h6>
</div>
</figure>

Feel free to open the sample code for this in *01_pie.html* and poke
around.

To draw those pretty wedges, we need to know a number of measurements,
including an inner and outer radius for each wedge, plus the starting
and ending angles. The purpose of the pie layout is to take your data
and calculate all those messy angles for you, sparing you from ever
having to think about radians.

Remember radians? <span id="ch13.xhtml_idm140093185468256"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="degrees vs. radians"></span><span id="ch13.xhtml_idm140093185467520"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="radians"></span>In case you don’t, here’s
a quick refresher. Just as there are 360° in a circle, there are 2π
radians. So π radians equals 180°, or half a circle. Most people find it
easier to think in terms of degrees; computers prefer radians.

For this pie chart, let’s start, as usual, with a very simple dataset:

``` calibre39
var dataset = [ 5, 10, 20, 45, 6, 25 ];
```

We can define a default pie layout very simply as:

``` calibre39
var pie = d3.pie();
```

Then, all that remains is to hand off our data to the new `pie()`
function, as in <span class="keep-together">`pie(dataset)`</span>.
Compare the datasets before and after in
<a href="#ch13.xhtml_pieified_data"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-2</a>.

<figure class="calibre35">
<div id="ch13.xhtml_pieified_data" class="figure">
<img
src="images/972bcb818f97df15a62de286a38b318128278275199fac9ac4a6c5208ffe40ad.png"
class="calibre209" alt="dvw2 1302" />
<h6 class="calibre37"><span class="keep-together">Figure 13-2.
</span>Your data, pie-ified</h6>
</div>
</figure>

The pie layout takes our simple array of numbers and generates an array
of objects, one object for each value. Each of those objects now has a
few new values—most important, `startAngle` and `endAngle`. Wow, that
was easy!

Now, <span id="ch13.xhtml_idm140093185367616"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.arc()"></span><span id="ch13.xhtml_idm140093185366880"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="wedges"></span>to actually draw the
wedges, we turn to `d3.arc()`, a handy built-in function for drawing
arcs as SVG `path` elements. As you know, `path` syntax is messy. For
example, here’s the code for the big, red wedge in
<a href="#ch13.xhtml_simple_pie_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-1</a>:

``` calibre39
<path fill="#d62728" d="M9.184850993605149e-15,-150A150,150 0 0,1
	83.99621792063931,124.27644738657631L0,0Z"></path>
```

It’s best to let functions like `d3.arc()` handle generating `path`s
programatically. You don’t want to try writing this stuff out by hand.

Arcs are defined as custom functions, and they require inner and outer
radius values:

``` calibre39
var w = 300;
var h = 300;

var outerRadius = w / 2;
var innerRadius = 0;
var arc = d3.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);
```

Here I’m setting the size of the whole chart to be 300 by 300 square.
Then I’m setting the `outerRadius` to half of that, or 150. The
`innerRadius` is zero. We’ll revisit
<span class="keep-together">`innerRadius`</span> in a moment.

We’re ready to draw some wedges! First, we create the SVG element, per
usual:

``` calibre39
//Create SVG element
var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);
```

Then we can create new groups for each incoming wedge, binding the
pie-ified data to the new elements, and translating each group into the
center of the chart, so the `path`s will appear in the right place:

``` calibre39
//Set up groups
var arcs = svg.selectAll("g.arc")
    .data(pie(dataset))
    .enter()
    .append("g")
    .attr("class", "arc")
    .attr("transform", "translate(" + outerRadius + ", " + outerRadius + ")");
```

Note that we’re saving a reference to each newly created `g` in a
variable called `arcs`.

Finally, within each new `g`, we append a `path`. A `path`s path
description is defined in the `d` attribute. So here we call the `arc`
generator, which generates the path information based on the data
already bound to this group:

``` calibre39
//Draw arc paths
arcs.append("path")
    .attr("fill", function(d, i) {
        return color(i);
    })
    .attr("d", arc);
```

The syntax in this last line is new to us. `arc` is our path generator
function (defined earlier), but you’ll notice here we’re not *calling*
the function (which would require parentheses, as in `arc()`), but we
are passing the `arc` function itself *as a parameter* to `attr()`. The
`attr()` function then sets a `d` attribute with the value set to the
results of the `arc()` function. When a named function is specified as a
parameter in this way, D3 automatically passes in the datum and index
values, without us having to write them out explicitly. So, that last
line of code:

``` calibre39
    .attr("d", arc);
```

is equivalent to the more verbose:

``` calibre39
    .attr("d", function(d, i) {
        return arc(d, i);
    });
```

Oh, <span id="ch13.xhtml_idm140093184979264"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="colors"
secondary="categorical"></span>and you might be wondering where those
colors are coming from. If you check out *01_pie.html*, you’ll note this
line:

``` calibre39
var color = d3.scaleOrdinal(d3.schemeCategory10);
```

D3 has a number of handy ways to generate categorical colors. They might
not be your favorite colors, but they are quick to drop into any
visualization while you’re in the prototyping stage.
`d3.schemeCategory10` is an array of 10 different colors. (Try typing
`d3.schemeCategory10` into the console to verify.)
<span id="ch13.xhtml_idm140093184934928"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="ordinal scales"></span>By feeding it to
`d3.scaleOrdinal()`, you can quickly generate an ordinal scale whose
output range is those 10 colors. (See <a href="http://bit.ly/2uCHTHC"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">the wiki</a> for
more information on the included color scales as well as
<a href="https://github.com/d3/d3-scale-chromatic"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">perceptually
calibrated color palettes</a>, based on research by Cynthia Brewer.)

Lastly, we can generate text labels for each wedge:

``` calibre39
arcs.append("text")
    .attr("transform", function(d) {
    	    return "translate(" + arc.centroid(d) + ")";
    })
    .attr("text-anchor", "middle")
    .text(function(d) {
    	    return d.value;
    });
```

Note that in `text()`, we reference the value with `d.value` instead of
just `d`. This is because we bound the pie-ified data, so instead of
referencing our original array (`d`), we have to reference the array of
objects (`d.value`).

The <span id="ch13.xhtml_idm140093184876544"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="centroids"></span><span id="ch13.xhtml_idm140093184875808"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="drawing"
secondary="irregular forms"></span>only thing new here is
`arc.centroid(d)`. Huh? A *centroid* is the calculated center point of
any shape, whether that shape is regular (like a square) or highly
irregular (like an outline of the state of Maryland). `arc.centroid()`
is a super-helpful function that calculates and returns the center point
of any arc. We translate each `text` label element to each arc’s
centroid, and that’s how we get the text labels to float right in the
middle of each wedge.

Bonus tip: <span id="ch13.xhtml_idm140093184872080"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="doughnut charts"></span><span id="ch13.xhtml_idm140093184871344"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="doughnut charts"></span>remember how `arc()` required an
`innerRadius` value? We can expand that to anything greater than zero,
and our pie chart becomes a *doughnut* chart like the one shown in
<a href="#ch13.xhtml_simple_doughnut_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-3</a>.

``` calibre39
var innerRadius = w / 3;
```

<figure class="calibre35">
<div id="ch13.xhtml_simple_doughnut_chart" class="figure">
<img
src="images/c8d836d74a0ae94fd2c9ee753c45b239011dec2d6f5455c6247ea9d43f851c99.png"
class="calibre210" alt="dvw2 1303" />
<h6 class="calibre37"><span class="keep-together">Figure 13-3. </span>A
simple doughnut chart</h6>
</div>
</figure>

Check <span id="ch13.xhtml_idm140093184773712"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="ring charts"></span><span id="ch13.xhtml_idm140093184772976"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts" secondary="ring charts"></span>it
out in *02_doughnut.html*.

One more thing: the pie layout automatically reordered our data values
from largest to smallest. Remember, we started with
`[ 5, 10, 20, 45, 6, 25 ]`, so the small value of 6 should have appeared
between 45 and 25, but no—the layout sorted our values in descending
order, so the chart began with 45 at the 12 o’clock position, and
everything just goes clockwise from
there.<span id="ch13.xhtml_idm140093184861728"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Lpie13"></span><span id="ch13.xhtml_idm140093184860784"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="pie13"></span>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Stack Layout">

<div id="ch13.xhtml_idm140093185479184" class="dedication">

# Stack Layout

`d3.stack()` <span id="ch13.xhtml_idm140093184858608"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.stack()"></span><span id="ch13.xhtml_Lstack13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="layouts"
secondary="stack layout"></span><span id="ch13.xhtml_BCstack13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="bar charts"
secondary="stacked"></span><span id="ch13.xhtml_idm140093184849696"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="stack layout"
secondary="creating"></span>converts two-dimensional data into “stacked”
data; it calculates a baseline value for each datum, so you can “stack”
layers of data on top of one another. This can be used to generate
stacked bar charts, stacked area charts, and even
<span class="keep-together">streamgraphs</span> (which are just stacked
area charts but without the rigid starting baseline value of zero).

For example, we’ll make the stacked bar chart in
<a href="#ch13.xhtml_simple_stacked_bar_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-4</a>. See all the code in
*03_stacked_bar.html*.

<figure class="calibre35">
<div id="ch13.xhtml_simple_stacked_bar_chart" class="figure">
<img
src="images/ba684c426ac6c544a1daeaaac8343acf3918bc6ee06eaa3153cfb1703758e0de.png"
class="calibre211" alt="dvw2 1304" />
<h6 class="calibre37"><span class="keep-together">Figure 13-4. </span>A
simple stacked bar chart (blue = apples, orange = oranges, green =
grapes)</h6>
</div>
</figure>

Start with some data, like this array of objects:

``` calibre39
var dataset = [
	{ apples: 5, oranges: 10, grapes: 22 },
	{ apples: 4, oranges: 12, grapes: 28 },
	{ apples: 2, oranges: 19, grapes: 32 },
	{ apples: 7, oranges: 23, grapes: 35 },
	{ apples: 23, oranges: 17, grapes: 43 }
];
```

Imagine each object in this array as corresponding to a single column or
stack of bars. Each category is represented by a different color. So the
first object (5 apples, 10, oranges, 22 grapes) corresponds to the bars
on the far left of the chart (short blue bar, taller orange bar, tallest
green bar).

The `dataset` is organized by *columns*. The stack layout reconfigures
the data to be organized by *categories*.

To achieve this, we initialize our stack layout function, specifying the
categories of interest with `keys()`. Then we call the stacking function
on `dataset`, storing the results in `series`:

``` calibre39
//Set up stack method
var stack = d3.stack()
              .keys([ "apples", "oranges", "grapes" ]);

//Data, stacked
var series = stack(dataset);
```

I strongly recommend typing both `dataset` and `series` in the console,
to compare the before and after states of the data.

<div class="calibre27 note" data-type="note">

# Exercise

In the console, find the first values of each type of fruit in
`dataset`. Then find the corresponding values in `series`. Try changing
the original values in `dataset`, then reload, and see how `series` is
impacted.

</div>

Note that `series` is now an array with three values, each one itself an
array corresponding to each categorical series: apples, oranges, and
grapes (in that order, because we specified them as such in `keys()`).

``` calibre39
//'series', the array formerly known as 'dataset'
[
	[ [ 0, 5],  [ 0, 4],  [ 0, 2],  [ 0, 7],  [ 0, 23] ],  // apples
	[ [ 5, 15], [ 4, 16], [ 2, 21], [ 7, 30], [23, 40] ],  // oranges
	[ [15, 37], [16, 44], [21, 53], [30, 65], [40, 83] ]   // grapes
]
```

Whoa, what are all these extra numbers? The first value in each
two-value array is the *baseline* value, and the second is the “topline”
value—the sum of all the preceding values. The baseline values are where
our bars begin, and the toplines are where they end. (Take the
difference to get the height of any given bar.)

Take a look at the original values for `apples` back in `dataset`. Note
that the `apples` values look like this: 5, 4, 2, 7, and 23. Now, find
those values in the first row of `series`. Note how the baseline values
in that first row are all 0. That makes sense, because `apples` is the
first series in the stack. That is, the apples are just sitting on the
ground (baseline of zero).

The oranges, however, will be stacked on top of the existing apples.
Find the original values for `oranges` back in `dataset`: 10, 12, 19,
23, and 17. You won’t be able to find those values in `series`, but take
a look at the `oranges` row. Note how the baseline values in that row
are the same as the data values from the preceding row (5, 4, 2, 7, and
23). The topline values are just the sum of those baseline values plus
the `oranges` data value. For example, `series[1][0]` is `[5, 15]`. The
baseline value is 5, and the topline value is 15 (5 apples plus 10
oranges).

The grapes are on the top of the stack, so in that series the baseline
values mirror the oranges’ topline values. The grapes’ topline values
are just the grapes’ baseline values plus the grapes’ data values.

Enough numbers! Let’s draw something. To “stack” elements visually, now
we can reference each data object’s baseline and topline values. Take
another look at *03_stacked_bar.html*, especially:

``` calibre39
// Add a group for each row of data
var groups = svg.selectAll("g")
    .data(series)
    .enter()
    .append("g")
    .style("fill", function(d, i) {
        return colors(i);
    });

// Add a rect for each data value
var rects = groups.selectAll("rect")
    .data(function(d) { return d; })
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
        return xScale(i);
    })
    .attr("y", function(d) {
        return yScale(d[0]);
    })
    .attr("height", function(d) {
        return yScale(d[1]) - yScale(d[0]);
    })
    .attr("width", xScale.bandwidth());
```

Note how for `y` and `height` we reference `d[0]` (the baseline value)
and `d[1]` (the topline value), respectively.

Also note how the resulting DOM structure involves three `g` groups,
each of which contains all of the `rect`s for each series. That
conveniently mirrors the structure of our `series` array, but it didn’t
happen automatically. At the top of the code, we begin by using the
selectAll/data/enter/append pattern to bind each row in `series` to a
new `g` group in the SVG (and set a `fill` for any elements in that
group). So, each `g` has part of `series` bound to it: `series[0]`,
`series[1]`, or `series[2]`.

Then, *within each group*, we select all the `rect`s (which don’t yet
exist) and bind a subset of that data with this line:

``` calibre39
    .data(function(d) { return d; })
```

We haven’t seen this syntax yet. Using an anonymous function within
`data()` lets us bind just a *portion* of the data. In this case, part
of `series` (such as `series[0]`) has already been bound to the parent
element `g`. So this anonymous function is taking the child elements of
that data (the individual values) and then binding those to the new
child elements (the `rect`s).

You will best understand this by spending a few minutes exploring each
of these DOM elements in the inspector and console, so you can see for
yourself what data is bound to each element.

<div class="section calibre2" data-type="sect2"
pdf-bookmark="A New Order">

<div id="ch13.xhtml_idm140093184475376" class="dedication">

## A New Order

Unless <span id="ch13.xhtml_idm140093184473968"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="stack layout"
secondary="specifying order"></span>otherwise specified, series will be
stacked in the order, well, specified in `keys()`. But you can use
`order()` to specify an alternate sequence to be applied before all the
stacked values are calculated.

In *04_stacked_bar_reordered.html*, I’ve added only one new line of
code:

``` calibre39
var stack = d3.stack()
              .keys([ "apples", "oranges", "grapes" ])
              .order(d3.stackOrderDescending);  // <-- New order!
```

You can see in <a href="#ch13.xhtml_stacked_bar_reordered"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-5</a> that the series now appear in a
different order.

<figure class="calibre35">
<div id="ch13.xhtml_stacked_bar_reordered" class="figure">
<img
src="images/f8702200f35549823772c9f004419e56a600e82af82b6d169be8cd93b5797165.png"
class="calibre212" alt="dvw2 1305" />
<h6 class="calibre37"><span class="keep-together">Figure 13-5.
</span>The same stacked bar chart, reordered</h6>
</div>
</figure>

Here are some other values you can feed to `order()` for bar charts. I
recommend you try each one, to see how they work.

`d3.stackOrderNone`  
Use the default order, as specified in `keys()`. This is the same as not
having specified `order()` at all. There really is no need to ever use
this, but hey, now you know.

`d3.stackOrderReverse`  
Use the opposite of whatever you specified in `keys()`.

`d3.stackOrderAscending`  
Sum all the values in each series, and put the series with the
*smallest* values at the bottom of the stack. Then stack the next
largest series on top, and so on.

`d3.stackOrderDescending`  
Sum all the values in each series, and put the series with the
*greatest* values at the bottom of the stack. Then stack the next
smallest series on top, and so on.

Note that when I write “the bottom of the stack,” I’m referring to the
stacked *data series*. The “bottom” of the stack is (usually) the one
with baseline values of zero. This data order is not necessarily the
same as the *visual* order in one’s final chart. Data “on the bottom”
doesn’t have to be visually “on the bottom,” and
*04_stacked_bar_reordered.html* is a case in point: the grapes series is
on the bottom of the data stack (with baseline values of zero), but the
green `rect`s depicting that data appears at the top of the chart.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Anchoring Those Bars">

<div id="ch13.xhtml_idm140093184454096" class="dedication">

## Anchoring Those Bars

Now <span id="ch13.xhtml_idm140093184452528"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="stack layout"
secondary="anchoring bars"></span>let’s anchor our stacked bars properly
to the bottom x-axis with just a few small modifications. I’ve carried
over `.order(d3.stackOrderDescending)` from the prior example (in
*05_stacked_bar_anchored.html*), so the series with the greatest sum
(grapes) is at the bottom of the stack, followed by the next smallest
series (oranges), and finally the smallest (apples).

Yet the *visual order* is reversed: the largest bars (grapes) sit at the
bottom, as in <a href="#ch13.xhtml_stacked_bar_anchored"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-6</a>.

<figure class="calibre35">
<div id="ch13.xhtml_stacked_bar_anchored" class="figure">
<img
src="images/68fcb13c270d59c644cc2c5d3002b83005981d78eb70b2310ad00a19acb2a007.png"
class="calibre213" alt="dvw2 1306" />
<h6 class="calibre37"><span class="keep-together">Figure 13-6.
</span>The same stacked bar chart, now anchored at the bottom</h6>
</div>
</figure>

I accomplished this by switching the `yScale`’s range from `[0, h]` to
`[h, 0]`, so low values start at the “bottom” of the chart and increase
“up,” instead of vice versa.

When creating the `rect`s, too, we have to change how we’re getting the
`y` and `height` values:

``` calibre39
.attr("y", function(d) {
    return yScale(d[1]);  // <-- Changed y value
})
.attr("height", function(d) {
    return yScale(d[0]) - yScale(d[1]);  // <-- Changed height value
})
```

Note that the stacked data `series` is identical in
*04_stacked_bar_reordered.html* and *05_stacked_bar_anchored.html*.
(Don’t believe me? Double-check for yourself in the console.) The
*visual representation*, however, has changed.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Stacked Areas">

<div id="ch13.xhtml_idm140093184317408" class="dedication">

## Stacked Areas

Stacking <span id="ch13.xhtml_idm140093184315680"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="stack layout"
secondary="stacking areas"></span>isn’t just for bars; we can stack
areas, too. This can be a valuable way to represent time series data,
when a sum total is derived from several related categories.

We learned how to make an area chart in
<a href="#ch11.xhtml_using_paths"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 11</a>. I’ve created a new example,
*06_stacked_area.html*, that uses both the stack layout and area
generators to make the chart shown in <a href="#ch13.xhtml_stacked_area"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-7</a>.

<figure class="calibre35">
<div id="ch13.xhtml_stacked_area" class="figure">
<img
src="images/4991021671214143e7a82ef74cb9f011962554f59aef6adfaad20bce72f8e6a4.png"
class="calibre214" alt="dvw2 1307" />
<h6 class="calibre37"><span class="keep-together">Figure 13-7. </span>A
stacked area chart</h6>
</div>
</figure>

This visualizes the data provided in *ev_sales_data.csv*, which reports
monthly unit sales of consumer electric vehicles in the US. Note that
I’ve included a tooltip, so you can mouse over an area to see which
model it represents, as in <a href="#ch13.xhtml_stacked_area_hover"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-8</a>.

<figure class="calibre35">
<div id="ch13.xhtml_stacked_area_hover" class="figure">
<img
src="images/1a6b3391b71e2e5fc62deaaf6548e903789e445b97f8dfaeb25f959711c16b0e.png"
class="calibre215" alt="dvw2 1308" />
<h6 class="calibre37"><span class="keep-together">Figure 13-8. </span>A
stacked area chart, with tooltips!</h6>
</div>
</figure>

With this stacked area representation, we can easily observe the overall
growth in sales. Note that the top edge of the top area represents the
sum of all values beneath that point. So in June 2013—the far-right edge
of the chart—we can see that about 4,500 electric vehicles were sold.

But we can also see which categories (vehicle models, in our case)
contribute those total, topline sums. For example, the bottom, blue area
represents sales of the Nissan Leaf. In the early days, the Leaf is
practically the only electric vehicle on the market. By 2013, several
other models are stacked “on top” of the Leaf. As sales of each vehicle
model fluctuate, the thickness (height) of each area expands and
contracts.

The greatest strength of a stacked area chart is its ability to display
both totals and relative contributions at the same time. But this is
also its greatest weakness. Perceptually, our human brains are good at
making comparisons against a fixed, stable baseline, as in a
(nonstacked) bar chart. When the baselines wiggle around, however, all
bets are off.

The Nissan Leaf is perceptually safe, for example: living at the bottom
of our “stack,” it has a consistent baseline. But the Tesla Model S is
sitting on top of the Leaf, so the Model S’s *baseline* is the Leaf’s
wiggly *topline*. Take a quick look at January 2013 on our chart. It
looks like overall electric vehicle sales took a dive that month—and
they did. But the vast majority of that decline was in Leaf sales, which
dipped from 1,489 in December 2012 to only 650 in January 2013. All of
the other vehicle areas, stacked on top of the Leaf, appear to also
decline sharply. In truth, Model S sales leapt from 900 in December 2012
to 1,350 in January 2013—a 50% *increase* in sales in one month
(assuming data correctness). Lesson learned: stacked area charts (and
stacked bar charts) have their uses, but our brains are not yet up to
the task of interpreting them honestly. (You could work around this
perceptual limitation with interactivity; enable a user to isolate a
specific vehicle, giving it a flat baseline. We’ll tackle this in
<a href="#ch16.xhtml_project_walkthrough"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 16</a>.)

Caveats aside, take a peek at *06_stacked_area.html* to see how to make
your own stacked area chart.

Most of what’s new in this example is specific to the dataset. For
example, there is code to grab all the column names dynamically (“Nissan
Leaf,” “Tesla Model S,” “Chevrolet Spark”) and to calculate the maximum
`yScale` domain based on the *sums* of each column of values (since they
will be “adding up” vertically).

The one, crucially important change here is in how we bind the data.
You’ll remember that in <a href="#ch11.xhtml_using_paths"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 11</a> we introduced `datum()` for binding our
data array to a single element, as though `dataset` were a single value:

``` calibre39
//Create areas
svg.append("path")
   .datum(dataset)
   .attr("class", "area")
   .attr("d", area);
```

That made sense, because a single area (`path` element) would represent
an entire array of values.

In our new example, we return to using selectAll/data/enter/append,
because we are creating not one `path`, but many `path`s, each one of
which represents an entire (stacked) array of values:

``` calibre39
//Create areas
svg.selectAll("path")
   .data(series)
   .enter()
   .append("path")
   .attr("class", "area")
   .attr("d", area)
	…
```

That takes the stacked dataset (called `series`) and creates a new
`path` element for each array in the `series`. Finally, the area
generator is called to operate on that data. Since `d3.stack()` took our
original data and generated baseline (`y0`) and topline (`y1`) values,
the areas wiggle right into place. Try logging `series` to the console
to inspect it and see all the time-saving stacking calculations D3 has
done for you.<span id="ch13.xhtml_idm140093184058912"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Lstack13"></span><span id="ch13.xhtml_idm140093184057936"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="BCstack13"></span>

</div>

</div>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Force Layout">

<div id="ch13.xhtml_idm140093184859712" class="dedication">

# Force Layout

Force-directed <span id="ch13.xhtml_Lforce13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="layouts"
secondary="force-directed layout"></span><span id="ch13.xhtml_idm140093184054800"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="uses for"></span>layouts are so called because they use
simulations of physical *forces* to arrange elements on the screen.
Arguably, they may be overused, yet they can be genuinely useful for
certain use cases, they demo well, and they just look *so darn cool*.
Everyone wants to learn how to make one, so let’s talk about it.

Force <span id="ch13.xhtml_idm140093184171696"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="graphs"
see="also charts"></span><span id="ch13.xhtml_Gforce13"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="graphs"
secondary="creating with force-directed layouts"></span><span id="ch13.xhtml_idm140093184169504"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="nodes"></span><span id="ch13.xhtml_idm140093184168832"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="edges"></span>layouts are typically used
with network data. In computer science, this kind of dataset is called a
*graph*. A simple graph is a list of *nodes* and *edges*. The nodes are
entities in the dataset, and the edges are the *connections* between
nodes. Some nodes will be connected by edges, and others won’t. Nodes
are commonly represented as circles, and edges as lines. But of course
the visual representation is up to you—D3 just helps manage all the
mechanics behind the scenes.

The physical metaphor here is of particles that repel each other, yet
are also connected by springs. The repelling forces push particles away
from each other, preventing visual overlap, and the springs prevent them
from just flying out into space, thereby keeping them on the screen
where we can see them.

<a href="#ch13.xhtml_force_layouta"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-9</a> provides a visual preview of what we’re
coding toward in *07_force.html*.

<figure class="calibre35">
<div id="ch13.xhtml_force_layouta" class="figure">
<img
src="images/6c6afce155471570904aa4cb7f1b72760fd90675bf37df9b366794302e694a6d.png"
class="calibre216" alt="dvw2 1309" />
<h6 class="calibre37"><span class="keep-together">Figure 13-9. </span>A
simple force layout</h6>
</div>
</figure>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Preparing the Network Data">

<div id="ch13.xhtml_idm140093184161744" class="dedication">

## Preparing the Network Data

D3’s <span id="ch13.xhtml_idm140093184160176"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="network data preparation"></span>force layout expects us to
provide nodes and edges separately, as arrays of objects. Here we have
one `dataset` object that contains two elements, `nodes` and `edges`,
each of which is itself an array of objects:

``` calibre39
var dataset = {
    nodes: [
        { name: "Adam" },
        { name: "Bob" },
        { name: "Carrie" },
        { name: "Donovan" },
        { name: "Edward" },
        { name: "Felicity" },
        { name: "George" },
        { name: "Hannah" },
        { name: "Iris" },
        { name: "Jerry" }
    ],
    edges: [
        { source: 0, target: 1 },
        { source: 0, target: 2 },
        { source: 0, target: 3 },
        { source: 0, target: 4 },
        { source: 1, target: 5 },
        { source: 2, target: 5 },
        { source: 2, target: 5 },
        { source: 3, target: 4 },
        { source: 5, target: 8 },
        { source: 5, target: 9 },
        { source: 6, target: 7 },
        { source: 7, target: 8 },
        { source: 8, target: 9 }
    ]
};
```

As usual for D3, you can store whatever data you like within these
objects. Our nodes are simple—just names of people. The edges contain
two values each: a source ID and a target ID. These IDs correspond to
the preceding nodes, so ID number 3 is Donovan, for example. If 3 is
connected to 4, then Donovan is connected to Edward.

The data shown is a bare minimum for using the force layout. You can add
more information, and, in fact, D3 will itself add a lot more data to
what we’ve provided, as we’ll see in a moment.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Defining the Force Simulation">

<div id="ch13.xhtml_idm140093183963456" class="dedication">

## Defining the Force Simulation

Here’s <span id="ch13.xhtml_idm140093183900384"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="initializing"></span><span id="ch13.xhtml_idm140093183899376"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.forceSimulation()"></span>how to
initialize a simple force layout:

``` calibre39
//Initialize a simple force layout, using the nodes and edges in dataset
var force = d3.forceSimulation(dataset.nodes)
              .force("charge", d3.forceManyBody())
              .force("link", d3.forceLink(dataset.edges))
              .force("center", d3.forceCenter().x(w/2).y(h/2));
```

Call `d3.forceSimulation()`, passing in a reference to the nodes. This
will generate a new simulator and automatically start running it, but
without any forces applied, it won’t be very interesting. To create
forces, call `force()` as many times as you like, each time specifying
an arbitrary name for each force (in case you want to reference it
later) and the name of a force function.

A force-directed layout usually involves several competing forces that,
after pushing and shoving the poor nodes and links around, eventually
reach some sort of equilibrium. The specific forces you apply (and how
you configure them) will determine how your network looks: Are nodes
spread out across space, or clustered together? The forces I’ve just
specified won’t be ideal for every dataset.
<span id="ch13.xhtml_idm140093183841696"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="list of forces and options"></span>You may want to reference
the
<a href="https://github.com/d3/d3-force/blob/master/README.md#forces"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">complete list of
forces and their options</a>, but I’ll briefly explain the three I used.

`d3.forceManyBody()`  
Creates a “many-body” force that acts on *all* nodes, meaning this can
be used to either attract all nodes to each other or repel all nodes
from each other. Try applying different `strength()` values, and see
what happens. Positive values attract; negative values repel. The
default `strength()` is –30, so we see a slight repelling force.

`d3.forceLink()`  
Our nodes are connected by edges (as opposed to being free-floating), so
we apply this force, specifying `dataset.edges`. Specify a target
`distance()` (the default is 30 pixels), and this force will struggle
against any competing forces to achieve that distance. Experiment by
plugging in different distance values—smaller numbers will result in
shorter edges, larger values in longer edges.

`d3.forceCenter()`  
This force centers the entire simulation around whatever point you
specify with `x()` and `y()`. In my example, I set x and y to the center
point of the SVG (`w/2` and `h/2`). Try setting those coordinates to
other values, and note how the entire composition is repositioned.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Creating the Visual Elements">

<div id="ch13.xhtml_idm140093183830400" class="dedication">

## Creating the Visual Elements

After <span id="ch13.xhtml_idm140093183828832"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="creating visual elements"></span>defining our force
simulation, we proceed to generate visual elements, using our old
friend: the selectAll/data/enter/append pattern (as first introduced in
<a href="#ch05.xhtml_data-chapter5"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 5</a>).

First we create a line for each edge:

``` calibre39
//Create edges as lines
var edges = svg.selectAll("line")
               .data(dataset.edges)
               .enter()
               .append("line")
               .style("stroke", "#ccc")
               .style("stroke-width", 1);
```

I set all the lines to have the same stroke color and weight, but of
course you could set this dynamically based on data (say, thicker or
darker lines for “stronger” connections, or some other value).

Then we create a circle for each node:

``` calibre39
//Create nodes as circles
var nodes = svg.selectAll("circle")
               .data(dataset.nodes)
               .enter()
               .append("circle")
               .attr("r", 10)
               .style("fill", function(d, i) {
                   return colors(i);
               });
```

I set all circles to have the same radius, but each gets a different
color fill, just because it’s prettier that way. Of course, these values
could be set dynamically, too, for a more meaningful visualization.

Since we created the circles last, they will be placed later in the SVG,
and therefore will appear “in front of” the lines. (As an experiment,
try switching the order, to see the lines appear in front.)

I also added a simple tooltip, so you can hover over each circle to see
which person it represents:

``` calibre39
//Add a simple tooltip
nodes.append("title")
    .text(function(d) {
        return d.name;
    });
```

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Updating Visuals over Time">

<div id="ch13.xhtml_idm140093183455664" class="dedication">

## Updating Visuals over Time

Finally, <span id="ch13.xhtml_idm140093183463040"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="updating visuals over time"></span><span id="ch13.xhtml_idm140093183462096"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="ticks (time measurement)"></span>we have
to specify what happens when the force layout “ticks.” Yes, these ticks
are different from the axis ticks addressed earlier, and definitely
different from those little blood-sucking insects. Physics simulations
use the word “tick” to refer to the passage of some amount of time, like
the ticking second hand of a clock. For example, if an animation were
running at 30 frames per second, you could have one tick represent
1/30th of a second. Then each time the simulation ticked, you’d see the
calculations of motion update in real time. In some applications, it’s
useful to run ticks faster than actual time. For example, if you were
trying to model the effects of climate change on the planet 50 years
from now, you wouldn’t want to wait 50 years to see the results, so
you’d program the system to tick on ahead, faster than real time.

For our purposes, what you need to know is that D3’s force simulation
“ticks” forward through time, just like every other physics simulation.
With each tick, the simulation adjusts the position values for each node
and edge according to the rules we specified when the layout was first
initialized. To see this progress visually, we need to update the
associated elements—the lines and circles—on every tick:

``` calibre39
//Every time the simulation "ticks", this will be called
force.on("tick", function() {

    edges.attr("x1", function(d) { return d.source.x; })
         .attr("y1", function(d) { return d.source.y; })
         .attr("x2", function(d) { return d.target.x; })
         .attr("y2", function(d) { return d.target.y; });

    nodes.attr("cx", function(d) { return d.x; })
         .attr("cy", function(d) { return d.y; });

});
```

This tells D3, “Okay, every time you tick, take the new x/y values for
each line and circle and update them in the DOM.”

Wait a minute. Where did these x/y values come from? We had only
specified `name`s, `source`s, and `target`s!

D3 calculated those x/y values and appended them to the existing objects
in our original `dataset` (see <a href="#ch13.xhtml_force_data_added"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-10</a>). Open *07_force.html* and type
**`dataset`** into the console. Expand any node or edge, and you’ll see
lots of additional data that we didn’t provide. That’s where D3 stores
the information it needs to continue running the physics simulation.
With `on("tick", …)`, we are just specifying how to take those updated
coordinates and map them on to the visual elements in the DOM.

<figure class="calibre35">
<div id="ch13.xhtml_force_data_added" class="figure">
<img
src="images/e8f581aaf79ae487985d34fc05a85a8577ba3dafbebcfc1080a29a58fc68e06d.png"
class="calibre217" alt="dvw2 1310" />
<h6 class="calibre37"><span class="keep-together">Figure 13-10.
</span>The first node in dataset, with lots of supplemental data added
by D3</h6>
</div>
</figure>

The final result, then, is the lovely entanglement displayed in
<a href="#ch13.xhtml_force_layout"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-11</a>.

<figure class="calibre35">
<div id="ch13.xhtml_force_layout" class="figure">
<img
src="images/6c6afce155471570904aa4cb7f1b72760fd90675bf37df9b366794302e694a6d.png"
class="calibre216" alt="dvw2 1311" />
<h6 class="calibre37"><span class="keep-together">Figure 13-11. </span>A
simple force layout with 10 nodes and 12 edges</h6>
</div>
</figure>

Again, you can run the final code youself in *07_force.html*.

Note that each time you reload the page, the circles and lines spring to
life, eventually resting in a state of equilibrium.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Draggable Nodes">

<div id="ch13.xhtml_idm140093183464016" class="dedication">

## Draggable Nodes

The <span id="ch13.xhtml_idm140093183349456"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="force-directed layouts"
secondary="draggable nodes"></span><span id="ch13.xhtml_idm140093183348448"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="nodes"></span>same force layout applied
to different datasets will produce wildly different results. It’s best
to tweak each force, as needed, to produce the most legible, explorable,
and meaningful composition for your dataset, but some simple
interactivity can help, too.

See *08_force_draggable.html*, which adds a `call()` statement to our
`nodes`:

``` calibre39
	…
	.call(d3.drag()  //Define what to do on drag events
        .on("start", dragStarted)
        .on("drag", dragging)
        .on("end", dragEnded));
```

This<span id="ch13.xhtml_idm140093183321280"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.drag()"></span> bit of code “calls”
the `d3.drag()` method on each node. `d3.drag()`, in turn, sets event
listeners for the three drag-related events (named as strings) and
specifies functions to trigger whenever one of those events occurs.

``` calibre39
//Define drag event functions
function dragStarted(d) {
    if (!d3.event.active) force.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragging(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragEnded(d) {
    if (!d3.event.active) force.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}
```

These three functions can be written however you like. But as written
here, they basically say, “Hey, as soon as the user starts dragging
something, make that thing follow the mouse position. Once the user lets
go, let the simulation resume positioning that thing in response to
forces.”

Try it out in *08_force_draggable.html*. Hmm, I want to get the orange
node by itself, so I’ll drag it down and to the left (see
<a href="#ch13.xhtml_force_drag"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-12</a>), and then I’ll move the yellowish one
into the same spot (see <a href="#ch13.xhtml_force_drag_2"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 13-13</a>).

<figure class="calibre35">
<div id="ch13.xhtml_force_drag" class="figure">
<img
src="images/a2a02970aff0787918cb24f04f4c377d57ca9c700dbb0333f1fd6269ac0d3ced.png"
class="calibre218" alt="dvw2 1312" />
<h6 class="calibre37"><span class="keep-together">Figure 13-12.
</span>Dragging a node to change the arrangement of nodes</h6>
</div>
</figure>

<figure class="calibre35">
<div id="ch13.xhtml_force_drag_2" class="figure">
<img
src="images/7da70141f09835219fac09fa1b84035094a00a9afd7deff0c2fa265b64c90d20.png"
class="calibre218" alt="dvw2 1313" />
<h6 class="calibre37"><span class="keep-together">Figure 13-13.
</span>Dragging some more</h6>
</div>
</figure>

As a bonus, interactivity + physics simulation = irresistable demo, even
when using meaningless dummy data! We humans just love seeing realistic
movement replicated on screens.<span id="ch13.xhtml_idm140093183082736"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Lforce13"></span><span id="ch13.xhtml_idm140093183081760"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="Gforce13"></span>

</div>

</div>

</div>

</div>

</div>

</div>

<span id="ch14.xhtml"></span>

<div id="ch14.xhtml_sbo-rt-content" class="calibre1">

<div id="ch14.xhtml_geomapping_chapter" class="dedication">

