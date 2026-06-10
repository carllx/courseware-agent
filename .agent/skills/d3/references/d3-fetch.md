## d3-fetch | D3 by Observable

**URL:** https://d3js.org/d3-fetch

**Contents:**
- d3-fetch ​
- blob(input, init) ​
- buffer(input, init) ​
- csv(input, init, row) ​
- dsv(delimiter, input, init, row) ​
- html(input, init) ​
- image(input, init) ​
- json(input, init) ​
- svg(input, init) ​
- text(input, init) ​

This module provides convenient parsing on top of Fetch. For example, to load a text file:

To load and parse a CSV file:

This module has built-in support for parsing JSON, CSV, and TSV. You can parse additional formats by using text directly. (This module replaced d3-request.)

Source · Fetches the binary file at the specified input URL as a Blob. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

Source · Fetches the binary file at the specified input URL as an ArrayBuffer. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

Source · Equivalent to d3.dsv with the comma character as the delimiter.

Source · Fetches the DSV file at the specified input URL. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields. An optional row conversion function may be specified to map and filter row objects to a more-specific representation; see dsv.parse for details. For example:

If only one of init and row is specified, it is interpreted as the row conversion function if it is a function, and otherwise an init object. See also d3.csv and d3.tsv.

Source · Fetches the file at the specified input URL as text and then parses it as HTML. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

Source · Fetches the image at the specified input URL. If init is specified, sets any additional properties on the image before loading. For example, to enable an anonymous cross-origin request:

Source · Fetches the JSON file at the specified input URL. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields. If the server returns a status code of 204 No Content or 205 Reset Content, the promise resolves to undefined.

Source · Fetches the file at the specified input URL as text and then parses it as SVG. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

Source · Fetches the text file at the specified input URL. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

Source · Equivalent to d3.dsv with the tab character as the delimiter.

Source · Fetches the file at the specified input URL as text and then parses it as XML. If init is specified, it is passed along to the underlying call to fetch; see RequestInit for allowed fields.

**Examples:**

Example 1 (swift):
```swift
const text = await d3.text("hello-world.txt"); // "Hello, world!"
```

Example 2 (json):
```json
const data = await d3.csv("hello-world.csv"); // [{"Hello": "world"}, …]
```

Example 3 (javascript):
```javascript
const blob = await d3.blob("example.db");
```

Example 4 (javascript):
```javascript
const buffer = await d3.buffer("example.db");
```
