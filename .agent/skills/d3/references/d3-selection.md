# D3 - D3-Selection

**Pages:** 8

---

## Local variables | D3 by Observable

**URL:** https://d3js.org/d3-selection/locals

**Contents:**
- Local variables ​
- local() ​
- local.set(node, value) ​
- local.get(node) ​
- local.remove(node) ​
- local.toString() ​

D3 locals allow you to define local state independent of data. For instance, when rendering small multiples of time-series data, you might want the same x scale for all charts but distinct y scales to compare the relative performance of each metric. D3 locals are scoped by DOM elements: on set, the value is stored on the given element; on get, the value is retrieved from given element or the nearest ancestor that defines it.

Locals are rarely used; you may find it easier to store whatever state you need in the selection’s data.

Source · Declares a new local variable.

Like var, each local is a distinct symbolic reference; unlike var, the value of each local is also scoped by the DOM.

Source · Sets the value of this local on the specified node to the value, and returns the specified value. This is often performed using selection.each:

If you are just setting a single variable, consider using selection.property:

Source · Returns the value of this local on the specified node.

If the node does not define this local, returns the value from the nearest ancestor that defines it. Returns undefined if no ancestor defines this local.

Source · Deletes this local’s value from the specified node.

Returns true if the node defined this local prior to removal, and false otherwise. If ancestors also define this local, those definitions are unaffected, and thus local.get will still return the inherited value.

Source · Returns the automatically-generated identifier for this local. This is the name of the property that is used to store the local’s value on elements, and thus you can also set or get the local’s value using element[local] or by using selection.property.

**Examples:**

Example 1 (javascript):
```javascript
const foo = d3.local();
```

Example 2 (r):
```r
selection.each(function(d) {
  foo.set(this, d.value);
});
```

Example 3 (scala):
```scala
selection.property(foo, (d) => d.value);
```

Example 4 (javascript):
```javascript
selection.each(function() {
  const value = foo.get(this);
});
```

---

## Namespaces | D3 by Observable

**URL:** https://d3js.org/d3-selection/namespaces

**Contents:**
- Namespaces ​
- namespace(name) ​
- namespaces ​

XML namespaces are fun! Right? 🤪 Fortunately you can mostly ignore them.

A case where you need to specify them is when appending an element to a parent that belongs to a different namespace; typically, to create a div inside a SVG foreignObject element:

Source · Qualifies the specified name, which may or may not have a namespace prefix.

If the name contains a colon (:), the substring before the colon is interpreted as the namespace prefix, which must be registered in d3.namespaces. Returns an object space and local attributes describing the full namespace URL and the local name. If the name does not contain a colon, this function merely returns the input name.

Source · The map of registered namespace prefixes. The initial value is:

Additional prefixes may be assigned as needed to create elements or attributes in other namespaces.

**Examples:**

Example 1 (swift):
```swift
d3.create("svg")
  .append("foreignObject")
    .attr("width", 300)
    .attr("height", 100)
  .append("xhtml:div")
    .text("Hello, HTML!");
```

Example 2 (css):
```css
d3.namespace("svg:text") // {space: "http://www.w3.org/2000/svg", local: "text"}
```

Example 3 (json):
```json
{
  svg: "http://www.w3.org/2000/svg",
  xhtml: "http://www.w3.org/1999/xhtml",
  xlink: "http://www.w3.org/1999/xlink",
  xml: "http://www.w3.org/XML/1998/namespace",
  xmlns: "http://www.w3.org/2000/xmlns/"
}
```

---

## Handling events | D3 by Observable

**URL:** https://d3js.org/d3-selection/events

**Contents:**
- Handling events ​
- selection.on(typenames, listener, options) ​
- selection.dispatch(type, parameters) ​
- pointer(event, target) ​
- pointers(event, target) ​

For interaction, selections allow listening for and dispatching of events.

