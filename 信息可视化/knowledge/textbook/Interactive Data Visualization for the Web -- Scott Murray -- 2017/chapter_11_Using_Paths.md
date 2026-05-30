# <span class="keep-together">Chapter 11. </span>Using Paths

`path` elements<span id="ch11.xhtml_path11"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="paths"></span><span id="ch11.xhtml_idm140093188675712"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="SVG (Scalable Vector Graphics)"
secondary="drawing irregular forms"
see="paths"></span><span id="ch11.xhtml_idm140093188674528"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="drawing" secondary="irregular forms"
seealso="paths"></span><span id="ch11.xhtml_idm140093188673312"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="elements (SVG)"></span> are SVG’s answer
to drawing irregular forms. Anything that’s not a `rect`, `circle`, or
another simple shape can be drawn as a `path`. The catch is that the
syntax for defining `path` values is not particularly human-friendly.
For example, here is a line that we’ll generate from data in this
chapter. <span id="ch11.xhtml_idm140093188670704"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="paths"
secondary="path syntax"></span>Note the `path` syntax, as specified in
the element’s `d` attribute and shown in
<a href="#ch11.xhtml_path_and_d"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-1</a>.

<figure class="calibre35">
<div id="ch11.xhtml_path_and_d" class="figure">
<img
src="images/2292aab9e1b42e34fa8fe8646f22babedaf96b53fc8eec68fddca71c3c0d5483.png"
class="calibre46" alt="dvw2 1101" />
<h6 class="calibre37"><span class="keep-together">Figure 11-1. </span>A
path and its d attribute</h6>
</div>
</figure>

If you can read that, then you don’t need this book.

Fortunately, D3 has lots of built-in functions that generate `path`s for
you. You’ve already met the axis functions, which express scales as
`path`, `line`, and `text` elements. In later chapters, you’ll learn
about `d3.arc()` and `d3.geoPath()`, both of which also generate `path`s
for different purposes. In this chapter, we’ll cover two other common
uses of `path`s: drawing line and area charts.

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Line Charts">

<div id="ch11.xhtml_idm140093188875840" class="dedication">

# Line Charts

Let’s <span id="ch11.xhtml_idm140093188874272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="line charts"
secondary="data preparation"></span><span id="ch11.xhtml_Cline11"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="line charts"></span><span id="ch11.xhtml_Pline11"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="paths"
secondary="drawing line charts with"></span>start with a simple line
chart. Actually generating the line is quite simple, but we need some
data in place first. For this chapter, I’m going to use a real-world
dataset.

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Data Preparation">

<div id="ch11.xhtml_idm140093188870368" class="dedication">

## Data Preparation

Line charts are great for time series, so I’ve decided to chart carbon
dioxide measurements over time. I’ve downloaded the
<a href="https://www.esrl.noaa.gov/gmd/ccgg/trends/data.html"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">“Mauna Loa
CO<sub>2</sub> monthly mean data”</a>, as provided by the National
Oceanic & Atmospheric Administration’s Earth System Research Laboratory.
(See the *README.md* in this chapter’s examples for details and a full
citation.)

This data includes monthly average values of CO<sub>2</sub> in parts per
million, as measured at the Mauna Loa Observatory in Hawaii. An excerpt
of the raw-text file looks like this:

``` calibre39
# CO2 expressed as a mole fraction in dry air, micromol/mol, abbreviated as ppm
#
#  (-99.99 missing data;  -1 no data for #daily means in month)
#
#            decimal     average   interpolated    trend    #days
#             date                             (season corr)
1958   3    1958.208      315.71      315.71      314.62     -1
1958   4    1958.292      317.45      317.45      315.29     -1
1958   5    1958.375      317.50      317.50      314.71     -1
1958   6    1958.458      -99.99      317.10      314.85     -1
1958   7    1958.542      315.86      315.86      314.98     -1
1958   8    1958.625      314.93      314.93      315.94     -1
1958   9    1958.708      313.20      313.20      315.91     -1
1958  10    1958.792      -99.99      312.66      315.61     -1
1958  11    1958.875      313.33      313.33      315.31     -1
1958  12    1958.958      314.67      314.67      315.61     -1
1959   1    1959.042      315.62      315.62      315.70     -1
1959   2    1959.125      316.38      316.38      315.88     -1
1959   3    1959.208      316.71      316.71      315.62     -1
1959   4    1959.292      317.72      317.72      315.56     -1
1959   5    1959.375      318.29      318.29      315.50     -1
1959   6    1959.458      318.15      318.15      315.92     -1
1959   7    1959.542      316.54      316.54      315.66     -1
1959   8    1959.625      314.80      314.80      315.81     -1
1959   9    1959.708      313.84      313.84      316.55     -1
1959  10    1959.792      313.26      313.26      316.19     -1
1959  11    1959.875      314.80      314.80      316.78     -1
1959  12    1959.958      315.58      315.58      316.52     -1
1960   1    1960.042      316.43      316.43      316.51     -1
```

