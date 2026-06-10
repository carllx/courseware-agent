> Source: [https://d3js.org/d3-ease](https://d3js.org/d3-ease)

<script setup>

import * as d3 from "d3";
import {ref} from "vue";
import ExampleEase from "./components/ExampleEase.vue";

const amplitude = ref(1);
const exponent = ref(2);
const period = ref(0.3);
const overshoot = ref(1.7);

</script>

# d3-ease

[Examples](https://observablehq.com/@d3/easing) · *Easing* is a method of distorting time to control apparent motion in animation. It is most commonly used for [slow-in, slow-out](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation#Slow_in_and_slow_out). By easing time, [animated transitions](./d3-transition.md) are smoother and exhibit more plausible motion.

The easing types in this module implement the [ease method](#_ease) which takes a normalized time *t* and returns the corresponding “eased” time *tʹ*. Both the normalized time and the eased time are typically in the range [0,1], where 0 represents the start of the animation and 1 represents the end; some easing types, such as [easeElastic](#easeElastic), may return eased times slightly outside this range. A good easing type should return 0 if *t* = 0 and 1 if *t* = 1.

These easing types are largely based on work by [Robert Penner](http://robertpenner.com/easing/).

## *ease*(*t*) {#_ease}

Given the specified normalized time *t*, typically in the range [0,1], returns the “eased” time *tʹ*, also typically in [0,1]. 0 represents the start of the animation and 1 represents the end. A good implementation returns 0 if *t* = 0 and 1 if *t* = 1. For example, to apply [easeCubic](#easeCubic) easing:

```js
const te = d3.easeCubic(t);
```

To apply custom [elastic](#easeElastic) easing, create your easing function before the animation starts:

```js
const ease = d3.easeElastic.period(0.4);
```

Then during the animation, apply the easing function:

```js
const te = ease(t);
```

See also [*transition*.ease](./d3-transition/timing.md#transition_ease).

## easeLinear {#easeLinear}

<ExampleEase :eases='[{y: d3.easeLinear}]' />

[Source](https://github.com/d3/d3-ease/blob/main/src/linear.js) · Linear easing; the identity function; *linear*(*t*) returns *t*.

## easePoly {#easePoly}

[Source](https://github.com/d3/d3-ease/blob/main/src/poly.js) · Alias for [easePolyInOut](#easePolyInOut).

### easePolyIn {#easePolyIn}

<ExampleEase label="exponent" :eases='[0.5, 1, 1.5, 2, 3, 4].map((e) => ({y: d3.easePolyIn.exponent(e), stroke: e}))' />

Polynomial easing; raises *t* to the specified [exponent](#easePoly_exponent). If the exponent is not specified, it defaults to 3, equivalent to [easeCubicIn](#easeCubicIn).

### easePolyOut {#easePolyOut}

<ExampleEase label="exponent" :eases='[0.5, 1, 1.5, 2, 3, 4].map((e) => ({y: d3.easePolyOut.exponent(e), stroke: e}))' />

Reverse polynomial easing; equivale

