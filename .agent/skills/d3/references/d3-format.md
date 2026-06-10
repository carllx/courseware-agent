## d3-time-format | D3 by Observable

**URL:** https://d3js.org/d3-time-format

**Contents:**
- d3-time-format ​
- timeFormat(specifier) ​
- timeParse(specifier) ​
- utcFormat(specifier) ​
- utcParse(specifier) ​
- isoFormat ​
- isoParse ​
- locale.format(specifier) ​
- locale.parse(specifier) ​
- locale.utcFormat(specifier) ​

This module provides an approximate JavaScript implementation of the venerable strptime and strftime functions from the C standard library, and can be used to parse or format dates in a variety of locale-specific representations. To format a date, create a formatter from a specifier (a string with the desired format directives, indicated by %); then pass a date to the formatter, which returns a string. For example, to convert the current date to a human-readable string:

Likewise, to convert a string back to a date, create a parser:

You can implement more elaborate conditional time formats, too. For example, here’s a multi-scale time format using time intervals:

This module is used by D3 time scales to generate human-readable ticks.

Also see date.toLocaleString.

An alias for locale.format on the default locale.

An alias for locale.parse on the default locale.

An alias for locale.utcFormat on the default locale.

An alias for locale.utcParse on the default locale.

Source · The full ISO 8601 UTC time formatter. Where available, this method will use Date.toISOString to format.

Source · The full ISO 8601 UTC time parser. Where available, this method will use the Date constructor to parse strings. If you depend on strict validation of the input format according to ISO 8601, you should construct a UTC parser function:

Source · Returns a new formatter for the given string specifier. The specifier string may contain the following directives:

Directives marked with an asterisk (*) may be affected by the locale definition.

For %U, all days in a new year preceding the first Sunday are considered to be in week 0. For %W, all days in a new year preceding the first Monday are considered to be in week 0. Week numbers are computed using interval.count. For example, 2015-52 and 2016-00 represent Monday, December 28, 2015, while 2015-53 and 2016-01 represent Monday, January 4, 2016. This differs from the ISO week date specification (%V), which uses a more complicated definition!

For %V,%g and %G, per the strftime man page:

In this system, weeks start on a Monday, and are numbered from 01, for the first week, up to 52 or 53, for the last week. Week 1 is the first week where four or more days fall within the new year (or, synonymously, week 01 is: the first week of the year that contains a Thursday; or, the week that has 4 January in it). If the ISO week number belongs to the previous or next year, that year is used instead.

The % sign indicating a directive may be immediately followed by a padding modifier:

If no padding modifier is specified, the default is 0 for all directives except %e, which defaults to _. (In some implementations of strftime and strptime, a directive may include an optional field width or precision; this feature is not yet implemented.)

The returned function formats a specified date, returning the corresponding string.

Source · Returns a new parser for the given string specifier. The specifier string may contain the same directives as locale.format. The %d and %e directives are considered equivalent for parsing.

The returned function parses a specified string, returning the corresponding date or null if the string could not be parsed according to this format’s specifier. Parsing is strict: if the specified string does not exactly match the associated specifier, this method returns null. For example, if the associated specifier is %Y-%m-%dT%H:%M:%SZ, then the string "2011-07-01T19:15:28Z" will be parsed as expected, but "2011-07-01T19:15:28", "2011-07-01 19:15:28" and "2011-07-01" will return null. (Note that the literal Z here is different from the time zone offset directive %Z.) If a more flexible parser is desired, try multiple formats sequentially until one returns non-null.

Source · Equivalent to locale.format, except all directives are interpreted as Coordinated Universal Time (UTC) rather than local time.

Source · Equivalent to locale.parse, except all directives are interpreted as Coordinated Universal Time (UTC) rather than local time.

Source · Returns a locale object for the specified definition with locale.format, locale.parse, locale.utcFormat, locale.utcParse methods. The definition must include the following properties:

Source · Equivalent to d3.timeFormatLocale, except it also redefines d3.timeFormat, d3.timeParse, d3.utcFormat and d3.utcParse to the new locale’s locale.format, locale.parse, locale.utcFormat and locale.utcParse. If you do not set a default locale, it defaults to U.S. English.

**Examples:**

Example 1 (javascript):
```javascript
const formatTime = d3.utcFormat("%B %d, %Y");
formatTime(new Date()); // "May 31, 2023"
```

Example 2 (javascript):
```javascript
const parseTime = d3.utcParse("%B %d, %Y");
parseTime("June 30, 2015"); // 2023-05-31
```

