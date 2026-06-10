# D3 - Scale Chromatic

## Sequential schemes | D3 by Observable

**URL:** https://d3js.org/d3-scale-chromatic/sequential

**Contents:**
- Sequential schemes ​
- interpolateBlues(t) ​
- interpolateGreens(t) ​
- interpolateGreys(t) ​
- interpolateOranges(t) ​
- interpolatePurples(t) ​
- interpolateReds(t) ​
- interpolateTurbo(t) ​
- interpolateViridis(t) ​
- interpolateInferno(t) ​

Sequential color schemes are available as continuous interpolators (often used with d3.scaleSequential) and as discrete schemes (often used with d3.scaleOrdinal).

Each discrete scheme, such as d3.schemeBlues, is represented as an array of arrays of hexadecimal color strings. The kth element of this array contains the color scheme of size k; for example, d3.schemeBlues[9] contains an array of nine strings representing the nine colors of the blue sequential color scheme. Sequential color schemes support a size k ranging from 3 to 9.

To create a sequential discrete nine-color scale using the Blues color scheme:

To create a sequential continuous color scale using the Blues color scheme:

Source · Given a number t in the range [0,1], returns the corresponding color from the “Blues” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Greens” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Greys” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Oranges” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Purples” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Reds” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “turbo” color scheme by Anton Mikhailov.

Source · Given a number t in the range [0,1], returns the corresponding color from the “viridis” perceptually-uniform color scheme designed by van der Walt, Smith and Firing for matplotlib, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “inferno” perceptually-uniform color scheme designed by van der Walt and Smith for matplotlib, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “magma” perceptually-uniform color scheme designed by van der Walt and Smith for matplotlib, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “plasma” perceptually-uniform color scheme designed by van der Walt and Smith for matplotlib, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “cividis” color vision deficiency-optimized color scheme designed by Nuñez, Anderton, and Renslow, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from a 180° rotation of Niccoli’s perceptual rainbow, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from Niccoli’s perceptual rainbow, represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from Green’s default Cubehelix represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “BuGn” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “BuPu” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “GnBu” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “OrRd” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PuBuGn” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PuBu” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PuRd” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “RdPu” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “YlGnBu” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “YlGn” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “YlOrBr” sequential color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “YlOrRd” sequential color scheme represented as an RGB string.

Source · The “Blues” discrete sequential color scheme of size k in 3–9.

Source · The “Greens” discrete sequential color scheme of size k in 3–9.

Source · The “Greys” discrete sequential color scheme of size k in 3–9.

Source · The “Oranges” discrete sequential color scheme of size k in 3–9.

Source · The “Purples” discrete sequential color scheme of size k in 3–9.

Source · The “Reds” discrete sequential color scheme of size k in 3–9.

Source · The “BuGn” discrete sequential color scheme of size k in 3–9.

Source · The “BuPu” discrete sequential color scheme of size k in 3–9.

Source · The “GnBu” discrete sequential color scheme of size k in 3–9.

Source · The “OrRd” discrete sequential color scheme of size k in 3–9.

Source · The “PuBuGn” discrete sequential color scheme of size k in 3–9.

Source · The “PuBu” discrete sequential color scheme of size k in 3–9.

Source · The “PuRd” discrete sequential color scheme of size k in 3–9.

Source · The “RdPu” discrete sequential color scheme of size k in 3–9.

Source · The “YlGnBu” discrete sequential color scheme of size k in 3–9.

Source · The “YlGn” discrete sequential color scheme of size k in 3–9.

Source · The “YlOrBr” discrete sequential color scheme of size k in 3–9.

Source · The “YlOrRd” discrete sequential color scheme of size k in 3–9.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleOrdinal(d3.schemeBlues[9]);
```

Example 2 (javascript):
```javascript
const color = d3.scaleSequential(d3.interpolateBlues);
```

---

## Categorical schemes | D3 by Observable

**URL:** https://d3js.org/d3-scale-chromatic/categorical

**Contents:**
- Categorical schemes ​
- schemeCategory10 ​
- schemeAccent ​
- schemeDark2 ​
- schemeObservable10 ​
- schemePaired ​
- schemePastel1 ​
- schemePastel2 ​
- schemeSet1 ​
- schemeSet2 ​

For example, to create a categorical color scale using the Accent color scheme:

Source · An array of ten categorical colors represented as RGB hexadecimal strings.

Source · An array of eight categorical colors represented as RGB hexadecimal strings.

Source · An array of eight categorical colors represented as RGB hexadecimal strings.

Source · An array of ten categorical colors represented as RGB hexadecimal strings.

Source · An array of twelve categorical colors represented as RGB hexadecimal strings.

Source · An array of nine categorical colors represented as RGB hexadecimal strings.

Source · An array of eight categorical colors represented as RGB hexadecimal strings.

Source · An array of nine categorical colors represented as RGB hexadecimal strings.

Source · An array of eight categorical colors represented as RGB hexadecimal strings.

Source · An array of twelve categorical colors represented as RGB hexadecimal strings.

Source · An array of ten categorical colors authored by Tableau as part of Tableau 10 represented as RGB hexadecimal strings.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleOrdinal(d3.schemeAccent);
```

