## d3-dispatch | D3 by Observable

**URL:** https://d3js.org/d3-dispatch

**Contents:**
- d3-dispatch ​
- dispatch(...types) ​
- dispatch.on(typenames, callback) ​
- dispatch.copy() ​
- dispatch.call(type, that, ...arguments) ​
- dispatch.apply(type, that, arguments) ​

Dispatching is a low-level interaction mechanism that allows you to register named callbacks and then call them with arbitrary arguments. A variety of D3 interaction components, such as d3-drag, use dispatch to emit events to listeners. Think of this as EventTarget except every listener has a well-defined name so it’s easy to remove or replace them.

For example, to create a dispatch for start and end events:

You can then register callbacks for these events using dispatch.on:

Then, you can invoke all the start callbacks using dispatch.call or dispatch.apply:

Like function.call, you may also specify the this context and any arguments:

Source · Creates a new dispatch for the specified event types. Each type is a string, such as "start" or "end".

Source · Adds, removes or gets the callback for the specified typenames. If a callback function is specified, it is registered for the specified (fully-qualified) typenames. If a callback was already registered for the given typenames, the existing callback is removed before the new callback is added.

The specified typenames is a string, such as start or end.foo. The type may be optionally followed by a period (.) and a name; the optional name allows multiple callbacks to be registered to receive events of the same type, such as start.foo and start.bar. To specify multiple typenames, separate typenames with spaces, such as start end or start.foo start.bar.

To remove all callbacks for a given name foo, say dispatch.on(".foo", null).

If callback is not specified, returns the current callback for the specified typenames, if any. If multiple typenames are specified, the first matching callback is returned.

Source · Returns a copy of this dispatch object. Changes to this dispatch do not affect the returned copy and vice versa.

Source · Like function.call, invokes each registered callback for the specified type, passing the callback the specified ...argument, with that as the this context. See dispatch.apply for more information.

Source · Like function.apply, invokes each registered callback for the specified type, passing the callback the specified arguments, with that as the this context. For example, if you wanted to dispatch your custom callbacks after handling a native click event, while preserving the current this context and arguments, you could say:

You can pass whatever arguments you want to callbacks; most commonly, you might create an object that represents an event, or pass the current datum (d) and index (i). See function.call and function.apply for further information.

**Examples:**

Example 1 (javascript):
```javascript
const dispatch = d3.dispatch("start", "end");
```

Example 2 (julia):
```julia
dispatch.on("start", callback1);
dispatch.on("start.foo", callback2);
dispatch.on("end", callback3);
```

Example 3 (unknown):
```unknown
dispatch.call("start");
```

Example 4 (css):
```css
dispatch.call("start", {about: "I am a context object"}, "I am an argument");
```