Source · Adds or removes a listener to each selected element for the specified event typenames.

The typenames is a string event type, such as click, mouseover, or submit; any DOM event type supported by your browser may be used. The type may be optionally followed by a period (.) and a name; the optional name allows multiple callbacks to be registered to receive events of the same type, such as click.foo and click.bar. To specify multiple typenames, separate typenames with spaces, such as input change or click.foo click.bar.

When a specified event is dispatched on a selected element, the specified listener will be evaluated for the element, being passed the current event (event) and the current datum (d), with this as the current DOM element (event.currentTarget). Listeners always see the latest datum for their element. Note: while you can use event.pageX and event.pageY directly, it is often convenient to transform the event position to the local coordinate system of the element that received the event using d3.pointer.

If an event listener was previously registered for the same typename on a selected element, the old listener is removed before the new listener is added. To remove a listener, pass null as the listener. To remove all listeners for a given name, pass null as the listener and .foo as the typename, where foo is the name; to remove all listeners with no name, specify . as the typename.

An optional options object may specify characteristics about the event listener, such as whether it is capturing or passive; see element.addEventListener.

If a listener is not specified, returns the currently-assigned listener for the specified event typename on the first (non-null) selected element, if any. If multiple typenames are specified, the first matching listener is returned.

Source · Dispatches a custom event of the specified type to each selected element, in order.

An optional parameters object may be specified to set additional properties of the event. It may contain the following fields:

If parameters is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). It must return the parameters for the current element.

Source · Returns a two-element array of numbers [x, y] representing the coordinates of the specified event relative to the specified target.

event can be a MouseEvent, a PointerEvent, a Touch, or a custom event holding a UIEvent as event.sourceEvent.

If target is not specified, it defaults to the source event’s currentTarget property, if available. If the target is an SVG element, the event’s coordinates are transformed using the inverse of the screen coordinate transformation matrix. If the target is an HTML element, the event’s coordinates are translated relative to the top-left corner of the target’s bounding client rectangle. (As such, the coordinate system can only be translated relative to the client coordinates. See also GeometryUtils.) Otherwise, [event.pageX, event.pageY] is returned.

Source · Returns an array [[x0, y0], [x1, y1]…] of coordinates of the specified event’s pointer locations relative to the specified target.

For touch events, the returned array of positions corresponds to the event.touches array; for other events, returns a single-element array.

If target is not specified, it defaults to the source event’s currentTarget property, if any.

**Examples:**

Example 1 (javascript):
```javascript
d3.selectAll("p").on("click", (event) => console.log(event))
```

Example 2 (csharp):
```csharp
d3.select("p").dispatch("click")
```

Example 3 (unknown):
```unknown
const [x, y] = d3.pointer(event);
```

Example 4 (javascript):
```javascript
const points = d3.pointers(event);
```

---

## Modifying elements | D3 by Observable

**URL:** https://d3js.org/d3-selection/modifying

**Contents:**
- Modifying elements ​
- selection.attr(name, value) ​
- selection.classed(names, value) ​
- selection.style(name, value, priority) ​
- selection.property(name, value) ​
- selection.text(value) ​
- selection.html(value) ​
- selection.append(type) ​
- selection.insert(type, before) ​
- selection.remove() ​

After selecting elements, use the selection to modify the elements. For example, to set the class and color style of all paragraph elements in the current document:

Selection methods typically return the current selection, or a new selection, allowing the concise application of multiple operations on a given selection via method chaining. The above is equivalent to:

Selections are immutable. All selection methods that affect which elements are selected (or their order) return a new selection rather than modifying the current selection. However, note that elements are necessarily mutable, as selections drive transformations of the document!

Source · If a value is specified, sets the attribute with the specified name to the specified value on the selected elements and returns this selection.

If the value is a constant, all elements are given the same attribute value; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to set each element’s attribute. A null value will remove the specified attribute.

