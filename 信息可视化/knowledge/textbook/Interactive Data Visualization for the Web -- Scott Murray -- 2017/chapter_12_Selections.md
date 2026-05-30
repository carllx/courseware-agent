# <span class="keep-together">Chapter 12. </span>Selections

Your <span id="ch12.xhtml_idm140093187432816"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="D3 methods for making"></span>first taste of a D3 selection
was simple, and involved only one element: `d3.select("body")`. Then you
learned about `selectAll()` for selecting multiple elements. When we
introduced binding data to elements, you learned about the now-familiar
selectAll/data/enter/append pattern for creating new elements. Later,
you saw how to use `merge()` to combine selections (such as when
applying updates to a chart) and `exit()` to select elements on their
way out. In <a href="#ch11.xhtml_using_paths"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 11</a>, you saw examples of how `datum()` could
be used to bind data to a single element, bypassing the usual data join
process.

For many visualizations, that’s all you’ll need to know. But as you
begin to dream up more complex and interactive pieces, a deeper
understanding of selections and how you can manipulate them will make
your life a lot easier.

Let’s explore some of the possibilities.

<div class="section calibre2" data-type="sect1"
pdf-bookmark="A Closer Look at Selections">

<div id="ch12.xhtml_idm140093187427472" class="dedication">

# A Closer Look at Selections

What<span id="ch12.xhtml_Sover12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="overview of"></span> is a selection, really? I am here to
demystify this concept for you. (Does that make me a demystic?)

Let’s look closely at a very simple selection. Note the result of
`d3.select("body")` in <a href="#ch12.xhtml_simple_selection"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-1</a>.

<figure class="calibre35">
<div id="ch12.xhtml_simple_selection" class="figure">
<img
src="images/7dce6737eb79a96a26ef3bd71eaa7ecc4d8a2c3c7fda762c3094609b691eeb41.png"
class="calibre180" alt="dvw2 1201" />
<h6 class="calibre37"><span class="keep-together">Figure 12-1. </span>A
simple selection</h6>
</div>
</figure>

So, a selection contains two arrays, `_groups` and `_parents`. We can
disregard `_parents` and also the `__proto__` object, which is an
essential feature of JavaScript’s prototype-based structure and also way
beyond the scope of this book.

Let’s expand `_groups`, as in <a href="#ch12.xhtml_selection_groups"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-2</a>.

<figure class="calibre35">
<div id="ch12.xhtml_selection_groups" class="figure">
<img
src="images/2cd09a2e36d40ad97fad862a89c89ba4987564709289e950c928e9d2f3af2c85.png"
class="calibre181" alt="dvw2 1202" />
<h6 class="calibre37"><span class="keep-together">Figure 12-2.
</span>Revealing _groups</h6>
</div>
</figure>

Ah, `_groups` contains yet another array, which itself contains a list
of elements—only one in this case: `body`. Let’s expand that further, as
in <a href="#ch12.xhtml_selection_body_expanded"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-3</a>.

<figure class="calibre35">
<div id="ch12.xhtml_selection_body_expanded" class="figure">
<img
src="images/e699c74f95288e0b75f48bceb63471c36afc1b5d6daa1df2fe39cad7736c65b1.png"
class="calibre182" alt="dvw2 1203" />
<h6 class="calibre37"><span class="keep-together">Figure 12-3.
</span>body, expanded</h6>
</div>
</figure>

In there we see lots of properties associated with `body`, most of which
we’ll never need to know about.

Okay, that’s all well and good, but I’ll ask it again: what *is* a
selection, really?

Let’s try this:

``` calibre39
typeof d3.select("body")  //Returns "object"
```

Ah, selections are *objects!* We already know about objects! It turns
out there’s nothing mysterious or mystical here at all. Selections are
just very special objects generated and interpreted by D3. You will
never manipulate a selection yourself—don’t bother trying to reach into
`_groups`—as that’s what all of D3’s selection methods are for. Still,
it’s instructive to use the console to look more closely. At some point,
while debugging a project, you’ll need to peek into your selections to
figure out what’s going on, so you may as well get comfortable doing so
now.

Let’s revisit a line chart from <a href="#ch11.xhtml_using_paths"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 11</a> and try a slightly different selection,
`d3.select("path")`, as shown in <a href="#ch12.xhtml_selection_path"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-4</a>.

<figure class="calibre35">
<div id="ch12.xhtml_selection_path" class="figure">
<img
src="images/7ee14274e6ca36b6870379c8c35d98128ba8199578482741d10f65fa17a33dc0.png"
class="calibre183" alt="dvw2 1204" />
<h6 class="calibre37"><span class="keep-together">Figure 12-4.
</span>Selecting a path</h6>
</div>
</figure>

This returns a selection of our single `path`, to which the bound data
is stored in the `__data__` property, an array of 707 values, in this
case. Remember, you can expand `__data__` to verify your bound data
appears as expected, as in <a href="#ch12.xhtml_selection_data"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-5</a>.

<figure class="calibre35">
<div id="ch12.xhtml_selection_data" class="figure">
<img
src="images/5ed2be778cd7bb3c245d1210fda587cb8298235973093f070145a138b01c0bc9.png"
class="calibre184" alt="dvw2 1205" />
<h6 class="calibre37"><span class="keep-together">Figure 12-5.
</span>Revealing the bound data</h6>
</div>
</figure>

