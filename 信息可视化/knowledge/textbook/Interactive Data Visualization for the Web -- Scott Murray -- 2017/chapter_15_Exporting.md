# <span class="keep-together">Chapter 15. </span>Exporting

Sometimes <span id="ch15.xhtml_DVexport15"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="data visualization"
secondary="exporting to other file types"></span>you need to take your
visualization beyond the browser, such as when you’re asked to present
your work in a TED talk or in your first solo show at MoMA.

Here are three easy ways to get D3 visualizations out of D3 and into
formats suitable for other, noninteractive media. D3 has no explicit
“export” function built in (although some people have built their own),
so what follows are simple techniques that will work for any SVG image
in a web browser.

<div class="section calibre2" data-type="sect1" pdf-bookmark="Bitmaps">

<div id="ch15.xhtml_idm140093179388384" class="dedication">

# Bitmaps

The <span id="ch15.xhtml_idm140093179386816"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="exporting D3 visualizations"
secondary="bitmaps"></span>easiest and lowest-quality option is,
obviously, to take a screenshot. Depending on your operating system, you
can do this using the Print Screen button on a PC, or ⌘-Shift-4 on the
Mac. (Drag those crosshairs over the area you want to capture, release,
and check your desktop for a PNG image.)

<a href="#ch15.xhtml_bitmap_export"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-1</a> is a bitmap screenshot I made using
⌘-Shift-4.

<figure class="calibre35">
<div id="ch15.xhtml_bitmap_export" class="figure">
<img
src="images/2481c17bbcc939793c5c93257fae42ecc68033ba0f808f2903bbc7f6460b58f4.webp"
class="calibre240" alt="dvw2 1501" />
<h6 class="calibre37"><span class="keep-together">Figure 15-1. </span>A
PNG screenshot</h6>
</div>
</figure>

This is easy and quick, but generates a bitmap image at screen
resolution. So, as you can see, the image won’t scale up nicely, nor
print with sharp edges. This approach is
<span class="keep-together">probably</span> suitable only for reuse
on-screen. (The exception to this is if you have a super high-res
display; then the resolution will be much finer.)

For visualizations that are too large to fit on your screen all at once,
I like the <a href="http://bit.ly/1Nc3qYz"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Awesome
Screenshot</a> extension for Chrome. Awesome Screenshot can capture the
entire page—in effect, scrolling up and down, snapping multiple
screenshots, and then stitching them together into a single image.

</div>

</div>

<div class="section calibre2" data-type="sect1" pdf-bookmark="PDF">

<div id="ch15.xhtml_idm140093179379392" class="dedication">

# PDF

Portable <span id="ch15.xhtml_idm140093179377984"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="exporting D3 visualizations"
secondary="PDFs"></span>Document Format documents can contain
vector-based artwork, such as SVG images, so exporting to PDF gives you
a quick, scalable copy of your visualization (see
<a href="#ch15.xhtml_pdf_export"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-2</a>).

<figure class="calibre35">
<div id="ch15.xhtml_pdf_export" class="figure">
<img
src="images/56d633f5383b7926b48793201b9b0fa5f9b46af2c6306a3c5e5dfbf844b8d14f.webp"
class="calibre241" alt="dvw2 1502" />
<h6 class="calibre37"><span class="keep-together">Figure 15-2. </span>A
PDF maintains the original vector data for clarity</h6>
</div>
</figure>

On <span id="ch15.xhtml_idm140093179373136"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="print-to-PDF functionality"></span>the
Mac, in your browser, go to File→Print. Then look for the PDF menu, and
choose Save as PDF.

On Windows 10, you can print directly to the “Microsoft Print to PDF”
virtual printer from any application. On older versions of Windows, use
Chrome’s built-in support for PDF export (Print→Save as PDF) or install
a third-party virtual PDF printer.

On Linux, well, it depends on your distribution, but you could also use
Chrome’s built-in PDF support.

</div>

</div>

<div class="section calibre2" data-type="sect1" pdf-bookmark="SVG">

<div id="ch15.xhtml_idm140093179370816" class="dedication">

# SVG

Finally, <span id="ch15.xhtml_EXsvg1"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="exporting D3 visualizations"
secondary="SVG format"></span><span id="ch15.xhtml_SVGexport15"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="SVG (Scalable Vector Graphics)"
secondary="exporting D3 visualizations as"></span>you probably realized
that, since we are using D3 to generate images in SVG format, we could
just save out a copy of the SVG image directly. This has all the
benefits of PDF: you maintain the original vector data, it’s scalable,
and you can even bring the results into
<a href="https://www.adobe.com/products/illustrator.html"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Illustrator</a>,
<a href="https://inkscape.org/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Inkscape</a>,
<a href="https://www.sketchapp.com"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">Sketch</a>, or
another SVG-compatible editor and tweak it after the fact. (This is true
to a certain extent for PDF files as well, but depending on the PDF
generator, sometimes elements get grouped and layered in unexpected
ways.)

