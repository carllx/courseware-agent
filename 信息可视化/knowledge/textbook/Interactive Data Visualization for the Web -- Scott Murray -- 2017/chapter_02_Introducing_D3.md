# <span class="keep-together">Chapter 2. </span>Introducing D3

D3—also <span id="ch02.xhtml_idm140093207962464"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="d3.js"
see="D3"></span><span id="ch02.xhtml_idm140093207961456"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="maps"
see="also geomapping"></span>referred to as d3.js—is a JavaScript
library for creating data visualizations. But that kind of undersells
it.

The <span id="ch02.xhtml_idm140093207959648"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="meaning of name"></span><span id="ch02.xhtml_idm140093207958640"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Data-Driven Documents"
see="D3"></span>abbreviation D3 references the tool’s full name,
*Data-Driven Documents*. The *data* is provided by you, and the
*documents* are web-based documents, meaning anything that can be
rendered by a web browser, such as HTML and SVG. D3 does the *driving*,
in the sense that it connects the data to the documents.

Of course, the name also functions as a clever allusion to the network
of technologies underlying the tool itself: the W3, or World Wide Web,
or, today, simply “the web.”

D3’s <span id="ch02.xhtml_idm140093207954800"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Bostock, Michael"></span><span id="ch02.xhtml_idm140093207954064"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="downloading"></span>primary author is the brilliant
<a href="http://bost.ocks.org/mike/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Mike Bostock</a>,
although there are several other dedicated contributors. The project is
entirely open source and freely available on
<a href="https://github.com/d3"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">GitHub</a>.

D3 is released under a
<a href="http://opensource.org/licenses/BSD-3-Clause"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">BSD license</a>,
so you may use, modify, and adapt the code for noncommercial or
commercial use at no cost.

D3’s official home on the Web is <a href="http://www.d3js.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"><em>d3js.org</em></a>.

<div class="section calibre2" data-type="sect1"
pdf-bookmark="What It Does">

<div id="ch02.xhtml_idm140093207948544" class="dedication">

# What It Does

Fundamentally, <span id="ch02.xhtml_idm140093207946976"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="underlying processes"></span>D3 is an elegant piece of
software that facilitates generation and manipulation of web documents
with data. It does this by:

- *Loading* data into the browser’s memory

- *Binding* data to elements within the document, creating new elements
  as needed

<div class="dedication">

</div>

- *Transforming* those elements by interpreting each element’s bound
  datum and setting its visual properties accordingly

- *Transitioning* elements between states in response to user input

Learning to use D3 is simply a process of learning its syntax, so you
can tell it how to load and bind data, and transform and transition
elements.

The *transformation* <span id="ch02.xhtml_idm140093207938240"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="transformations"></span>step is most
important, as this is where the *mapping* happens.
<span id="ch02.xhtml_idm140093207936992"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data mapping"
secondary="design application in"></span>D3 provides a structure for
applying these transformations, but, as we’ll see, you define the
mapping rules. Should larger values make taller bars or brighter
circles? Will clusters be sorted on the x-axis by age or category? What
color palette is used to fill in countries on your world map? All of the
visual design decisions are up to you. You provide the concept, you
craft the rules, and D3 executes it—without telling you what to do.

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="What It Doesn’t Do">

<div id="ch02.xhtml_idm140093207935264" class="dedication">

# What It Doesn’t Do

Here is a list of things D3 does not do:

- D3 doesn’t generate predefined or “canned” visualizations for you.
  This is on purpose. <span id="ch02.xhtml_idm140093207932736"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="D3"
  secondary="explanatory visualizations with"></span><span id="ch02.xhtml_idm140093207931744"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm"
  primary="exploratory vs. explanatory visualizations"></span>D3 is
  intended primarily for highly customized visualization work, whether
  that is designing one-off explanatory charts or complex, interactive,
  exploratory tools. It is the most powerful tool for visualization on
  the web specifically because it enables you to develop whatever you
  can imagine from scratch. There are no templates or chart “wizards” in
  D3 (although you may become one by the time you finish this book).
  There are, however, many excellent tools built on top of D3 that *do*
  provide access to preconfigured chart types. (See the section
  <a href="#ch02.xhtml_alternatives_2"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="xref">“Alternatives”</a>.)