If a value is not specified, returns the current value of the specified attribute for the first (non-null) element in the selection. This is generally useful only if you know that the selection contains exactly one element.

The specified name may have a namespace prefix, such as xlink:href to specify the href attribute in the XLink namespace. See namespaces for the map of supported namespaces; additional namespaces can be registered by adding to the map.

Source · If a value is specified, assigns or unassigns the specified CSS class names on the selected elements by setting the class attribute or modifying the classList property and returns this selection.

The specified names is a string of space-separated class names. For example, to assign the classes foo and bar to the selected elements:

If the value is truthy, then all elements are assigned the specified classes; otherwise, the classes are unassigned.

If the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to assign or unassign classes on each element.

If a value is not specified, returns true if and only if the first (non-null) selected element has the specified classes. This is generally useful only if you know the selection contains exactly one element.

Source · If a value is specified, sets the style property with the specified name to the specified value on the selected elements and returns this selection.

If the value is a constant, then all elements are given the same style property value; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to set each element’s style property. A null value will remove the style property. An optional priority may also be specified, either as null or the string important (without the exclamation point).

If a value is not specified, returns the current value of the specified style property for the first (non-null) element in the selection. The current value is defined as the element’s inline value, if present, and otherwise its computed value. Accessing the current style value is generally useful only if you know the selection contains exactly one element.

Unlike many SVG attributes, CSS styles typically have associated units. For example, 3px is a valid stroke-width property value, while 3 is not. Some browsers implicitly assign the px (pixel) unit to numeric values, but not all browsers do: IE, for example, throws an “invalid arguments” error!

Source · Some HTML elements have special properties that are not addressable using attributes or styles, such as a form field’s text value and a checkbox’s checked boolean. Use this method to get or set these properties.

If a value is specified, sets the property with the specified name to the specified value on selected elements. If the value is a constant, then all elements are given the same property value; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to set each element’s property. A null value will delete the specified property.

If a value is not specified, returns the value of the specified property for the first (non-null) element in the selection. This is generally useful only if you know the selection contains exactly one element.

Source · If a value is specified, sets the text content to the specified value on all selected elements, replacing any existing child elements.

If the value is a constant, then all elements are given the same text content; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to set each element’s text content. A null value will clear the content.

If a value is not specified, returns the text content for the first (non-null) element in the selection. This is generally useful only if you know the selection contains exactly one element.

Source · If a value is specified, sets the inner HTML to the specified value on all selected elements, replacing any existing child elements.

If the value is a constant, then all elements are given the same inner HTML; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function’s return value is then used to set each element’s inner HTML. A null value will clear the content.

If a value is not specified, returns the inner HTML for the first (non-null) element in the selection. This is generally useful only if you know the selection contains exactly one element.

Use selection.append or selection.insert instead to create data-driven content; this method is intended for when you want a little bit of HTML, say for rich formatting. Also, selection.html is only supported on HTML elements. SVG elements and other non-HTML elements do not support the innerHTML property, and thus are incompatible with selection.html. Consider using XMLSerializer to convert a DOM subtree to text. See also the innersvg polyfill, which provides a shim to support the innerHTML property on SVG elements.

Source · If the specified type is a string, appends a new element of this type (tag name) as the last child of each selected element, or before the next following sibling in the update selection if this is an enter selection. The latter behavior for enter selections allows you to insert elements into the DOM in an order consistent with the new bound data; however, note that selection.order may still be required if updating elements change order (i.e., if the order of new data is inconsistent with old data).

If the specified type is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). This function should return an element to be appended. (The function typically creates a new element, but it may instead return an existing element.) For example, to append a paragraph to each DIV element:

This is equivalent to:

Which is equivalent to:

In both cases, this method returns a new selection containing the appended elements. Each new element inherits the data of the current elements, if any, in the same manner as selection.select.

