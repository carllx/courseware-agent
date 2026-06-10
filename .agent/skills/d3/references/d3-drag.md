## d3-drag | D3 by Observable

**URL:** https://d3js.org/d3-drag

**Contents:**
- d3-drag ​
- drag() ​
- drag(selection) ​
- drag.container(container) ​
- drag.filter(filter) ​
- drag.touchable(touchable) ​
- drag.subject(subject) ​
- drag.clickDistance(distance) ​
- drag.on(typenames, listener) ​
- dragDisable(window) ​

Examples · Drag-and-drop is a popular interaction method for manipulating spatial elements: move the pointer to an object, press and hold to grab it, “drag” the object to a new location, and release to “drop”. D3’s drag behavior provides a flexible abstraction for drag-and-drop. For example, you can drag nodes in a force-directed graph:

Or a simulation of colliding circles:

The drag behavior isn’t just for moving elements around; there are a variety of ways to respond to a drag gesture. For example, you can use it to lasso elements in a scatterplot, or to paint lines on a canvas:

The drag behavior can be combined with other behaviors, such as d3-zoom for zooming:

The drag behavior is agnostic about the DOM, so you can use it with SVG, HTML or even Canvas! And you can extend it with advanced selection techniques, such as a Voronoi overlay or a closest-target search:

The drag behavior unifies mouse and touch input and avoids browser quirks. In the future the drag behavior will support Pointer Events, too.

Source · Creates a new drag behavior. The returned behavior, drag, is both an object and a function, and is typically applied to selected elements via selection.call.

Source · Applies this drag behavior to the specified selection. This function is typically not invoked directly, and is instead invoked via selection.call. For example, to instantiate a drag behavior and apply it to a selection:

Internally, the drag behavior uses selection.on to bind the necessary event listeners for dragging. The listeners use the name .drag, so you can subsequently unbind the drag behavior as follows:

Applying the drag behavior also sets the -webkit-tap-highlight-color style to transparent, disabling the tap highlight on iOS. If you want a different tap highlight color, remove or re-apply this style after applying the drag behavior.

Source · If container is specified, sets the container accessor to the specified object or function and returns the drag behavior. If container is not specified, returns the current container accessor, which defaults to:

The container of a drag gesture determines the coordinate system of subsequent drag events, affecting event.x and event.y. The element returned by the container accessor is subsequently passed to pointer to determine the local coordinates of the pointer.

The default container accessor returns the parent node of the element in the originating selection (see drag) that received the initiating input event. This is often appropriate when dragging SVG or HTML elements, since those elements are typically positioned relative to a parent. For dragging graphical elements with a Canvas, however, you may want to redefine the container as the initiating element itself:

Alternatively, the container may be specified as the element directly, such as drag.container(canvas).

Source · If filter is specified, sets the event filter to the specified function and returns the drag behavior. If filter is not specified, returns the current filter, which defaults to:

If the filter returns falsey, the initiating event is ignored and no drag gestures are started. Thus, the filter determines which input events are ignored; the default filter ignores mousedown events on secondary buttons, since those buttons are typically intended for other purposes, such as the context menu.

Source · If touchable is specified, sets the touch support detector to the specified function and returns the drag behavior. If touchable is not specified, returns the current touch support detector, which defaults to:

Touch event listeners are only registered if the detector returns truthy for the corresponding element when the drag behavior is applied. The default detector works well for most browsers that are capable of touch input, but not all; Chrome’s mobile device emulator, for example, fails detection.

Source · If subject is specified, sets the subject accessor to the specified object or function and returns the drag behavior. If subject is not specified, returns the current subject accessor, which defaults to:

The subject of a drag gesture represents the thing being dragged. It is computed when an initiating input event is received, such as a mousedown or touchstart, immediately before the drag gesture starts. The subject is then exposed as event.subject on subsequent drag events for this gesture.

The default subject is the datum of the element in the originating selection (see drag) that received the initiating input event; if this datum is undefined, an object representing the coordinates of the pointer is created. When dragging circle elements in SVG, the default subject is thus the datum of the circle being dragged. With Canvas, the default subject is the canvas element’s datum (regardless of where on the canvas you click). In this case, a custom subject accessor would be more appropriate, such as one that picks the closest circle to the mouse within a given search radius:

If necessary, the above can be accelerated using quadtree.find, simulation.find or delaunay.find.

