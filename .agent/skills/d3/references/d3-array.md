# D3 - D3-Array

**Pages:** 12

---

## Interning values | D3 by Observable

**URL:** https://d3js.org/d3-array/intern

**Contents:**
- Interning values ​
- new InternMap(iterable, key) ​
- new InternSet(iterable, key) ​

The InternMap and InternSet classes extend the native JavaScript Map and Set classes, respectively, allowing Dates and other non-primitive keys by bypassing the SameValueZero algorithm when determining key equality. d3.group, d3.rollup and d3.index use an InternMap rather than a native Map.

Examples · Source · Constructs a new Map given the specified iterable of [key, value] entries. The keys are interned using the specified key function which defaults to object.valueOf for non-primitive values. For example, to retrieve a value keyed by a given date:

Examples · Source · Constructs a new Set given the specified iterable of values. The values are interned using the specified key function which defaults to object.valueOf for non-primitive values. For example, to query for a given date:

**Examples:**

Example 1 (json):
```json
const valueByDate = new d3.InternMap([
  [new Date("2021-01-01"), 42],
  [new Date("2022-01-01"), 12],
  [new Date("2023-01-01"), 45]
]);
```

Example 2 (unknown):
```unknown
valueByDate.get(new Date("2022-01-01")) // 12
```

Example 3 (javascript):
```javascript
const dates = new d3.InternSet([
  new Date("2021-01-01"),
  new Date("2022-01-01"),
  new Date("2023-01-01")
]);
```

Example 4 (unknown):
```unknown
dates.has(new Date("2022-01-01")) // true
```

---

## Binning data | D3 by Observable

**URL:** https://d3js.org/d3-array/bin

**Contents:**
- Binning data ​
- bin() ​
- bin(data) ​
- bin.value(value) ​
- bin.domain(domain) ​
- bin.thresholds(thresholds) ​
- thresholdFreedmanDiaconis(values, min, max) ​
- thresholdScott(values, min, max) ​
- thresholdSturges(values, min, max) ​

Bin quantitative values into consecutive, non-overlapping intervals, as in histograms. (See also Observable Plot’s bin transform.)

Examples · Source · Constructs a new bin generator with the default settings. The returned bin generator supports method chaining, so this constructor is typically chained with bin.value to assign a value accessor. The returned generator is also a function; pass it data to bin.

Bins the given iterable of data samples. Returns an array of bins, where each bin is an array containing the associated elements from the input data. Thus, the length of the bin is the number of elements in that bin. Each bin has two additional attributes:

Any null or non-comparable values in the given data, or those outside the domain, are ignored.

If value is specified, sets the value accessor to the specified function or constant and returns this bin generator.

If value is not specified, returns the current value accessor, which defaults to the identity function.

When bins are generated, the value accessor will be invoked for each element in the input data array, being passed the element d, the index i, and the array data as three arguments. The default value accessor assumes that the input data are orderable (comparable), such as numbers or dates. If your data are not, then you should specify an accessor that returns the corresponding orderable value for a given datum.

This is similar to mapping your data to values before invoking the bin generator, but has the benefit that the input data remains associated with the returned bins, thereby making it easier to access other fields of the data.

If domain is specified, sets the domain accessor to the specified function or array and returns this bin generator.

If domain is not specified, returns the current domain accessor, which defaults to extent. The bin domain is defined as an array [min, max], where min is the minimum observable value and max is the maximum observable value; both values are inclusive. Any value outside of this domain will be ignored when the bins are generated.

For example, to use a bin generator with a linear scale x, you might say:

You can then compute the bins from an array of numbers like so:

If the default extent domain is used and the thresholds are specified as a count (rather than explicit values), then the computed domain will be niced such that all bins are uniform width.

Note that the domain accessor is invoked on the materialized array of values, not on the input data array.

If thresholds is specified as a number, then the domain will be uniformly divided into approximately that many bins; see ticks.

If thresholds is specified as an array, sets the thresholds to the specified values and returns this bin generator. Thresholds are defined as an array of values [x0, x1, …]. Any value less than x0 will be placed in the first bin; any value greater than or equal to x0 but less than x1 will be placed in the second bin; and so on. Thus, the generated bins will have thresholds.length + 1 bins. Any threshold values outside the domain are ignored. The first bin.x0 is always equal to the minimum domain value, and the last bin.x1 is always equal to the maximum domain value.