The specified name may have a namespace prefix, such as svg:text to specify a text attribute in the SVG namespace. See namespaces for the map of supported namespaces; additional namespaces can be registered by adding to the map. If no namespace is specified, the namespace will be inherited from the parent element; or, if the name is one of the known prefixes, the corresponding namespace will be used (for example, svg implies svg:svg).

Source · If the specified type is a string, inserts a new element of this type (tag name) before the first element matching the specified before selector for each selected element. For example, a before selector :first-child will prepend nodes before the first child. If before is not specified, it defaults to null. (To append elements in an order consistent with bound data, use selection.append.)

Both type and before may instead be specified as functions which are evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The type function should return an element to be inserted; the before function should return the child element before which the element should be inserted. For example, to append a paragraph to each DIV element:

This is equivalent to:

Which is equivalent to:

In both cases, this method returns a new selection containing the appended elements. Each new element inherits the data of the current elements, if any, in the same manner as selection.select.

The specified name may have a namespace prefix, such as svg:text to specify a text attribute in the SVG namespace. See namespaces for the map of supported namespaces; additional namespaces can be registered by adding to the map. If no namespace is specified, the namespace will be inherited from the parent element; or, if the name is one of the known prefixes, the corresponding namespace will be used (for example, svg implies svg:svg).

Source · Removes the selected elements from the document. Returns this selection (the removed elements) which are now detached from the DOM. There is not currently a dedicated API to add removed elements back to the document; however, you can pass a function to selection.append or selection.insert to re-add elements.

Source · Inserts clones of the selected elements immediately following the selected elements and returns a selection of the newly added clones. If deep is truthy, the descendant nodes of the selected elements will be cloned as well. Otherwise, only the elements themselves will be cloned. Equivalent to:

Source · Returns a new selection that contains a copy of each group in this selection sorted according to the compare function. After sorting, re-inserts elements to match the resulting order (per selection.order).

The compare function, which defaults to ascending, is passed two elements’ data a and b to compare. It should return either a negative, positive, or zero value. If negative, then a should be before b; if positive, then a should be after b; otherwise, a and b are considered equal and the order is arbitrary.

Source · Re-inserts elements into the document such that the document order of each group matches the selection order. This is equivalent to calling selection.sort if the data is already sorted, but much faster.

Source · Re-inserts each selected element, in order, as the last child of its parent. Equivalent to:

Source · Re-inserts each selected element, in order, as the first child of its parent. Equivalent to:

Source · Given the specified element name, returns a single-element selection containing a detached element of the given name in the current document. This method assumes the HTML namespace, so you must specify a namespace explicitly when creating SVG or other non-HTML elements; see namespace for details on supported namespace prefixes.

Source · Given the specified element name, returns a function which creates an element of the given name, assuming that this is the parent element. This method is used internally by selection.append and selection.insert to create new elements. For example, this:

See namespace for details on supported namespace prefixes, such as for SVG elements.

**Examples:**

Example 1 (unknown):
```unknown
d3.selectAll("p")
    .attr("class", "graf")
    .style("color", "red");
```

Example 2 (javascript):
```javascript
const p = d3.selectAll("p");
p.attr("class", "graf");
p.style("color", "red");
```

Example 3 (unknown):
```unknown
selection.attr("color", "red")
```

Example 4 (unknown):
```unknown
selection.attr("color") // "red"
```

---

## d3-selection | D3 by Observable

**URL:** https://d3js.org/d3-selection

**Contents:**
- d3-selection ​

Selections allow powerful data-driven transformation of the document object model (DOM): set attributes, styles, properties, HTML or text content, and more. Using the data join’s enter and exit selections, you can also add or remove elements to correspond to data.

For more, see the d3-selection collection on Observable.

---

## Selecting elements | D3 by Observable

**URL:** https://d3js.org/d3-selection/selecting