What do selections look like when they contain more than one element?
Let’s revisit a scatterplot from <a href="#ch08.xhtml_axes-chapter8"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 8</a> and try `d3.selectAll("circle")`, as
shown in <a href="#ch12.xhtml_selection_circles"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-6</a>.
<span id="ch12.xhtml_idm140093187505760"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.select()"></span>Remember, `select()`
returns only the *first* matching item it finds, while `selectAll()`
returns *all* matching items.

<figure class="calibre35">
<div id="ch12.xhtml_selection_circles" class="figure">
<img
src="images/94bc8db61c7477f44162cbd40c31e1c518756a297ac1c464e2398ffb384975bf.png"
class="calibre185" alt="dvw2 1206" />
<h6 class="calibre37"><span class="keep-together">Figure 12-6.
</span>Selecting all the circles</h6>
</div>
</figure>

As expected, the selection array now includes all 50 circles. Mousing
over an element in the selection highlights the corresponding DOM
element up above, as shown in <a href="#ch12.xhtml_selection_hover"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-7</a>.

<figure class="calibre35">
<div id="ch12.xhtml_selection_hover" class="figure">
<img
src="images/8fc648eb9a3553090154e506518079598b89ac1bf9e6533cc973fd8acd91abc6.png"
class="calibre150" alt="dvw2 1207" />
<h6 class="calibre37"><span class="keep-together">Figure 12-7.
</span>Mousing over an element to identify it</h6>
</div>
</figure>

This is also extremely useful for debugging, as you can manually verify
whether or not the values stored in any given element’s `__data__`
property are expressed visually as you
intended.<span id="ch12.xhtml_idm140093187396912"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="Sover12"></span>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Getting More Specific">

<div id="ch12.xhtml_idm140093187426528" class="dedication">

# Getting More Specific

Typically, <span id="ch12.xhtml_Schain12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="chained syntax for"></span>you use selections in D3’s chained
syntax, not as one-off commands in the console. You can leverage this
chain syntax to get very specific and select exactly the elements you
want.

`d3.select()` and `d3.selectAll()` operate at the page level, so we have
to start with one of those.

``` calibre39
var body = d3.select("body");
var svg = d3.select("svg");
var paths = d3.selectAll("path");
var groups = d3.selectAll("g");
```

`select()` and `selectAll()` can be chained together, in which case they
operate on the preceding selection, instead of the whole page. For
example:

``` calibre39
var allGroups = d3.selectAll("g");

var allCircles = d3.selectAll("circle");

var allCirclesInGroups = d3.selectAll("g")
                           .selectAll("circle");
```

Now `allCirclesInGroups` would store a selection to all `circle`
elements on the page that are contained within (“descendant elements
of”) `g` elements.

You could simplify that as:

``` calibre39
var allCirclesInGroups = d3.selectAll("g circle");
```

While it’s possible to string together adjacent `select()` and
`selectAll()` statements like this, doing so isn’t common. What’s more
common (and more useful) is to modify related elements in succession,
starting with those highest on the DOM tree and getting more specific at
each step. For example:

``` calibre39
d3.select("svg")             //Select the first SVG on the page
    .attr("width", 500)      //Set its width
    .attr("height", 300)     //Set its height
    .selectAll("circle")     //Select all circles *within* that SVG
    .attr("cx", 250)         //Set each circle’s cx attribute
    .attr("cy", 150)         //Set each circle’s cy attribute
    .selectAll("title")      //Select all title elements *within* circles
    .text("Circles rock!");  //Set the text of those titles
```

Note <span id="ch12.xhtml_idm140093187296016"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="active selection"></span>that the *active
selection* changes at three different points along this chain.

``` calibre39
d3.select("svg")             //Select the first SVG on the page
    .attr("width", 500)
    .attr("height", 300)
    .selectAll("circle")     //Select all circles *within* that SVG
    .attr("cx", 250)
    .attr("cy", 150)
    .selectAll("title")      //Select all title elements *within* circles
    .text("Circles rock!");
```

The `select()` and `selectAll()`
<span id="ch12.xhtml_idm140093187026464"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.select()"></span>statements create
*new* selections, and hand those new selections off to the subsequent
methods.

Also note, however, that many methods leave the active selection intact.
They modify associated DOM elements (such as by setting or changing
attribute values), but then merely relay the same selection they
received to the following method.

``` calibre39
d3.select("svg")
    .attr("width", 500)      //Receives SVG as selection, hands off SVG
    .attr("height", 300)     //Receives SVG as selection, hands off SVG
    .selectAll("circle")
    .attr("cx", 250)         //Receives circles as selection, hands off circles
    .attr("cy", 150)         //Receives circles as selection, hands off circles
    .selectAll("title")
    .text("Circles rock!");  //Receives titles as selection, chain ends
```

Thus, when chaining methods together, you must be very careful to pay
attention to which methods generate *new selections*, or you could
inadvertently modify the wrong DOM elements.