If thresholds is specified as a function, the function will be passed three arguments: the array of input values derived from the data, and the domain represented as min and max. The function may then return either the array of numeric thresholds or the count of bins; in the latter case the domain is divided uniformly into approximately count bins; see ticks. For instance, you might want to use time ticks when binning time-series data; see example.

If thresholds is not specified, returns the current threshold generator, which by default implements Sturges’ formula. (Thus by default, the values to be binned must be numbers!)

Source · Returns the number of bins according to the Freedman–Diaconis rule; the input values must be numbers.

Source · Returns the number of bins according to Scott’s normal reference rule; the input values must be numbers.

Source · Returns the number of bins according to Sturges’ formula; the input values must be numbers.

**Examples:**

Example 1 (javascript):
```javascript
const bin = d3.bin().value((d) => d.culmen_length_mm);
```

Example 2 (javascript):
```javascript
const bins = d3.bin().value((d) => d.culmen_length_mm)(penguins);
```

Example 3 (javascript):
```javascript
const bin = d3.bin().value((d) => d.culmen_length_mm);
```

Example 4 (scala):
```scala
bin.value() // (d) => d.culmen_length_mm
```

---

## Sorting data | D3 by Observable

**URL:** https://d3js.org/d3-array/sort

**Contents:**
- Sorting data ​
- ascending(a, b) ​
- descending(a, b) ​
- permute(source, keys) ​
- quickselect(array, k, lo, hi, compare) ​
- reverse(iterable) ​
- shuffle(array, start, stop) ​
- shuffler(random) ​
- sort(iterable, comparator) ​

Sort values; see also bisect.

Examples · Source · Returns -1 if a is less than b, 1 if a is greater than b, 0 if a and b are equivalent, and otherwise NaN.

This is the comparator function for natural order, and can be used with array.sort to arrange elements in ascending order.

Examples · Source · Returns -1 if a is greater than b, 1 if a is less than b, 0 if a and b are equivalent, and otherwise NaN.

This is the comparator function for natural order, and can be used with array.sort to arrange elements in descending order.

Examples · Source · Returns a permutation of the specified source array or object using the specified iterable of keys. The returned array contains the corresponding property of the source object for each key in keys, in order.

The given source need not be an array; for example, given an object

three fields could be extract like so

Examples · Source · Rearranges the elements of array between lo and hi (inclusive) in-place such that array[k] is the (k - lo + 1)-th smallest value and array.slice(lo, k) are the k smallest elements, according to the given compare function, and returns the given array. If lo is not specified, it defaults to zero; if hi is not specified, it defaults to array.length - 1; if compare is not specified, it defaults to ascending.

For example, given an array of numbers:

To select the smallest 8 elements:

The rearranged numbers is

where numbers[8] is 53: greater than the preceding k elements and less than the following elements. Implemented by Volodymyr Agafonkin’s quickselect.

Source · Returns an array containing the values in the given iterable in reverse order.

Equivalent to array.reverse, except that it does not mutate the given input and works with any iterable.

Examples · Source · Randomizes the order of the specified array in-place using the Fisher–Yates shuffle and returns the array.

If start is specified, it is the starting index (inclusive) of the array to shuffle; if start is not specified, it defaults to zero. If stop is specified, it is the ending index (exclusive) of the array to shuffle; if stop is not specified, it defaults to array.length. For example, to shuffle the first ten elements of the array: shuffle(array, 0, 10).

Source · Returns a shuffle function given the specified random source.

Often used with d3.randomLcg for a deterministic shuffle.

Source · Returns an array containing the values in the given iterable in the sorted order defined by the given comparator or accessor function. If comparator is not specified, it defaults to d3.ascending.

If an accessor (a function that does not take exactly two arguments) is specified,

it is equivalent to a comparator using natural order:

The accessor is only invoked once per element, and thus the returned sorted order is consistent even if the accessor is nondeterministic. Multiple accessors may be specified to break ties.