**Contents:**
- Selecting elements ​
- selection() ​
- select(selector) ​
- selectAll(selector) ​
- selection.select(selector) ​
- selection.selectAll(selector) ​
- selection.filter(filter) ​
- selection.selectChild(selector) ​
- selection.selectChildren(selector) ​
- selection.selection() ​

A selection is a set of elements from the DOM. Typically these elements are identified by selectors such as .fancy for elements with the class fancy, or div to select DIV elements.

Selection methods come in two forms, select and selectAll: the former selects only the first matching element, while the latter selects all matching elements in document order. The top-level selection methods, d3.select and d3.selectAll, query the entire document; the subselection methods, selection.select and selection.selectAll, restrict selection to descendants of the selected elements. There is also selection.selectChild and selection.selectChildren for direct children.

By convention, selection methods that return the current selection such as selection.attr use four spaces of indent, while methods that return a new selection use only two. This helps reveal changes of context by making them stick out of the chain:

Source · Selects the root element, document.documentElement.

This function can also be used to test for selections (instanceof d3.selection) or to extend the selection prototype. For example, to add a method to check checkboxes:

Source · Selects the first element that matches the specified selector string.

If no elements match the selector, returns an empty selection. If multiple elements match the selector, only the first matching element (in document order) will be selected. For example, to select the first anchor element:

If the selector is not a string, instead selects the specified node; this is useful if you already have a reference to a node, such as document.body.

Or, to make a clicked paragraph red:

Source · Selects all elements that match the specified selector string.

The elements will be selected in document order (top-to-bottom). If no elements in the document match the selector, or if the selector is null or undefined, returns an empty selection.

If the selector is not a string, instead selects the specified array of nodes; this is useful if you already have a reference to nodes, such as this.childNodes within an event listener or a global such as document.links. The nodes may instead be an iterable, or a pseudo-array such as a NodeList. For example, to color all links red:

Source · For each selected element, selects the first descendant element that matches the specified selector string.

If no element matches the specified selector for the current element, the element at the current index will be null in the returned selection. (If the selector is null, every element in the returned selection will be null, resulting in an empty selection.) If the current element has associated data, this data is propagated to the corresponding selected element. If multiple elements match the selector, only the first matching element in document order is selected.

If the selector is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). It must return an element, or null if there is no matching element. For example, to select the previous sibling of each paragraph:

Unlike selection.selectAll, selection.select does not affect grouping: it preserves the existing group structure and indexes, and propagates data (if any) to selected children. Grouping plays an important role in the data join. See Nested Selections and How Selections Work for more on this topic.

selection.select propagates the parent’s data to the selected child.

Source · For each selected element, selects the descendant elements that match the specified selector string.

The elements in the returned selection are grouped by their corresponding parent node in this selection. If no element matches the specified selector for the current element, or if the selector is null, the group at the current index will be empty. The selected elements do not inherit data from this selection; use selection.data to propagate data to children.

If the selector is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). It must return an array of elements (or an iterable, or a pseudo-array such as a NodeList), or the empty array if there are no matching elements. For example, to select the previous and next siblings of each paragraph:

Unlike selection.select, selection.selectAll does affect grouping: each selected descendant is grouped by the parent element in the originating selection. Grouping plays an important role in the data join. See Nested Selections and How Selections Work for more on this topic.

Source · Filters the selection, returning a new selection that contains only the elements for which the specified filter is true. For example, to filter a selection of table rows to contain only even rows:

This is approximately equivalent to using d3.selectAll directly, although the indexes may be different:

The filter may be specified either as a selector string or a function. If the filter is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). Using a function:

Or using selection.select (and avoiding an arrow function, since this is needed to refer to the current element):

Note that the :nth-child pseudo-class is a one-based index rather than a zero-based index. Also, the above filter functions do not have precisely the same meaning as :nth-child; they rely on the selection index rather than the number of preceding sibling elements in the DOM.

The returned filtered selection preserves the parents of this selection, but like array.filter, it does not preserve indexes as some elements may be removed; use selection.select to preserve the index, if needed.

