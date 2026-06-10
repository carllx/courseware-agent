> Source: [https://d3js.org/d3-time-format](https://d3js.org/d3-time-format)

# d3-time-format

This module provides an approximate JavaScript implementation of the venerable [strptime](http://pubs.opengroup.org/onlinepubs/009695399/functions/strptime.html) and [strftime](http://pubs.opengroup.org/onlinepubs/007908799/xsh/strftime.html) functions from the C standard library, and can be used to parse or format [dates](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) in a variety of locale-specific representations. To format a date, create a [formatter](#locale_format) from a specifier (a string with the desired format *directives*, indicated by `%`); then pass a date to the formatter, which returns a string. For example, to convert the current date to a human-readable string:

```js
const formatTime = d3.utcFormat("%B %d, %Y");
formatTime(new Date()); // "May 31, 2023"
```

Likewise, to convert a string back to a date, create a [parser](#locale_parse):

```js
const parseTime = d3.utcParse("%B %d, %Y");
parseTime("June 30, 2015"); // 2023-05-31
```

You can implement more elaborate conditional time formats, too. For example, here’s a multi-scale time format using [time intervals](./d3-time.md):

```js
const formatMillisecond = d3.utcFormat(".%L"),
    formatSecond = d3.utcFormat(":%S"),
    formatMinute = d3.utcFormat("%I:%M"),
    formatHour = d3.utcFormat("%I %p"),
    formatDay = d3.utcFormat("%a %d"),
    formatWeek = d3.utcFormat("%b %d"),
    formatMonth = d3.utcFormat("%B"),
    formatYear = d3.utcFormat("%Y");

function multiFormat(date) {
  return (d3.utcSecond(date) < date ? formatMillisecond
      : d3.utcMinute(date) < date ? formatSecond
      : d3.utcHour(date) < date ? formatMinute
      : d3.utcDay(date) < date ? formatHour
      : d3.utcMonth(date) < date ? (d3.utcWeek(date) < date ? formatDay : formatWeek)
      : d3.utcYear(date) < date ? formatMonth
      : formatYear)(date);
}
```

This module is used by D3 [time scales](./d3-scale/time.md) to generate human-readable ticks.

Also see [*date*.toLocaleString](https://observablehq.com/@mbostock/date-formatting).

## timeFormat(*specifier*) {#timeFormat}

```js
d3.timeFormat("%b %d")
```

An alias for [*locale*.format](#locale_format) on the [default locale](#timeFormatDefaultLocale).

## timeParse(*specifier*) {#timeParse}

```js
d3.timeParse("%b %d")
```

An alias for [*locale*.parse](#locale_parse) on the [default locale](#timeFormatDefaultLocale).

## utcFormat(*specifier*) {#utcFormat}

```js
d3.utcFormat("%b %d")
```

An alias for [*locale*.utcFormat](#locale_utcFormat) on the [default locale](#timeFormatDefaultLocale).

## utcParse(*specifier*) {#utcParse}

```js
d3.utcParse("%b %d")
```

An alias for [*locale*.utcParse](#locale_utcParse) on the [default locale](#timeFormatDefaultLocale).

## isoFormat {#isoFormat}

```js
d3.isoFormat(new Date()) // "2023-05-31T18:17:36.788Z"
```

[Source](https://github.com/d3/d3-time-format/blob/main/src/isoFormat.js) · The full [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) UTC time formatter. Where available, this method will use [Date.toISOString](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Date/toISOString) to format.

## isoParse {#isoParse}

```js
d3.isoParse("2023-05-31T18:17:36.788Z")
```

[Source](https://github.com/d3/d3-time-format/blob/main/src/isoParse.js) · The full [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) UTC time parser. Where available, this method will use the [Date constructor](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Date) to parse strings. If you depend on strict validation of the input format according to ISO 8601, you should construct a [UTC parser function](