The above is equivalent to:

Unlike array.sort, d3.sort does not mutate the given input, the comparator defaults to natural order instead of lexicographic order, and the input can be any iterable.

**Examples:**

Example 1 (json):
```json
[39, 21, 1, 104, 22].sort(d3.ascending) // [1, 21, 22, 39, 104]
```

Example 2 (json):
```json
[39, 21, 1, 104, 22].sort(d3.descending) // [104, 39, 22, 21, 1]
```

Example 3 (unknown):
```unknown
d3.permute(["a", "b", "c"], [1, 2, 0]) // returns ["b", "c", "a"]
```

Example 4 (css):
```css
const object = {yield: 27, variety: "Manchuria", year: 1931, site: "University Farm"};
```

---

## Bisecting data | D3 by Observable

**URL:** https://d3js.org/d3-array/bisect

**Contents:**
- Bisecting data ​
- bisector(accessor) ​
- bisector.right(array, x, lo, hi) ​
- bisector.left(array, x, lo, hi) ​
- bisector.center(array, x, lo, hi) ​
- bisect(array, x, lo, hi) ​
- bisectRight(array, x, lo, hi) ​
- bisectLeft(array, x, lo, hi) ​
- bisectCenter(array, x, lo, hi) ​

Bisection, or binary search, quickly finds a given value in a sorted array. It is often used to find the position at which to insert a new value into an array while maintaining sorted order.

Examples · Source · Returns a new bisector using the specified accessor function.

If the given accessor takes two arguments, it is interpreted as a comparator function for comparing an element d in the data with a search value x. Use a comparator rather than an accessor if you want values to be sorted in an order different than natural order, such as in descending rather than ascending order. The above is equivalent to:

The bisector can be used to bisect sorted arrays of objects (in contrast to bisect, which is for bisecting primitives).

Like bisectRight, but using this bisector’s accessor. The code above finds the index of the row immediately following Jan. 2, 2014 in the aapl sample dataset.

Like bisectLeft, but using this bisector’s accessor. The code above finds the index of the row for Jan. 2, 2014 in the aapl sample dataset.

Returns the index of the closest value to x in the given sorted array. This expects that the bisector’s accessor returns a quantitative value, or that the bisector’s comparator returns a signed distance; otherwise, this method is equivalent to bisector.left. The arguments lo (inclusive) and hi (exclusive) may be used to specify a subset of the array which should be considered; by default the entire array is used.

Alias for bisectRight.

Like bisectLeft, but returns an insertion point which comes after (to the right of) any existing entries equivalent to x in array. The returned insertion point i partitions the array into two halves so that all v <= x for v in array.slice(lo, i) for the left side and all v > x for v in array.slice(i, hi) for the right side. See also bisector.right.

Returns the insertion point for x in array to maintain sorted order. The arguments lo and hi may be used to specify a subset of the array which should be considered; by default the entire array is used. If x is already present in array, the insertion point will be before (to the left of) any existing entries. The return value is suitable for use as the first argument to array.splice assuming that array is already sorted. The returned insertion point i partitions the array into two halves so that all v < x for v in array.slice(lo, i) for the left side and all v >= x for v in array.slice(i, hi) for the right side. See also bisector.left.

Returns the index of the value closest to x in the given array of numbers. The arguments lo (inclusive) and hi (exclusive) may be used to specify a subset of the array which should be considered; by default the entire array is used. See also bisector.center.

**Examples:**

Example 1 (javascript):
```javascript
const bisector = d3.bisector((d) => d.Date);
```

Example 2 (javascript):
```javascript
const bisector = d3.bisector((d, x) => d.Date - x);
```

Example 3 (scala):
```scala
d3.bisector((d) => d.Date).right(aapl, new Date("2014-01-02")) // 163
```

Example 4 (scala):
```scala
d3.bisector((d) => d.Date).left(aapl, new Date("2014-01-02")) // 162
```

---

## Grouping data | D3 by Observable

**URL:** https://d3js.org/d3-array/group

