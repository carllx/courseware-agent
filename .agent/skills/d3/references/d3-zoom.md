## d3-zoom | D3 by Observable

**URL:** https://d3js.org/d3-zoom

**Contents:**
- d3-zoom ​
- zoom() ​
- zoom(selection) ​
- zoom.transform(selection, transform, point) ​
- zoom.translateBy(selection, x, y) ​
- zoom.translateTo(selection, x, y, p) ​
- zoom.scaleBy(selection, k, p) ​
- zoom.scaleTo(selection, k, p) ​
- zoom.constrain(constrain) ​
- zoom.filter(filter) ​

Examples · Panning and zooming let the user focus on a region of interest by restricting the view. It uses direct manipulation: click-and-drag to pan (translate), spin the wheel to zoom (scale), or pinch with touch. Panning and zooming are widely used in web-based mapping, but can also be used in visualization such as dense time series and scatterplots.

The zoom behavior is a flexible abstraction, handling a surprising variety of input modalities and browser quirks. The zoom behavior is agnostic about the DOM, so you can use it with HTML, SVG, or Canvas. You can use d3-zoom with d3-scale and d3-axis to zoom axes. You can restrict zooming using zoom.scaleExtent and panning using zoom.translateExtent. You can combine d3-zoom with other behaviors such as d3-drag for dragging and d3-brush for focus + context.

The zoom behavior can be controlled programmatically using zoom.transform, allowing you to implement user interface controls which drive the display or to stage animated tours through your data. Smooth zoom transitions are based on “Smooth and efficient zooming and panning” by Jarke J. van Wijk and Wim A.A. Nuij.

See also d3-tile for examples panning and zooming maps.

Source · Creates a new zoom behavior. The returned behavior, zoom, is both an object and a function, and is typically applied to selected elements via selection.call.

Source · Applies this zoom behavior to the specified selection, binding the necessary event listeners to allow panning and zooming, and initializing the zoom transform on each selected element to the identity transform if not already defined.

This function is typically not invoked directly, and is instead invoked via selection.call. For example, to instantiate a zoom behavior and apply it to a selection:

Internally, the zoom behavior uses selection.on to bind the necessary event listeners for zooming. The listeners use the name .zoom, so you can subsequently unbind the zoom behavior as follows:

To disable just wheel-driven zooming (say to not interfere with native scrolling), you can remove the zoom behavior’s wheel event listener after applying the zoom behavior to the selection:

Alternatively, use zoom.filter for greater control over which events can initiate zoom gestures.

Applying the zoom behavior also sets the -webkit-tap-highlight-color style to transparent, disabling the tap highlight on iOS. If you want a different tap highlight color, remove or re-apply this style after applying the drag behavior.

The zoom behavior stores the zoom state on the element to which the zoom behavior was applied, not on the zoom behavior itself. This allows the zoom behavior to be applied to many elements simultaneously with independent zooming. The zoom state can change either on user interaction or programmatically via zoom.transform.

To retrieve the zoom state, use event.transform on the current zoom event within a zoom event listener (see zoom.on), or use zoomTransform for a given node. The latter is useful for modifying the zoom state programmatically, say to implement buttons for zooming in and out.

Source · If selection is a selection, sets the current zoom transform of the selected elements to the specified transform, instantaneously emitting start, zoom and end events.

If selection is a transition, defines a “zoom” tween to the specified transform using interpolateZoom, emitting a start event when the transition starts, zoom events for each tick of the transition, and then an end event when the transition ends (or is interrupted). The transition will attempt to minimize the visual movement around the specified point; if the point is not specified, it defaults to the center of the viewport extent.

The transform may be specified either as a zoom transform or as a function that returns a zoom transform; similarly, the point may be specified either as a two-element array [x, y] or a function that returns such an array. If a function, it is invoked for each selected element, being passed the current event (event) and datum d, with the this context as the current DOM element.

This function is typically not invoked directly, and is instead invoked via selection.call or transition.call. For example, to reset the zoom transform to the identity transform instantaneously:

To smoothly reset the zoom transform to the identity transform over 750 milliseconds:

