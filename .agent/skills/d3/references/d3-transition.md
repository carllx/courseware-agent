## Selecting elements | D3 by Observable

**URL:** https://d3js.org/d3-transition/selecting

**Contents:**
- Selecting elements ​
- selection.transition(name) ​
- transition(name) ​
- transition.select(selector) ​
- transition.selectAll(selector) ​
- transition.selectChild(selector) ​
- transition.selectChildren(selector) ​
- transition.filter(filter) ​
- transition.merge(other) ​
- transition.transition() ​

Transitions are derived from selections via selection.transition. You can also create a transition on the document root element using d3.transition.

Source · Returns a new transition on the given selection with the specified name. If a name is not specified, null is used. The new transition is only exclusive with other transitions of the same name.

If the name is a transition instance, the returned transition has the same id and name as the specified transition. If a transition with the same id already exists on a selected element, the existing transition is returned for that element. Otherwise, the timing of the returned transition is inherited from the existing transition of the same id on the nearest ancestor of each selected element. Thus, this method can be used to synchronize a transition across multiple selections, or to re-select a transition for specific elements and modify its configuration. For example:

If the specified transition is not found on a selected node or its ancestors (such as if the transition already ended), the default timing parameters are used; however, in a future release, this will likely be changed to throw an error. See #59.

Source · Returns a new transition on the root element, document.documentElement, with the specified name. If a name is not specified, null is used. The new transition is only exclusive with other transitions of the same name. The name may also be a transition instance; see selection.transition. This method is equivalent to:

This function can also be used to test for transitions (instanceof d3.transition) or to extend the transition prototype.

Source · For each selected element, selects the first descendant element that matches the specified selector string, if any, and returns a transition on the resulting selection. The selector may be specified either as a selector string or a function. If a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element. The new transition has the same id, name and timing as this transition; however, if a transition with the same id already exists on a selected element, the existing transition is returned for that element.

This method is equivalent to deriving the selection for this transition via transition.selection, creating a subselection via selection.select, and then creating a new transition via selection.transition:

Source · For each selected element, selects all descendant elements that match the specified selector string, if any, and returns a transition on the resulting selection. The selector may be specified either as a selector string or a function. If a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element. The new transition has the same id, name and timing as this transition; however, if a transition with the same id already exists on a selected element, the existing transition is returned for that element.

This method is equivalent to deriving the selection for this transition via transition.selection, creating a subselection via selection.selectAll, and then creating a new transition via selection.transition:

Source · For each selected element, selects the first child element that matches the specified selector string, if any, and returns a transition on the resulting selection. The selector may be specified either as a selector string or a function. If a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element. The new transition has the same id, name and timing as this transition; however, if a transition with the same id already exists on a selected element, the existing transition is returned for that element.

This method is equivalent to deriving the selection for this transition via transition.selection, creating a subselection via selection.selectChild, and then creating a new transition via selection.transition:

Source · For each selected element, selects all children that match the specified selector string, if any, and returns a transition on the resulting selection. The selector may be specified either as a selector string or a function. If a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element. The new transition has the same id, name and timing as this transition; however, if a transition with the same id already exists on a selected element, the existing transition is returned for that element.

This method is equivalent to deriving the selection for this transition via transition.selection, creating a subselection via selection.selectChildren, and then creating a new transition via selection.transition:

Source · For each selected element, selects only the elements that match the specified filter, and returns a transition on the resulting selection. The filter may be specified either as a selector string or a function. If a function, it is evaluated for each selected element, in order, being passed the current datum (d), the current index (i), and the current group (nodes), with this as the current DOM element. The new transition has the same id, name and timing as this transition; however, if a transition with the same id already exists on a selected element, the existing transition is returned for that element.

This method is equivalent to deriving the selection for this transition via transition.selection, creating a subselection via selection.filter, and then creating a new transition via selection.transition:

Source · Returns a new transition merging this transition with the specified other transition, which must have the same id as this transition. The returned transition has the same number of groups, the same parents, the same name and the same id as this transition. Any missing (null) elements in this transition are filled with the corresponding element, if present (not null), from the other transition.

This method is equivalent to deriving the selection for this transition via transition.selection, merging with the selection likewise derived from the other transition via selection.merge, and then creating a new transition via selection.transition:

Source · Returns a new transition on the same selected elements as this transition, scheduled to start when this transition ends. The new transition inherits a reference time equal to this transition’s time plus its delay and duration. The new transition also inherits this transition’s name, duration, and easing. This method can be used to schedule a sequence of chained transitions. For example:

The delay for each transition is relative to its previous transition. Thus, in the above example, apples will stay red for one second before the last transition to brown starts.

Source · Returns the selection corresponding to this transition.

Examples · Source · Returns the active transition on the specified node with the specified name, if any. If no name is specified, null is used. Returns null if there is no such active transition on the specified node. This method is useful for creating chained transitions. For example, to initiate disco mode:

**Examples:**

Example 1 (swift):
```swift
const t = d3.transition()
    .duration(750)
    .ease(d3.easeLinear);

d3.selectAll(".apple").transition(t)
    .style("fill", "red");

d3.selectAll(".orange").transition(t)
    .style("fill", "orange");
```