- D3 <span id="ch02.xhtml_idm140093207928176"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="D3"
  secondary="browser support"></span><span id="ch02.xhtml_idm140093207927168"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="browsers"
  secondary="support for"></span>doesn’t even try to support older
  browsers. This helps keep the D3 codebase clean and free of hacks to
  support old versions of Internet Explorer, for example. The philosophy
  is that by creating more compelling tools and refusing to support
  older browsers, we encourage more people to upgrade (rather than
  forestall the process, thereby requiring us to continue to support
  those browsers, and so on—a vicious cycle). When D3 was first released
  in 2011, this was a fairly radical position. I’m happy to say that
  browsers, people, and organizations have since modernized sufficiently
  to the point that this is practically a nonissue. Bureaucracies that
  continue to support ancient browsers miss out on all the benefits of
  D3. (More for us!)

- D3’s *core* <span id="ch02.xhtml_idm140093207923840"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm"
  primary="bitmap map tiles"></span><span id="ch02.xhtml_idm140093207923104"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm"
  primary="map tiles"></span><span id="ch02.xhtml_idm140093207922432"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm"
  primary="Google Maps"></span><span id="ch02.xhtml_idm140093207921760"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="maps"
  secondary="Google Maps"></span><span id="ch02.xhtml_idm140093207920816"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm"
  primary="Mapbox"></span><span id="ch02.xhtml_idm140093207920144"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="D3"
  secondary="geomapping in"></span><span id="ch02.xhtml_idm140093207919200"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="geomapping"
  secondary="D3 support for"></span>functionality doesn’t handle bitmap
  map tiles, such as those provided by Google Maps or Mapbox. D3 is
  great with anything vector—SVG images or GeoJSON data—but wasn’t
  originally intended to work with traditional map tiles. (*Bitmap*
  images are made up of pixels, so resizing them larger or smaller is
  difficult without a loss in quality. *Vector* images are defined by
  points, lines, and curves—mathematical equations, really—and can be
  scaled up or down without a loss in quality.) Fortunately, the
  <a href="https://github.com/d3/d3-tile"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-tile
  plug-in</a> can be used for tile-based mapping, though it is not
  covered in this book.