**Contents:**
- Grouping data ​
- group(iterable, ...keys) ​
- groups(iterable, ...keys) ​
- rollup(iterable, reduce, ...keys) ​
- rollups(iterable, reduce, ...keys) ​
- index(iterable, ...keys) ​
- indexes(iterable, ...keys) ​
- flatGroup(iterable, ...keys) ​
- flatRollup(iterable, reduce, ...keys) ​
- groupSort(iterable, comparator, key) ​

Group discrete values.

Examples · Source · Groups the specified iterable of values into an InternMap from key to array of value. For example, to group the penguins sample dataset by species field:

To get the elements whose species field is Adelie:

If more than one key is specified, a nested InternMap is returned. For example:

To get the penguins whose species is Adelie and whose sex is FEMALE:

Elements are returned in the order of the first instance of each key.

Equivalent to group, but returns an array of [key, value] entries instead of a map. If more than one key is specified, each value will be a nested array of [key, value] entries. Elements are returned in the order of the first instance of each key.

Examples · Source · Groups and reduces the specified iterable of values into an InternMap from key to reduced value. For example, to group and count the penguins sample dataset by species field:

To get the count of penguins whose species is Adelie:

If more than one key is specified, a nested InternMap is returned. For example:

To get the count of penguins whose species is Adelie and whose sex is FEMALE:

Elements are returned in the order of the first instance of each key.

Equivalent to rollup, but returns an array of [key, value] entries instead of a map. If more than one key is specified, each value will be a nested array of [key, value] entries. Elements are returned in the order of the first instance of each key.

Uses rollup with a reducer that extracts the first element from each group, and throws an error if the group has more than one element. For example, to index the aapl same dataset by date:

You can then quickly retrieve a value by date:

Elements are returned in input order.

Like index, but returns an array of [key, value] entries instead of a map. This probably isn’t useful for anything, but is included for symmetry with groups and rollups.

Examples · Source · Equivalent to group, but returns a flat array of [key0, key1, …, values] instead of nested maps; useful for iterating over all groups.

Examples · Source · Equivalent to rollup, but returns a flat array of [key0, key1, …, value] instead of nested maps; useful for iterating over all groups.

Examples · Source · Groups the specified iterable of elements according to the specified key function, sorts the groups according to the specified comparator, and then returns an array of keys in sorted order. For example, to order the species of the penguins sample dataset by ascending median body mass:

For descending order, negate the group value:

If a comparator is passed instead of an accessor (i.e., if the second argument is a function that takes exactly two arguments), it will be asked to compare two groups a and b and should return a negative value if a should be before b, a positive value if a should be after b, or zero for a partial ordering.

**Examples:**

Example 1 (javascript):
```javascript
const species = d3.group(penguins, (d) => d.species);
```

Example 2 (unknown):
```unknown
species.get("Adelie") // Array(152)
```

Example 3 (javascript):
```javascript
const speciesSex = d3.group(penguins, (d) => d.species, (d) => d.sex)
```

Example 4 (unknown):
```unknown
speciesSex.get("Adelie").get("FEMALE") // Array(73)
```

---

## Set operations | D3 by Observable

**URL:** https://d3js.org/d3-array/sets

**Contents:**
- Set operations ​
- difference(iterable, ...others) ​
- union(...iterables) ​
- intersection(...iterables) ​
- superset(a, b) ​
- subset(a, b) ​
- disjoint(a, b) ​

Logical set operations for any iterable.

Source · Returns a new InternSet containing every value in iterable that is not in any of the others iterables.

Source · Returns a new InternSet containing every (distinct) value that appears in any of the given iterables. The order of values in the returned set is based on their first occurrence in the given iterables.

Source · Returns a new InternSet containing every (distinct) value that appears in all of the given iterables. The order of values in the returned set is based on their first occurrence in the given iterables.

Source · Returns true if a is a superset of b: if every value in the given iterable b is also in the given iterable a.

Source · Returns true if a is a subset of b: if every value in the given iterable a is also in the given iterable b.

Source · Returns true if a and b are disjoint: if a and b contain no shared value.

**Examples:**

Example 1 (unknown):
```unknown
d3.difference([0, 1, 2, 0], [1]) // Set {0, 2}
```