Note that the first column indicates a year, while the second indicates
a month (1–12). This version of the file contains values from March 1958
through January 2017. The fourth column, “average,” is the
CO<sub>2</sub> value we’re interested in.

You probably noticed that these values aren’t comma-separated; rather,
they are provided in fixed-width columns in an otherwise unformatted
text file. D3 needs a little more structure than this, so my first step
is to wrangle this into CSV form, using the free, amazing tool
<a href="http://openrefine.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">OpenRefine</a>.

I won’t detail the steps involved here, as there are other books and
<a href="http://bit.ly/2uD7zEm"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">tutorials</a> on
using OpenRefine. In short, I cut out everything but the three relevant
columns, and my resulting file, *mauna_loa_co2_monthly_averages.csv*,
looks like this:

``` calibre39
year,month,average
1958,3,315.71
1958,4,317.45
1958,5,317.5
1958,6,-99.99
1958,7,315.86
1958,8,314.93
1958,9,313.2
1958,10,-99.99
1958,11,313.33
1958,12,314.67
1959,1,315.62
1959,2,316.38
1959,3,316.71
1959,4,317.72
1959,5,318.29
1959,6,318.15
1959,7,316.54
1959,8,314.8
1959,9,313.84
1959,10,313.26
1959,11,314.8
1959,12,315.58
1960,1,316.43
…
```

Much better! Next, I’ll define a row conversion function, as described
in <a href="#ch05.xhtml_data-chapter5"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 5</a>.

``` calibre39
var rowConverter = function(d) {
    return {
        //Make a new Date object for each year + month
        date: new Date(+d.year, (+d.month - 1)),
        //Convert from string to float
        average: parseFloat(d.average)
    };
}
```

This will convert the three columns of data in our CSV into just two:
`date` and `average`. The `date` consists of a `new Date()`, a new
JavaScript `Date` object, into which we are passing the year and the
month. The `+` operator, in this context, forces the `d.year` and
`d.month` values to be typed as numbers instead of strings. And because
JavaScript’s month counting begins at zero (as in, 0 = January, 1 =
February, and 2 = March) but the data’s month counting begins at one (1
= January), I’ve subtracted one from each month value. (See
<a href="https://mzl.la/2uD1E1W"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">MDN’s docs on
the <code class="calibre23">Date</code> object</a> for more.)

The `average` value is parsed from a string to a float.

We call the row conversion function when we load in the CSV data:

``` calibre39
//Load in data
d3.csv("mauna_loa_co2_monthly_averages.csv", rowConverter, function(data) {

    var dataset = data;

    //Print data to console as table, for verification
    console.table(dataset, ["date", "average"]);

    //…
```

Feast <span id="ch11.xhtml_idm140093188551424"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="console.table()"></span>your eyes on
`console.table()`, a <span id="ch11.xhtml_idm140093188434048"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="console.log"></span>fancy improvement on
`console.log()` that prints everything in nice, pretty columns that are
easier on your brain. Here I’ve (optionally) specified the names of the
two columns of interest: `date` and `average`. You can verify for
yourself in <a href="#ch11.xhtml_using_consoletable"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-2</a> that the values match that from our
original dataset.

<figure class="calibre35">
<div id="ch11.xhtml_using_consoletable" class="figure">
<img
src="images/7a21503e939b5d3b30f19df61675e8bcd64002f1510772e7169bd1e504ce9b8c.png"
class="calibre173" alt="dvw2 1102" />
<h6 class="calibre37"><span class="keep-together">Figure 11-2.
</span>Using console.table() to verify data</h6>
</div>
</figure>