To <span id="ch12.xhtml_idm140093186945488"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="coding tips"
secondary="D3 chained syntax"></span><span id="ch12.xhtml_idm140093186944800"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="space-based indentation"></span><span id="ch12.xhtml_idm140093186944128"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="indentation convention"></span>minimize
this confusion, Mike Bostock recommends using an indentation convention
of four spaces when the selection is unchanged, but only two when a new
selection is returned. Here is an example from Mike, taken from the
<a href="https://github.com/d3/d3-selection/blob/master/README.md"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-selection
documentation</a>:

``` calibre39
d3.select("body")
  .append("svg")
    .attr("width", 960)
    .attr("height", 500)
  .append("g")
    .attr("transform", "translate(20,20)")
  .append("rect")
    .attr("width", 920)
    .attr("height", 460);
```

Let me annotate that, to explain:

``` calibre39
d3.select("body")                           // New selection
  .append("svg")                            // New selection
    .attr("width", 960)                     // Acts on svg
    .attr("height", 500)                    // Acts on svg
  .append("g")                              // New selection
    .attr("transform", "translate(20,20)")  // Acts on g
  .append("rect")                           // New selection
    .attr("width", 920)                     // Acts on rect
    .attr("height", 460);                   // Acts on rect
```

`select()` <span id="ch12.xhtml_idm140093186867760"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="append()"></span>and `append()` are
methods that return new selections. `attr()` does not, but merely relays
whatever selection it just acted on. Note that this example only works
because of these elements’ parent/child relationships: `body` is the
parent of `svg`, which is the parent of `g`, which is the parent of
`rect`.

Mike uses this indentation convention consistently—you will see it in
all of his thousands of examples—and many others in the D3 community
have followed suit. So now you know what it means.

I made a conscious decision to *not* use Mike’s space-based indentation
in this book, primarily because, based on my observations teaching D3,
it can cause unnecessary confusion to the uninitiated. (“Why are the
code blocks wiggling in and out?”) It wouldn’t have made sense to
explain the convention until now, 12 chapters in. Also, I’m a tabs
guy.<span id="ch12.xhtml_idm140093187150432"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="Schain12"></span>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Storing Selections">

<div id="ch12.xhtml_idm140093187395024" class="dedication">

# Storing Selections

One <span id="ch12.xhtml_idm140093187148208"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="storing"></span>more important point from the
<a href="https://github.com/d3/d3-selection/blob/master/README.md"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-selection
documentation</a>: “Selections are immutable. All selection methods that
affect which elements are selected (or their order) return a new
selection rather than modifying the current selection.”

That is, once you make a selection, you can’t modify it. You can only
make a new one, which could be a subset of the original, and overwrite
it (if you like). For example:

``` calibre39
//Store new selection in z
var z = d3.select("svg");

//Returns a new selection, based on elements in z,
//but doesn’t modify the value of z
z.selectAll("rect");

//Returns the same new selection as above, but then
//overwrites z with the newly returned selection
z = z.selectAll("rect");
```

Also remember that, when you’re storing results in a variable, the
selection returned by the *last* link in the chain is what will be
captured. For example, if I were to store the results of my earlier
example:

``` calibre39
var titles = d3.select("svg")
               .attr("width", 500)
               .attr("height", 300)
               .selectAll("circle")
               .attr("cx", 250)
               .attr("cy", 150)
               .selectAll("title")
               .text("Circles rock!");
```

…`titles` would contain a selection of all `title` elements inside
`circle` elements inside the SVG, which is not particularly useful. It’s
more likely I’d want to save a reference to the circles, so I could act
on them (and their enclosed `title`s) later, in which case I could
write:

``` calibre39
var circles = d3.select("svg")
                .attr("width", 500)
                .attr("height", 300)
                .selectAll("circle")
                .attr("cx", 250)
                .attr("cy", 150);

circles.selectAll("title")
       .text("Circles rock!");
```

That is exactly equivalent to:

``` calibre39
var circles = d3.select("svg")
                .attr("width", 500)
                .attr("height", 300)
                .selectAll("circle");

circles.attr("cx", 250)
       .attr("cy", 150);
       .selectAll("title")
       .text("Circles rock!");
```

Selections are very flexible; I recommend you make and store them in
whatever sequence makes the most sense to you, for your project, coding
style, and way of working.

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Enter, Merge, and Exit">

<div id="ch12.xhtml_idm140093187149312" class="dedication">

# Enter, Merge, and Exit

The <span id="ch12.xhtml_DJenter12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data joins"
secondary="enter, merge, and exit selections"></span>data join is D3’s
essential feature. We discussed it in
<a href="#ch09.xhtml_updates-chapter9"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 9</a>, but now we can more closely explore the
role selections play in this process.

We finished up <a href="#ch09.xhtml_updates-chapter9"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 9</a> with this dynamic bar chart and functions
to add and remove values, as shown in <a href="#ch12.xhtml_bars_merge"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-8</a>.

<figure class="calibre35">
<div id="ch12.xhtml_bars_merge" class="figure">
<img
src="images/3e2ba59816e5afb828854357872faee4bd93f38d0be55e1bbfd5c51ce7715689.png"
class="calibre186" alt="dvw2 1208" />
<h6 class="calibre37"><span class="keep-together">Figure 12-8.
</span>Bar chart with options to add and remove values</h6>
</div>
</figure>