This method requires that you specify the new zoom transform completely, and does not enforce the defined scale extent and translate extent, if any. To derive a new transform from the existing transform, and to enforce the scale and translate extents, see the convenience methods zoom.translateBy, zoom.scaleBy and zoom.scaleTo.

Source · If selection is a selection, translates the current zoom transform of the selected elements by x and y, such that the new tx1 = tx0 + kx and ty1 = ty0 + ky. If selection is a transition, defines a “zoom” tween translating the current transform. This method is a convenience method for zoom.transform. The x and y translation amounts may be specified either as numbers or as functions that return numbers. If a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element.

Source · If selection is a selection, translates the current zoom transform of the selected elements such that the given position ⟨x,y⟩ appears at given point p. The new tx = px - kx and ty = py - ky. If p is not specified, it defaults to the center of the viewport extent. If selection is a transition, defines a “zoom” tween translating the current transform. This method is a convenience method for zoom.transform. The x and y coordinates may be specified either as numbers or as functions that returns numbers; similarly the p point may be specified either as a two-element array [px,py] or a function. If a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element.

Source · If selection is a selection, scales the current zoom transform of the selected elements by k, such that the new k₁ = k₀k. The reference point p does move. If p is not specified, it defaults to the center of the viewport extent. If selection is a transition, defines a “zoom” tween translating the current transform. This method is a convenience method for zoom.transform. The k scale factor may be specified either as a number or a function that returns a number; similarly the p point may be specified either as a two-element array [px,py] or a function. If a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element.

Source · If selection is a selection, scales the current zoom transform of the selected elements to k, such that the new k₁ = k. The reference point p does move. If p is not specified, it defaults to the center of the viewport extent. If selection is a transition, defines a “zoom” tween translating the current transform. This method is a convenience method for zoom.transform. The k scale factor may be specified either as a number or a function that returns a number; similarly the p point may be specified either as a two-element array [px,py] or a function. If a function, it is invoked for each selected element, being passed the current datum d and index i, with the this context as the current DOM element.

Source · If constrain is specified, sets the transform constraint function to the specified function and returns the zoom behavior. If constrain is not specified, returns the current constraint function, which defaults to:

The constraint function must return a [transform]#zoomTransform) given the current transform, viewport extent and translate extent. The default implementation attempts to ensure that the viewport extent does not go outside the translate extent.

Source · If filter is specified, sets the filter to the specified function and returns the zoom behavior. If filter is not specified, returns the current filter, which defaults to:

The filter is passed the current event (event) and datum d, with the this context as the current DOM element. If the filter returns falsey, the initiating event is ignored and no zoom gestures are started. Thus, the filter determines which input events are ignored. The default filter ignores mousedown events on secondary buttons, since those buttons are typically intended for other purposes, such as the context menu.

Source · If touchable is specified, sets the touch support detector to the specified function and returns the zoom behavior. If touchable is not specified, returns the current touch support detector, which defaults to:

Touch event listeners are only registered if the detector returns truthy for the corresponding element when the zoom behavior is applied. The default detector works well for most browsers that are capable of touch input, but not all; Chrome’s mobile device emulator, for example, fails detection.

Source · If delta is specified, sets the wheel delta function to the specified function and returns the zoom behavior. If delta is not specified, returns the current wheel delta function, which defaults to:

The value Δ returned by the wheel delta function determines the amount of scaling applied in response to a WheelEvent. The scale factor transform.k is multiplied by 2Δ; for example, a Δ of +1 doubles the scale factor, Δ of -1 halves the scale factor.

Source · If extent is specified, sets the viewport extent to the specified array of points [[x0, y0], [x1, y1]], where [x0, y0] is the top-left corner of the viewport and [x1, y1] is the bottom-right corner of the viewport, and returns this zoom behavior. The extent may also be specified as a function which returns such an array; if a function, it is invoked for each selected element, being passed the current datum d, with the this context as the current DOM element.

If extent is not specified, returns the current extent accessor, which defaults to [[0, 0], [width, height]] where width is the client width of the element and height is its client height; for SVG elements, the nearest ancestor SVG element’s viewBox, or width and height attributes, are used. Alternatively, consider using element.getBoundingClientRect.