Isn’t it beautiful?

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Scale Setup">

<div id="ch11.xhtml_idm140093188869776" class="dedication">

## Scale Setup

The <span id="ch11.xhtml_idm140093188427344"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="line charts"
secondary="scale setup"></span>process of setting up our scales should
be familiar by now. First, `xScale` will handle time, and `yScale`
handles the CO<sub>2</sub> values. I’ve set a zero baseline (low domain
value of 0) to start.

``` calibre39
    xScale = d3.scaleTime()
               .domain([
                    d3.min(dataset, function(d) { return d.date; }),
                    d3.max(dataset, function(d) { return d.date; })
                ])
               .range([0, w]);

    yScale = d3.scaleLinear()
               .domain([0, d3.max(dataset, function(d) { return d.average; })])
               .range([h, 0]);
```

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Line ’em Up">

<div id="ch11.xhtml_idm140093188423200" class="dedication">

## Line ’em Up

With our data and scales in place, finally we get to draw a line! (It’s
the small things in life…)

Start <span id="ch11.xhtml_idm140093188344320"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="d3.line()"></span><span id="ch11.xhtml_idm140093188343616"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="line charts"
secondary="line generator function"></span><span id="ch11.xhtml_idm140093188342640"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="line generator function"></span><span id="ch11.xhtml_idm140093188341968"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="functions"
secondary="line generator functions"></span>by defining a line generator
function, much as we defined axis generator functions to make axes. To
do this, we call `d3.line()`, making sure to specify x and y accessors.

``` calibre39
    //Define line generator
    var line = d3.line()
                 .x(function(d) { return xScale(d.date); })
                 .y(function(d) { return yScale(d.average); });
```

The x and y accessors tell the line generator how to decide *where* to
place each point on the line. Note that for x, we specify the scaled
value of `d.date`, and y gets the scaled value of `d.average`. Later,
when the line generator is called, it will look for the bound data and
loop through each value, using the accessor logic here to calculate
where to position each point. Drawing the line itself is really just a
matter of connecting those carefully positioned dots.

For this barebones example, I then create the SVG element and finally
append a new `path` element.

``` calibre39
    //Create SVG element
    var svg = d3.select("body")
                .append("svg")
                .attr("width", w)
                .attr("height", h);

    //Create line
    svg.append("path")
       .datum(dataset)
       .attr("class", "line")
       .attr("d", line);
```

Huh? What happened to your old friend, the selectAll/data/enter/append
pattern?

Until now, our examples involved one graphical mark corresponding to one
data value (or one “row” of related values), as in our bar charts and
scatterplots. A line chart, however, calls for a *single* graphical mark
that represents *many* data values. We can skip the
selectAll/data/enter/append pattern, because we already know how many
new marks we need: just one.

Instead <span id="ch11.xhtml_idm140093188232720"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="data()"></span><span id="ch11.xhtml_idm140093188232016"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="datum()"></span>of using `data()` to bind
each value in our `dataset` array to a different element, we use
`datum()`, the method for binding a *single* data value to a single
element. The entire `dataset` array is bound to the new `path` we just
created.

Following that, we assign a class of `line` (to enable easy CSS
selection and styling) and then—finally—set a `d` attribute, passing in
our line generator function as an argument. Since the data has already
been bound to the `path`, the line generator simply grabs that data,
plots the points as we specified, and draws a line connecting them. This
produces the output we saw in <a href="#ch11.xhtml_path_and_d"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-1</a>, at the start of this chapter. The
final code is in *01_line_chart.html*.

To verify how the entire `dataset` was bound to one element, try
selecting that line in the console using `d3.select(".line")`. Note the
complete, 707-value-long array that appears under `__data__` in
<a href="#ch11.xhtml_verifying_data_array_bound_path"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-3</a>.

<figure class="calibre35">
<div id="ch11.xhtml_verifying_data_array_bound_path" class="figure">
<img
src="images/5242f49686e6754ac07dc35e6132f553282cac3491ebe31fe1d6a3dca9b16ac4.png"
class="calibre46" alt="dvw2 1103" />
<h6 class="calibre37"><span class="keep-together">Figure 11-3.
</span>Verifying the data array bound to a single path element</h6>
</div>
</figure>

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Dealing with Missing Data">