In *01_enter_merge_exit.html*, I have
<span id="ch12.xhtml_idm140093186749184"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="console.log"></span>added several
`console.log()` statements so we can see what’s going on with each
selection change. I recommend uncommenting each statement, one at a
time, and exploring them in the console. In case you don’t have your
computer handy, I’ll walk you through the most important parts here.

<div class="calibre27 note" data-type="note">

###### Note

You’ll never modify D3 selections directly, so don’t let the following
complexity freak you out. Still, a peek under the hood will deepen your
own understanding of D3’s inner workings. Just use D3’s built-in
selection methods, and everything will be fine.

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="The Enter Selection">

<div id="ch12.xhtml_idm140093186746096" class="dedication">

## The Enter Selection

You’ll <span id="ch12.xhtml_Senter12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="enter selection"></span><span id="ch12.xhtml_entsel12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="enter selections"></span>remember that we
created the bars using the standard selectAll/data/enter/append pattern:

``` calibre39
//Create bars
svg.selectAll("rect")
   .data(dataset, key)
   .enter()
   .append("rect")
   …
```

Let’s look at that first selection, `svg.selectAll("rect")`:

<figure class="calibre35">
<div class="figure">
<img
src="images/544c0e7290b5a78fdabda56c9c8d213951d3e693730e5a3a1dd2bb4863cf882f.png"
class="calibre187" alt="dvw2 12in01" />
<h6 class="calibre37"></h6>
</div>
</figure>

This looks like a normal, empty selection. (Remember, no `rect`s exist
yet!) `_groups` contains a `NodeList` array with a length of zero.

Now let’s uncomment `svg.selectAll("rect").data(dataset, key)`:

<figure class="calibre35">
<div class="figure">
<img
src="images/3e0e4c83c4a60fbb5b1e3138b3650434b72e198d01fc48a6312df0dde37b826b.png"
class="calibre188" alt="dvw2 12in02" />
<h6 class="calibre37"></h6>
</div>
</figure>

Interesting! The selection returned from a data join includes both the
`_enter` and `_exit` subselections. So this is where those things live!

Let’s expand each of those, plus `_groups`:

<figure class="calibre35">
<div class="figure">
<img
src="images/6f0075c992533b921c3696fd8ddb006689968a82ef1780585a1c103acb972439.png"
class="calibre189" alt="dvw2 12in03" />
<h6 class="calibre37"></h6>
</div>
</figure>

`_exit` contains an empty array, as expected, but look: `_enter`
contains an array with 20 positions. (Confusingly, `_groups`, despite
being empty, has a set `length` of 20. Please suspend your disbelief for
just a moment.) Let’s expand that further:

<figure class="calibre35">
<div class="figure">
<img
src="images/739699f2edbf3c749afd1b8a746950c292f9cb6293a0b6babe2d4f8a323aa46c.png"
class="calibre190" alt="dvw2 12in04" />
<h6 class="calibre37"></h6>
</div>
</figure>

Aha! Each one is an `EnterNode`. These are the magical placeholder
elements to which data is bound, to be replaced shortly by actual DOM
elements.

Let’s expand the first `EnterNode`:

<figure class="calibre35">
<div class="figure">
<img
src="images/8bb6541cf9ea65f52dff584ef5a0aa5f488460b274170ec2d93955fc5d571fb7.png"
class="calibre190" alt="dvw2 12in05" />
<h6 class="calibre37"></h6>
</div>
</figure>

Fantastic: there is our `__data__`, bound to the placeholder element, as
expected.

Let’s now log the results of using `enter()` to grab just the enter
selection, as with `svg.selectAll("rect").data(dataset, key).enter()`:

<figure class="calibre35">
<div class="figure">
<img
src="images/dd4919bd8daa55b2c6c9e0e89f4bdfb4de5c7450b40f9798cbca6041badb4b8d.png"
class="calibre191" alt="dvw2 12in06" />
<h6 class="calibre37"></h6>
</div>
</figure>

Okay, this looks like a normal selection again. Let’s expand `_groups`:

<figure class="calibre35">
<div class="figure">
<img
src="images/8d61d95f5cff9ef1c591cda29546c361743f8acb4dd33b529757937b89dfc4d2.png"
class="calibre190" alt="dvw2 12in07" />
<h6 class="calibre37"></h6>
</div>
</figure>

There are those `EnterNode`s again! This is not super exciting, but it’s
nice to validate that, as promised, `enter()` merely grabs the enter
subselection from a data join and hands that off.

In the final step of the selectAll/data/enter/append pattern, we use
`append()` to add new rectangles, as in:

``` calibre39
svg.selectAll("rect").data(dataset, key).enter().append("rect")
```

<figure class="calibre35">
<div class="figure">
<img
src="images/f9f77691494a1df32db6aacb6ec45de8443c83621d0bfe8caff16efe97ccc0f9.png"
class="calibre192" alt="dvw2 12in08" />
<h6 class="calibre37"></h6>
</div>
</figure>

This, too, looks like a normal selection. Let’s expand `_groups`:

<figure class="calibre35">
<div class="figure">
<img
src="images/eb0480e6c94fec213ebc1415e3f64826b61ce44d639fff5b986ca63f6a6e953b.png"
class="calibre190" alt="dvw2 12in09" />
<h6 class="calibre37"></h6>
</div>
</figure>