Example 2 (unknown):
```unknown
d3.union([0, 2, 1, 0], [1, 3]) // Set {0, 2, 1, 3}
```

Example 3 (unknown):
```unknown
d3.intersection([0, 2, 1, 0], [1, 3]) // Set {1}
```

Example 4 (unknown):
```unknown
d3.superset([0, 2, 1, 3, 0], [1, 3]) // true
```

---

## Transforming data | D3 by Observable

**URL:** https://d3js.org/d3-array/transform

**Contents:**
- Transforming data ​
- cross(...iterables, reducer) ​
- merge(iterables) ​
- pairs(iterable, reducer) ​
- transpose(matrix) ​
- zip(...arrays) ​
- filter(iterable, test) ​
- map(iterable, mapper) ​
- reduce(iterable, reducer, initialValue) ​

Transform arrays and generate new arrays.

Examples · Source · Returns the Cartesian product of the specified iterables.

If a reducer is specified, it is invoked for each combination of elements from each of the given iterables, and returns the corresponding reduced value.

Examples · Source · Merges the specified iterable of iterables into a new flat array. This method is similar to the built-in array.concat method, but is more convenient when you have an array of arrays or an iterable of iterables.

Examples · Source · Returns an array of adjacent pairs of elements from the specified iterable, in order. If the specified iterable has fewer than two elements, returns the empty array.

If a reducer function is specified, it is successively passed an element i - 1 and element i from the iterable.

Examples · Source · Uses the zip operator as a two-dimensional matrix transpose.

Examples · Source · Returns an array of arrays, where the ith array contains the ith element from each of the argument arrays. The returned array is truncated in length to the shortest array in arrays. If arrays contains only a single array, the returned array contains one-element arrays. With no arguments, the returned array is empty.

Source · Returns a new array containing the values from iterable, in order, for which the given test function returns true.

Like array.filter, but works with any iterable.

Source · Returns a new array containing the mapped values from iterable, in order, as defined by given mapper function.

Like array.map, but works with any iterable.

Source · Returns the reduced value defined by given reducer function, which is repeatedly invoked for each value in iterable, being passed the current reduced value and the next value.

Like array.reduce, but works with any iterable.

**Examples:**

Example 1 (unknown):
```unknown
d3.cross([1, 2], ["x", "y"]) // [[1, "x"], [1, "y"], [2, "x"], [2, "y"]]
```

Example 2 (scala):
```scala
d3.cross([1, 2], ["x", "y"], (a, b) => a + b) // ["1x", "1y", "2x", "2y"]
```

Example 3 (swift):
```swift
d3.merge([[1], [2, 3]]) // [1, 2, 3]
```

Example 4 (swift):
```swift
d3.merge(new Set([new Set([1]), new Set([2, 3])])) // [1, 2, 3]
```

---

## Ticks | D3 by Observable

**URL:** https://d3js.org/d3-array/ticks

**Contents:**
- Ticks ​
- ticks(start, stop, count) ​
- tickIncrement(start, stop, count) ​
- tickStep(start, stop, count) ​
- nice(start, stop, count) ​
- range(start, stop, step) ​

Generate representative values from a continuous interval.

Examples · Source · Returns an array of approximately count + 1 uniformly-spaced, nicely-rounded values between start and stop (inclusive). Each value is a power of ten multiplied by 1, 2 or 5.

Ticks are inclusive in the sense that they may include the specified start and stop values if (and only if) they are exact, nicely-rounded values consistent with the inferred step. More formally, each returned tick t satisfies start ≤ t and t ≤ stop.

Source · Like d3.tickStep, except requires that start is always less than or equal to stop, and if the tick step for the given start, stop and count would be less than one, returns the negative inverse tick step instead.

This method is always guaranteed to return an integer, and is used by d3.ticks to guarantee that the returned tick values are represented as precisely as possible in IEEE 754 floating point.

Source · Returns the difference between adjacent tick values if the same arguments were passed to d3.ticks: a nicely-rounded value that is a power of ten multiplied by 1, 2 or 5.

If stop is less than start, may return a negative tick step to indicate descending ticks.

Note that due to the limited precision of IEEE 754 floating point, the returned value may not be exact decimals; use d3-format to format numbers for human consumption.

