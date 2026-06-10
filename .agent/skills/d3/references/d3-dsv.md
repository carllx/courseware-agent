> Source: [https://d3js.org/d3-dsv](https://d3js.org/d3-dsv)

# d3-dsv

This module provides a parser and formatter for delimiter-separated values, most commonly [comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values) (CSV) or tab-separated values (TSV). These tabular formats are popular with spreadsheet programs such as Microsoft Excel, and are often more space-efficient than JSON. This implementation is based on [RFC 4180](http://tools.ietf.org/html/rfc4180).

For example, to parse:

```js
d3.csvParse("foo,bar\n1,2") // [{foo: "1", bar: "2"}, columns: ["foo", "bar"]]
```
```js
d3.tsvParse("foo\tbar\n1\t2") // [{foo: "1", bar: "2"}, columns: ["foo", "bar"]]
```

To format:

```js
d3.csvFormat([{foo: "1", bar: "2"}]) // "foo,bar\n1,2"
```
```js
d3.tsvFormat([{foo: "1", bar: "2"}]) // "foo\tbar\n1\t2"
```

To use a different delimiter, such as “|” for pipe-separated values, use [d3.dsvFormat](#dsvFormat):

```js
d3.dsvFormat("|").parse("foo|bar\n1|2")) // [{foo: "1", bar: "2"}, columns: ["foo", "bar"]]
```

For easy loading of DSV files in a browser, see [d3-fetch](./d3-fetch.md)’s [d3.csv](./d3-fetch.md#csv), [d3.tsv](./d3-fetch.md#tsv) and [d3.dsv](./d3-fetch.md#dsv) methods.

## dsvFormat(*delimiter*) {#dsvFormat}

```js
const csv = d3.dsvFormat(",");
```

[Source](https://github.com/d3/d3-dsv/blob/main/src/dsv.js) · Constructs a new DSV parser and formatter for the specified *delimiter*. The *delimiter* must be a single character (*i.e.*, a single 16-bit code unit); so, ASCII delimiters are fine, but emoji delimiters are not.

## *dsv*.parse(*string*, *row*) {#dsv_parse}

:::warning CAUTION
This method requires the unsafe-eval [content security policy](#content-security-policy).
:::

```js
d3.csvParse("foo,bar\n1,2") // [{foo: "1", bar: "2"}, columns: ["foo", "bar"]]
```

[Source](https://github.com/d3/d3-dsv/blob/main/src/dsv.js) · Parses the specified *string*, which must be in the delimiter-separated values format with the appropriate delimiter, returning an array of objects representing the parsed rows.

Unlike [*dsv*.parseRows](#dsv_parseRows), this method requires that the first line of the DSV content contains a delimiter-separated list of column names; these column names become the attributes on the returned objects. For example, consider the following CSV file:

```
Year,Make,Model,Length
1997,Ford,E350,2.34
2000,Mercury,Cougar,2.38
```

The resulting JavaScript array is:

```js
[
  {"Year": "1997", "Make": "Ford", "Model": "E350", "Length": "2.34"},
  {"Year": "2000", "Make": "Mercury", "Model": "Cougar", "Length": "2.38"}
]
```

The returned array also exposes a `columns` property containing the column names in input order (in contrast to Object.keys, whose iteration order is arbitrary). For example:

```js
data.columns // ["Year", "Make", "Model", "Length"]
```

If the column names are not unique, only the last value is returned for each name; to access all values, use [*dsv*.parseRows](#dsv_parseRows) instead (see [example](https://observablehq.com/@d3/parse-csv-with-duplicate-column-names)).

If a *row* conversion function is not specified, field values are strings. For safety, there is no automatic conversion to numbers, dates, or other types. In some cases, JavaScript may coerce strings to numbers for you automatically (for example, using the `+` operator), but better is to specify a *row* conversion function. See [d3.autoType](#autoType) for a convenient *row* conversion function that infers and coerces common types like numbers and strings.

If a *row* conversion function is specified, the specified function is invoked for each row, being passed an object representing the current row (`d`), the index (`i`) starting at zero for the first non-header row, and the array of column names. If the returned value is null or undefined, the row is skipped and will be omitted from the array returned by *dsv*.parse; otherwise, the returned value defines the corresponding row object. For example:

```js
const data = d3.csvParse(string, (d) => {
  return {
    year: new Date(+d.Year, 0, 1), // lowercase and convert "Year" to Date
    make: d.Make, // lowercase
    model: d.Model, // lowercase
    length: +d.Length // lowercase and convert "Length" to number
  };
});
```

Note: using `+` or `Number` rather than [parseInt](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/parseInt) or [parseFloat](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/parseFloat) is typically faster, though more restrictive. For example, `"30px"` when coerced using `+` returns `NaN`, while parseInt and parseFloat return `30`.

## *dsv*.parseRows(*string*, *row*) {#dsv_parseRow