Fun! The 20 elements formerly known as `EnterNode`s are now fully
realized `rect`s. D3 has appended a new `rect` for each placeholder, and
here is returning the resulting selection, *after* the append. We can
even verify that the joined data values have transferred over:

<figure class="calibre35">
<div class="figure">
<img
src="images/8ce168f2781eade149836b897e7ba6b4cad03394163689f966551a65044e98ec.png"
class="calibre193" alt="dvw2 12in10" />
<h6 class="calibre37"></h6>
</div>
</figure>

You can see the `__data__` attached to the first `rect`.
Success\!<span id="ch12.xhtml_idm140093186439360"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Senter12"></span><span id="ch12.xhtml_idm140093186438352"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="entsel12"></span>

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Merging Selections">

<div id="ch12.xhtml_idm140093186745152" class="dedication">

## Merging Selections

The <span id="ch12.xhtml_Smerg12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="merging"></span><span id="ch12.xhtml_mergsel12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="merging selections"></span>limited
interaction for this chart enabled us to add and remove values.
Everything described hereafter happens post-click.

After clicking, we log out `svg.selectAll("rect")` and, as expected, see
a selection containing a `NodeList` array of 20 items:

<figure class="calibre35">
<div class="figure">
<img
src="images/789dd8219818c823ace8ef6aa8a36a107c0cf1d905eb1ee7a79aa11b962a605d.png"
class="calibre194" alt="dvw2 12in11" />
<h6 class="calibre37"></h6>
</div>
</figure>

We bind the new dataset, and, as before, `data()` returns a selection
that includes the enter and exit subselections. Here’s
`svg.selectAll("rect").data(dataset, key)`:

<figure class="calibre35">
<div class="figure">
<img
src="images/fc9db5fa583fbda34606337359fea449e8355acd23e324a4aacae4da055eedb5.png"
class="calibre195" alt="dvw2 12in12" />
<h6 class="calibre37"></h6>
</div>
</figure>

Let’s expand the `_enter` and `_exit` subselections.

<figure class="calibre35">
<div class="figure">
<img
src="images/b4db2874f76e3cf77514a78e6b95e4774d7c898782166a81103bf4dddd844be8.png"
class="calibre185" alt="dvw2 12in13" />
<h6 class="calibre37"></h6>
</div>
</figure>

When *adding* a value (such as by clicking “Add a new data value” in our
example), the `length` of the `_enter` selection is increased by one.
Note that the array’s `length` is now set to 21, even though the array
itself contains only a single `EnterNode`. D3 is tracking both the total
number of elements needed (21) as well as the number of placeholders for
*new* elements (only 1).

<aside data-type="sidebar" epub:type="sidebar" class="calibre31">

<div id="ch12.xhtml_idm140093186421216" class="sidebar">

##### More Than You Ever Wanted to Know About JavaScript Array Lengths

You <span id="ch12.xhtml_idm140093186419488"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="array.length"></span><span id="ch12.xhtml_idm140093186418752"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="JavaScript"
secondary="array.length"></span>may find it confusing to see an array
with a `length` of 21, despite containing only a single element. (If you
don’t find it confusing, I’m worried about you.)

In many languages, `array.length` reports the true length of an array:
the number of values or elements stored within it. But in JavaScript,
arrays are objects, and `length` is just another property that can be
modified.

``` calibre39
var test = [1, 2, 3]
typeof test        //Returns "object"
test.length        //Returns 3
test.length = 100  //Sets length to 100
test.length        //Returns 100
```

Confusing, isn’t it? Or at least not intuitive.

Here’s another way we could change an array’s length: by adding a new
value to a numerically named property.

<figure class="calibre35">
<div class="figure">
<img
src="images/ec1e69b53306b60c7dbd38ddbb2228d49af0383f96e56858957a06d25795e18b.png"
class="pcalibre7 calibre196" alt="dvw2 12in14" />
<h6 class="calibre37"></h6>
</div>
</figure>

When we set the value of `test[100]` to `"surprise!"`, it doesn’t matter
that values `test[3]` through `test[99]` don’t yet exist. Once we set
`test[100]`, the value of `test.length` has been auto-incremented to
101.

Since arrays are just objects, the index positions are actually just
object property names. Above, we see property names of `0`, `1`, `2`,
`100`, and `length`.

Adding a nonnumerically named property to an array does *not* affect the
`length`:

<figure class="calibre35">
<div class="figure">
<img
src="images/aee8c9a516703678de89600cd2fe72a78e9d7b560ffa8d98a778ec303ce94501.png"
class="calibre197 pcalibre7" alt="dvw2 12in15" />
<h6 class="calibre37"></h6>
</div>
</figure>

Weirdly, we now have an array whose `length` is 101, despite storing
only five elements (object properties), one of which is nonnumeric. (If
you count `length` itself, that makes six elements.) I’m telling you:
JavaScript is a total free-for-all.

Think I’m making this up? Try it out in the console yourself. Then see
MDN’s documentation on <a href="https://mzl.la/2tNK8Up"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">Array.length</code></a> and the
<a href="https://mzl.la/2tNOKtj"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">“Relationship
between <code class="calibre23">length</code> and numerical
properties”</a> for all the gory details.