Source · Returns a new interval [niceStart, niceStop] covering the given interval [start, stop] and where niceStart and niceStop are guaranteed to align with the corresponding tick step.

Like d3.tickIncrement, this requires that start is less than or equal to stop.

Examples · Source · Returns an array containing an arithmetic progression, similar to the Python built-in range. This method is often used to iterate over a sequence of uniformly-spaced numeric values, such as the indexes of an array or the ticks of a linear scale. (See also d3.ticks for nicely-rounded values.)

If step is omitted, it defaults to 1. If start is omitted, it defaults to 0. The stop value is exclusive; it is not included in the result. If step is positive, the last element is the largest start + i * step less than stop; if step is negative, the last element is the smallest start + i * step greater than stop.

If the returned array would contain an infinite number of values, an empty range is returned.

The arguments are not required to be integers; however, the results are more predictable if they are. The values in the returned array are defined as start + i * step, where i is an integer from zero to one minus the total number of elements in the returned array.

This behavior is due to IEEE 754 double-precision floating point, which defines 0.2 * 3 = 0.6000000000000001. Use d3-format to format numbers for human consumption with appropriate rounding; see also linear.tickFormat in d3-scale. Likewise, if the returned array should have a specific length, consider using array.map on an integer range.

**Examples:**

Example 1 (unknown):
```unknown
d3.ticks(1, 9, 5) // [2, 4, 6, 8]
```

Example 2 (unknown):
```unknown
d3.ticks(1, 9, 20) // [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9]
```

Example 3 (unknown):
```unknown
d3.tickIncrement(1, 9, 5) // 2
```

Example 4 (unknown):
```unknown
d3.tickIncrement(1, 9, 20) // -2, meaning a tick step 0.5
```

---

## Summarizing data | D3 by Observable

**URL:** https://d3js.org/d3-array/summarize

**Contents:**
- Summarizing data ​
- count(iterable, accessor) ​
- min(iterable, accessor) ​
- minIndex(iterable, accessor) ​
- max(iterable, accessor) ​
- maxIndex(iterable, accessor) ​
- least(iterable, comparator) ​
- leastIndex(iterable, comparator) ​
- greatest(iterable, comparator) ​
- greatestIndex(iterable, comparator) ​

Compute summary statistics.

Examples · Source · Returns the number of valid number values (i.e., not null, NaN, or undefined) in the specified iterable; accepts an accessor.

Examples · Source · Returns the minimum value in the given iterable using natural order.

Unlike Math.min, d3.min does not coerce the inputs to numbers; for example, the minimum of the strings ["20", "3"] is "20", while the minimum of the numbers [20, 3] is 3.

Also unlike Math.min, this method ignores undefined, null and NaN values, which is useful for ignoring missing data.

An optional accessor function may be specified, which is similar to calling Array.from before computing the minimum value. The accessor function is repeatedly passed an element from the given iterable (often d) and the zero-based index (i).

Because undefined values are ignored, you can use the accessor function to ignore values. For example, to get the frequency of the least-common letter than is not Z:

If the iterable contains no comparable values, returns undefined.

See also extent and least.

Source · Like min, but returns the index of the minimum value rather than the value itself.

This method can find the least element according to the given accessor, similar to least:

Examples · Source · Returns the maximum value in the given iterable using natural order.

Unlike Math.max, d3.max does not coerce the inputs to numbers; for example, the maximum of the strings ["20", "3"] is "3", while the maximum of the numbers [20, 3] is 20.

Also unlike Math.max, this method ignores undefined, null and NaN values, which is useful for ignoring missing data.

An optional accessor function may be specified, which is similar to calling Array.from before computing the maximum value. The accessor function is repeatedly passed an element from the given iterable (often d) and the zero-based index (i).

Because undefined values are ignored, you can use the accessor function to ignore values. For example, to get the frequency of the most-common letter than is not E:

If the iterable contains no comparable values, returns undefined.

See also extent and greatest.

Source · Like max, but returns the index of the maximum value rather than the value itself.

This method can find the greatest element according to the given accessor, similar to greatest:

See also greatestIndex.

