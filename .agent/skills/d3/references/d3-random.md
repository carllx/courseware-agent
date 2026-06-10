> Source: [https://d3js.org/d3-random](https://d3js.org/d3-random)

<script setup>

import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import PlotRender from "./components/PlotRender.js";

</script>

# d3-random

Generate random numbers from various distributions. For seeded random number generation, see [*random*.source](#random_source) and [randomLcg](#randomLcg).

## randomUniform(*min*, *max*) {#randomUniform}

<PlotRender :options='{
  height: 120,
  nice: true,
  marks: [
    Plot.dotX(Array.from({length: 1000}, d3.randomUniform.source(d3.randomLcg(42))(6)), Plot.dodgeY({r: 2, fill: "currentColor"}))
  ]
}' />

```js
d3.randomUniform(6) // generate numbers ≥0 and <6
```

[Examples](https://observablehq.com/@d3/d3-random#uniform) · [Source](https://github.com/d3/d3-random/blob/main/src/uniform.js) · Returns a function for generating random numbers with a [uniform distribution](https://en.wikipedia.org/wiki/Uniform_distribution_\(continuous\)). The minimum allowed value of a returned number is *min* (inclusive), and the maximum is *max* (exclusive). If *min* is not specified, it defaults to 0; if *max* is not specified, it defaults to 1. For example:

## randomInt(*min*, *max*) {#randomInt}

<PlotRender :options='{
  height: 120,
  nice: true,
  marks: [
    Plot.dotX(Array.from({length: 1000}, d3.randomInt.source(d3.randomLcg(42))(100)), Plot.dodgeY({r: 2, fill: "currentColor"}))
  ]
}' />

```js
d3.randomInt(100) // generate integers ≥0 and <100
```

[Examples](https://observablehq.com/@d3/d3-random#int) · [Source](https://github.com/d3/d3-random/blob/main/src/int.js) · Returns a function for generating random integers with a [uniform distribution](https://en.wikipedia.org/wiki/Uniform_distribution_\(continuous\)). The minimum allowed value of a returned number is ⌊*min*⌋ (inclusive), and the maximum is ⌊*max* - 1⌋ (inclusive). If *min* is not specified, it defaults to 0. For example:

## randomNormal(*mu*, *sigma*) {#randomNormal}

<PlotRender defer :options='{
  height: 240,
  nice: true,
  marks: [
    Plot.dotX(Array.from({length: 1000}, d3.randomNormal.source(d3.randomLcg(42))(0, 1)), Plot.dodgeY({r: 2, fill: "currentColor"}))
  ]
}' />

```js
d3.randomNormal(0, 1) // mean of 0, and standard deviation of 1
```

[Examples](https://observablehq.com/@d3/d3-random#normal) · [Source](https://github.com/d3/d3-random/blob/main/src/normal.js) · Returns a function for generating random numbers with a [normal (Gaussian) distribution](https://en.wikipedia.org/wiki/Normal_distribution). The expected value of the generated numbers is *mu*, with the given standard deviation *sigma*. If *mu* is not specified, it defaults to 0; if *sigma* is not specified, it defaults to 1.

## randomLogNormal(*mu*, *sigma*) {#randomLogNormal}

<PlotRender defer :options='{
  height: 240,
  nice: true,
  marks: [
    Plot.dotX(Array.from({length: 400}, d3.randomLogNormal.source(d3.randomLcg(36))(0, 1)), Plot.dodgeY({r: 2, fill: "currentColor"}))
  ]
}' />

`