</div>

</aside>

At this point, our `_exit` selection contains an array with a `length`
of 20, despite being empty. This sort of makes sense, because we have
only 20 bars so far, and none of them are exiting, so the exit selection
is empty.

`_groups` contains an array with a `length` of 21, although it actually
contains only 20 elements—references to the existing `rect`s. Scrolling
down, you can see the final `rect` has a position value of 19 (the
“20th” `rect`):

<figure class="calibre35">
<div class="figure">
<img
src="images/781327eacba981364b0ac27d53955828313dc41f734eebffafbd18e3fef4ac4d.png"
class="calibre198" alt="dvw2 12in16" />
<h6 class="calibre37"></h6>
</div>
</figure>

As mere mortals, we don’t have to fully understand, let alone agree
with, the apparent discrepancies between `length` values and actual
array contents. I’m only pointing this out to show you that D3 is,
indeed, tracking what’s going on. As long as you use D3’s built-in
methods to manipulate selections and don’t try to alter anything
manually, the math will work out.

Now, let’s illustrate how these selections would be different if we had
instead *removed* a data value. Note a numerical shift in the opposite
direction; the `_enter` selection now contains an array of 19 (not 21)
items.

<figure class="calibre35">
<div class="figure">
<img
src="images/326ea5e5b0aab169924e2a9b08a6b70d31247b0af793777a6475872dbddb0e3d.png"
class="calibre199" alt="dvw2 12in17" />
<h6 class="calibre37"></h6>
</div>
</figure>

Back to *adding* data values. In the next step, we grab `bars.enter()`:

<figure class="calibre35">
<div class="figure">
<img
src="images/658a5e4739f276ebda9cfa207c76b3951dac50feca89002f2601d4321603d891.png"
class="calibre200" alt="dvw2 12in18" />
<h6 class="calibre37"></h6>
</div>
</figure>

That’s just the enter subselection from earlier. Again, note the array
with a `length` of 21, but actual contents of a single `EnterNode` in
position 20.

We then append a rectangle for the one placeholder element, using
`bars.enter().append("rect")`:

<figure class="calibre35">
<div class="figure">
<img
src="images/f093f9bcd3db592add0cca739e94f7e5bb0dde001adf0fb403114338afcc0070.png"
class="calibre201" alt="dvw2 12in19" />
<h6 class="calibre37"></h6>
</div>
</figure>

Boom! The `EnterNode` has blossomed into a beautiful `rect`.

Having created a new rectangle, we now need to create a selection that
includes *all* the rectangles (the new one plus the existing ones), so
we can update all of their visual attributes—x, y, width, height—at the
same time. We accomplish that by taking the preceding selection and
merging in `bars`, a selection containing references to the preexisting
`rect`s. By convention, this is called the “update” selection, and we
create it using `bars.enter().append("rect").merge(bars)`:

<figure class="calibre35">
<div class="figure">
<img
src="images/2cb1114b8f07f955069e559b311bbc93a8d6fd21bf7b658e0ae3b2f5691f4db6.png"
class="calibre202" alt="dvw2 12in20" />
<h6 class="calibre37"></h6>
</div>
</figure>

There you have it: an array containing all 21 `rect`s. (And yes, if you
scroll down, there are actually 21 `rect`s *and* the `length` of the
array is set to 21. Isn’t is nice when things work
out?)<span id="ch12.xhtml_idm140093186257088"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="Smerg12"></span><span id="ch12.xhtml_idm140093186256112"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="mergsel12"></span>

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="The Exit Selection">

<div id="ch12.xhtml_idm140093186436496" class="dedication">

## The Exit Selection

Upon <span id="ch12.xhtml_idm140093186254112"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="exit selection"></span><span id="ch12.xhtml_idm140093186253104"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="exit selection"></span>clicking “Remove a
data value,” after all the data binding, entering, and updating is done,
we look at the exit selection, `bars.exit()`:

<figure class="calibre35">
<div class="figure">
<img
src="images/819e1524dc51d97b174c217d860b93b7d6b0bd37951236be0595e93a746f272e.png"
class="calibre200" alt="dvw2 12in21" />
<h6 class="calibre37"></h6>
</div>
</figure>

We see an array containing a single `rect`. Don’t be misled by the
`length` of 20; there’s only one outgoing rectangle because we only
removed a single data value. (Sorry to see you go, little guy.)

Finally, it’s time to say goodbye, so we call `bars.exit().remove()`:

<figure class="calibre35">
<div class="figure">
<img
src="images/0401e4158f063f25647ed2f282dc6f88e53e517cf0b975d9512a26d55c9e9ca9.png"
class="calibre200" alt="dvw2 12in22" />
<h6 class="calibre37"></h6>
</div>
</figure>

That single `rect` has been deleted from the DOM, never to be seen
again. Yet, interestingly, D3 still returns a selection to the deleted
element. If you wanted to, you could store this selection somewhere, in
case you needed to access its bound data values or perform some other
operation, like put it in a box in your attic.

If any of this is confusing (and how could it *not* be?), open
*01_enter_merge_exit.html*, uncomment those log statements one at a
time, and step through them at your own
pace.<span id="ch12.xhtml_idm140093186243728"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="DJenter12"></span>