Examples · Source · Returns the least element of the specified iterable according to the specified comparator.

If the comparator takes a single argument, is interpreted as an accessor and the returned elements are compared using natural order.

If comparator is not specified, it defaults to ascending.

If the given iterable contains no comparable elements (i.e., the comparator returns NaN when comparing each element to itself), returns undefined.

This function is similar to min, except it allows the use of a comparator rather than an accessor.

Source · Returns the index of the least element of the specified iterable according to the specified comparator or accessor. If the given iterable contains no comparable elements (i.e., the comparator returns NaN when comparing each element to itself), returns -1. If comparator is not specified, it defaults to ascending. For example:

This function is similar to minIndex, except it allows the use of a comparator rather than an accessor.

Examples · Source · Returns the greatest element of the specified iterable according to the specified comparator or accessor. If the given iterable contains no comparable elements (i.e., the comparator returns NaN when comparing each element to itself), returns undefined. If comparator is not specified, it defaults to ascending. For example:

This function is similar to max, except it allows the use of a comparator rather than an accessor.

Source · Returns the index of the greatest element of the specified iterable according to the specified comparator or accessor. If the given iterable contains no comparable elements (i.e., the comparator returns NaN when comparing each element to itself), returns -1. If comparator is not specified, it defaults to ascending. For example:

This function is similar to maxIndex, except it allows the use of a comparator rather than an accessor.

Examples · Source · Returns the minimum and maximum value in the given iterable using natural order.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the extent.

If the iterable contains no comparable values, returns [undefined, undefined].

Examples · Source · Returns the mode of the given iterable, i.e. the value which appears the most often. Ignores undefined, null and NaN values.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the mode.

In case of equality, returns the first of the relevant values. If the iterable contains no comparable values, returns undefined.

Examples · Source · Returns the sum of the given iterable of numbers. Ignores undefined, null and NaN values.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the sum.

If the iterable contains no numbers, returns 0. See also fsum.

Examples · Source · Returns the mean of the given iterable of numbers. Ignores undefined, null and NaN values.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the mean.

If the iterable contains no numbers, returns undefined.

Examples · Source · Returns the median of the given iterable of numbers using the R-7 method. Ignores undefined, null and NaN values.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the median.

If the iterable contains no numbers, returns undefined.

Source · Like median, but returns the index of the element to the left of the median.

Examples · Source · Returns the cumulative sum of the given iterable of numbers, as a Float64Array of the same length.

An optional accessor function may be specified, which is equivalent to calling Array.from before computing the cumulative sum.

This method ignores undefined and NaN values; this is useful for ignoring missing data. If the iterable contains no numbers, returns zeros. See also fcumsum.

Examples · Source · Returns the p-quantile of the given iterable of numbers, where p is a number in the range [0, 1]. For example, the median can be computed using p = 0.5, the first quartile at p = 0.25, and the third quartile at p = 0.75. This particular implementation uses the R-7 method, which is the default for the R programming language and Excel.

An optional accessor function may be specified, which is equivalent to calling array.map before computing the quantile.

Source · Similar to quantile, but returns the index to the left of p.

Examples · Source · Similar to quantile, but expects the input to be a sorted array of values. In contrast with quantile, the accessor is only called on the elements needed to compute the quantile.

Examples · Source · Returns an array with the rank of each value in the iterable, i.e. the zero-based index of the value when the iterable is sorted. Nullish values are sorted to the end and ranked NaN. An optional comparator or accessor function may be specified; the latter is equivalent to calling array.map before computing the ranks. If comparator is not specified, it defaults to ascending. Ties (equivalent values) all get the same rank, defined as the first time the value is found.

Examples · Source · Returns an unbiased estimator of the population variance of the given iterable of numbers using Welford’s algorithm. If the iterable has fewer than two numbers, returns undefined. An optional accessor function may be specified, which is equivalent to calling Array.from before computing the variance. This method ignores undefined and NaN values; this is useful for ignoring missing data.

Examples · Source · Returns the standard deviation, defined as the square root of the bias-corrected variance, of the given iterable of numbers. If the iterable has fewer than two numbers, returns undefined. An optional accessor function may be specified, which is equivalent to calling Array.from before computing the standard deviation. This method ignores undefined and NaN values; this is useful for ignoring missing data.