The returned subject should be an object that exposes x and y properties, so that the relative position of the subject and the pointer can be preserved during the drag gesture. If the subject is null or undefined, no drag gesture is started for this pointer; however, other starting touches may yet start drag gestures. See also drag.filter.

The subject of a drag gesture may not be changed after the gesture starts. The subject accessor is invoked with the same context and arguments as selection.on listeners: the current event (event) and datum d, with the this context as the current DOM element. During the evaluation of the subject accessor, event is a beforestart drag event. Use event.sourceEvent to access the initiating input event and event.identifier to access the touch identifier. The event.x and event.y are relative to the container, and are computed using pointer.

Source · If distance is specified, sets the maximum distance that the mouse can move between mousedown and mouseup that will trigger a subsequent click event. If at any point between mousedown and mouseup the mouse is greater than or equal to distance from its position on mousedown, the click event following mouseup will be suppressed. If distance is not specified, returns the current distance threshold, which defaults to zero. The distance threshold is measured in client coordinates (event.clientX and event.clientY).

Source · If listener is specified, sets the event listener for the specified typenames and returns the drag behavior. If an event listener was already registered for the same type and name, the existing listener is removed before the new listener is added. If listener is null, removes the current event listeners for the specified typenames, if any. If listener is not specified, returns the first currently-assigned listener matching the specified typenames, if any. When a specified event is dispatched, each listener will be invoked with the same context and arguments as selection.on listeners: the current event (event) and datum d, with the this context as the current DOM element.

The typenames is a string containing one or more typename separated by whitespace. Each typename is a type, optionally followed by a period (.) and a name, such as drag.foo and drag.bar; the name allows multiple listeners to be registered for the same type. The type must be one of the following:

See dispatch.on for more.

Changes to registered listeners via drag.on during a drag gesture do not affect the current drag gesture. Instead, you must use event.on, which also allows you to register temporary event listeners for the current drag gesture. Separate events are dispatched for each active pointer during a drag gesture. For example, if simultaneously dragging multiple subjects with multiple fingers, a start event is dispatched for each finger, even if both fingers start touching simultaneously. See Drag Events for more.

Source · Prevents native drag-and-drop and text selection on the specified window. As an alternative to preventing the default action of mousedown events (see #9), this method prevents undesirable default actions following mousedown. In supported browsers, this means capturing dragstart and selectstart events, preventing the associated default actions, and immediately stopping their propagation. In browsers that do not support selection events, the user-select CSS property is set to none on the document element. This method is intended to be called on mousedown, followed by dragEnable on mouseup.

Source · Allows native drag-and-drop and text selection on the specified window; undoes the effect of dragDisable. This method is intended to be called on mouseup, preceded by dragDisable on mousedown. If noclick is true, this method also temporarily suppresses click events. The suppression of click events expires after a zero-millisecond timeout, such that it only suppress the click event that would immediately follow the current mouseup event, if any.

When a drag event listener is invoked, it receives the current drag event as its first argument. The event object exposes several fields:

The event.active field is useful for detecting the first start event and the last end event in a sequence of concurrent drag gestures: it is zero when the first drag gesture starts, and zero when the last drag gesture ends.

The event object also exposes the event.on method.

This table describes how the drag behavior interprets native events:

The propagation of all consumed events is immediately stopped. If you want to prevent some events from initiating a drag gesture, use drag.filter.

¹ Necessary to capture events outside an iframe; see #9. ² Only applies during an active, mouse-based gesture; see #9. ³ Only applies immediately after some mouse-based gestures; see drag.clickDistance. ⁴ Necessary to allow click emulation on touch input; see #9. ⁵ Ignored if within 500ms of a touch gesture ending; assumes click emulation.

Source · Equivalent to drag.on, but only applies to the current drag gesture. Before the drag gesture starts, a copy of the current drag event listeners is made. This copy is bound to the current drag gesture and modified by event.on. This is useful for temporary listeners that only receive events for the current drag gesture. For example, this start event listener registers temporary drag and end event listeners as closures:

**Examples:**

Example 1 (javascript):
```javascript
const drag = d3.drag();
```

Example 2 (unknown):
```unknown
d3.selectAll(".node").call(d3.drag().on("start", started));
```

Example 3 (unknown):
```unknown
selection.on(".drag", null);
```

Example 4 (javascript):
```javascript
function container() {
  return this.parentNode;
}
```