- D3 doesn’t hide your original data.
  <span id="ch02.xhtml_idm140093207915376"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="D3"
  secondary="data sharing in"></span>Because D3 code is executed on the
  client side (meaning, in the user’s web browser, as opposed to on the
  web server), the data you want visualized must be sent to the client.
  <span id="ch02.xhtml_idm140093207914080"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
  data-type="indexterm" primary="data sharing"></span>If your data can’t
  be shared, then don’t use D3. Alternatives include using proprietary
  browser plug-ins (like Flash) or prerendering visualizations as static
  images and sending those to the browser. (Yet, if you’re not
  interested in sharing your data, why would you bother visualizing it?
  The purpose of visualization is to communicate the data, so you might
  sleep better at night by choosing openness and transparency, rather
  than having nightmares about <a href="http://www.datathief.org/"
  class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">data thieves</a>.)

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Origins and Context">

<div id="ch02.xhtml_idm140093207911616" class="dedication">

# Origins and Context

The <span id="ch02.xhtml_idm140093207909856"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="development of"></span>first web browsers rendered static
pages; interactivity was limited to clicking links.
<span id="ch02.xhtml_idm140093207908720"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="JavaScript"
secondary="introduction of"></span>In 1996, Netscape introduced the
first browser with JavaScript, a new scripting language that could be
interpreted *by the browser while the page was being viewed*.

This <span id="ch02.xhtml_idm140093207906720"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="browsers"
secondary="development of interactivity"></span><span id="ch02.xhtml_idm140093207905696"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="interactivity"
secondary="browser development and"></span>doesn’t sound as
groundbreaking as it turned out to be, but this enabled web browsers to
evolve from merely passive *browsers* to dynamic frames for interactive,
networked experiences. This shift ultimately enabled every intrapage
interaction we have on the web today. Without JavaScript, D3 would never
have existed, and web-based data visualizations would be limited to
prerendered, noninteractive GIFs. (Yuck. Thank you, Netscape!)

Jump <span id="ch02.xhtml_idm140093207903152"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="prefuse toolkit"></span><span id="ch02.xhtml_idm140093207902416"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Heer, Jeffrey"></span><span id="ch02.xhtml_idm140093208177712"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Card, Stuart"></span><span id="ch02.xhtml_idm140093208177040"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Landay, James"></span><span id="ch02.xhtml_idm140093208176368"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data visualization"
secondary="early applications for"></span>ahead to 2005, when Jeffrey
Heer, Stuart Card, and James Landay introduced
<a href="http://prefuse.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">prefuse</a>, a
toolkit for bringing data visualization to the web. prefuse (spelled
with all lowercase letters) was written in Java, a compiled language,
with programs that could run in web browsers via a Java plug-in. (Note
that *Java* is a completely different programming language than
*JavaScript*, despite their similar names.)

prefuse was a breakthrough application—the first to make web-based
visualization accessible to less-than-expert programmers. Until prefuse
came along, any data vis on the web was very much a custom affair.

Two <span id="ch02.xhtml_idm140093208172640"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Flare"></span><span id="ch02.xhtml_idm140093208171904"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Adobe Flash Player"></span>years later,
Jeff Heer introduced <a href="http://flare.prefuse.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Flare</a>, a
similar toolkit, but written in ActionScript, so its visualizations
could be viewed on the web through Adobe’s Flash Player. Flare, like
prefuse, relied on a browser plug-in. Flare was a huge improvement, but
as web browsers continued to evolve, it was clear that visualizations
could be created with native browser technology, no plug-ins required.

By <span id="ch02.xhtml_idm140093208169600"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Bostock, Michael"></span><span id="ch02.xhtml_idm140093208168864"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm"
primary="Protovis visualization toolkit"></span>2009, Jeff Heer had
moved to Stanford, where he was advising a graduate student named
Michael Bostock. Together, in Stanford’s Vis Group, they created
<a href="http://mbostock.github.com/protovis/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Protovis</a>, a
JavaScript-based visualization toolkit that relied
<span class="keep-together">exclusively</span> on native browser
technologies.

Protovis made generating visualizations simple, even for users without
prior programming experience. Yet, to achieve this, it created an
abstract representation layer. The designer could address this layer
using Protovis syntax, but it wasn’t accessible through standard
methods, so debugging was difficult.

In <span id="ch02.xhtml_idm140093208165296"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="Ogievetsky, Vadim"></span>2011, Mike
Bostock, Vadim Ogievetsky, and Jeff Heer
<a href="http://vis.stanford.edu/papers/d3"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">officially
announced D3</a>, the next evolution in web visualization tools. Unlike
Protovis, D3 operates directly on the web document itself. This means
easier debugging, easier experimentation, and more visual possibilities.
The only downside to this approach is a potentially steeper learning
curve, but this book will make that as painless as possible. Plus, all
the skills you gain while learning about D3 will prove useful even
beyond the realm of data vis.

If <span id="ch02.xhtml_idm140093208162784"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="philosophy underlying"></span>you’re familiar with any of
these groundbreaking tools, you’ll appreciate that D3 descends from a
prestigious lineage. And if you have any interest in the philosophy
underlying D3’s elegant technical design, I highly recommend Mike,
Vadim, and Jeff’s
<a href="http://vis.stanford.edu/files/2011-D3-InfoVis.pdf"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">InfoVis
paper</a>, which clearly articulates the need for this kind of tool. The
paper encapsulates years’ worth of learning and insights made while
developing visualization tools.

</div>

</div>

<div class="section calibre2" data-type="sect1"
pdf-bookmark="Alternatives">

<div id="ch02.xhtml_alternatives_2" class="dedication">

# Alternatives

D3 <span id="ch02.xhtml_D3alt02"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="alternative tools"></span><span id="ch02.xhtml_DValt02"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data visualization"
secondary="alternative tools for"></span>might not be perfect for every
project. Sometimes you just need a quick chart and you don’t have time
to code it from scratch. Or you might need to support *really* old
browsers and can’t rely on the presence of technologies like SVG.

For those situations, it’s good to know what other tools are out there.
Here is a brief, noncomprehensive list of D3 alternatives, all of which
use web-standard technologies (mostly JavaScript) and are free to
download and use.

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Easy Charts">

<div id="ch02.xhtml_idm140093208154512" class="dedication">

## Easy Charts

<a href="http://datawrapper.de"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">DataWrapper</a>  
A <span id="ch02.xhtml_idm140093208151312"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="alternative tools for"></span>beautiful web service that lets
you upload your data and quickly generate a chart that you can republish
elsewhere, embed on your site, or export to PDF. This service was
originally intended for journalists, but it is helpful for everyone.
DataWrapper displays interactive charts in current browsers and static
images for old ones. (Brilliant!) You can also download all the code and
run it on your own server instead of using theirs.

<a href="http://www.flotcharts.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Flot</a>  
A <span id="ch02.xhtml_idm140093208148080"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="jQuery"
secondary="libraries and plug-ins for"></span>plotting library for
jQuery that uses the HTML canvas element and supports older browsers,
even all the way back to Internet Explorer 6. It supports limited visual
forms (lines, points, bars, areas), but it is easy to use.

<a href="https://developers.google.com/chart/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Google Chart
Tools</a>  
Having evolved from Google’s earlier
<a href="https://developers.google.com/chart/image/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Image Charts
API</a>, Google’s Chart Tools can be used to generate several standard
chart types, with support for old versions of IE.

<a href="http://www.highcharts.com/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Highcharts</a>  
A JavaScript-based charting library with several predesigned themes and
chart types. The tool is free only for noncommercial use.

<a href="http://benpickles.github.com/peity/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Peity</a>  
A jQuery plug-in for very simple and very *tiny* bar, line, and pie
charts that supports only recent browsers. Did I mention that this makes
only very *tiny* visualizations? +10 cuteness points.

<a href="http://timeline.knightlab.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Timeline.js</a>  
A library specifically for generating interactive timelines. No coding
is required; just use the code generator. There is not much room for
customization, but hey, timelines are really hard to do well.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Graph Visualizations">

<div id="ch02.xhtml_idm140093208137392" class="dedication">

## Graph Visualizations

A “graph” <span id="ch02.xhtml_idm140093208136064"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="graphs"
secondary="alternative tools for"></span>is just data with a networked
structure (for example, B is connected to A, and A is connected to C).

<a href="http://arborjs.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Arbor.js</a>  
A library for graph visualization using jQuery. Even if you never use
this, you should check out how the documentation is presented as a
graph, using the tool itself. (It’s so *meta*.) It uses the HTML canvas,
so it won’t work in older browsers.

<a href="http://js.cytoscape.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Cytoscape.js</a>  
Library for graph theory analysis and visualization.

<a href="http://sigmajs.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Sigma.js</a>  
A very lightweight library for graph visualization. Sigma.js is
beautiful and fast, and it also uses canvas.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Geomapping">

<div id="ch02.xhtml_idm140093208128112" class="dedication">

## Geomapping

In <span id="ch02.xhtml_idm140093208126784"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="geomapping"
secondary="alternative tools for"></span>this book, I distinguish
between *mapping* (all visualizations are maps) and *geomapping*
(visualizations that include geographic data, or geodata, such as
traditional maps). D3 has a lot of geomapping functionality, but you
should know about these other tools.

<a href="http://kartograph.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Kartograph</a>  
A JavaScript-and-Python combo for gorgeous, entirely vector-based
mapping by Gregor Aisch with must-see demos. Please go look at them now.
I promise you’ve never seen online maps this beautiful.

<a href="http://leafletjs.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Leaflet</a>  
A library for tiled maps, designed for smooth interaction on both
desktop and mobile devices. It includes some support for displaying data
layers of SVG on top of the map tiles. (See Mike’s demo
<a href="http://bost.ocks.org/mike/leaflet/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">“Using D3 with
Leaflet”</a>.)

<a href="http://modestmaps.com/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Modest Maps</a>  
The granddaddy of tiled map libraries, Modest Maps has been succeeded by
Polymaps and D3, but lots of people still love it, as it is lightweight
and works with old versions of IE and other browsers. Modest Maps has
been adapted for ActionScript, Processing, Python, PHP, Cinder,
openFrameworks…yeah, basically everything. File this under “oldie, but
goodie.”

<a href="http://polymaps.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Polymaps</a>  
A predecssor of D3 by Mike Bostock, this library is for displaying tiled
maps, with layers of data on top of the tiles. Polymaps relies on SVG
and thus works best with current browsers. That said, you may be better
off using D3 and the <a href="https://github.com/d3/d3-tile"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-tile
plug-in</a>.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Almost from Scratch">

<div id="ch02.xhtml_idm140093208114448" class="dedication">

## Almost from Scratch

These <span id="ch02.xhtml_idm140093208113088"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="drawing"
secondary="alternative tools for"></span>tools, like D3, provide methods
of drawing visual forms, but without predesigned visual templates. If
you enjoy the creative freedom of starting from scratch, you might enjoy
these.

<a href="http://p5js.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">p5.js</a>  
p5 takes <a href="http://processing.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Processing</a>,
the fantastic programming language for artists and designers, and
reimagines it in JavaScript for the web. Imagine the friendly
nomenclature of Processing, and the webby strength of JavaScript. The p5
project is led by <a href="http://www.lauren-mccarthy.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Lauren
McCarthy</a>, and it renders using canvas, so only modern browsers are
supported.

<a href="http://paperjs.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Paper.js</a>  
A framework for rendering vector graphics to canvas. Also, its website
is one of the most beautiful on the internet, and their demos are
unbelievable. (Go play with them now.)

<a href="http://dmitrybaranovskiy.github.io/raphael/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Raphaël</a>  
A well-established library for drawing vector graphics by Dmitry
Baranovskiy, popular due to its friendly syntax and support for older
browsers.

<a href="http://snapsvg.io"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Snap.svg</a>  
A pretty fantastic, modern library for SVG creating and animation, this
is also primarily by Dmitry. Consider it Raphaël’s successor.

<a href="https://two.js.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Two.js</a>  
JavaScript library for two-dimensional drawing in modern browsers,
rendering to SVG, canvas, and WebGL, by <a href="http://jonobr1.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Jono Brandel</a>.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Three-Dimensional">

<div id="ch02.xhtml_idm140093208110960" class="dedication">

## Three-Dimensional

D3 <span id="ch02.xhtml_idm140093208296896"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="3D drawing"
secondary="alternative tools for"></span><span id="ch02.xhtml_idm140093208295888"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="3D drawing"
secondary="alternative tools for"
primary-sortas="threeD drawing"></span><span id="ch02.xhtml_idm140093208294672"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="drawing" secondary="3D drawing"
secondary-sortas="threeD drawing"></span>is not the best at 3D, simply
because web browsers are historically two-dimensional beasts. But with
increased support for WebGL, there are now more opportunities for 3D web
experiences.

<a href="http://www.senchalabs.org/philogl/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">PhiloGL</a>  
A WebGL framework specifically for 3D visualization (no longer under
active development, unfortunately).

<a href="http://mrdoob.github.com/three.js/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Three.js</a>  
A library for generating any sort of 3D scene you could imagine,
produced by Google’s Data Arts team. You could spend all day exploring
the mind-blowing demos on their site.

</div>

</div>

<div class="section calibre2" data-type="sect2"
pdf-bookmark="Tools Built with D3">

<div id="ch02.xhtml_idm140093208288672" class="dedication">

## Tools Built with D3

<div class="section calibre2" data-type="sect3"
pdf-bookmark="General-use charting libraries">

<div id="ch02.xhtml_idm140093208287664" class="dedication">

### General-use charting libraries

There <span id="ch02.xhtml_D3tools02"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="D3"
secondary="tools built with"></span><span id="ch02.xhtml_idm140093208285056"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="charts"
secondary="general-use libraries for"></span>are many different charting
libraries built on top of D3. Theoretically, these make it easier to
generate a visualization quickly, and often without having to write any
D3 code yourself. The trade-off is generally less customization; you
have to be comfortable with the chart templates supported by each tool.
Also, each library has its own syntax and quirks. I recommend taking a
quick glance at each one to decide what works best for you.

<a href="https://eventbrite.github.io/britecharts/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Britecharts</a>  
A reusable charting library by for D3 4.x brought to you by Eventbrite’s
engineering team. And, wow, <a
href="http://eventbrite.github.io/britecharts/tutorial-kitchen-sink.html"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">those colors</a>
sure are “brite.”

<a href="http://c3js.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">C3.js</a>  
Reusable charting by Masayuki Tanaka. Not yet updated to work with D3
4.x at the time of this writing. (But what a nice demo!)

<a href="http://forio.com/contour/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Contour</a>  
Beautifully designed, simple chart types.

<a href="http://d3plus.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">D3plus</a>  
Charting library that also includes some nice utilities for easy text
wrapping, color legibility, and other things you’d probably want help
with.

<a href="http://visible.io"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">D4</a>  
Library with lots of supported chart types.

<a href="http://dimplejs.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">dimple</a>  
Library intended for business analysts.

<a href="http://nvd3.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">NVD3</a>  
NVD3 was one of the first D3-based charting libraries, and offers lots
of beautiful examples, with room for customization.

<a href="https://plot.ly/javascript/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">plotly.js</a>  
Quick and easy charting. Just drop in your data values, and you’re off!

<a href="http://plottablejs.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Plottable</a>  
Promises “the power and flexibility of D3, but easier,” by providing
predefined “components” that you can reuse.

<a href="http://imaginea.github.io/uvCharts/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">uvCharts</a>  
Another such library, with 12 supported chart types.

<a href="http://vega.github.io/vega/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Vega</a>  
A “visualization grammar” with which you define chart types, visual
properties, interaction rules, and data in a simple JSON object (more on
JSON in <a href="#ch03.xhtml_technology_fundamentals"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1" data-type="xref"
data-xrefstyle="chap-num-title">Chapter 3, <em>Technology
Fundamentals</em></a>). Then Vega translates your specifications into a
working, interactive chart, using D3 under the hood. Version 2 of this
amazing, powerful tool was primarily authored by Arvind Satyanarayan,
and was produced in Jeff Heer’s new
<a href="https://idl.cs.washington.edu"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Interactive Data
Lab</a> at the University of Washington (Jeff’s next stop after
Stanford).

</div>

</div>

<div class="section calibre2" data-type="sect3"
pdf-bookmark="More specialized tools">

<div id="ch02.xhtml_idm140093208282288" class="dedication">

### More specialized tools

This section includes D3-based libraries with more specialized use cases
(such as for time series data), as well as plug-ins for use with D3 and
other related tools.

<a href="http://square.github.com/crossfilter/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Crossfilter</a>  
A library for working with large, multivariate datasets, written
primarily by Mike Bostock. This is useful for trying to squeeze your
“big data” into a relatively small web browser. Not technically built
with D3, but is commonly used with D3.

<a href="http://square.github.com/cubism/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Cubism</a>  
A D3 plug-in for visualizing time series data, also written by Mike
Bostock. (One of my favorite demos.)

<a href="http://d3-annotation.susielu.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-annotation</a>  
A module for painlessly implementing visual annotations in D3 by Susie
Lu.

<a href="https://github.com/patorjk/d3-context-menu"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3-context-menu</a>  
A plug-in for adding contextual menus to your D3 projects, by Patrick
Gillespie.

<a href="https://github.com/sebastian-meier/d3.sketchy"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3.sketchy</a>  
This tool by Sebastian Meier takes your SVG shapes and makes them look
hand-drawn. Useful when you are working in code, but need to convey to
others that the output is rough and your design is still in process
(like a sketch). Be sure to play with the
<a href="http://prjcts.sebastianmeier.eu/sketch/examples/index_2.html"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">interactive
customizer</a>.

<a href="http://d3-legend.susielu.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">D3 SVG
Legend</a>  
A reusable legend component for D3 by Susie Lu.

<a href="http://labratrevenge.com/d3-tip/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">D3-tip</a>  
A tool for generating tooltips in D3 charts, in case you get tired of
making your own, as described in <a href="#ch10.xhtml_interactivity"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Chapter 10</a>.

<a href="https://github.com/lighterio/d6"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">D6</a>  
To be honest, I don’t understand this one, but I had to share it here
because the name stands for “Dynamically Downloaded Data-Driven
Documents, Dude.”

<a href="http://dc-js.github.io/dc.js/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">dc.js</a>  
The “dc” is short for *dimensional charting*, as this library is
optimized for exploring large, multidimensional datasets.

<a href="https://github.com/boundary/firespray"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Firespray</a>  
Super-fast charting library for streaming data. (Think high-density
real-time data dashboards.)

<a href="http://robinforest.net/forest-d3/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Forest D3</a>  
A time-series charting library built on D3, by Robin Hu.

<a href="http://metricsgraphicsjs.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">MetricsGraphics.js</a>  
A very nice library for working with time-series data, by Ali Almossawi
and Hamilton Ulmer.

<a href="http://misoproject.com/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Miso Project</a>  
An open source project that includes
<a href="http://misoproject.com/d3-chart/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">d3.chart</a>, “a
framework for building reusable charts with d3.js,” as well as other
useful tools, from the brilliant people at <a href="https://bocoup.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Bocoup</a> and
<a href="http://bit.ly/2uRORGK"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">The Guardian
Interactive team</a>.

<a href="http://rawgraphs.io"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">RAW Graphs</a>  
Paste your spreadsheet into this amazing tool and generate an array of
different chart types in seconds. A project initiated at the esteemed
<a href="http://densitydesign.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Density
Design</a> research lab in Milan.

<a href="https://github.com/jamesthomson/R2D3"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">R2D3</a>  
A unique blend of D3 and R that enables you to use R to create D3
visualizations.

<a href="http://code.shutterstock.com/rickshaw/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Rickshaw</a>  
A toolkit for displaying time series data that is also very
customizable.

<a href="http://techanjs.org"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">TechanJS</a>  
A library specifically for financial data charting and analysis.

<a href="http://tributary.io"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Tributary</a>  
A great tool for experimenting with live coding using D3, by Ian
Johnson.<span id="ch02.xhtml_idm140093208219488"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="DValt02"></span><span id="ch02.xhtml_idm140093208218512"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="D3alt02"></span><span id="ch02.xhtml_idm140093208217568"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="D3tools02"></span>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<span id="ch03.xhtml"></span>

<div id="ch03.xhtml_sbo-rt-content" class="calibre1">

<div id="ch03.xhtml_technology_fundamentals" class="dedication">

