## d3-time | D3 by Observable

**URL:** https://d3js.org/d3-time

**Contents:**
- d3-time ​
- interval(date) ​
- interval.floor(date) ​
- interval.round(date) ​
- interval.ceil(date) ​
- interval.offset(date, step) ​
- interval.range(start, stop, step) ​
- interval.filter(test) ​
- interval.every(step) ​
- interval.count(start, end) ​

When visualizing time series data, analyzing temporal patterns, or working with time in general, the irregularities of conventional time units quickly become apparent. In the Gregorian calendar, for example, most months have 31 days but some have 28, 29 or 30; most years have 365 days but leap years have 366; and with daylight saving, most days have 24 hours but some have 23 or 25. Adding to complexity, daylight saving conventions vary around the world.

As a result of these temporal peculiarities, it can be difficult to perform seemingly-trivial tasks. For example, if you want to compute the number of days that have passed between two dates, you can’t simply subtract and divide by 24 hours (86,400,000 ms):

You can, however, use d3.timeDay.count:

The day interval is one of several provided by d3-time. Each interval represents a conventional unit of time — hours, weeks, months, etc. — and has methods to calculate boundary dates. For example, d3.timeDay computes midnight (typically 12:00 AM local time) of the corresponding day. In addition to rounding and counting, intervals can also be used to generate arrays of boundary dates. For example, to compute each Sunday in the current month:

The d3-time module does not implement its own calendaring system; it merely implements a convenient API for calendar math on top of ECMAScript Date. Thus, it ignores leap seconds and can only work with the local time zone and Coordinated Universal Time (UTC).

This module is used by D3’s time scales to generate sensible ticks, by D3’s time format, and can also be used directly to do things like calendar layouts.

Source · Equivalent to interval.floor, except if date is not specified, it defaults to the current time. For example, d3.timeYear(date) and d3.timeYear.floor(date) are equivalent.

Source · Returns a new date representing the latest interval boundary date before or equal to date. For example, d3.timeDay.floor(date) typically returns 12:00 AM local time on the given date.

This method is idempotent: if the specified date is already floored to the current interval, a new date with an identical time is returned. Furthermore, the returned date is the minimum expressible value of the associated interval, such that interval.floor(interval.floor(date) - 1) returns the preceding interval boundary date.

Note that the == and === operators do not compare by value with Date objects, and thus you cannot use them to tell whether the specified date has already been floored. Instead, coerce to a number and then compare:

This is more reliable than testing whether the time is 12:00 AM, as in some time zones midnight may not exist due to daylight saving.

Source · Returns a new date representing the closest interval boundary date to date. For example, d3.timeDay.round(date) typically returns 12:00 AM local time on the given date if it is on or before noon, and 12:00 AM of the following day if it is after noon.

This method is idempotent: if the specified date is already rounded to the current interval, a new date with an identical time is returned.

Source · Returns a new date representing the earliest interval boundary date after or equal to date. For example, d3.timeDay.ceil(date) typically returns 12:00 AM local time on the date following the given date.

This method is idempotent: if the specified date is already ceilinged to the current interval, a new date with an identical time is returned. Furthermore, the returned date is the maximum expressible value of the associated interval, such that interval.ceil(interval.ceil(date) + 1) returns the following interval boundary date.

Source · Returns a new date equal to date plus step intervals. If step is not specified it defaults to 1. If step is negative, then the returned date will be before the specified date; if step is zero, then a copy of the specified date is returned; if step is not an integer, it is floored. This method does not round the specified date to the interval. For example, if date is today at 5:34 PM, then d3.timeDay.offset(date, 1) returns 5:34 PM tomorrow (even if daylight saving changes!).

Source · Returns an array of dates representing every interval boundary after or equal to start (inclusive) and before stop (exclusive). If step is specified, then every stepth boundary will be returned; for example, for the d3.timeDay interval a step of 2 will return every other day. If step is not an integer, it is floored.

The first date in the returned array is the earliest boundary after or equal to start; subsequent dates are offset by step intervals and floored. Thus, two overlapping ranges may be consistent. For example, this range contains odd days:

While this contains even days:

To make ranges consistent when a step is specified, use interval.every instead.

For convenience, aliases for interval.range are also provided as plural forms of the corresponding interval, such as utcMondays.