Source · Returns a new selection with the (first) child of each element of the current selection matching the selector.

If no selector is specified, selects the first child (if any). If the selector is specified as a string, selects the first child that matches (if any). If the selector is a function, it is evaluated for each of the children nodes, in order, being passed the child (child), the child’s index (i), and the list of children (children); the method selects the first child for which the selector return truthy, if any.

selection.selectChild propagates the parent’s data to the selected child.

Source · Returns a new selection with the children of each element of the current selection matching the selector. If no selector is specified, selects all the children. If the selector is specified as a string, selects the children that match (if any). If the selector is a function, it is evaluated for each of the children nodes, in order, being passed the child (child), the child’s index (i), and the list of children (children); the method selects all children for which the selector return truthy.

Source · Returns the selection (for symmetry with transition.selection).

Source · Given the specified selector, returns a function which returns true if this element matches the specified selector. This method is used internally by selection.filter. For example, this:

(Although D3 is not a compatibility layer, this implementation does support vendor-prefixed implementations due to the recent standardization of element.matches.)

Source · Given the specified selector, returns a function which returns the first descendant of this element that matches the specified selector. This method is used internally by selection.select. For example, this:

Source · Given the specified selector, returns a function which returns all descendants of this element that match the specified selector. This method is used internally by selection.selectAll. For example, this:

Source · Returns the owner window for the specified node. If node is a node, returns the owner document’s default view; if node is a document, returns its default view; otherwise returns the node.

Source · Returns the value of the style property with the specified name for the specified node. If the node has an inline style with the specified name, its value is returned; otherwise, the computed property value is returned. See also selection.style.

**Examples:**