<div id="ch11.xhtml_idm140093188422608" class="dedication">

## Dealing with Missing Data

In *02_line_chart_axes.html*, I’ve
<span id="ch11.xhtml_idm140093188218768"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="line charts"
secondary="dealing with missing data"></span><span id="ch11.xhtml_idm140093188217744"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="missing data"></span><span id="ch11.xhtml_idm140093188217072"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data"
secondary="dealing with missing data"></span>added some padding on the
left and bottom edges plus axes, as shown in
<a href="#ch11.xhtml_adding_padding_axes"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-4</a>.

<figure class="calibre35">
<div id="ch11.xhtml_adding_padding_axes" class="figure">
<img
src="images/8dbcfbe60b32fc6235fccb09491f0eb9c7978990f1a5dcaabdc55c9c0e20ff3a.png"
class="calibre174" alt="dvw2 1104" />
<h6 class="calibre37"><span class="keep-together">Figure 11-4.
</span>Added padding and axes</h6>
</div>
</figure>

Now, with the axes labeled, it’s time for a sanity check: could
CO<sub>2</sub> levels *really* have dropped below zero, as those
downward spikes seem to indicate? (Are negative CO<sub>2</sub> ppm
values even *possible?* Answer: no.)

This spiky anomaly is explained by a note in the original datafile:

``` calibre39
#  (-99.99 missing data;  -1 no data for #daily means in month)
```

Ah, so carbon-measuring machines (and even scientists themselves) are
not infallible! A –99.99 value is not a true measurement, but stands in
for “no data available for that month.”

We <span id="ch11.xhtml_idm140093188157792"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="defined()"></span>could manually remove
those –99.99 values from our dataset. Or we could leave the data
untouched, and use the line generator’s `defined()` method to determine,
on the fly, whether or not each individual value is defined (or valid).
`defined()` is just another configuration method, like `x()` and `y()`.
If the result of its anonymous function is true, then that data value is
included. If not, the value is excluded.

This simple use of `defined()` checks merely to see if any value exists
at all:

``` calibre39
.defined(function(d) { return d; })
```

So, if `d` exists, this will be interpreted as true.

But in our case, the –99.99 values do *exist*; it’s just that we humans
know they aren’t valid measurements. To exclude them, we could use a
comparison operator, which will return a logical result (true or false):

``` calibre39
//Define line generator
var line = d3.line()
             .defined(function(d) { return d.average >= 0; })
             .x(function(d) { return xScale(d.date); })
             .y(function(d) { return yScale(d.average); });
```

For every row in the dataset, if `d.average` is greater than or equal to
zero, this will return true, and the value will be included. All
negative values, including –99.99, will be thrown out.

See *03_line_chart_missing.html* for that final code, which renders the
chart shown in <a href="#ch11.xhtml_line_chart_invalid_excluded"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-5</a>.

<figure class="calibre35">
<div id="ch11.xhtml_line_chart_invalid_excluded" class="figure">
<img
src="images/a8fec0651bd68280301c623bfd03d3b661ed5cdcb7fb45f159bec4f767e5550b.png"
class="calibre175" alt="dvw2 1105" />
<h6 class="calibre37"><span class="keep-together">Figure 11-5.
</span>Line chart, invalid CO<sub>2</sub> values excluded</h6>
</div>
</figure>

Note the *veeeeery tiny* gaps, where there used to be (graphically
dishonest) spikes.

Actually, this would be a nice time to show off SVG’s fundamentally
scalable nature. Use your browser’s zoom functionality to zoom in to
this chart as much as possible. Note that the entire chart—consisting of
vector SVG elements—remains as sharp and clear as ever.
<a href="#ch11.xhtml_line_chart_invalid_excluded_big"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-6</a> shows our chart at 500% zoom, where the
gaps are clearly visible.