The viewport extent affects several functions: the center of the viewport remains fixed during changes by zoom.scaleBy and zoom.scaleTo; the viewport center and dimensions affect the path chosen by interpolateZoom; and the viewport extent is needed to enforce the optional translate extent.

Source · If extent is specified, sets the scale extent to the specified array of numbers [k0, k1] where k0 is the minimum allowed scale factor and k1 is the maximum allowed scale factor, and returns this zoom behavior. If extent is not specified, returns the current scale extent, which defaults to [0, ∞]. The scale extent restricts zooming in and out. It is enforced on interaction and when using zoom.scaleBy, zoom.scaleTo and zoom.translateBy; however, it is not enforced when using zoom.transform to set the transform explicitly.

If the user tries to zoom by wheeling when already at the corresponding limit of the scale extent, the wheel events will be ignored and not initiate a zoom gesture. This allows the user to scroll down past a zoomable area after zooming in, or to scroll up after zooming out. If you would prefer to always prevent scrolling on wheel input regardless of the scale extent, register a wheel event listener to prevent the browser default behavior:

Source · If extent is specified, sets the translate extent to the specified array of points [[x0, y0], [x1, y1]], where [x0, y0] is the top-left corner of the world and [x1, y1] is the bottom-right corner of the world, and returns this zoom behavior. If extent is not specified, returns the current translate extent, which defaults to [[-∞, -∞], [+∞, +∞]]. The translate extent restricts panning, and may cause translation on zoom out. It is enforced on interaction and when using zoom.scaleBy, zoom.scaleTo and zoom.translateBy; however, it is not enforced when using zoom.transform to set the transform explicitly.

Source · If distance is specified, sets the maximum distance that the mouse can move between mousedown and mouseup that will trigger a subsequent click event. If at any point between mousedown and mouseup the mouse is greater than or equal to distance from its position on mousedown, the click event following mouseup will be suppressed. If distance is not specified, returns the current distance threshold, which defaults to zero. The distance threshold is measured in client coordinates (event.clientX and event.clientY).

Source · If distance is specified, sets the maximum distance that a double-tap gesture can move between first touchstart and second touchend that will trigger a subsequent double-click event. If distance is not specified, returns the current distance threshold, which defaults to 10. The distance threshold is measured in client coordinates (event.clientX and event.clientY).

Source · If duration is specified, sets the duration for zoom transitions on double-click and double-tap to the specified number of milliseconds and returns the zoom behavior. If duration is not specified, returns the current duration, which defaults to 250 milliseconds. If the duration is not greater than zero, double-click and -tap trigger instantaneous changes to the zoom transform rather than initiating smooth transitions.

To disable double-click and double-tap transitions, you can remove the zoom behavior’s dblclick event listener after applying the zoom behavior to the selection:

Source · If interpolate is specified, sets the interpolation factory for zoom transitions to the specified function. If interpolate is not specified, returns the current interpolation factory, which defaults to interpolateZoom to implement smooth zooming. To apply direct interpolation between two views, try interpolate instead.

Source · If listener is specified, sets the event listener for the specified typenames and returns the zoom behavior. If an event listener was already registered for the same type and name, the existing listener is removed before the new listener is added. If listener is null, removes the current event listeners for the specified typenames, if any. If listener is not specified, returns the first currently-assigned listener matching the specified typenames, if any. When a specified event is dispatched, each listener will be invoked with the same context and arguments as selection.on listeners: the current event (event) and datum d, with the this context as the current DOM element.

The typenames is a string containing one or more typename separated by whitespace. Each typename is a type, optionally followed by a period (.) and a name, such as zoom.foo and zoom.bar; the name allows multiple listeners to be registered for the same type. The type must be one of the following:

See dispatch.on for more.

When a zoom event listener is invoked, it receives the current zoom event as a first argument. The event object exposes several fields:

The zoom behavior handles a variety of interaction events:

The propagation of all consumed events is immediately stopped.