Example 1 (csharp):
```csharp
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

Example 2 (javascript):
```javascript
const root = d3.selection();
```

Example 3 (kotlin):
```kotlin
d3.selection.prototype.checked = function(value) {
  return arguments.length < 1
      ? this.property("checked")
      : this.property("checked", !!value);
};
```

Example 4 (sass):
```sass
d3.selectAll("input[type=checkbox]").checked(true);
```

---

## Joining data | D3 by Observable

**URL:** https://d3js.org/d3-selection/joining

**Contents:**
- Joining data ​
- selection.data(data, key) ​
- selection.join(enter, update, exit) ​
- selection.enter() ​
- selection.exit() ​
- selection.datum(value) ​
- selection.merge(other) ​

For an introduction, see Thinking With Joins and the selection.join notebook.

Source · Binds the specified array of data with the selected elements, returning a new selection that represents the update selection: the elements successfully bound to data. Also defines the enter and exit selections on the returned selection, which can be used to add or remove elements to correspond to the new data. The specified data is an array of arbitrary values (e.g., numbers or objects), or a function that returns an array of values for each group. When data is assigned to an element, it is stored in the property __data__, thus making the data “sticky” and available on re-selection.

The data is specified for each group in the selection. If the selection has multiple groups (such as d3.selectAll followed by selection.selectAll), then data should typically be specified as a function. This function will be evaluated for each group in order, being passed the group’s parent datum (d, which may be undefined), the group index (i), and the selection’s parent nodes (nodes), with this as the group’s parent element.

In conjunction with selection.join (or more explicitly with selection.enter, selection.exit, selection.append and selection.remove), selection.data can be used to enter, update and exit elements to match data. For example, to create an HTML table from a matrix of numbers:

In this example the data function is the identity function: for each table row, it returns the corresponding row from the data matrix.

If a key function is not specified, then the first datum in data is assigned to the first selected element, the second datum to the second selected element, and so on. A key function may be specified to control which datum is assigned to which element, replacing the default join-by-index, by computing a string identifier for each datum and element. This key function is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]); the returned string is the element’s key. The key function is then also evaluated for each new datum in data, being passed the current datum (d), the current index (i), and the group’s new data, with this as the group’s parent DOM element; the returned string is the datum’s key. The datum for a given key is assigned to the element with the matching key. If multiple elements have the same key, the duplicate elements are put into the exit selection; if multiple data have the same key, the duplicate data are put into the enter selection.

For example, given this document:

You could join data by key as follows:

This example key function uses the datum d if present, and otherwise falls back to the element’s id property. Since these elements were not previously bound to data, the datum d is null when the key function is evaluated on selected elements, and non-null when the key function is evaluated on the new data.

The update and enter selections are returned in data order, while the exit selection preserves the selection order prior to the join. If a key function is specified, the order of elements in the selection may not match their order in the document; use selection.order or selection.sort as needed. For more on how the key function affects the join, see A Bar Chart, Part 2 and Object Constancy.

If data is not specified, this method returns the array of data for the selected elements.

This method cannot be used to clear bound data; use selection.datum instead.

Source · Appends, removes and reorders elements as necessary to match the data that was previously bound by selection.data, returning the merged enter and update selection. This method is a convenient alternative to the explicit general update pattern, replacing selection.enter, selection.exit, selection.append, selection.remove, and selection.order. For example:

The enter function may be specified as a string shorthand, as above, which is equivalent to selection.append with the given element name. Likewise, optional update and exit functions may be specified, which default to the identity function and calling selection.remove, respectively. The shorthand above is thus equivalent to:

By passing separate functions on enter, update and exit, you have greater control over what happens. And by specifying a key function to selection.data, you can minimize changes to the DOM to optimize performance. For example, to set different fill colors for enter and update:

The selections returned by the enter and update functions are merged and then returned by selection.join.

You can animate enter, update and exit by creating transitions inside the enter, update and exit functions. If the enter and update functions return transitions, their underlying selections are merged and then returned by selection.join. The return value of the exit function is not used.

For more, see the selection.join notebook.

Source · Returns the enter selection: placeholder nodes for each datum that had no corresponding DOM element in the selection. (The enter selection is empty for selections not returned by selection.data.)

The enter selection is typically used to create “missing” elements corresponding to new data. For example, to create DIV elements from an array of numbers:

If the body is initially empty, the above code will create six new DIV elements, append them to the body in-order, and assign their text content as the associated (string-coerced) number:

Conceptually, the enter selection’s placeholders are pointers to the parent element (in this example, the document body). The enter selection is typically only used transiently to append elements, and is often merged with the update selection after appending, such that modifications can be applied to both entering and updating elements.

Source · Returns the exit selection: existing DOM elements in the selection for which no new datum was found. (The exit selection is empty for selections not returned by selection.data.)

The exit selection is typically used to remove “superfluous” elements corresponding to old data. For example, to update the DIV elements created previously with a new array of numbers:

Since a key function was specified (as the identity function), and the new data contains the numbers [4, 8, 16] which match existing elements in the document, the update selection contains three DIV elements. Leaving those elements as-is, we can append new elements for [1, 2, 32] using the enter selection:

Likewise, to remove the exiting elements [15, 23, 42]:

Now the document body looks like this:

The order of the DOM elements matches the order of the data because the old data’s order and the new data’s order were consistent. If the new data’s order is different, use selection.order to reorder the elements in the DOM. See the general update pattern notebook for more on data joins.

Source · Gets or sets the bound data for each selected element. Unlike selection.data, this method does not compute a join and does not affect indexes or the enter and exit selections.

If a value is specified, sets the element’s bound data to the specified value on all selected elements. If the value is a constant, all elements are given the same datum; otherwise, if the value is a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). The function is then used to set each element’s new data. A null value will delete the bound data.

If a value is not specified, returns the bound datum for the first (non-null) element in the selection. This is generally useful only if you know the selection contains exactly one element.

This method is useful for accessing HTML5 custom data attributes. For example, given the following elements:

You can expose the custom data attributes by setting each element’s data as the built-in dataset property:

Source · Returns a new selection merging this selection with the specified other selection or transition. The returned selection has the same number of groups and the same parents as this selection. Any missing (null) elements in this selection are filled with the corresponding element, if present (not null), from the specified selection. (If the other selection has additional groups or parents, they are ignored.)

This method is used internally by selection.join to merge the enter and update selections after binding data. You can also merge explicitly, although note that since merging is based on element index, you should use operations that preserve index, such as selection.select instead of selection.filter. For example:

See selection.data for more.

This method is not intended for concatenating arbitrary selections, however: if both this selection and the specified other selection have (non-null) elements at the same index, this selection’s element is returned in the merge and the other selection’s element is ignored.

**Examples:**

Example 1 (javascript):
```javascript
const matrix = [
  [11975,  5871, 8916, 2868],
  [ 1951, 10048, 2060, 6171],
  [ 8010, 16145, 8090, 8045],
  [ 1013,   990,  940, 6907]
];