The simplest way is to copy the SVG code straight out of the DOM (see
<a href="#ch15.xhtml_copy_the_svg"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-3</a>). First, inspect the SVG element. Click
the element in the web inspector, and then click Copy.

<figure class="calibre35">
<div id="ch15.xhtml_copy_the_svg" class="figure">
<img
src="images/76c1864fe7b1966b120f9109e2dc106facdc46855085013666fd0cbb8f56ca8b.webp"
class="calibre242" alt="dvw2 1503" />
<h6 class="calibre37"><span class="keep-together">Figure 15-3.
</span>Copying the D3-generated SVG code from the DOM</h6>
</div>
</figure>

Switch back to your text editor, and paste the contents into a new file,
as shown in <a href="#ch15.xhtml_paste_the_svg"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-4</a>.

<figure class="calibre35">
<div id="ch15.xhtml_paste_the_svg" class="figure">
<img
src="images/ec5cc2e2eee48c7942e75c5886185ad9630e48d83cc903d9ebc8bab332a362d7.webp"
class="calibre243" alt="dvw2 1504" />
<h6 class="calibre37"><span class="keep-together">Figure 15-4.
</span>SVG code pasted into a new document</h6>
</div>
</figure>

Then just save the file as *something.svg*. Now you can open it up in
Sketch, as shown in <a href="#ch15.xhtml_svg_in_sketch"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-5</a>, or any other SVG-compatible program.

<figure class="calibre35">
<div id="ch15.xhtml_svg_in_sketch" class="figure">
<img
src="images/b2e53bdee5312b6e72ecc4b61b04bbe330d4d50c8382b896ca2db373e768c160.webp"
class="calibre243" alt="dvw2 1505" />
<h6 class="calibre37"><span class="keep-together">Figure 15-5.
</span>Exported SVG opened in Sketch</h6>
</div>
</figure>

As you can see in <a href="#ch15.xhtml_edit_the_svg"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-6</a>, all of the elements remain
individually selectable and editable.

<figure class="calibre35">
<div id="ch15.xhtml_edit_the_svg" class="figure">
<img
src="images/497f72c524d14b2b7231966a9f7f0d996465b7b9a4681ee5a81a50de924971ac.webp"
class="calibre243" alt="dvw2 1506" />
<h6 class="calibre37"><span class="keep-together">Figure 15-6.
</span>One SVG element selected</h6>
</div>
</figure>

I like to use Sketch because it respects images’ hierarchical structure;
SVG `g` elements are interpreted as “grouped” elements in Sketch. Even
the `title` values, which I’d originally intended as browser tooltips,
appear here, so I can, say, easily select Edward or Felicity. Using `g`s
and `title`s not only keeps your DOM structure tidy and readable—it
makes it so much easier to select elements during manual editing for
print.

For example, it’s now super quick to select all the circles in the
sidebar to apply style changes. In the version shown in
<a href="#ch15.xhtml_edited_svg"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="xref">Figure 15-7</a>, I’ve made some “enhancements” to my
design. As I always say, when in doubt, use gradients. (To be clear,
this is a joke, and is the *opposite* of what I always say, which is
“Pretty much never use gradients.”)

<figure class="calibre35">
<div id="ch15.xhtml_edited_svg" class="figure">
<img
src="images/43fc2573c1a3a7aa5f358ae17f136a56834bfb2f4e78072320059c0c8d443844.webp"
class="calibre243" alt="dvw2 1507" />
<h6 class="calibre37"><span class="keep-together">Figure 15-7.
</span>Don’t try gradients at home</h6>
</div>
</figure>

A shortcut to this whole copy-paste approach is to use Shan Carter’s
<a href="https://nytimes.github.io/svg-crowbar/"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1">SVG Crowbar</a>,
a Chrome bookmarklet that, with some caveats, extracts an SVG from its
web page with just a single click on your part.

As you can see, there are many options for getting your work out of the
browser, documented, and saved for use in other contexts, whether for
print or for the screen.<span id="ch15.xhtml_idm140093179340928"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="DVexport15"></span><span id="ch15.xhtml_idm140093179339952"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary=""
startref="EXsvg1"></span><span id="ch15.xhtml_idm140093179339008"
class="calibre5 pcalibre pcalibre2 pcalibre3 pcalibre1"
data-type="indexterm" primary="" startref="SVGexport15"></span>

</div>

</div>

</div>

</div>

<span id="ch16.xhtml"></span>

<div id="ch16.xhtml_sbo-rt-content" class="calibre1">

<div id="ch16.xhtml_project_walkthrough" class="dedication">