¹ Necessary to capture events outside an iframe; see d3-drag#9. ² Only applies during an active, mouse-based gesture; see d3-drag#9. ³ Only applies immediately after some mouse-based gestures; see zoom.clickDistance. ⁴ Necessary to allow click emulation on touch input; see d3-drag#9. ⁵ Ignored if within 500ms of a touch gesture ending; assumes click emulation. ⁶ Double-click and double-tap initiate a transition that emits start, zoom and end events; see zoom.tapDistance. ⁷ The first wheel event emits a start event; an end event is emitted when no wheel events are received for 150ms. ⁸ Ignored if already at the corresponding limit of the scale extent.

Source · Returns the current transform for the specified node. Note that node should typically be a DOM element, not a selection. (A selection may consist of multiple nodes, in different states, and this function only returns a single transform.) If you have a selection, call selection.node first:

In the context of an event listener, the node is typically the element that received the input event (which should be equal to event.transform), this:

Internally, an element’s transform is stored as element.__zoom; however, you should use this method rather than accessing it directly. If the given node has no defined transform, returns the transform of the closest ancestor, or if none exists, the identity transformation. The returned transform represents a two-dimensional transformation matrix of the form:

(This matrix is capable of representing only scale and translation; a future release may also allow rotation, though this would probably not be a backwards-compatible change.) The position ⟨x,y⟩ is transformed to ⟨xk + tx,yk + ty⟩. The transform object exposes the following properties:

These properties should be considered read-only; instead of mutating a transform, use transform.scale and transform.translate to derive a new transform. Also see zoom.scaleBy, zoom.scaleTo and zoom.translateBy for convenience methods on the zoom behavior. To create a transform with a given k, tx, and ty:

To apply the transformation to a Canvas 2D context, use context.translate followed by context.scale:

Similarly, to apply the transformation to HTML elements via CSS:

To apply the transformation to SVG:

Or more simply, taking advantage of transform.toString:

Note that the order of transformations matters! The translate must be applied before the scale.

Source · The identity transform, where k = 1, tx = ty = 0.

Source · Returns a transform with scale k and translation (x, y).

Source · Returns a transform whose scale k₁ is equal to k₀k, where k₀ is this transform’s scale.

Source · Returns a transform whose translation tx1 and ty1 is equal to tx0 + tk x and ty0 + tk y, where tx0 and ty0 is this transform’s translation and tk is this transform’s scale.

Source · Returns the transformation of the specified point which is a two-element array of numbers [x, y]. The returned point is equal to [xk + tx, yk + ty].

Source · Returns the transformation of the specified x-coordinate, xk + tx.

Source · Returns the transformation of the specified y coordinate, yk + ty.

Source · Returns the inverse transformation of the specified point which is a two-element array of numbers [x, y]. The returned point is equal to [(x - tx) / k, (y - ty) / k].

Source · Returns the inverse transformation of the specified x-coordinate, (x - tx) / k.

Source · Returns the inverse transformation of the specified y coordinate, (y - ty) / k.

Source · Returns a copy of the continuous scale x whose domain is transformed. This is implemented by first applying the inverse x-transform on the scale’s range, and then applying the inverse scale to compute the corresponding domain:

The scale x must use interpolateNumber; do not use continuous.rangeRound as this reduces the accuracy of continuous.invert and can lead to an inaccurate rescaled domain. This method does not modify the input scale x; x thus represents the untransformed scale, while the returned scale represents its transformed view.

Source · Returns a copy of the continuous scale y whose domain is transformed. This is implemented by first applying the inverse y-transform on the scale’s range, and then applying the inverse scale to compute the corresponding domain:

The scale y must use interpolateNumber; do not use continuous.rangeRound as this reduces the accuracy of continuous.invert and can lead to an inaccurate rescaled domain. This method does not modify the input scale y; y thus represents the untransformed scale, while the returned scale represents its transformed view.

Source · Returns a string representing the SVG transform corresponding to this transform. Implemented as:

**Examples:**

Example 1 (unknown):
```unknown
selection.call(d3.zoom().on("zoom", zoomed));
```

Example 2 (unknown):
```unknown
selection.on(".zoom", null);
```

Example 3 (unknown):
```unknown
selection
    .call(zoom)
    .on("wheel.zoom", null);
```

Example 4 (csharp):
```csharp
selection.call(zoom.transform, d3.zoomIdentity);
```