d3.select("body")
  .append("table")
  .selectAll("tr")
  .data(matrix)
  .join("tr")
  .selectAll("td")
  .data(d => d)
  .join("td")
    .text(d => d);
```

Example 2 (jsx):
```jsx
<div id="Ford"></div>
<div id="Jarrah"></div>
<div id="Kwon"></div>
<div id="Locke"></div>
<div id="Reyes"></div>
<div id="Shephard"></div>
```

Example 3 (json):
```json
const data = [
  {name: "Locke", number: 4},
  {name: "Reyes", number: 8},
  {name: "Ford", number: 15},
  {name: "Jarrah", number: 16},
  {name: "Shephard", number: 23},
  {name: "Kwon", number: 42}
];

d3.selectAll("div")
  .data(data, function(d) { return d ? d.name : this.id; })
    .text(d => d.number);
```

Example 4 (rust):
```rust
svg.selectAll("circle")
  .data(data)
  .join("circle")
    .attr("fill", "none")
    .attr("stroke", "black");
```

---

## Control flow | D3 by Observable

**URL:** https://d3js.org/d3-selection/control-flow

**Contents:**
- Control flow ​
- selection.each(function) ​
- selection.call(function, ...arguments) ​
- selection.empty() ​
- selection.nodes() ​
- selection[Symbol.iterator]() ​
- selection.node() ​
- selection.size() ​

For advanced usage, selections provide methods for custom control flow.

Source · Invokes the specified function for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element (nodes[i]). This method can be used to invoke arbitrary code for each selected element, and is useful for creating a context to access parent and child data simultaneously, such as:

See sized donut multiples for an example.

Source · Invokes the specified function exactly once, passing in this selection along with any optional arguments. Returns this selection. This is equivalent to invoking the function by hand but facilitates method chaining. For example, to set several styles in a reusable function:

This is roughly equivalent to:

The only difference is that selection.call always returns the selection and not the return value of the called function, name.

Source · Returns true if this selection contains no (non-null) elements.

Source · Returns an array of all (non-null) elements in this selection.

Source · Returns an iterator over the selected (non-null) elements. For example, to iterate over the selected elements:

To flatten the selection to an array:

Source · Returns the first (non-null) element in this selection. If the selection is empty, returns null.

Source · Returns the total number of (non-null) elements in this selection.

**Examples:**

Example 1 (swift):
```swift
parent.each(function(p, j) {
  d3.select(this)
    .selectAll(".child")
      .text(d => `child ${d.name} of ${p.name}`);
});
```

Example 2 (javascript):
```javascript
function name(selection, first, last) {
  selection
      .attr("first-name", first)
      .attr("last-name", last);
}
```

Example 3 (unknown):
```unknown
d3.selectAll("div").call(name, "John", "Snow");
```

Example 4 (unknown):
```unknown
name(d3.selectAll("div"), "John", "Snow");
```

---