</div>

</div>

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Filtering Selections Based on Data">

<div id="ch12.xhtml_idm140093186242656" class="dedication">

# Filtering Selections Based on Data

It’s <span id="ch12.xhtml_Sfilter12"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="selections"
secondary="filtering based on data"></span>often very useful to filter
selections based on data values.

You might remember the example of conditionally formatted paragraphs
from <a href="#ch05.xhtml_data-chapter5"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 5</a>, as shown in
<a href="#ch12.xhtml_conditional_paras"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-9</a>.

<figure class="calibre35">
<div id="ch12.xhtml_conditional_paras" class="figure">
<img
src="images/3a0b03bbd75a830a6a10bdfe5ef0be5511fe0ff48e9cc36073c6628e161beacd.png"
class="calibre85" alt="dvw2 1209" />
<h6 class="calibre37"><span class="keep-together">Figure 12-9.
</span>Conditionally formatted paragraphs</h6>
</div>
</figure>

The code driving this is as follows:

``` calibre39
var dataset = [ 5, 10, 15, 20, 25 ];

d3.select("body").selectAll("p")
    .data(dataset)
    .enter()
    .append("p")
    .text(function(d) {
        return "I can count up to " + d;
    })
    .style("color", function(d) {
        if (d > 15) {	//Threshold of 15
            return "red";
        } else {
            return "black";
        }
    });
```

Note<span id="ch12.xhtml_idm140093186232336"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.style()"></span> how the conditional
logic resides in the `style()` method. If the value of `d` exceeds 15,
then the color is set to red; otherwise, it’s set to black. This is not
a bad approach, but if you wanted to apply any other modifications to
the red paragraphs, you’d have to repeat the same logic within each
`attr()` or `style()` method.

We could rewrite this using <a href="http://bit.ly/2t1G7N6"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">filter()</code></a> to filter the initial selection of
all paragraphs. This is equivalent to the preceding approach:

``` calibre39
d3.select("body").selectAll("p")
    .data(dataset)
    .enter()
    .append("p")
    .text(function(d) {
        return "I can count up to " + d;
    })
    .filter(function(d) {  //Filter current selection of all paragraphs
        return d > 15;  //Returns true only if d > 15
    })  //New selection of filtered elements is handed off here
    .style("color", "red");  //Applies only to elements in the filtered selection
```

`filter()` takes a selection and an anonymous function. If the function
returns `true` for a given element, then that element is included in the
new selection returned by `filter()`. You can see how I’ve maintained
the same `d > 15` logic from the earlier `style()` statement, although
here it’s tucked next to the `return` keyword.

We could rewrite that again to store each of these selections
separately:

``` calibre39
var allParas = d3.select("body").selectAll("p")
    .data(dataset)
    .enter()
    .append("p")
    .text(function(d) {
        return "I can count up to " + d;
    });

var redParas = allParas.filter(function(d) {
        return d > 15;
    })
    .style("color", "red");
```

See that code in *02_paragraphs.html*. Type `allParas` and `redParas`
into the console, and you’ll see that `allParas` includes references to
all five paragraphs, while `redParas` includes only the last two.

Also note that when we create `redParas`, we start with `allParas`, and
then apply the filter to that selection. There’s no need to be redundant
and reselect all the paragraphs with `d3.selectAll("p")`.

For a more visual example, see *03_slider.html*, in which we can drag a
slider up and down to specify the threshold value used for the filter,
as in <a href="#ch12.xhtml_slide_to_filter"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-10</a>.

<figure class="calibre35">
<div id="ch12.xhtml_slide_to_filter" class="figure">
<img
src="images/96b0c4bf91e2e2726174809018b9b6b3938d394bd88f026d66d7252bf3192289.png"
class="calibre203" alt="dvw2 1210" />
<h6 class="calibre37"><span class="keep-together">Figure 12-10.
</span>Dragging a slider to filter by value</h6>
</div>
</figure>

Yes, that’s our old bar chart with a slider on the side. Here’s the most
relevant snippet of code:

``` calibre39
//On change, update styling
d3.select("input")
    .on("change", function() {

        var threshold = +d3.select(this).node().value;

        svg.selectAll("rect")
            .attr("fill", function(d) {
                return "rgb(0, 0, " + (d.value * 10) + ")";
            })
            .filter(function(d) {
                return d.value <= threshold;
            })
            .attr("fill", "red");

    });
```

Whenever you drag and release the slider, the `change` event is fired.
We then grab the current value of the slider, select all `rect`s, set
their fill as before, filter that selection based on the threshold
value, and make any qualifying rectangles red.

I’ve employed the same principle in *04_radios.html*, using radio
buttons and a scatterplot, as shown in
<a href="#ch12.xhtml_radio_filter_threshold"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-11</a>.

<figure class="calibre35">
<div id="ch12.xhtml_radio_filter_threshold" class="figure">
<img
src="images/6e4998bd9b9c269c074b7a17e4e7445aba9cf4529186f4fb525fe76fa9f6f02a.png"
class="calibre204" alt="dvw2 1211" />
<h6 class="calibre37"><span class="keep-together">Figure 12-11.
</span>Using radio buttons to set the filter threshold value</h6>
</div>
</figure>