Example 2 (swift):
```swift
d3.selection()
  .transition(name)
```

Example 3 (swift):
```swift
transition
  .selection()
  .select(selector)
  .transition(transition)
```

Example 4 (swift):
```swift
transition
  .selection()
  .selectAll(selector)
  .transition(transition)
```

---

## d3-transition | D3 by Observable

**URL:** https://d3js.org/d3-transition

**Contents:**
- d3-transition ​

A transition is a selection-like interface for animating changes to the DOM. Instead of applying changes instantaneously, transitions smoothly interpolate the DOM from its current state to the desired target state over a given duration.

To apply a transition, select elements, call selection.transition, and then make the desired changes. For example:

Transitions support most selection methods (such as transition.attr and transition.style in place of selection.attr and selection.style), but not all methods are supported; for example, you must append elements or bind data before a transition starts. A transition.remove operator is provided for convenient removal of elements when the transition ends.

To compute intermediate state, transitions leverage a variety of built-in interpolators. Colors, numbers, and transforms are automatically detected. Strings with embedded numbers are also detected, as is common with many styles (such as padding or font sizes) and paths. To specify a custom interpolator, use transition.attrTween, transition.styleTween or transition.tween.

**Examples:**

Example 1 (swift):
```swift
d3.select("body")
  .transition()
    .style("background-color", "red");
```

---

## d3-timer | D3 by Observable

**URL:** https://d3js.org/d3-timer

**Contents:**
- d3-timer ​
- now() ​
- timer(callback, delay, time) ​
- timer.restart(callback, delay, time) ​
- timer.stop() ​
- timerFlush() ​
- timeout(callback, delay, time) ​
- interval(callback, delay, time) ​

This module provides an efficient queue capable of managing thousands of concurrent animations, while guaranteeing consistent, synchronized timing with concurrent or staged animations. Internally, it uses requestAnimationFrame for fluid animation (if available), switching to setTimeout for delays longer than 24ms.

Source · Returns the current time as defined by performance.now if available, and Date.now if not.

The current time is updated at the start of a frame; it is thus consistent during the frame, and any timers scheduled during the same frame will be synchronized. If this method is called outside of a frame, such as in response to a user event, the current time is calculated and then fixed until the next frame, again ensuring consistent timing during event handling.

Source · Schedules a new timer, invoking the specified callback repeatedly until the timer is stopped. An optional numeric delay in milliseconds may be specified to invoke the given callback after a delay; if delay is not specified, it defaults to zero. The delay is relative to the specified time in milliseconds; if time is not specified, it defaults to now.

The callback is passed the (apparent) elapsed time since the timer became active. For example:

This produces roughly the following console output:

(The exact values may vary depending on your JavaScript runtime and what else your computer is doing.) Note that the first elapsed time is 3ms: this is the elapsed time since the timer started, not since the timer was scheduled. Here the timer started 150ms after it was scheduled due to the specified delay. The apparent elapsed time may be less than the true elapsed time if the page is backgrounded and requestAnimationFrame is paused; in the background, apparent time is frozen.

If timer is called within the callback of another timer, the new timer callback (if eligible as determined by the specified delay and time) will be invoked immediately at the end of the current frame, rather than waiting until the next frame. Within a frame, timer callbacks are guaranteed to be invoked in the order they were scheduled, regardless of their start time.

Source · Restart a timer with the specified callback and optional delay and time. This is equivalent to stopping this timer and creating a new timer with the specified arguments, although this timer retains the original invocation priority.

Source · Stops this timer, preventing subsequent callbacks. This method has no effect if the timer has already stopped.

Source · Immediately invoke any eligible timer callbacks. Note that zero-delay timers are normally first executed after one frame (~17ms). This can cause a brief flicker because the browser renders the page twice: once at the end of the first event loop, then again immediately on the first timer callback. By flushing the timer queue at the end of the first event loop, you can run any zero-delay timers immediately and avoid the flicker.

Source · Like timer, except the timer automatically stops on its first callback. A suitable replacement for setTimeout that is guaranteed to not run in the background. The callback is passed the elapsed time.

Source · Like timer, except the callback is invoked only every delay milliseconds; if delay is not specified, this is equivalent to timer. A suitable replacement for setInterval that is guaranteed to not run in the background. The callback is passed the elapsed time.

**Examples:**

Example 1 (unknown):
```unknown
d3.now() // 1236.3000000715256
```

Example 2 (javascript):
```javascript
const t = d3.timer((elapsed) => {
  console.log(elapsed);
  if (elapsed > 200) t.stop();
}, 150);
```

Example 3 (unknown):
```unknown
3
25
48
65
85
106
125
146
167
189
209
```

---

## d3-ease | D3 by Observable

**URL:** https://d3js.org/d3-ease

**Contents:**
- d3-ease ​
- ease(t) ​
- easeLinear ​
- easePoly ​
  - easePolyIn ​
  - easePolyOut ​
  - easePolyInOut ​
  - easePoly.exponent(e) ​