---

## Cyclical schemes | D3 by Observable

**URL:** https://d3js.org/d3-scale-chromatic/cyclical

**Contents:**
- Cyclical schemes ​
- interpolateRainbow(t) ​
- interpolateSinebow(t) ​

To create a cyclical continuous color scale using the Rainbow color scheme:

Source · Given a number t in the range [0,1], returns the corresponding color from d3.interpolateWarm scale from [0.0, 0.5] followed by the d3.interpolateCool scale from [0.5, 1.0], thus implementing the cyclical less-angry rainbow color scheme.

Source · Given a number t in the range [0,1], returns the corresponding color from the “sinebow” color scheme by Jim Bumgardner and Charlie Loyd.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleSequential(d3.interpolateRainbow);
```

---

## d3-scale-chromatic | D3 by Observable

**URL:** https://d3js.org/d3-scale-chromatic

**Contents:**
- d3-scale-chromatic ​

This module provides sequential, diverging and categorical color schemes designed to work with d3-scale’s d3.scaleOrdinal and d3.scaleSequential. Most of these schemes are derived from Cynthia A. Brewer’s ColorBrewer. Since ColorBrewer publishes only discrete color schemes, the sequential and diverging scales are interpolated using uniform B-splines.

---

## Diverging schemes | D3 by Observable

**URL:** https://d3js.org/d3-scale-chromatic/diverging

**Contents:**
- Diverging schemes ​
- interpolateBrBG(t) ​
- interpolatePRGn(t) ​
- interpolatePiYG(t) ​
- interpolatePuOr(t) ​
- interpolateRdBu(t) ​
- interpolateRdGy(t) ​
- interpolateRdYlBu(t) ​
- interpolateRdYlGn(t) ​
- interpolateSpectral(t) ​

Diverging color schemes are available as continuous interpolators (often used with d3.scaleSequential) and as discrete schemes (often used with d3.scaleOrdinal).

Each discrete scheme, such as d3.schemeBrBG, is represented as an array of arrays of hexadecimal color strings. The kth element of this array contains the color scheme of size k; for example, d3.schemeBrBG[9] contains an array of nine strings representing the nine colors of the brown-blue-green diverging color scheme. Diverging color schemes support a size k ranging from 3 to 11.

To create a diverging continuous color scale using the PiYG color scheme:

To create a diverging discrete nine-color scale using the PiYG color scheme:

Source · Given a number t in the range [0,1], returns the corresponding color from the “BrBG” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PRGn” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PiYG” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “PuOr” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “RdBu” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “RdGy” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “RdYlBu” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “RdYlGn” diverging color scheme represented as an RGB string.

Source · Given a number t in the range [0,1], returns the corresponding color from the “Spectral” diverging color scheme represented as an RGB string.

Source · The “BrBG” discrete diverging color scheme of size k in 3–11.

Source · The “PRGn” discrete diverging color scheme of size k in 3–11.

Source · The “PiYG” discrete diverging color scheme of size k in 3–11.

Source · The “PuOr” discrete diverging color scheme of size k in 3–11.

Source · The “RdBu” discrete diverging color scheme of size k in 3–11.

Source · The “RdGy” discrete diverging color scheme of size k in 3–11.

Source · The “RdYlBu” discrete diverging color scheme of size k in 3–11.

Source · The “RdYlGn” discrete diverging color scheme of size k in 3–11.

Source · The “Spectral” discrete diverging color scheme of size k in 3–11.

**Examples:**

Example 1 (javascript):
```javascript
const color = d3.scaleSequential(d3.interpolatePiYG);
```

Example 2 (javascript):
```javascript
const color = d3.scaleOrdinal(d3.schemePiYG[9]);
```

---