But what if we used these radio buttons to apply slightly more complex
conditions than simply highlighting values below a simple threshold?

See *05_combinations.html*, as shown in
<a href="#ch12.xhtml_radio_filter_combos"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-12</a>.

<figure class="calibre35">
<div id="ch12.xhtml_radio_filter_combos" class="figure">
<img
src="images/6f47dff37dc9f8b4c359a5f2ef5828d3be7bcbe60c4b9d04baa9e2c9bdb40347.png"
class="calibre205" alt="dvw2 1212" />
<h6 class="calibre37"><span class="keep-together">Figure 12-12.
</span>Using radio buttons to set different conditions on filters</h6>
</div>
</figure>

In this example, we can choose None (the default), Center, Edges, or
Quadrants. Each case introduces a little more complexity in its
filtering logic, but the core principle—start with all circles, then
filter to narrow the selection—is the same.

<div class="section calibre2" data-type="sect2"
pdf-bookmark="To each() Their Own">

<div id="ch12.xhtml_idm140093185726752" class="dedication">

## To each() Their Own

The most <span id="ch12.xhtml_idm140093185724960"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="each()"></span>common purpose of creating
a selection is ultimately to modify it in some way, such as by using
`attr()` or `style()`. But it can be useful to define your own
functions, especially for custom calculations or modifications that will
be repeated.

Fortunately, we can use <a
href="https://github.com/d3/d3-selection/blob/master/README.md#selection_each"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><code
class="calibre23">each()</code></a> to run an arbitrary function once
for each element in a selection. `each()` takes whatever selection it’s
given and calls the specified function once for each item in the
selection.

You can pass in an anonymous function, as in:

``` calibre39
selection.each(function(d, i) {
    //The 'this' context is now set to
    //the element on which you’re acting.
    //
    //Do something with 'this', d, and/or i here.
});
```

Or pass the name of a function you’ve already defined, as in:

``` calibre39
selection.each(zoomAndEnhance);
```

If you include `d` and `i` within your function definition, D3 will hand
off those values, as you’d expect.

See an example of this in *06_each.html*. I’ve created a simple button,
which you can see in <a href="#ch12.xhtml_before_each"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-13</a>.

<figure class="calibre35">
<div id="ch12.xhtml_before_each" class="figure">
<img
src="images/d6aed4d121b0f02c050d683c641c329185af8638f4024fd1425a94ec40528256.png"
class="calibre206" alt="dvw2 1213" />
<h6 class="calibre37"><span class="keep-together">Figure 12-13.
</span>Scatterplot, prior to calling each() on each circle</h6>
</div>
</figure>

This code listens for a button click:

``` calibre39
//On button click, execute a function for each circle in the allCircles selection
d3.selectAll("input")
    .on("click", function() {
        allCircles.each(freakOut);  //Hold on to your hats!
    });
```

When the button is clicked, all the circles just, like, totally freak
out! In a more technical sense, the `allCircles` selection is passed
into `each()`, which calls the `freakOut()` function on each element in
the selection (i.e., each individual circle on the chart).

As I’ve said, `each()` is used to run an arbitrary function on a
selection. Well, you can’t get any more arbitrary than `freakOut()`:

``` calibre39
//Define the freakOut function
var freakOut = function(d, i) {

    //Since this function will be called by 'each()',
    //it will be aware of each element on which it operates.
    //The 'this' context will be updated, and d and i will
    //be populated with the associated values.

    var colors = d3.schemeCategory20;
    var colorIndex = Math.round(Math.random() * 20);

    d3.select(this)
        .transition()
        .delay(i * 25)
        .duration(2000)
        .ease(d3.easeElasticOut)
        .attr("fill", colors[colorIndex])
        .attr("r", 25);

};
```

Can you picture in your mind’s eye what this code will do?

Before we get to the big reveal, there are a few serious points to note:

- Since the `d` and `i` arguments are specified in the function
  definition, D3 will populate them for you.

- The value of `this` will also be set by D3 to reflect “the element
  upon which we’re currently acting.” So `d3.select(this)` will create a
  selection with whatever that element is.

- In `delay()` or any other function within `freakOut()`, we can
  reference the values `d` and `i` directly—no need to write
  `function(d, i)…`, although it has become part of our muscle memory at
  this point.

Ready <span id="ch12.xhtml_idm140093185501856"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="Sfilter12"></span>to see that
in action? I really recommend running *06_each.html* yourself—it’s much
more fun—but you can get the gist of it in
<a href="#ch12.xhtml_after_each"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 12-14</a>.

<figure class="calibre35">
<div id="ch12.xhtml_after_each" class="figure">
<img
src="images/51f58ee28c3854effb71be76acc8b75823191f3436f3906341e925a014ccf8ec.png"
class="calibre207" alt="dvw2 1214" />
<h6 class="calibre37"><span class="keep-together">Figure 12-14.
</span>each() circle, freaking out, over time</h6>
</div>
</figure>

</div>

</div>

</div>

</div>

</div>

</div>

<span id="ch13.xhtml"></span>

<div id="ch13.xhtml_sbo-rt-content" class="calibre1">

<div id="ch13.xhtml_chapter11-layouts" class="dedication">