Source · Returns true if the given test function returns true for every value in the given iterable. This method returns as soon as test returns a non-truthy value or all values are iterated over. Equivalent to array.every:

Source · Returns true if the given test function returns true for any value in the given iterable. This method returns as soon as test returns a truthy value or all values are iterated over. Equivalent to array.some:

**Examples:**

Example 1 (scala):
```scala
d3.count(penguins, (d) => d.body_mass_g) // 342
```

Example 2 (unknown):
```unknown
d3.min([3, 2, 1, 1, 6, 2, 4]) // 1
```

Example 3 (unknown):
```unknown
d3.min(["bob", "alice", "carol"]) // "alice"
```

Example 4 (unknown):
```unknown
d3.min([new Date("2018-01-01"), new Date("2011-03-09")]) // 2011-03-09
```

---

## Adding numbers | D3 by Observable

**URL:** https://d3js.org/d3-array/add

**Contents:**
- Adding numbers ​
- new Adder() ​
- adder.add(number) ​
- adder.valueOf() ​
- fsum(values, accessor) ​
- fcumsum(values, accessor) ​

Add floating point numbers with full precision.

Examples · Source · Creates a new adder with an initial value of 0.

Adds the specified number to the adder’s current value and returns the adder.

Returns the IEEE 754 double-precision representation of the adder’s current value. Most useful as the short-hand notation +adder, or when coercing as Number(adder).

Examples · Source · Returns a full-precision summation of the given values. Although slower, d3.fsum can replace d3.sum wherever greater precision is needed.

If an accessor is specified, invokes the given function for each element in the input values, being passed the element d, the index i, and the array data as three arguments; the returned values will then be added.

Examples · Source · Returns a full-precision cumulative sum of the given values as a Float64Array. Although slower, d3.fcumsum can replace d3.cumsum when greater precision is needed.

If an accessor is specified, invokes the given function for each element in the input values, being passed the element d, the index i, and the array data as three arguments; the returned values will then be added.

**Examples:**

Example 1 (javascript):
```javascript
const adder = new d3.Adder();
```

Example 2 (unknown):
```unknown
adder.add(42)
```

Example 3 (unknown):
```unknown
adder.valueOf() // 42
```

Example 4 (unknown):
```unknown
d3.fsum([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]) // 1
```

---

## Blurring data | D3 by Observable

**URL:** https://d3js.org/d3-array/blur

**Contents:**
- Blurring data ​
- blur(data, radius) ​
- blur2({data, width, height}, rx, ry) ​
- blurImage(imageData, rx, ry) ​

A box blur implementation for 1D, 2D, and RGBA images; supports fractional radius.

Examples · Source · Blurs an array of data in-place by applying three iterations of a moving average transform (box filter) for a fast approximation of a Gaussian kernel of the given radius, a non-negative number. Returns the given data.

Examples · Source · Blurs a matrix of the given width and height in-place by applying a horizontal blur of radius rx and a vertical blur of radius ry (which defaults to rx). The matrix values data are stored in a flat (one-dimensional) array. If height is not specified, it is inferred from the given width and data.length. Returns the blurred matrix {data, width, height}.

Examples · Source · Blurs the given ImageData in-place, blurring each of the RGBA layers independently by applying an horizontal blur of radius rx and a vertical blur of radius ry (which defaults to rx). Returns the blurred ImageData.

**Examples:**

Example 1 (javascript):
```javascript
const numbers = d3.cumsum({length: 1000}, () => Math.random() - 0.5);
d3.blur(numbers, 5); // a smoothed random walk
```

Example 2 (css):
```css
const matrix = {
  width: 4,
  height: 3,
  data: [
    1, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 1
  ]
};

d3.blur2(matrix, 1);
```

Example 3 (javascript):
```javascript
const imageData = context.getImageData(0, 0, width, height);
d3.blurImage(imageData, 5);
```

---

## d3-array | D3 by Observable

**URL:** https://d3js.org/d3-array

**Contents:**
- d3-array ​

Array manipulation, ordering, searching, summarizing, etc.

---