Source · Returns a new interval that is a filtered subset of this interval using the specified test function. The test function is passed a date and should return true if and only if the specified date should be considered part of the interval. For example, to create an interval that returns the 1st, 11th, 21th and 31th (if it exists) of each month:

The returned filtered interval does not support interval.count. See also interval.every.

Source · Returns a filtered view of this interval representing every stepth date. The meaning of step is dependent on this interval’s parent interval as defined by the field function. For example, d3.timeMinute.every(15) returns an interval representing every fifteen minutes, starting on the hour: :00, :15, :30, :45, etc. Note that for some intervals, the resulting dates may not be uniformly-spaced; d3.timeDay’s parent interval is d3.timeMonth, and thus the interval number resets at the start of each month. If step is not valid, returns null. If step is one, returns this interval.

This method can be used in conjunction with interval.range to ensure that two overlapping ranges are consistent. For example, this range contains odd days:

The returned filtered interval does not support interval.count. See also interval.filter.

Source · Returns the number of interval boundaries after start (exclusive) and before or equal to end (inclusive). Note that this behavior is slightly different than interval.range because its purpose is to return the zero-based number of the specified end date relative to the specified start date. For example, to compute the current zero-based day-of-year number:

Likewise, to compute the current zero-based week-of-year number for weeks that start on Sunday:

Source · Constructs a new custom interval given the specified floor and offset functions and an optional count function.

The floor function takes a single date as an argument and rounds it down to the nearest interval boundary.

The offset function takes a date and an integer step as arguments and advances the specified date by the specified number of boundaries; the step may be positive, negative or zero.

The optional count function takes a start date and an end date, already floored to the current interval, and returns the number of boundaries between the start (exclusive) and end (inclusive). If a count function is not specified, the returned interval does not expose interval.count or interval.every methods. Note: due to an internal optimization, the specified count function must not invoke interval.count on other time intervals.

The optional field function takes a date, already floored to the current interval, and returns the field value of the specified date, corresponding to the number of boundaries between this date (exclusive) and the latest previous parent boundary. For example, for the d3.timeDay interval, this returns the number of days since the start of the month. If a field function is not specified, it defaults to counting the number of interval boundaries since the UNIX epoch of January 1, 1970 UTC. The field function defines the behavior of interval.every.

Source · Milliseconds in local time; the shortest available time unit.

Source · Seconds in local time (e.g., 01:23:45.0000 AM); 1,000 milliseconds.

Source · Minutes in local time (e.g., 01:02:00 AM); 60 seconds. Note that ECMAScript ignores leap seconds.

Source · Hours in local time (e.g., 01:00 AM); 60 minutes. Note that advancing time by one hour in local time can return the same hour or skip an hour due to daylight saving.

Source · Days in local time (e.g., February 7, 2012 at 12:00 AM); typically 24 hours. Days in local time may range from 23 to 25 hours due to daylight saving. d3.unixDay is like d3.utcDay, except it counts days since the UNIX epoch (January 1, 1970) such that interval.every returns uniformly-spaced dates rather than varying based on day-of-month.

Source · Alias for d3.timeSunday; 7 days and typically 168 hours. Weeks in local time may range from 167 to 169 hours due to daylight saving.

Source · Sunday-based weeks in local time (e.g., February 5, 2012 at 12:00 AM).

Source · Monday-based weeks in local time (e.g., February 6, 2012 at 12:00 AM).

Source · Tuesday-based weeks in local time (e.g., February 7, 2012 at 12:00 AM).

Source · Wednesday-based weeks in local time (e.g., February 8, 2012 at 12:00 AM).

Source · Thursday-based weeks in local time (e.g., February 9, 2012 at 12:00 AM).

Source · Friday-based weeks in local time (e.g., February 10, 2012 at 12:00 AM).

Source · Saturday-based weeks in local time (e.g., February 11, 2012 at 12:00 AM).

Source · Months in local time (e.g., February 1, 2012 at 12:00 AM); ranges from 28 to 31 days.

Source · Years in local time (e.g., January 1, 2012 at 12:00 AM); ranges from 365 to 366 days.

Source · Milliseconds in UTC time; the shortest available time unit.

Source · Seconds in UTC time (e.g., 01:23:45.0000 AM); 1,000 milliseconds.

Source · Minutes in UTC time (e.g., 01:02:00 AM); 60 seconds. Note that ECMAScript ignores leap seconds.