- easeQuad ​
  - easeQuadIn ​

Examples · Easing is a method of distorting time to control apparent motion in animation. It is most commonly used for slow-in, slow-out. By easing time, animated transitions are smoother and exhibit more plausible motion.

The easing types in this module implement the ease method which takes a normalized time t and returns the corresponding “eased” time tʹ. Both the normalized time and the eased time are typically in the range [0,1], where 0 represents the start of the animation and 1 represents the end; some easing types, such as easeElastic, may return eased times slightly outside this range. A good easing type should return 0 if t = 0 and 1 if t = 1.

These easing types are largely based on work by Robert Penner.

Given the specified normalized time t, typically in the range [0,1], returns the “eased” time tʹ, also typically in [0,1]. 0 represents the start of the animation and 1 represents the end. A good implementation returns 0 if t = 0 and 1 if t = 1. For example, to apply easeCubic easing:

To apply custom elastic easing, create your easing function before the animation starts:

Then during the animation, apply the easing function:

See also transition.ease.

Source · Linear easing; the identity function; linear(t) returns t.

Source · Alias for easePolyInOut.

Polynomial easing; raises t to the specified exponent. If the exponent is not specified, it defaults to 3, equivalent to easeCubicIn.

Reverse polynomial easing; equivalent to 1 - easePolyIn(1 - t). If the exponent is not specified, it defaults to 3, equivalent to easeCubicOut.

Symmetric polynomial easing; scales easePolyIn for t in 0–0.5 and easePolyOut for t in 0.5–1. If the exponent is not specified, it defaults to 3, equivalent to easeCubic.

Returns a new polynomial easing with the specified exponent e. For example, to create equivalents of easeLinear, easeQuad, and easeCubic:

Source · Alias for easeQuadInOut.

Quadratic easing; equivalent to easePolyIn.exponent(2).

Reverse quadratic easing; equivalent to 1 - easeQuadIn(1 - t). Also equivalent to easePolyOut.exponent(2).

Symmetric quadratic easing; scales easeQuadIn for t in 0–0.5 and easeQuadOut for t in 0.5–1. Also equivalent to easePoly.exponent(2).

Source · Alias for easeCubicInOut.

Cubic easing; equivalent to easePolyIn.exponent(3).

Reverse cubic easing; equivalent to 1 - easeCubicIn(1 - t). Also equivalent to easePolyOut.exponent(3).

Symmetric cubic easing; scales easeCubicIn for t in 0–0.5 and easeCubicOut for t in 0.5–1. Also equivalent to easePoly.exponent(3).

Source · Alias for easeSinInOut.

Sinusoidal easing; returns sin(t).

Reverse sinusoidal easing; equivalent to 1 - easeSinIn(1 - t).

Symmetric sinusoidal easing; scales easeSinIn for t in 0–0.5 and easeSinOut for t in 0.5–1.

Source · Alias for easeExpInOut.

Exponential easing; raises 2 to the exponent 10 × (t - 1).

Reverse exponential easing; equivalent to 1 - easeExpIn(1 - t).

Symmetric exponential easing; scales easeExpIn for t in 0–0.5 and easeExpOut for t in 0.5–1.

Source · Alias for easeCircleInOut.

Reverse circular easing; equivalent to 1 - easeCircleIn(1 - t).

Symmetric circular easing; scales easeCircleIn for t in 0–0.5 and easeCircleOut for t in 0.5–1.

Source · Alias for easeElasticOut.

Elastic easing, like a rubber band. The amplitude and period of the oscillation are configurable; if not specified, they default to 1 and 0.3, respectively.

Reverse elastic easing; equivalent to 1 - elasticIn(1 - t).

Symmetric elastic easing; scales elasticIn for t in 0–0.5 and elasticOut for t in 0.5–1.

Returns a new elastic easing with the specified amplitude a. The amplitude a must be greater than or equal to 1.

Returns a new elastic easing with the specified period p.

Source · Alias for easeBackInOut.

Anticipatory easing like a dancer bending her knees before jumping off the floor. The degree of overshoot is configurable; if not specified, it defaults to 1.70158.

Reverse anticipatory easing; equivalent to 1 - easeBackIn(1 - t).

Symmetric anticipatory easing; scales easeBackIn for t in 0–0.5 and easeBackOut for t in 0.5–1.

Returns a new back easing with the specified overshoot s.

Source · Alias for easeBounceOut.

Bounce easing, like a rubber ball.

Reverse bounce easing; equivalent to 1 - easeBounceIn(1 - t).

Symmetric bounce easing; scales easeBounceIn for t in 0–0.5 and easeBounceOut for t in 0.5–1.

**Examples:**

Example 1 (javascript):
```javascript
const te = d3.easeCubic(t);
```

Example 2 (javascript):
```javascript
const ease = d3.easeElastic.period(0.4);
```

Example 3 (javascript):
```javascript
const te = ease(t);
```

Example 4 (javascript):
```javascript
const linear = d3.easePoly.exponent(1);
const quad = d3.easePoly.exponent(2);
const cubic = d3.easePoly.exponent(3);
```

---