Example 3 (javascript):
```javascript
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

Example 4 (unknown):
```unknown
d3.timeFormat("%b %d")
```

---

## d3-format | D3 by Observable

**URL:** https://d3js.org/d3-format

**Contents:**
- d3-format ​
- format(specifier) ​
- formatPrefix(specifier, value) ​
- formatLocale(definition) ​
- formatDefaultLocale(definition) ​
- locale.format(specifier) ​
- locale.formatPrefix(specifier, value) ​
- formatSpecifier(specifier) ​
- new d3.FormatSpecifier(specifier) ​
- precisionFixed(step) ​

Ever noticed how sometimes JavaScript doesn’t display numbers the way you expect? Like, you tried to print tenths with a simple loop:

Welcome to binary floating point! ಠ_ಠ

Yet rounding error is not the only reason to customize number formatting. A table of numbers should be formatted consistently for comparison; above, 0.0 would be better than 0. Large numbers should have grouped digits (e.g., 42,000) or be in scientific or metric notation (4.2e+4, 42k). Currencies should have fixed precision ($3.50). Reported numerical results should be rounded to significant digits (4021 becomes 4000). Number formats should appropriate to the reader’s locale (42.000,00 or 42,000.00). The list goes on.

Formatting numbers for human consumption is the purpose of d3-format, which is modeled after Python 3’s format specification mini-language (PEP 3101). Revisiting the example above:

But d3-format is much more than an alias for number.toFixed! A few more examples:

See locale.format for a detailed specification, and try running d3.formatSpecifier on the above formats to decode their meaning.

Also see number.toLocaleString.

Source · An alias for locale.format on the default locale.

Source · An alias for locale.formatPrefix on the default locale.

Source · Returns a locale object for the specified definition with locale.format and locale.formatPrefix methods. The definition must include the following properties:

Note that the thousands property is a misnomer, as the grouping definition allows groups other than thousands.

Source · Equivalent to d3.formatLocale, except it also redefines d3.format and d3.formatPrefix to the new locale’s locale.format and locale.formatPrefix. If you do not set a default locale, it defaults to U.S. English.

Source · Returns a new format function for the given string specifier. The returned function takes a number as the only argument, and returns a string representing the formatted number. The general form of a specifier is:

The fill can be any character. The presence of a fill character is signaled by the align character following it, which must be one of the following:

The zero (0) option enables zero-padding; this implicitly sets fill to 0 and align to =. The width defines the minimum field width; if not specified, then the width will be determined by the content. The comma (,) option enables the use of a group separator, such as a comma for thousands.

Depending on the type, the precision either indicates the number of digits that follow the decimal point (types f and %), or the number of significant digits (types ​, e, g, r, s and p). If the precision is not specified, it defaults to 6 for all types except ​ (none), which defaults to 12. Precision is ignored for integer formats (types b, o, d, x, and X) and character data (type c). See precisionFixed and precisionRound for help picking an appropriate precision.

The ~ option trims insignificant trailing zeros across all format types. This is most commonly used in conjunction with types r, e, s and %. For example:

The available type values are:

The type ​ (none) is also supported as shorthand for ~g (with a default precision of 12 instead of 6), and the type n is shorthand for ,g. For the g, n and ​ (none) types, decimal notation is used if the resulting string would have precision or fewer digits; otherwise, exponent notation is used. For example:

Source · Equivalent to locale.format, except the returned function will convert values to the units of the appropriate SI prefix for the specified numeric reference value before formatting in fixed point notation. The following prefixes are supported:

Unlike locale.format with the s format type, this method returns a formatter with a consistent SI prefix, rather than computing the prefix dynamically for each number. In addition, the precision for the given specifier represents the number of digits past the decimal point (as with f fixed point notation), not the number of significant digits. For example:

This method is useful when formatting multiple numbers in the same units for easy comparison. See precisionPrefix for help picking an appropriate precision.

Source · Parses the specified specifier, returning an object with exposed fields that correspond to the format specification mini-language and a toString method that reconstructs the specifier. For example, formatSpecifier("s") returns:

This method is useful for understanding how format specifiers are parsed and for deriving new specifiers. For example, you might compute an appropriate precision based on the numbers you want to format using precisionFixed and then create a new format:

Source · Given the specified specifier object, returning an object with exposed fields that correspond to the format specification mini-language and a toString method that reconstructs the specifier. For example, new FormatSpecifier({type: "s"}) returns:

Source · Returns a suggested decimal precision for fixed point notation given the specified numeric step value. The step represents the minimum absolute difference between values that will be formatted. (This assumes that the values to be formatted are also multiples of step.) For example, given the numbers 1, 1.5, and 2, the step should be 0.5 and the suggested precision is 1:

Whereas for the numbers 1, 2 and 3, the step should be 1 and the suggested precision is 0:

Note: for the % format type, subtract two:

Source · Returns a suggested decimal precision for use with locale.formatPrefix given the specified numeric step and reference value. The step represents the minimum absolute difference between values that will be formatted, and value determines which SI prefix will be used. (This assumes that the values to be formatted are also multiples of step.) For example, given the numbers 1.1e6, 1.2e6, and 1.3e6, the step should be 1e5, the value could be 1.3e6, and the suggested precision is 1:

Source · Returns a suggested decimal precision for format types that round to significant digits given the specified numeric step and max values. The step represents the minimum absolute difference between values that will be formatted, and the max represents the largest absolute value that will be formatted. (This assumes that the values to be formatted are also multiples of step.) For example, given the numbers 0.99, 1.0, and 1.01, the step should be 0.01, the max should be 1.01, and the suggested precision is 3:

Whereas for the numbers 0.9, 1.0, and 1.1, the step should be 0.1, the max should be 1.1, and the suggested precision is 2:

Note: for the e format type, subtract one:

**Examples:**

Example 1 (sass):
```sass
for (let i = 0; i < 10; ++i) {
  console.log(0.1 * i);
}
```

Example 2 (unknown):
```unknown
0
0.1
0.2
0.30000000000000004
0.4
0.5
0.6000000000000001
0.7000000000000001
0.8
0.9
```

Example 3 (javascript):
```javascript
const f = d3.format(".1f");
for (let i = 0; i < 10; ++i) {
  console.log(f(0.1 * i));
}
```

Example 4 (unknown):
```unknown
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
```

---