Source · Hours in UTC time (e.g., 01:00 AM); 60 minutes.

Source · Days in UTC time (e.g., February 7, 2012 at 12:00 AM); 24 hours.

Source · Alias for d3.timeSunday; 7 days and 168 hours.

Source · Sunday-based weeks in UTC time (e.g., February 5, 2012 at 12:00 AM).

Source · Monday-based weeks in UTC time (e.g., February 6, 2012 at 12:00 AM).

Source · Tuesday-based weeks in UTC time (e.g., February 7, 2012 at 12:00 AM).

Source · Wednesday-based weeks in UTC time (e.g., February 8, 2012 at 12:00 AM).

Source · Thursday-based weeks in UTC time (e.g., February 9, 2012 at 12:00 AM).

Source · Friday-based weeks in UTC time (e.g., February 10, 2012 at 12:00 AM).

Source · Saturday-based weeks in UTC time (e.g., February 11, 2012 at 12:00 AM).

Source · Months in UTC time (e.g., February 1, 2012 at 12:00 AM); ranges from 28 to 31 days.

Source · Years in UTC time (e.g., January 1, 2012 at 12:00 AM); ranges from 365 to 366 days.

Like d3.utcDay, except it counts days since the UNIX epoch (January 1, 1970) such that interval.every returns uniformly-spaced dates rather than varying based on day-of-month.

Alias for d3.timeMillisecond.range.

Alias for d3.timeSecond.range.

Alias for d3.timeMinute.range.

Alias for d3.timeHour.range.

Alias for d3.timeDay.range.

Alias for d3.timeWeek.range.

Alias for d3.timeSunday.range.

Alias for d3.timeMonday.range.

Alias for d3.timeTuesday.range.

Alias for d3.timeWednesday.range.

Alias for d3.timeThursday.range.

Alias for d3.timeFriday.range.

Alias for d3.timeSaturday.range.

Alias for d3.timeMonth.range.

Alias for d3.timeYear.range.

Alias for d3.utcMillisecond.range.

Alias for d3.utcSecond.range.

Alias for d3.utcMinute.range.

Alias for d3.utcHour.range.

Alias for d3.utcDay.range.

Alias for d3.utcWeek.range.

Alias for d3.utcSunday.range.

Alias for d3.utcMonday.range.

Alias for d3.utcTuesday.range.

Alias for d3.utcWednesday.range.

Alias for d3.utcThursday.range.

Alias for d3.utcFriday.range.

Alias for d3.utcSaturday.range.

Alias for d3.utcMonth.range.

Alias for d3.utcYear.range.

Source · Equivalent to d3.utcTicks, but in local time.

Source · Returns the time interval that would be used by d3.timeTicks given the same arguments.

Source · Returns an array of approximately count dates at regular intervals between start and stop (inclusive). If stop is before start, dates are returned in reverse chronological order; otherwise dates are returned in chronological order. The following UTC time intervals are considered:

Multiples of milliseconds (for small ranges) and years (for large ranges) are also considered, following the rules of d3.ticks. The interval producing the number of dates that is closest to count is used. For example:

If count is a time interval, this function behaves similarly to interval.range except that both start and stop are inclusive and it may return dates in reverse chronological order if stop is before start.

Source · Returns the time interval that would be used by d3.utcTicks given the same arguments. If there is no associated interval, such as when start or stop is invalid, returns null.

**Examples:**

Example 1 (javascript):
```javascript
const start = new Date(2015, 02, 01); // 2015-03-01T00:00
const end = new Date(2015, 03, 01); // 2015-04-01T00:00
const days = (end - start) / 864e5; // 30.958333333333332, oops! 🤯
```

Example 2 (julia):
```julia
d3.timeDay.count(start, end) // 31 😌
```

Example 3 (javascript):
```javascript
const start = d3.timeMonth.floor(new Date(2015, 0, 15)); // 2015-01-01T00:00
const stop = d3.timeMonth.ceil(new Date(2015, 0, 15)); // 2015-02-01T00:00
const weeks = d3.timeWeek.range(start, stop); // [2015-01-04T00:00, 2015-01-11T00:00, 2015-01-18T00:00, 2015-01-25T00:00]
```

Example 4 (unknown):
```unknown
d3.utcMonday() // the latest preceding Monday, UTC time
```

---