<figure class="calibre35">
<div id="ch11.xhtml_line_chart_invalid_excluded_big" class="figure">
<img
src="images/0c91f295035305425bdc3a47c339e1df0109f9952fe354737a74064aebec7d40.png"
class="calibre176" alt="dvw2 1106" />
<h6 class="calibre37"><span class="keep-together">Figure 11-6.
</span>Zoomed in to reveal the gaps</h6>
</div>
</figure>

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Refining the Visuals">

<div id="ch11.xhtml_idm140093188220288" class="dedication">

## Refining the Visuals

In *04_line_chart_adjusted.html*, I’ve
<span id="ch11.xhtml_idm140093188112272"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="line charts"
secondary="refining visual presentation"></span>adjusted the `yScale`
domain to emphasize the upward trajectory, so there is no longer a zero
baseline. I’ve also manually added a red line corresponding to 350 ppm,
considered the maximum “safe” level of atmospheric CO<sub>2</sub> by
many scientists, and used the `stroke-dasharray` property to make it a
dashed line. See <a href="#ch11.xhtml_line_chart_adjusted"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-7</a>.

<figure class="calibre35">
<div id="ch11.xhtml_line_chart_adjusted" class="figure">
<img
src="images/740aa1268f32a684b830e73b3d6ca6f3d7a1e8fea28df76e37b4a1e7906d8c05.png"
class="calibre177" alt="dvw2 1107" />
<h6 class="calibre37"><span class="keep-together">Figure 11-7.
</span>Adjusted yScale and new red line</h6>
</div>
</figure>

At <span id="ch11.xhtml_idm140093188106592"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="rhetoric—design decisions"></span><span id="ch11.xhtml_idm140093188105792"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data visualization"
secondary="rhetoric-design decisions"></span>this point, we are dealing
in visual rhetoric—design decisions that express a point of view by
influencing how others interpret our chart. (For great examples of
climate change–related visual rhetoric, see Duarte Design’s graphics and
animations, as used by Al Gore in the Academy Award–winning
<a href="https://en.wikipedia.org/wiki/An_Inconvenient_Truth"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em>An
Inconvenient Truth</em></a>.)

Having acknowledged that, let’s say I want to emphasize the portions of
the line that are above the 350 ppm line. I could approach that by
simply creating a second data-driven line. I could use `defined()` to
include only data points of 350 or greater for the new red line, and to
*exclude* such points for the original teal line:

``` calibre39
//Define line generators
line = d3.line()
            .defined(function(d) { return d.average >= 0 && d.average <= 350; })
            .x(function(d) { return xScale(d.date); })
            .y(function(d) { return yScale(d.average); });

dangerLine = d3.line()
            .defined(function(d) { return d.average >= 350; })
            .x(function(d) { return xScale(d.date); })
            .y(function(d) { return yScale(d.average); });
```

That, plus some styling changes for each line and a new text label,
produces what you see in *05_line_chart_labeled.html* and
<a href="#ch11.xhtml_line_chart_labeled"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-8</a>.

<figure class="calibre35">
<div id="ch11.xhtml_line_chart_labeled" class="figure">
<img
src="images/99420b66d947854c22a6787681cf723ef7b7161ac59c197099c6b10d45c83506.png"
class="calibre177" alt="dvw2 1108" />
<h6 class="calibre37"><span class="keep-together">Figure 11-8.
</span>Labeled line chart with two lines, teal and red</h6>
</div>
</figure>

This is just one of many possible visual solutions. A close look reveals
small gaps in the line near the 350 ppm mark. An alternative approach
would be to render two full lines in their entirety, but mask them using
SVG clipping paths, as described in
<a href="#ch09.xhtml_contain_viselements"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">“Containing visual elements with clipping paths”</a> in
<a href="#ch09.xhtml_updates-chapter9"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 9</a>.<span id="ch11.xhtml_idm140093187870848"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Cline11"></span><span id="ch11.xhtml_idm140093187869872"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="Pline11"></span>

</div>

</div>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Area Charts">

<div id="ch11.xhtml_idm140093187868800" class="dedication">

# Area Charts

Areas <span id="ch11.xhtml_idm140093187867104"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="area charts"></span><span id="ch11.xhtml_idm140093187866368"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="area charts"></span>are not too different from lines. If a
line is a series of connected x/y points, then an area is just that same
line, plus a second such line (usually a flat baseline), with all the
space in between filled in.

<a href="#ch11.xhtml_area_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-9</a> illustrates this and shows what we’re
working toward.

<figure class="calibre35">
<div id="ch11.xhtml_area_chart" class="figure">
<img
src="images/01d1da095ee989397eb733a3fecbc1310ec567c521ec42685f73d864dcb8d155.png"
class="calibre178" alt="dvw2 1109" />
<h6 class="calibre37"><span class="keep-together">Figure 11-9.
</span>Area chart</h6>
</div>
</figure>

The <span id="ch11.xhtml_idm140093187861600"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.area()"></span>main difference is
calling `d3.area()` to define an *area generator* instead of a line
generator:

``` calibre39
area = d3.area()
         .defined(function(d) { return d.average >= 0; })
         .x(function(d) { return xScale(d.date); })
         .y0(function() { return yScale.range()[0]; })
         .y1(function(d) { return yScale(d.average); });
```

You’ll notice I’ve specified `x`, `y0`, and `y1` accessors. The `x`
accessor is unchanged from earlier. `y0` represents the area’s
*baseline*, while `y1` represents the top, or data value. You’ll notice
that `y1` is the same as our earlier `y` accessor. But `y0` is new. For
every data value, this accessor returns the first value in `yScale`’s
range: that is, the “bottom” edge of the chart.

I don’t know about you, but to me this sure *feels* like a whole lot
more carbon dioxide. (Suddenly, I hope you are reading this as an ebook
powered by renewable energy. If you’re reading the dead-tree version,
don’t feel bad; use what you’re learning here for good.)

One potential downside of an area chart is that, if there are missing
data points, those absences will be keenly felt, as in
<a href="#ch11.xhtml_area_chart"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-9</a>. Those slices punctuating the data
don’t sit right with me, but they are graphically honest. You *could* go
fudge the data to patch those holes, but then how would you sleep at
night?

I’ll define the second area (the red one) like so:

``` calibre39
dangerArea = d3.area()
            .defined(function(d) { return d.average >= 350; })
            .x(function(d) { return xScale(d.date); })
            .y0(function() { return yScale(350); })
            .y1(function(d) { return yScale(d.average); });
```

Note that, in this case, I specify a baseline value of
`yScale(350)`—that is, the 350 ppm mark—because this area doesn’t need
to extend all the way down to the bottom of the chart. Nice!

Later in the code, we make sure to call the new area generators instead
of the old line generators:

``` calibre39
//Create areas
svg.append("path")
    .datum(dataset)
    .attr("class", "area")
    .attr("d", area);  // <-- Area!

svg.append("path")
    .datum(dataset)
    .attr("class", "area danger")
    .attr("d", dangerArea);  // <-- Area!
```

I also made some minor adjustments to variable names and CSS properties.
But mainly you only need to change `line` to `area` and specify `y0` and
`y1` accessors.

See that chart in *06_area_chart.html* and
<a href="#ch11.xhtml_area_chart_red"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 11-10</a>.

<figure class="calibre35">
<div id="ch11.xhtml_area_chart_red" class="figure">
<img
src="images/4636dd0ee040d363aeb97cdc3e753ca328f834a042d7721e61d4d9998766b0a8.png"
class="calibre179" alt="dvw2 1110" />
<h6 class="calibre37"><span class="keep-together">Figure 11-10.
</span>Area chart, with both areas</h6>
</div>
</figure>

As a <span id="ch11.xhtml_idm140093187438944"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="clipping paths"></span><span id="ch11.xhtml_idm140093187438208"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transitions"
secondary="clipping paths"></span>designer, I must point out that, yes,
you can see the tiniest bit of the teal area bleeding around the edges
of the red area. Most people won’t notice this, but if you do, I’m sorry
for you, but glad to meet someone else with the same affliction. In any
case, you could remove that cleanly by using SVG clipping paths (again,
see <a href="#ch09.xhtml_updates-chapter9"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 9</a>).<span id="ch11.xhtml_idm140093187435984"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="path11"></span>

</div>

</div>

</div>

</div>

<span id="ch12.xhtml"></span>

<div id="ch12.xhtml_sbo-rt-content" class="calibre1">

<div id="ch12.xhtml_selections" class="dedication">

