# Jinja2_Docs - Other

**Pages:** 22

---

## Integration — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/integration/

**Contents:**
- Integration¶
- Flask¶
- Django¶
- Babel¶
- Pylons¶

The Flask web application framework, also maintained by Pallets, uses Jinja templates by default. Flask sets up a Jinja environment and template loader for you, and provides functions to easily render templates from view functions.

Django supports using Jinja as its template engine, see https://docs.djangoproject.com/en/stable/topics/templates/#support-for-template-engines.

Jinja provides support for extracting gettext messages from templates via a Babel extractor entry point called jinja2.ext.babel_extract. The support is implemented as part of the i18n Extension extension.

Gettext messages are extracted from both trans tags and code expressions.

To extract gettext messages from templates, the project needs a Jinja section in its Babel extraction method mapping file:

The syntax related options of the Environment are also available as configuration values in the mapping file. For example, to tell the extractor that templates use % as line_statement_prefix you can use this code:

Extensions may also be defined by passing a comma separated list of import paths as the extensions value. The i18n extension is added automatically.

Template syntax errors are ignored by default. The assumption is that tests will catch syntax errors in templates. If you don’t want to ignore errors, add silent = false to the settings.

It’s easy to integrate Jinja into a Pylons application.

The template engine is configured in config/environment.py. The configuration for Jinja looks something like this:

After that you can render Jinja templates by using the render_jinja function from the pylons.templating module.

Additionally it’s a good idea to set the Pylons c object to strict mode. By default attribute access on missing attributes on the c object returns an empty string and not an undefined object. To change this add this to config/environment.py:

---

## Sandbox — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/sandbox/

**Contents:**
- Sandbox¶
- Security Considerations¶
- API¶
- Operator Intercepting¶

The Jinja sandbox can be used to render untrusted templates. Access to attributes, method calls, operators, mutating data structures, and string formatting can be intercepted and prohibited.

A sandboxed environment can be useful, for example, to allow users of an internal reporting system to create custom emails. You would document what data is available in the templates, then the user would write a template using that information. Your code would generate the report data and pass it to the user’s sandboxed template to render.

The sandbox alone is not a solution for perfect security. Keep these things in mind when using the sandbox.

Templates can still raise errors when compiled or rendered. Your code should attempt to catch errors instead of crashing.

It is possible to construct a relatively small template that renders to a very large amount of output, which could correspond to a high use of CPU or memory. You should run your application with limits on resources such as CPU and memory to mitigate this.

Jinja only renders text, it does not understand, for example, JavaScript code. Depending on how the rendered template will be used, you may need to do other postprocessing to restrict the output.

Pass only the data that is relevant to the template. Avoid passing global data, or objects with methods that have side effects. By default the sandbox prevents private and internal attribute access. You can override is_safe_attribute() to further restrict attributes access. Decorate methods with unsafe() to prevent calling them from templates when passing objects as data. Use ImmutableSandboxedEnvironment to prevent modifying lists and dictionaries.

The sandboxed environment. It works like the regular environment but tells the compiler to generate sandboxed code. Additionally subclasses of this environment may override the methods that tell the runtime what attributes or functions are safe to access.

If the template tries to access insecure code a SecurityError is raised. However also other exceptions may occur during the rendering so the caller has to ensure that all exceptions are caught.

default callback table for the binary operators. A copy of this is available on each instance of a sandboxed environment as binop_table

default callback table for the unary operators. A copy of this is available on each instance of a sandboxed environment as unop_table

a set of binary operators that should be intercepted. Each operator that is added to this set (empty by default) is delegated to the call_binop() method that will perform the operator. The default operator callback is specified by binop_table.

The following binary operators are interceptable: //, %, +, *, -, /, and **

The default operation form the operator table corresponds to the builtin function. Intercepted calls are always slower than the native operator call, so make sure only to intercept the ones you are interested in.

Added in version 2.6.

a set of unary operators that should be intercepted. Each operator that is added to this set (empty by default) is delegated to the call_unop() method that will perform the operator. The default operator callback is specified by unop_table.

The following unary operators are interceptable: +, -

The default operation form the operator table corresponds to the builtin function. Intercepted calls are always slower than the native operator call, so make sure only to intercept the ones you are interested in.

Added in version 2.6.

The sandboxed environment will call this method to check if the attribute of an object is safe to access. Per default all attributes starting with an underscore are considered private as well as the special attributes of internal python objects as returned by the is_internal_attribute() function.

Check if an object is safely callable. By default callables are considered safe unless decorated with unsafe().

This also recognizes the Django convention of setting func.alters_data = True.

For intercepted binary operator calls (intercepted_binops()) this function is executed instead of the builtin operator. This can be used to fine tune the behavior of certain operators.

Added in version 2.6.

For intercepted unary operator calls (intercepted_unops()) this function is executed instead of the builtin operator. This can be used to fine tune the behavior of certain operators.

Added in version 2.6.

Works exactly like the regular SandboxedEnvironment but does not permit modifications on the builtin mutable objects list, set, and dict by using the modifies_known_mutable() function.

Raised if a template tries to do something insecure if the sandbox is enabled.

Marks a function or method as unsafe.

Test if the attribute given is an internal python attribute. For example this function returns True for the func_code attribute of python objects. This is useful if the environment method is_safe_attribute() is overridden.

This function checks if an attribute on a builtin mutable object (list, dict, set or deque) or the corresponding ABCs would modify it if called.

If called with an unsupported object, False is returned.

For performance, Jinja outputs operators directly when compiling. This means it’s not possible to intercept operator behavior by overriding SandboxEnvironment.call by default, because operator special methods are handled by the Python interpreter, and might not correspond with exactly one method depending on the operator’s use.

The sandbox can instruct the compiler to output a function to intercept certain operators instead. Override SandboxedEnvironment.intercepted_binops and SandboxedEnvironment.intercepted_unops with the operator symbols you want to intercept. The compiler will replace the symbols with calls to SandboxedEnvironment.call_binop() and SandboxedEnvironment.call_unop() instead. The default implementation of those methods will use SandboxedEnvironment.binop_table and SandboxedEnvironment.unop_table to translate operator symbols into operator functions.

For example, the power (**) operator can be disabled:

---

## Extensions — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/extensions/

**Contents:**
- Extensions¶
- Adding Extensions¶
- i18n Extension¶
  - Environment Methods¶
  - Whitespace Trimming¶
  - New Style Gettext¶
- Expression Statement¶
- Loop Controls¶
- With Statement¶
- Autoescape Extension¶

Jinja supports extensions that can add extra filters, tests, globals or even extend the parser. The main motivation of extensions is to move often used code into a reusable class like adding support for internationalization.

Extensions are added to the Jinja environment at creation time. To add an extension pass a list of extension classes or import paths to the extensions parameter of the Environment constructor. The following example creates a Jinja environment with the i18n extension loaded:

To add extensions after creation time, use the add_extension() method:

Import name: jinja2.ext.i18n

The i18n extension can be used in combination with gettext or Babel. When it’s enabled, Jinja provides a trans statement that marks a block as translatable and calls gettext.

After enabling, an application has to provide functions for gettext, ngettext, and optionally pgettext and npgettext, either globally or when rendering. A _() function is added as an alias to the gettext function.

A convenient way to provide these functions is to call one of the below methods depending on the translation system in use. If you do not require actual translation, use Environment.install_null_translations to install no-op functions.

After enabling the extension, the environment provides the following additional methods:

Installs a translation globally for the environment. The translations object must implement gettext, ngettext, and optionally pgettext and npgettext. gettext.NullTranslations, gettext.GNUTranslations, and Babels Translations are supported.

Changed in version 3.0: Added pgettext and npgettext.

Changed in version 2.5: Added new-style gettext support.

Install no-op gettext functions. This is useful if you want to prepare the application for internationalization but don’t want to implement the full system yet.

Changed in version 2.5: Added new-style gettext support.

Install the given gettext, ngettext, pgettext, and npgettext callables into the environment. They should behave exactly like gettext.gettext(), gettext.ngettext(), gettext.pgettext() and gettext.npgettext().

If newstyle is activated, the callables are wrapped to work like newstyle callables. See New Style Gettext for more information.

Changed in version 3.0: Added pgettext and npgettext.

Added in version 2.5: Added new-style gettext support.

Uninstall the environment’s globally installed translation.

Extract localizable strings from the given template node or source.

For every string found this function yields a (lineno, function, message) tuple, where:

lineno is the number of the line on which the string was found.

function is the name of the gettext function used (if the string was extracted from embedded Python code).

message is the string itself, or a tuple of strings for functions with multiple arguments.

If Babel is installed, see Babel to extract the strings.

For a web application that is available in multiple languages but gives all the users the same language (for example, multilingual forum software installed for a French community), the translation may be installed when the environment is created.

The get_gettext_translations function would return the translator for the current configuration, for example by using gettext.find.

The usage of the i18n extension for template designers is covered in the template documentation.

Added in version 2.10.

Within {% trans %} blocks, it can be useful to trim line breaks and whitespace so that the block of text looks like a simple string with single spaces in the translation file.

Linebreaks and surrounding whitespace can be automatically trimmed by enabling the ext.i18n.trimmed policy.

Added in version 2.5.

New style gettext calls are less to type, less error prone, and support autoescaping better.

You can use “new style” gettext calls by setting env.newstyle_gettext = True or passing newstyle=True to env.install_translations. They are fully supported by the Babel extraction tool, but might not work as expected with other extraction tools.

With standard gettext calls, string formatting is a separate step done with the |format filter. This requires duplicating work for ngettext calls.

New style gettext make formatting part of the call, and behind the scenes enforce more consistency.

The advantages of newstyle gettext are:

There’s no separate formatting step, you don’t have to remember to use the |format filter.

Only named placeholders are allowed. This solves a common problem translators face because positional placeholders can’t switch positions meaningfully. Named placeholders always carry semantic information about what value goes where.

String formatting is used even if no placeholders are used, which makes all strings use a consistent format. Remember to escape any raw percent signs as %%, such as 100%%.

The translated string is marked safe, formatting performs escaping as needed. Mark a parameter as |safe if it has already been escaped.

Import name: jinja2.ext.do

The “do” aka expression-statement extension adds a simple do tag to the template engine that works like a variable expression but ignores the return value.

Import name: jinja2.ext.loopcontrols

This extension adds support for break and continue in loops. After enabling, Jinja provides those two keywords which work exactly like in Python.

Import name: jinja2.ext.with_

Changed in version 2.9: This extension is now built-in and no longer does anything.

Import name: jinja2.ext.autoescape

Changed in version 2.9: This extension was removed and is now built-in. Enabling the extension no longer does anything.

Import name: jinja2.ext.debug

Adds a {% debug %} tag to dump the current context as well as the available filters and tests. This is useful to see what’s available to use in the template without setting up a debugger.

By writing extensions you can add custom tags to Jinja. This is a non-trivial task and usually not needed as the default tags and expressions cover all common use cases. The i18n extension is a good example of why extensions are useful. Another one would be fragment caching.

When writing extensions you have to keep in mind that you are working with the Jinja template compiler which does not validate the node tree you are passing to it. If the AST is malformed you will get all kinds of compiler or runtime errors that are horrible to debug. Always make sure you are using the nodes you create correctly. The API documentation below shows which nodes exist and how to use them.

The following example implements a cache tag for Jinja by using the cachelib library:

And here is how you use it in an environment:

Inside the template it’s then possible to mark blocks as cacheable. The following example caches a sidebar for 300 seconds:

The following example demonstrates using Extension.filter_stream() to parse calls to the _() gettext function inline with static data without needing Jinja blocks.

It requires the i18n extension to be loaded and configured.

Extensions always have to extend the jinja2.ext.Extension class:

Extensions can be used to add extra functionality to the Jinja template system at the parser level. Custom extensions are bound to an environment but may not store environment specific data on self. The reason for this is that an extension can be bound to another environment (for overlays) by creating a copy and reassigning the environment attribute.

As extensions are created by the environment they cannot accept any arguments for configuration. One may want to work around that by using a factory function, but that is not possible as extensions are identified by their import name. The correct way to configure the extension is storing the configuration values on the environment. Because this way the environment ends up acting as central configuration storage the attributes may clash which is why extensions have to ensure that the names they choose for configuration are not too generic. prefix for example is a terrible name, fragment_cache_prefix on the other hand is a good name as includes the name of the extension (fragment cache).

environment (Environment)

The identifier of the extension. This is always the true import name of the extension class and must not be changed.

If the extension implements custom tags this is a set of tag names the extension is listening for.

This method is called before the actual lexing and can be used to preprocess the source. The filename is optional. The return value must be the preprocessed source.

filename (str | None)

It’s passed a TokenStream that can be used to filter tokens returned. This method has to return an iterable of Tokens, but it doesn’t have to return a TokenStream.

TokenStream | Iterable[Token]

If any of the tags matched this method is called with the parser as first argument. The token the parser stream is pointing at is the name token that matched. This method has to return one or a list of multiple nodes.

Return an attribute node for the current extension. This is useful to pass constants on extensions to generated template code.

Call a method of the extension. This is a shortcut for attr() + jinja2.nodes.Call.

args (List[Expr] | None)

kwargs (List[Keyword] | None)

dyn_args (Expr | None)

dyn_kwargs (Expr | None)

The parser passed to Extension.parse() provides ways to parse expressions of different types. The following methods may be used by extensions:

This is the central parsing class Jinja uses. It’s passed to extensions and can be used to parse expressions or statements.

environment (Environment)

filename (str | None)

The filename of the template the parser processes. This is not the load name of the template. For the load name see name. For templates that were not loaded form the file system this is None.

The load name of the template.

The current TokenStream

Convenience method that raises exc with the message, passed line number or last line number as well as the current name and filename.

exc (Type[TemplateSyntaxError])

Return a new free identifier as InternalName.

Parse multiple statements into a list until one of the end tokens is reached. This is used to parse the body of statements as it also parses template data if appropriate. The parser checks first if the current token is a colon and skips it if there is one. Then it checks for the block end and parses until if one of the end_tokens is reached. Per default the active token in the stream at the end of the call is the matched end token. If this is not wanted drop_needle can be set to True and the end token is removed.

end_tokens (Tuple[str, ...])

Parse an assignment target. As Jinja allows assignments to tuples, this function can parse all allowed assignment targets. Per default assignments to tuples are parsed, that can be disable however by setting with_tuple to False. If only assignments to names are wanted name_only can be set to True. The extra_end_rules parameter is forwarded to the tuple parsing function. If with_namespace is enabled, a namespace assignment may be parsed.

extra_end_rules (Tuple[str, ...] | None)

with_namespace (bool)

Parse an expression. Per default all expressions are parsed, if the optional with_condexpr parameter is set to False conditional expressions are not parsed.

Works like parse_expression but if multiple expressions are delimited by a comma a Tuple node is created. This method could also return a regular expression instead of a tuple if no commas where found.

The default parsing mode is a full tuple. If simplified is True only names and literals are parsed; with_namespace allows namespace attr refs as well. The no_condexpr parameter is forwarded to parse_expression().

Because tuples do not require delimiters and may end in a bogus comma an extra hint is needed that marks the end of a tuple. For example for loops support tuples between for and in. In that case the extra_end_rules is set to ['name:in'].

explicit_parentheses is true if the parsing was triggered by an expression in parentheses. This is used to figure out if an empty tuple is a valid expression or not.

extra_end_rules (Tuple[str, ...] | None)

explicit_parentheses (bool)

with_namespace (bool)

A token stream is an iterable that yields Tokens. The parser however does not iterate over it but calls next() to go one token ahead. The current active token is stored as current.

generator (Iterable[Token])

filename (str | None)

Are we at the end of the stream?

Push a token back to the stream.

Look at the next token.

Perform the token test and return the token if it matched. Otherwise the return value is None.

Like next_if() but only returns True or False.

Go one token ahead and return the old one.

Use the built-in next() instead of calling this directly.

Expect a given token type and return it. This accepts the same argument as jinja2.lexer.Token.test().

The line number of the token

The type of the token. This string is interned so you may compare it with arbitrary strings using the is operator.

The value of the token.

Test a token against a token expression. This can either be a token type or 'token_type:token_value'. This can only test against string values and types.

Test against multiple token expressions.

There is also a utility function in the lexer module that can count newline characters in strings:

Count the number of newline characters in the string. This is useful for extensions that filter a stream.

The AST (Abstract Syntax Tree) is used to represent a template after parsing. It’s build of nodes that the compiler then converts into executable Python code objects. Extensions that provide custom statements can return nodes to execute custom Python code.

The list below describes all nodes that are currently available. The AST may change between Jinja versions but will stay backwards compatible.

For more information have a look at the repr of jinja2.Environment.parse().

Baseclass for all Jinja nodes. There are a number of nodes available of different types. There are four major types:

Template: the outermost wrapper node

All nodes have fields and attributes. Fields may be other nodes, lists, or arbitrary values. Fields are passed to the constructor as regular positional arguments, attributes as keyword arguments. Each node has two attributes: lineno (the line number of the node) and environment. The environment attribute is set at the end of the parsing process for all nodes automatically.

This method iterates over all fields that are defined and yields (key, value) tuples. Per default all fields are returned, but it’s possible to limit that to some fields by providing the only parameter or to exclude some using the exclude parameter. Both should be sets or tuples of field names.

exclude (Container[str] | None)

only (Container[str] | None)

Iterator[Tuple[str, Any]]

Iterates over all direct child nodes of the node. This iterates over all fields and yields the values of they are nodes. If the value of a field is a list all the nodes in that list are returned.

exclude (Container[str] | None)

only (Container[str] | None)

Find the first node of a given type. If no such node exists the return value is None.

node_type (Type[_NodeBound])

Find all the nodes of a given type. If the type is a tuple, the check is performed for any of the tuple items.

node_type (Type[_NodeBound] | Tuple[Type[_NodeBound], ...])

Reset the context of a node and all child nodes. Per default the parser will all generate nodes that have a ‘load’ context as it’s the most common one. This method is used in the parser to set assignment targets and other nodes to a store context.

Set the line numbers of the node and children.

Set the environment for all nodes.

environment (Environment)

Baseclass for all expressions.

Return the value of the expression as constant or raise Impossible if this was not possible.

An EvalContext can be provided, if none is given a default context is created which requires the nodes to have an attached environment.

Changed in version 2.4: the eval_ctx parameter was added.

eval_ctx (EvalContext | None)

Check if it’s possible to assign something to this node.

Apply a filter to an expression. name is the name of the filter, the other fields are the same as Call.

If node is None, the filter is being used in a filter block and is applied to the content of the block.

Apply a test to an expression. name is the name of the test, the other field are the same as Call.

Changed in version 3.0: as_const shares the same logic for filters and tests. Tests check for volatile, async, and @pass_context etc. decorators.

Baseclass for all binary expressions.

Add the left to the right node.

Divides the left by the right node.

Divides the left by the right node and converts the result into an integer by truncating.

Multiplies the left with the right node.

Left to the power of right.

Subtract the right from the left node.

Calls an expression. args is a list of arguments, kwargs a list of keyword arguments (list of Keyword nodes), and dyn_args and dyn_kwargs has to be either None or a node that is used as node for dynamic positional (*args) or keyword (**kwargs) arguments.

Compares an expression with some other expressions. ops must be a list of Operands.

Concatenates the list of expressions provided after converting them to strings.

A conditional expression (inline if expression). ({{ foo if bar else baz }})

Returns the current template context. It can be used like a Name node, with a 'load' ctx and will return the current Context object.

Here an example that assigns the current template name to a variable named foo:

This is basically equivalent to using the pass_context() decorator when using the high-level API, which causes a reference to the context to be passed as the first argument to a function.

Return the current template context including locals. Behaves exactly like ContextReference, but includes local variables, such as from a for loop.

Added in version 2.11.

Loads an attribute from the environment object. This is useful for extensions that want to call a callback stored on the environment.

Returns the attribute of an extension bound to the environment. The identifier is the identifier of the Extension.

This node is usually constructed by calling the attr() method on an extension.

Get an attribute or item from an expression that is a ascii-only bytestring and prefer the attribute.

Get an attribute or item from an expression and prefer the item.

If created with an import name the import name is returned on node access. For example ImportedName('cgi.escape') returns the escape function from the cgi module on evaluation. Imports are optimized by the compiler so there is no need to assign them to local variables.

An internal name in the compiler. You cannot create these nodes yourself but the parser provides a free_identifier() method that creates a new identifier for you. This identifier is not available from the template and is not treated specially by the compiler.

Baseclass for literals.

All constant values. The parser will return this node for simple constants such as 42 or "foo" but it can be used to store more complex values such as lists too. Only constants with a safe representation (objects where eval(repr(x)) == x is true).

Any dict literal such as {1: 2, 3: 4}. The items must be a list of Pair nodes.

Any list literal such as [1, 2, 3]

A constant template string.

For loop unpacking and some other things like multiple arguments for subscripts. Like for Name ctx specifies if the tuple is used for loading the names or storing.

Mark the wrapped expression as safe (wrap it as Markup).

Mark the wrapped expression as safe (wrap it as Markup) but only if autoescaping is active.

Added in version 2.5.

Looks up a name or stores a value in a name. The ctx of the node can be one of the following values:

store: store a value in the name

param: like store but if the name was defined as function parameter.

Reference to a namespace value assignment

Represents a slice object. This must only be used as argument for Subscript.

Baseclass for all unary expressions.

Make the expression negative.

Negate the expression.

Make the expression positive (noop for most expressions)

Nodes that exist in a specific context only.

A key, value pair for keyword arguments where key is a string.

Holds an operator and an expression.

A key, value pair for dicts.

Base node for all statements.

Assigns an expression to a target.

Assigns a block to a target.

A node that represents a block.

Changed in version 3.0.0: the required field was added.

Like a macro without a name but a call instead. call is called with the unnamed macro as caller argument this node holds.

Modifies the eval context. For each option that should be modified, a Keyword has to be added to the options list.

Example to change the autoescape setting:

Modifies the eval context and reverts it later. Works exactly like EvalContextModifier but will only modify the EvalContext for nodes in the body.

A statement that evaluates an expression and discards the result.

Represents an extends statement.

Node for filter sections.

The for loop. target is the target for the iteration (usually a Name or Tuple), iter the iterable. body is a list of nodes that are used as loop-body, and else_ a list of nodes for the else block. If no else node exists it has to be an empty list.

For filtered nodes an expression can be stored as test, otherwise None.

A node that represents the from import tag. It’s important to not pass unsafe names to the name attribute. The compiler translates the attribute lookups directly into getattr calls and does not use the subscript callback of the interface. As exported variables may not start with double underscores (which the parser asserts) this is not a problem for regular Jinja code, but if this node is used in an extension extra care must be taken.

The list of names may contain tuples if aliases are wanted.

If test is true, body is rendered, else else_.

A node that represents the import tag.

A node that represents the include tag.

A macro definition. name is the name of the macro, args a list of arguments and defaults a list of defaults if there are any. body is a list of nodes for the macro body.

A node that holds multiple expressions which are then printed out. This is used both for the print statement and the regular template data.

An overlay scope for extensions. This is a largely unoptimized scope that however can be used to introduce completely arbitrary variables into a sub scope from a dictionary or dictionary like object. The context field has to evaluate to a dictionary object.

Added in version 2.10.

Specific node for with statements. In older versions of Jinja the with statement was implemented on the base of the Scope node instead.

Added in version 2.9.3.

Node that represents a template. This must be the outermost node that is passed to the compiler.

Raised if the node could not perform a requested action.

---

## Frequently Asked Questions — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/faq/

**Contents:**
- Frequently Asked Questions¶
- Why is it called Jinja?¶
- How fast is Jinja?¶
- Isn’t it a bad idea to put logic in templates?¶
- Why is HTML escaping not the default?¶

“Jinja” is a Japanese Shinto shrine, or temple, and temple and template share a similar English pronunciation. It is not named after the city in Uganda.

Jinja is relatively fast among template engines because it compiles and caches template code to Python code, so that the template does not need to be parsed and interpreted each time. Rendering a template becomes as close to executing a Python function as possible.

Jinja also makes extensive use of caching. Templates are cached by name after loading, so future uses of the template avoid loading. The template loading itself uses a bytecode cache to avoid repeated compiling. The caches can be external to persist across restarts. Templates can also be precompiled and loaded as fast Python imports.

We dislike benchmarks because they don’t reflect real use. Performance depends on many factors. Different engines have different default configurations and tradeoffs that make it unclear how to set up a useful comparison. Often, database access, API calls, and data processing have a much larger effect on performance than the template engine.

Without a doubt you should try to remove as much logic from templates as possible. With less logic, the template is easier to understand, has fewer potential side effects, and is faster to compile and render. But a template without any logic means processing must be done in code before rendering. A template engine that does that is shipped with Python, called string.Template, and while it’s definitely fast it’s not convenient.

Jinja’s features such as blocks, statements, filters, and function calls make it much easier to write expressive templates, with very few restrictions. Jinja doesn’t allow arbitrary Python code in templates, or every feature available in the Python language. This keeps the engine easier to maintain, and keeps templates more readable.

Some amount of logic is required in templates to keep everyone happy. Too much logic in the template can make it complex to reason about and maintain. It’s up to you to decide how your application will work and balance how much logic you want to put in the template.

Jinja provides a feature that can be enabled to escape HTML syntax in rendered templates. However, it is disabled by default.

Jinja is a general purpose template engine, it is not only used for HTML documents. You can generate plain text, LaTeX, emails, CSS, JavaScript, configuration files, etc. HTML escaping wouldn’t make sense for any of these document types.

While automatic escaping means that you are less likely have an XSS problem, it also requires significant extra processing during compiling and rendering, which can reduce performance. Jinja uses MarkupSafe for escaping, which provides optimized C code for speed, but it still introduces overhead to track escaping across methods and formatting.

---

## Introduction — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/intro/

**Contents:**
- Introduction¶
- Installation¶
  - Dependencies¶
  - Optional Dependencies¶

Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.

Template inheritance and inclusion.

Define and import macros within templates.

HTML templates can use autoescaping to prevent XSS from untrusted user input.

A sandboxed environment can safely render untrusted templates.

Async support for generating templates that automatically handle sync and async functions without extra syntax.

I18N support with Babel.

Templates are compiled to optimized Python code just-in-time and cached, or can be compiled ahead-of-time.

Exceptions point to the correct line in templates to make debugging easier.

Extensible filters, tests, functions, and even syntax.

Jinja’s philosophy is that while application logic belongs in Python if possible, it shouldn’t make the template designer’s job difficult by restricting functionality too much.

We recommend using the latest version of Python. Jinja supports Python 3.7 and newer. We also recommend using a virtual environment in order to isolate your project dependencies from other projects and the system.

Install the most recent Jinja version using pip:

These will be installed automatically when installing Jinja.

MarkupSafe escapes untrusted input when rendering templates to avoid injection attacks.

These distributions will not be installed automatically.

Babel provides translation support in templates.

---

## Extensions — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/extensions/

**Contents:**
- Extensions¶
- Adding Extensions¶
- i18n Extension¶
  - Environment Methods¶
  - Whitespace Trimming¶
  - New Style Gettext¶
- Expression Statement¶
- Loop Controls¶
- With Statement¶
- Autoescape Extension¶

Jinja supports extensions that can add extra filters, tests, globals or even extend the parser. The main motivation of extensions is to move often used code into a reusable class like adding support for internationalization.

Extensions are added to the Jinja environment at creation time. To add an extension pass a list of extension classes or import paths to the extensions parameter of the Environment constructor. The following example creates a Jinja environment with the i18n extension loaded:

To add extensions after creation time, use the add_extension() method:

Import name: jinja2.ext.i18n

The i18n extension can be used in combination with gettext or Babel. When it’s enabled, Jinja provides a trans statement that marks a block as translatable and calls gettext.

After enabling, an application has to provide functions for gettext, ngettext, and optionally pgettext and npgettext, either globally or when rendering. A _() function is added as an alias to the gettext function.

A convenient way to provide these functions is to call one of the below methods depending on the translation system in use. If you do not require actual translation, use Environment.install_null_translations to install no-op functions.

After enabling the extension, the environment provides the following additional methods:

Installs a translation globally for the environment. The translations object must implement gettext, ngettext, and optionally pgettext and npgettext. gettext.NullTranslations, gettext.GNUTranslations, and Babels Translations are supported.

Changed in version 3.0: Added pgettext and npgettext.

Changed in version 2.5: Added new-style gettext support.

Install no-op gettext functions. This is useful if you want to prepare the application for internationalization but don’t want to implement the full system yet.

Changed in version 2.5: Added new-style gettext support.

Install the given gettext, ngettext, pgettext, and npgettext callables into the environment. They should behave exactly like gettext.gettext(), gettext.ngettext(), gettext.pgettext() and gettext.npgettext().

If newstyle is activated, the callables are wrapped to work like newstyle callables. See New Style Gettext for more information.

Changed in version 3.0: Added pgettext and npgettext.

Added in version 2.5: Added new-style gettext support.

Uninstall the environment’s globally installed translation.

Extract localizable strings from the given template node or source.

For every string found this function yields a (lineno, function, message) tuple, where:

lineno is the number of the line on which the string was found.

function is the name of the gettext function used (if the string was extracted from embedded Python code).

message is the string itself, or a tuple of strings for functions with multiple arguments.

If Babel is installed, see Babel to extract the strings.

For a web application that is available in multiple languages but gives all the users the same language (for example, multilingual forum software installed for a French community), the translation may be installed when the environment is created.

The get_gettext_translations function would return the translator for the current configuration, for example by using gettext.find.

The usage of the i18n extension for template designers is covered in the template documentation.

Added in version 2.10.

Within {% trans %} blocks, it can be useful to trim line breaks and whitespace so that the block of text looks like a simple string with single spaces in the translation file.

Linebreaks and surrounding whitespace can be automatically trimmed by enabling the ext.i18n.trimmed policy.

Added in version 2.5.

New style gettext calls are less to type, less error prone, and support autoescaping better.

You can use “new style” gettext calls by setting env.newstyle_gettext = True or passing newstyle=True to env.install_translations. They are fully supported by the Babel extraction tool, but might not work as expected with other extraction tools.

With standard gettext calls, string formatting is a separate step done with the |format filter. This requires duplicating work for ngettext calls.

New style gettext make formatting part of the call, and behind the scenes enforce more consistency.

The advantages of newstyle gettext are:

There’s no separate formatting step, you don’t have to remember to use the |format filter.

Only named placeholders are allowed. This solves a common problem translators face because positional placeholders can’t switch positions meaningfully. Named placeholders always carry semantic information about what value goes where.

String formatting is used even if no placeholders are used, which makes all strings use a consistent format. Remember to escape any raw percent signs as %%, such as 100%%.

The translated string is marked safe, formatting performs escaping as needed. Mark a parameter as |safe if it has already been escaped.

Import name: jinja2.ext.do

The “do” aka expression-statement extension adds a simple do tag to the template engine that works like a variable expression but ignores the return value.

Import name: jinja2.ext.loopcontrols

This extension adds support for break and continue in loops. After enabling, Jinja provides those two keywords which work exactly like in Python.

Import name: jinja2.ext.with_

Changed in version 2.9: This extension is now built-in and no longer does anything.

Import name: jinja2.ext.autoescape

Changed in version 2.9: This extension was removed and is now built-in. Enabling the extension no longer does anything.

Import name: jinja2.ext.debug

Adds a {% debug %} tag to dump the current context as well as the available filters and tests. This is useful to see what’s available to use in the template without setting up a debugger.

By writing extensions you can add custom tags to Jinja. This is a non-trivial task and usually not needed as the default tags and expressions cover all common use cases. The i18n extension is a good example of why extensions are useful. Another one would be fragment caching.

When writing extensions you have to keep in mind that you are working with the Jinja template compiler which does not validate the node tree you are passing to it. If the AST is malformed you will get all kinds of compiler or runtime errors that are horrible to debug. Always make sure you are using the nodes you create correctly. The API documentation below shows which nodes exist and how to use them.

The following example implements a cache tag for Jinja by using the cachelib library:

And here is how you use it in an environment:

Inside the template it’s then possible to mark blocks as cacheable. The following example caches a sidebar for 300 seconds:

The following example demonstrates using Extension.filter_stream() to parse calls to the _() gettext function inline with static data without needing Jinja blocks.

It requires the i18n extension to be loaded and configured.

Extensions always have to extend the jinja2.ext.Extension class:

Extensions can be used to add extra functionality to the Jinja template system at the parser level. Custom extensions are bound to an environment but may not store environment specific data on self. The reason for this is that an extension can be bound to another environment (for overlays) by creating a copy and reassigning the environment attribute.

As extensions are created by the environment they cannot accept any arguments for configuration. One may want to work around that by using a factory function, but that is not possible as extensions are identified by their import name. The correct way to configure the extension is storing the configuration values on the environment. Because this way the environment ends up acting as central configuration storage the attributes may clash which is why extensions have to ensure that the names they choose for configuration are not too generic. prefix for example is a terrible name, fragment_cache_prefix on the other hand is a good name as includes the name of the extension (fragment cache).

environment (Environment)

The identifier of the extension. This is always the true import name of the extension class and must not be changed.

If the extension implements custom tags this is a set of tag names the extension is listening for.

This method is called before the actual lexing and can be used to preprocess the source. The filename is optional. The return value must be the preprocessed source.

filename (str | None)

It’s passed a TokenStream that can be used to filter tokens returned. This method has to return an iterable of Tokens, but it doesn’t have to return a TokenStream.

TokenStream | Iterable[Token]

If any of the tags matched this method is called with the parser as first argument. The token the parser stream is pointing at is the name token that matched. This method has to return one or a list of multiple nodes.

Return an attribute node for the current extension. This is useful to pass constants on extensions to generated template code.

Call a method of the extension. This is a shortcut for attr() + jinja2.nodes.Call.

args (List[Expr] | None)

kwargs (List[Keyword] | None)

dyn_args (Expr | None)

dyn_kwargs (Expr | None)

The parser passed to Extension.parse() provides ways to parse expressions of different types. The following methods may be used by extensions:

This is the central parsing class Jinja uses. It’s passed to extensions and can be used to parse expressions or statements.

environment (Environment)

filename (str | None)

The filename of the template the parser processes. This is not the load name of the template. For the load name see name. For templates that were not loaded form the file system this is None.

The load name of the template.

The current TokenStream

Convenience method that raises exc with the message, passed line number or last line number as well as the current name and filename.

exc (Type[TemplateSyntaxError])

Return a new free identifier as InternalName.

Parse multiple statements into a list until one of the end tokens is reached. This is used to parse the body of statements as it also parses template data if appropriate. The parser checks first if the current token is a colon and skips it if there is one. Then it checks for the block end and parses until if one of the end_tokens is reached. Per default the active token in the stream at the end of the call is the matched end token. If this is not wanted drop_needle can be set to True and the end token is removed.

end_tokens (Tuple[str, ...])

Parse an assignment target. As Jinja allows assignments to tuples, this function can parse all allowed assignment targets. Per default assignments to tuples are parsed, that can be disable however by setting with_tuple to False. If only assignments to names are wanted name_only can be set to True. The extra_end_rules parameter is forwarded to the tuple parsing function. If with_namespace is enabled, a namespace assignment may be parsed.

extra_end_rules (Tuple[str, ...] | None)

with_namespace (bool)

Parse an expression. Per default all expressions are parsed, if the optional with_condexpr parameter is set to False conditional expressions are not parsed.

Works like parse_expression but if multiple expressions are delimited by a comma a Tuple node is created. This method could also return a regular expression instead of a tuple if no commas where found.

The default parsing mode is a full tuple. If simplified is True only names and literals are parsed; with_namespace allows namespace attr refs as well. The no_condexpr parameter is forwarded to parse_expression().

Because tuples do not require delimiters and may end in a bogus comma an extra hint is needed that marks the end of a tuple. For example for loops support tuples between for and in. In that case the extra_end_rules is set to ['name:in'].

explicit_parentheses is true if the parsing was triggered by an expression in parentheses. This is used to figure out if an empty tuple is a valid expression or not.

extra_end_rules (Tuple[str, ...] | None)

explicit_parentheses (bool)

with_namespace (bool)

A token stream is an iterable that yields Tokens. The parser however does not iterate over it but calls next() to go one token ahead. The current active token is stored as current.

generator (Iterable[Token])

filename (str | None)

Are we at the end of the stream?

Push a token back to the stream.

Look at the next token.

Perform the token test and return the token if it matched. Otherwise the return value is None.

Like next_if() but only returns True or False.

Go one token ahead and return the old one.

Use the built-in next() instead of calling this directly.

Expect a given token type and return it. This accepts the same argument as jinja2.lexer.Token.test().

The line number of the token

The type of the token. This string is interned so you may compare it with arbitrary strings using the is operator.

The value of the token.

Test a token against a token expression. This can either be a token type or 'token_type:token_value'. This can only test against string values and types.

Test against multiple token expressions.

There is also a utility function in the lexer module that can count newline characters in strings:

Count the number of newline characters in the string. This is useful for extensions that filter a stream.

The AST (Abstract Syntax Tree) is used to represent a template after parsing. It’s build of nodes that the compiler then converts into executable Python code objects. Extensions that provide custom statements can return nodes to execute custom Python code.

The list below describes all nodes that are currently available. The AST may change between Jinja versions but will stay backwards compatible.

For more information have a look at the repr of jinja2.Environment.parse().

Baseclass for all Jinja nodes. There are a number of nodes available of different types. There are four major types:

Template: the outermost wrapper node

All nodes have fields and attributes. Fields may be other nodes, lists, or arbitrary values. Fields are passed to the constructor as regular positional arguments, attributes as keyword arguments. Each node has two attributes: lineno (the line number of the node) and environment. The environment attribute is set at the end of the parsing process for all nodes automatically.

This method iterates over all fields that are defined and yields (key, value) tuples. Per default all fields are returned, but it’s possible to limit that to some fields by providing the only parameter or to exclude some using the exclude parameter. Both should be sets or tuples of field names.

exclude (Container[str] | None)

only (Container[str] | None)

Iterator[Tuple[str, Any]]

Iterates over all direct child nodes of the node. This iterates over all fields and yields the values of they are nodes. If the value of a field is a list all the nodes in that list are returned.

exclude (Container[str] | None)

only (Container[str] | None)

Find the first node of a given type. If no such node exists the return value is None.

node_type (Type[_NodeBound])

Find all the nodes of a given type. If the type is a tuple, the check is performed for any of the tuple items.

node_type (Type[_NodeBound] | Tuple[Type[_NodeBound], ...])

Reset the context of a node and all child nodes. Per default the parser will all generate nodes that have a ‘load’ context as it’s the most common one. This method is used in the parser to set assignment targets and other nodes to a store context.

Set the line numbers of the node and children.

Set the environment for all nodes.

environment (Environment)

Baseclass for all expressions.

Return the value of the expression as constant or raise Impossible if this was not possible.

An EvalContext can be provided, if none is given a default context is created which requires the nodes to have an attached environment.

Changed in version 2.4: the eval_ctx parameter was added.

eval_ctx (EvalContext | None)

Check if it’s possible to assign something to this node.

Apply a filter to an expression. name is the name of the filter, the other fields are the same as Call.

If node is None, the filter is being used in a filter block and is applied to the content of the block.

Apply a test to an expression. name is the name of the test, the other field are the same as Call.

Changed in version 3.0: as_const shares the same logic for filters and tests. Tests check for volatile, async, and @pass_context etc. decorators.

Baseclass for all binary expressions.

Add the left to the right node.

Divides the left by the right node.

Divides the left by the right node and converts the result into an integer by truncating.

Multiplies the left with the right node.

Left to the power of right.

Subtract the right from the left node.

Calls an expression. args is a list of arguments, kwargs a list of keyword arguments (list of Keyword nodes), and dyn_args and dyn_kwargs has to be either None or a node that is used as node for dynamic positional (*args) or keyword (**kwargs) arguments.

Compares an expression with some other expressions. ops must be a list of Operands.

Concatenates the list of expressions provided after converting them to strings.

A conditional expression (inline if expression). ({{ foo if bar else baz }})

Returns the current template context. It can be used like a Name node, with a 'load' ctx and will return the current Context object.

Here an example that assigns the current template name to a variable named foo:

This is basically equivalent to using the pass_context() decorator when using the high-level API, which causes a reference to the context to be passed as the first argument to a function.

Return the current template context including locals. Behaves exactly like ContextReference, but includes local variables, such as from a for loop.

Added in version 2.11.

Loads an attribute from the environment object. This is useful for extensions that want to call a callback stored on the environment.

Returns the attribute of an extension bound to the environment. The identifier is the identifier of the Extension.

This node is usually constructed by calling the attr() method on an extension.

Get an attribute or item from an expression that is a ascii-only bytestring and prefer the attribute.

Get an attribute or item from an expression and prefer the item.

If created with an import name the import name is returned on node access. For example ImportedName('cgi.escape') returns the escape function from the cgi module on evaluation. Imports are optimized by the compiler so there is no need to assign them to local variables.

An internal name in the compiler. You cannot create these nodes yourself but the parser provides a free_identifier() method that creates a new identifier for you. This identifier is not available from the template and is not treated specially by the compiler.

Baseclass for literals.

All constant values. The parser will return this node for simple constants such as 42 or "foo" but it can be used to store more complex values such as lists too. Only constants with a safe representation (objects where eval(repr(x)) == x is true).

Any dict literal such as {1: 2, 3: 4}. The items must be a list of Pair nodes.

Any list literal such as [1, 2, 3]

A constant template string.

For loop unpacking and some other things like multiple arguments for subscripts. Like for Name ctx specifies if the tuple is used for loading the names or storing.

Mark the wrapped expression as safe (wrap it as Markup).

Mark the wrapped expression as safe (wrap it as Markup) but only if autoescaping is active.

Added in version 2.5.

Looks up a name or stores a value in a name. The ctx of the node can be one of the following values:

store: store a value in the name

param: like store but if the name was defined as function parameter.

Reference to a namespace value assignment

Represents a slice object. This must only be used as argument for Subscript.

Baseclass for all unary expressions.

Make the expression negative.

Negate the expression.

Make the expression positive (noop for most expressions)

Nodes that exist in a specific context only.

A key, value pair for keyword arguments where key is a string.

Holds an operator and an expression.

A key, value pair for dicts.

Base node for all statements.

Assigns an expression to a target.

Assigns a block to a target.

A node that represents a block.

Changed in version 3.0.0: the required field was added.

Like a macro without a name but a call instead. call is called with the unnamed macro as caller argument this node holds.

Modifies the eval context. For each option that should be modified, a Keyword has to be added to the options list.

Example to change the autoescape setting:

Modifies the eval context and reverts it later. Works exactly like EvalContextModifier but will only modify the EvalContext for nodes in the body.

A statement that evaluates an expression and discards the result.

Represents an extends statement.

Node for filter sections.

The for loop. target is the target for the iteration (usually a Name or Tuple), iter the iterable. body is a list of nodes that are used as loop-body, and else_ a list of nodes for the else block. If no else node exists it has to be an empty list.

For filtered nodes an expression can be stored as test, otherwise None.

A node that represents the from import tag. It’s important to not pass unsafe names to the name attribute. The compiler translates the attribute lookups directly into getattr calls and does not use the subscript callback of the interface. As exported variables may not start with double underscores (which the parser asserts) this is not a problem for regular Jinja code, but if this node is used in an extension extra care must be taken.

The list of names may contain tuples if aliases are wanted.

If test is true, body is rendered, else else_.

A node that represents the import tag.

A node that represents the include tag.

A macro definition. name is the name of the macro, args a list of arguments and defaults a list of defaults if there are any. body is a list of nodes for the macro body.

A node that holds multiple expressions which are then printed out. This is used both for the print statement and the regular template data.

An overlay scope for extensions. This is a largely unoptimized scope that however can be used to introduce completely arbitrary variables into a sub scope from a dictionary or dictionary like object. The context field has to evaluate to a dictionary object.

Added in version 2.10.

Specific node for with statements. In older versions of Jinja the with statement was implemented on the base of the Scope node instead.

Added in version 2.9.3.

Node that represents a template. This must be the outermost node that is passed to the compiler.

Raised if the node could not perform a requested action.

---

## Introduction — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/intro/

**Contents:**
- Introduction¶
- Installation¶
  - Dependencies¶
  - Optional Dependencies¶

Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.

Template inheritance and inclusion.

Define and import macros within templates.

HTML templates can use autoescaping to prevent XSS from untrusted user input.

A sandboxed environment can safely render untrusted templates.

Async support for generating templates that automatically handle sync and async functions without extra syntax.

I18N support with Babel.

Templates are compiled to optimized Python code just-in-time and cached, or can be compiled ahead-of-time.

Exceptions point to the correct line in templates to make debugging easier.

Extensible filters, tests, functions, and even syntax.

Jinja’s philosophy is that while application logic belongs in Python if possible, it shouldn’t make the template designer’s job difficult by restricting functionality too much.

We recommend using the latest version of Python. Jinja supports Python 3.7 and newer. We also recommend using a virtual environment in order to isolate your project dependencies from other projects and the system.

Install the most recent Jinja version using pip:

These will be installed automatically when installing Jinja.

MarkupSafe escapes untrusted input when rendering templates to avoid injection attacks.

These distributions will not be installed automatically.

Babel provides translation support in templates.

---

## Tips and Tricks — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/tricks/

**Contents:**
- Tips and Tricks¶
- Null-Default Fallback¶
- Alternating Rows¶
- Highlighting Active Menu Items¶
- Accessing the parent Loop¶

This part of the documentation shows some tips and tricks for Jinja templates.

Jinja supports dynamic inheritance and does not distinguish between parent and child template as long as no extends tag is visited. While this leads to the surprising behavior that everything before the first extends tag including whitespace is printed out instead of being ignored, it can be used for a neat trick.

Usually child templates extend from one template that adds a basic HTML skeleton. However it’s possible to put the extends tag into an if tag to only extend from the layout template if the standalone variable evaluates to false, which it does by default if it’s not defined. Additionally a very basic skeleton is added to the file so that if it’s indeed rendered with standalone set to True a very basic HTML skeleton is added:

If you want to have different styles for each row of a table or list you can use the cycle method on the loop object:

cycle can take an unlimited number of strings. Each time this tag is encountered the next item from the list is rendered.

Often you want to have a navigation bar with an active navigation item. This is really simple to achieve. Because assignments outside of blocks in child templates are global and executed before the layout template is evaluated it’s possible to define the active menu item in the child template:

The layout template can then access active_page. Additionally it makes sense to define a default for that variable:

The special loop variable always points to the innermost loop. If it’s desired to have access to an outer loop it’s possible to alias it:

---

## Changes — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/changes/

**Contents:**
- Changes¶
- Version 3.1.6¶
- Version 3.1.5¶
- Version 3.1.4¶
- Version 3.1.3¶
- Version 3.1.2¶
- Version 3.1.1¶
- Version 3.1.0¶
- Version 3.0.3¶
- Version 3.0.2¶

The |attr filter does not bypass the environment’s attribute lookup, allowing the sandbox to apply its checks. GHSA-cpwx-vrp4-4pq7

The sandboxed environment handles indirect calls to str.format, such as by passing a stored reference to a filter that calls its argument. GHSA-q2x7-8rv6-6q7h

Escape template name before formatting it into error messages, to avoid issues with names that contain f-string syntax. #1792, GHSA-gmj6-6f8f-6699

Sandbox does not allow clear and pop on known mutable sequence types. #2032

Calling sync render for an async template uses asyncio.run. #1952

Avoid unclosed auto_aiter warnings. #1960

Return an aclose-able AsyncGenerator from Template.generate_async. #1960

Avoid leaving root_render_func() unclosed in Template.generate_async. #1960

Avoid leaving async generators unclosed in blocks, includes and extends. #1960

The runtime uses the correct concat function for the current environment when calling block references. #1701

Make |unique async-aware, allowing it to be used after another async-aware filter. #1781

|int filter handles OverflowError from scientific notation. #1921

Make compiling deterministic for tuple unpacking in a {% set ... %} call. #2021

Fix dunder protocol (copy/pickle/etc) interaction with Undefined objects. #2025

Fix copy/pickle support for the internal missing object. #2027

Environment.overlay(enable_async) is applied correctly. #2061

The error message from FileSystemLoader includes the paths that were searched. #1661

PackageLoader shows a clearer error message when the package does not contain the templates directory. #1705

Improve annotations for methods returning copies. #1880

urlize does not add mailto: to values like @a@b. #1870

Tests decorated with @pass_context` can be used with the |select filter. #1624

Using set for multiple assignment (a, b = 1, 2) does not fail when the target is a namespace attribute. #1413

Using set in all branches of {% if %}{% elif %}{% else %} blocks does not cause the variable to be considered initially undefined. #1253

The xmlattr filter does not allow keys with / solidus, > greater-than sign, or = equals sign, in addition to disallowing spaces. Regardless of any validation done by Jinja, user input should never be used as keys to this filter, or must be separately validated first. GHSA-h75v-3vvj-5mfj

Fix compiler error when checking if required blocks in parent templates are empty. #1858

xmlattr filter does not allow keys with spaces. GHSA-h5c8-rqwp-cp95

Make error messages stemming from invalid nesting of {% trans %} blocks more helpful. #1918

Add parameters to Environment.overlay to match __init__. #1645

Handle race condition in FileSystemBytecodeCache. #1654

The template filename on Windows uses the primary path separator. #1637

Drop support for Python 3.6. #1534

Remove previously deprecated code. #1544

WithExtension and AutoEscapeExtension are built-in now.

contextfilter and contextfunction are replaced by pass_context. evalcontextfilter and evalcontextfunction are replaced by pass_eval_context. environmentfilter and environmentfunction are replaced by pass_environment.

Markup and escape should be imported from MarkupSafe.

Compiled templates from very old Jinja versions may need to be recompiled.

Legacy resolve mode for Context subclasses is no longer supported. Override resolve_or_missing instead of resolve.

unicode_urlencode is renamed to url_quote.

Add support for native types in macros. #1510

The {% trans %} tag can use pgettext and npgettext by passing a context string as the first token in the tag, like {% trans "title" %}. #1430

Update valid identifier characters from Python 3.6 to 3.7. #1571

Filters and tests decorated with @async_variant are pickleable. #1612

Add items filter. #1561

Subscriptions ([0], etc.) can be used after filters, tests, and calls when the environment is in async mode. #1573

The groupby filter is case-insensitive by default, matching other comparison filters. Added the case_sensitive parameter to control this. #1463

Windows drive-relative path segments in template names will not result in FileSystemLoader and PackageLoader loading from drive-relative paths. #1621

Fix traceback rewriting internals for Python 3.10 and 3.11. #1535

Fix how the native environment treats leading and trailing spaces when parsing values on Python 3.10. #1537

Improve async performance by avoiding checks for common types. #1514

Revert change to hash(Node) behavior. Nodes are hashed by id again #1521

PackageLoader works when the package is a single module file. #1512

Fix a loop scoping bug that caused assignments in nested loops to still be referenced outside of it. #1427

Make compile_templates deterministic for filter and import names. #1452, 1453

Revert an unintended change that caused Undefined to act like StrictUndefined for the in operator. #1448

Imported macros have access to the current template globals in async environments. #1494

PackageLoader will not include a current directory (.) path segment. This allows loading templates from the root of a zip import. #1467

Update MarkupSafe dependency to >= 2.0. #1418

Mark top-level names as exported so type checking understands imports in user projects. #1426

Fix some types that weren’t available in Python 3.6.0. #1433

The deprecation warning for unneeded autoescape and with_ extensions shows more relevant context. #1429

Fixed calling deprecated jinja2.Markup without an argument. Use markupsafe.Markup instead. #1438

Calling sync render for an async template uses asyncio.new_event_loop This fixes a deprecation that Python 3.10 introduces. #1443

Drop support for Python 2.7 and 3.5.

Bump MarkupSafe dependency to >=1.1.

Bump Babel optional dependency to >=2.1.

Remove code that was marked deprecated.

Add type hinting. #1412

Use PEP 451 API to load templates with PackageLoader. #1168

Fix a bug that caused imported macros to not have access to the current template’s globals. #688

Add ability to ignore trim_blocks using +%}. #1036

Fix a bug that caused custom async-only filters to fail with constant input. #1279

Fix UndefinedError incorrectly being thrown on an undefined variable instead of Undefined being returned on NativeEnvironment on Python 3.10. #1335

Blocks can be marked as required. They must be overridden at some point, but not necessarily by the direct child. #1147

Deprecate the autoescape and with extensions, they are built-in to the compiler. #1203

The urlize filter recognizes mailto: links and takes extra_schemes (or env.policies["urlize.extra_schemes"]) to recognize other schemes. It tries to balance parentheses within a URL instead of ignoring trailing characters. The parsing in general has been updated to be more efficient and match more cases. URLs without a scheme are linked as https:// instead of http://. #522, 827, 1172, #1195

Filters that get attributes, such as map and groupby, can use a false or empty value as a default. #1331

Fix a bug that prevented variables set in blocks or loops from being accessed in custom context functions. #768

Fix a bug that caused scoped blocks from accessing special loop variables. #1088

Update the template globals when calling Environment.get_template(globals=...) even if the template was already loaded. #295

Do not raise an error for undefined filters in unexecuted if-statements and conditional expressions. #842

Add is filter and is test tests to test if a name is a registered filter or test. This allows checking if a filter is available in a template before using it. Test functions can be decorated with @pass_environment, @pass_eval_context, or @pass_context. #842, #1248

Support pgettext and npgettext (message contexts) in i18n extension. #441

The |indent filter’s width argument can be a string to indent by. #1167

The parser understands hex, octal, and binary integer literals. #1170

Undefined.__contains__ (in) raises an UndefinedError instead of a TypeError. #1198

Undefined is iterable in an async environment. #1294

NativeEnvironment supports async mode. #1362

Template rendering only treats \n, \r\n and \r as line breaks. Other characters are left unchanged. #769, 952, 1313

|groupby filter takes an optional default argument. #1359

The function and filter decorators have been renamed and unified. The old names are deprecated. #1381

pass_context replaces contextfunction and contextfilter.

pass_eval_context replaces evalcontextfunction and evalcontextfilter

pass_environment replaces environmentfunction and environmentfilter.

Async support no longer requires Jinja to patch itself. It must still be enabled with Environment(enable_async=True). #1390

Overriding Context.resolve is deprecated, override resolve_or_missing instead. #1380

Improve the speed of the urlize filter by reducing regex backtracking. Email matching requires a word character at the start of the domain part, and only word characters in the TLD. #1343

Fix a bug that caused callable objects with __getattr__, like Mock to be treated as a contextfunction(). #1145

Update wordcount filter to trigger Undefined methods by wrapping the input in soft_str(). #1160

Fix a hang when displaying tracebacks on Python 32-bit. #1162

Showing an undefined error for an object that raises AttributeError on access doesn’t cause a recursion error. #1177

Revert changes to PackageLoader from 2.10 which removed the dependency on setuptools and pkg_resources, and added limited support for namespace packages. The changes caused issues when using Pytest. Due to the difficulty in supporting Python 2 and PEP 451 simultaneously, the changes are reverted until 3.0. #1182

Fix line numbers in error messages when newlines are stripped. #1178

The special namespace() assignment object in templates works in async environments. #1180

Fix whitespace being removed before tags in the middle of lines when lstrip_blocks is enabled. #1138

NativeEnvironment doesn’t evaluate intermediate strings during rendering. This prevents early evaluation which could change the value of an expression. #1186

Fix a bug that prevented looking up a key after an attribute ({{ data.items[1:] }}) in an async template. #1141

Drop support for Python 2.6, 3.3, and 3.4. This will be the last version to support Python 2.7 and 3.5.

Added a new ChainableUndefined class to support getitem and getattr on an undefined object. #977

Allow {%+ syntax (with NOP behavior) when lstrip_blocks is disabled. #748

Added a default parameter for the map filter. #557

Exclude environment globals from meta.find_undeclared_variables(). #931

Float literals can be written with scientific notation, like 2.56e-3. #912, #922

Int and float literals can be written with the ‘_’ separator for legibility, like 12_345. #923

Fix a bug causing deadlocks in LRUCache.setdefault. #1000

The trim filter takes an optional string of characters to trim. #828

A new jinja2.ext.debug extension adds a {% debug %} tag to quickly dump the current context and available filters and tests. #174, #798, 983

Lexing templates with large amounts of whitespace is much faster. #857, #858

Parentheses around comparisons are preserved, so {{ 2 * (3 < 5) }} outputs “2” instead of “False”. #755, #938

Add new boolean, false, true, integer and float tests. #824

The environment’s finalize function is only applied to the output of expressions (constant or not), not static template data. #63

When providing multiple paths to FileSystemLoader, a template can have the same name as a directory. #821

Always return Undefined when omitting the else clause in a {{ 'foo' if bar }} expression, regardless of the environment’s undefined class. Omitting the else clause is a valid shortcut and should not raise an error when using StrictUndefined. #710, #1079

Fix behavior of loop control variables such as length and revindex0 when looping over a generator. #459, 751, 794, #993

Async support is only loaded the first time an environment enables it, in order to avoid a slow initial import. #765

In async environments, the |map filter will await the filter call if needed. #913

In for loops that access loop attributes, the iterator is not advanced ahead of the current iteration unless length, revindex, nextitem, or last are accessed. This makes it less likely to break groupby results. #555, #1101

In async environments, the loop attributes length and revindex work for async iterators. #1101

In async environments, values from attribute/property access will be awaited if needed. #1101

PackageLoader doesn’t depend on setuptools or pkg_resources. #970

PackageLoader has limited support for PEP 420 namespace packages. #1097

Support os.PathLike objects in FileSystemLoader and ModuleLoader. #870

NativeTemplate correctly handles quotes between expressions. "'{{ a }}', '{{ b }}'" renders as the tuple ('1', '2') rather than the string '1, 2'. #1020

Creating a NativeTemplate directly creates a NativeEnvironment instead of a default Environment. #1091

After calling LRUCache.copy(), the copy’s queue methods point to the correct queue. #843

Compiling templates always writes UTF-8 instead of defaulting to the system encoding. #889

|wordwrap filter treats existing newlines as separate paragraphs to be wrapped individually, rather than creating short intermediate lines. #175

Add break_on_hyphens parameter to |wordwrap filter. #550

Cython compiled functions decorated as context functions will be passed the context. #1108

When chained comparisons of constants are evaluated at compile time, the result follows Python’s behavior of returning False if any comparison returns False, rather than only the last one. #1102

Tracebacks for exceptions in templates show the correct line numbers and source for Python >= 3.7. #1104

Tracebacks for template syntax errors in Python 3 no longer show internal compiler frames. #763

Add a DerivedContextReference node that can be used by extensions to get the current context and local variables such as loop. #860

Constant folding during compilation is applied to some node types that were previously overlooked. #733

TemplateSyntaxError.source is not empty when raised from an included template. #457

Passing an Undefined value to get_template (such as through extends, import, or include), raises an UndefinedError consistently. select_template will show the undefined message in the list of attempts rather than the empty string. #1037

TemplateSyntaxError can be pickled. #1117

Fix a typo in Babel entry point in setup.py that was preventing installation.

Fix Python 3.7 deprecation warnings.

Using range in the sandboxed environment uses xrange on Python 2 to avoid memory use. #933

Use Python 3.7’s better traceback support to avoid a core dump when using debug builds of Python 3.7. #1050

SandboxedEnvironment securely handles str.format_map in order to prevent code execution through untrusted format strings. The sandbox already handled str.format.

Added a new extension node called OverlayScope which can be used to create an unoptimized scope that will look up all variables from a derived context.

Added an in test that works like the in operator. This can be used in combination with reject and select.

Added previtem and nextitem to loop contexts, providing access to the previous/next item in the loop. If such an item does not exist, the value is undefined.

Added changed(*values) to loop contexts, providing an easy way of checking whether a value has changed since the last iteration (or rather since the last call of the method)

Added a namespace function that creates a special object which allows attribute assignment using the set tag. This can be used to carry data across scopes, e.g. from a loop body to code that comes after the loop.

Added a trimmed modifier to {% trans %} to strip linebreaks and surrounding whitespace. Also added a new policy to enable this for all trans blocks.

The random filter is no longer incorrectly constant folded and will produce a new random choice each time the template is rendered. #478

Added a unique filter. #469

Added min and max filters. #475

Added tests for all comparison operators: eq, ne, lt, le, gt, ge. #665

import statement cannot end with a trailing comma. #617, #618

indent filter will not indent blank lines by default. #685

Add reverse argument for dictsort filter. #692

Add a NativeEnvironment that renders templates to native Python types instead of strings. #708

Added filter support to the block set tag. #489

tojson filter marks output as safe to match documented behavior. #718

Resolved a bug where getting debug locals for tracebacks could modify template context.

Fixed a bug where having many {% elif ... %} blocks resulted in a “too many levels of indentation” error. These blocks now compile to native elif ..: instead of else: if ..: #759

Fixed custom context behavior in fast resolve mode #675

Restored the original repr of the internal _GroupTuple because this caused issues with ansible and it was an unintended change. #654

Added back support for custom contexts that override the old resolve method since it was hard for people to spot that this could cause a regression.

Correctly use the buffer for the else block of for loops. This caused invalid syntax errors to be caused on 2.x and completely wrong behavior on Python 3 #669

Resolve an issue where the {% extends %} tag could not be used with async environments. #668

Reduce memory footprint slightly by reducing our unicode database dump we use for identifier matching on Python 3 #666

Fixed autoescaping not working for macros in async compilation mode. #671

Solved some warnings for string literals. #646

Increment the bytecode cache version which was not done due to an oversight before.

Corrected bad code generation and scoping for filtered loops. #649

Resolved an issue where top-level output silencing after known extend blocks could generate invalid code when blocks where contained in if statements. #651

Made the truncate.leeway default configurable to improve compatibility with older templates.

Restored the use of blocks in macros to the extend that was possible before. On Python 3 it would render a generator repr instead of the block contents. #645

Set a consistent behavior for assigning of variables in inner scopes when the variable is also read from an outer scope. This now sets the intended behavior in all situations however it does not restore the old behavior where limited assignments to outer scopes was possible. For more information and a discussion see #641

Resolved an issue where block scoped would not take advantage of the new scoping rules. In some more exotic cases a variable overridden in a local scope would not make it into a block.

Change the code generation of the with statement to be in line with the new scoping rules. This resolves some unlikely bugs in edge cases. This also introduces a new internal With node that can be used by extensions.

Fixed a regression that caused for loops to not be able to use the same variable for the target as well as source iterator. #640

Add support for a previously unknown behavior of macros. It used to be possible in some circumstances to explicitly provide a caller argument to macros. While badly buggy and unintended it turns out that this is a common case that gets copy pasted around. To not completely break backwards compatibility with the most common cases it’s now possible to provide an explicit keyword argument for caller if it’s given an explicit default. #642

Resolved a regression with call block scoping for macros. Nested caller blocks that used the same identifiers as outer macros could refer to the wrong variable incorrectly.

Released 2017-01-07, codename Derivation

Change cache key definition in environment. This fixes a performance regression introduced in 2.8.

Added support for generator_stop on supported Python versions (Python 3.5 and later)

Corrected a long standing issue with operator precedence of math operations not being what was expected.

Added support for Python 3.6 async iterators through a new async mode.

Added policies for filter defaults and similar things.

Urlize now sets “rel noopener” by default.

Support attribute fallback for old-style classes in 2.x.

Support toplevel set statements in extend situations.

Restored behavior of Cycler for Python 3 users.

Subtraction now follows the same behavior as other operators on undefined values.

map and friends will now give better error messages if you forgot to quote the parameter.

Depend on MarkupSafe 0.23 or higher.

Improved the truncate filter to support better truncation in case the string is barely truncated at all.

Change the logic for macro autoescaping to be based on the runtime autoescaping information at call time instead of macro define time.

Ported a modified version of the tojson filter from Flask to Jinja and hooked it up with the new policy framework.

Block sets are now marked safe by default.

On Python 2 the asciification of ASCII strings can now be disabled with the compiler.ascii_str policy.

Tests now no longer accept an arbitrary expression as first argument but a restricted one. This means that you can now properly use multiple tests in one expression without extra parentheses. In particular you can now write foo is divisibleby 2 or foo is divisibleby 3 as you would expect.

Greatly changed the scoping system to be more consistent with what template designers and developers expect. There is now no more magic difference between the different include and import constructs. Context is now always propagated the same way. The only remaining differences is the defaults for with context and without context.

The with and autoescape tags are now built-in.

Added the new select_autoescape function which helps configuring better autoescaping easier.

Fixed a runtime error in the sandbox when attributes of async generators were accessed.

Fixed the for_qs flag for urlencode.

Fixed regression when applying int to non-string values.

SECURITY: if the sandbox mode is used format expressions are now sandboxed with the same rules as in Jinja. This solves various information leakage problems that can occur with format strings.

Released 2015-07-26, codename Replacement

Added target parameter to urlize function.

Added support for followsymlinks to the file system loader.

The truncate filter now counts the length.

Added equalto filter that helps with select filters.

Changed cache keys to use absolute file names if available instead of load names.

Fixed loop length calculation for some iterators.

Changed how Jinja enforces strings to be native strings in Python 2 to work when people break their default encoding.

Added make_logging_undefined which returns an undefined object that logs failures into a logger.

If unmarshalling of cached data fails the template will be reloaded now.

Implemented a block set tag.

Default cache size was increased to 400 from a low 50.

Fixed is number test to accept long integers in all Python versions.

Changed is number to accept Decimal as a number.

Added a check for default arguments followed by non-default arguments. This change makes {% macro m(x, y=1, z) %} a syntax error. The previous behavior for this code was broken anyway (resulting in the default value being applied to y).

Add ability to use custom subclasses of jinja2.compiler.CodeGenerator and jinja2.runtime.Context by adding two new attributes to the environment (code_generator_class and context_class). #404

Added support for context/environment/evalctx decorator functions on the finalize callback of the environment.

Escape query strings for urlencode properly. Previously slashes were not escaped in that place.

Add ‘base’ parameter to ‘int’ filter.

Security issue: Corrected the security fix for the cache folder. This fix was provided by RedHat.

Prefix loader was not forwarding the locals properly to inner loaders. This is now fixed.

Security issue: Changed the default folder for the filesystem cache to be user specific and read and write protected on UNIX systems. See Debian bug 734747 for more information.

Fixed a bug with call_filter not working properly on environment and context filters.

Fixed lack of Python 3 support for bytecode caches.

Reverted support for defining blocks in included templates as this broke existing templates for users.

Fixed some warnings with hashing of undefineds and nodes if Python is run with warnings for Python 3.

Added support for properly hashing undefined objects.

Fixed a bug with the title filter not working on already uppercase strings.

Released 2013-05-20, codename Translation

Choice and prefix loaders now dispatch source and template lookup separately in order to work in combination with module loaders as advertised.

Fixed filesizeformat.

Added a non-silent option for babel extraction.

Added urlencode filter that automatically quotes values for URL safe usage with utf-8 as only supported encoding. If applications want to change this encoding they can override the filter.

Added keep-trailing-newline configuration to environments and templates to optionally preserve the final trailing newline.

Accessing last on the loop context no longer causes the iterator to be consumed into a list.

Python requirement changed: 2.6, 2.7 or >= 3.3 are required now, supported by same source code, using the “six” compatibility library.

Allow contextfunction and other decorators to be applied to __call__.

Added support for changing from newline to different signs in the wordwrap filter.

Added support for ignoring memcache errors silently.

Added support for keeping the trailing newline in templates.

Added finer grained support for stripping whitespace on the left side of blocks.

Added map, select, reject, selectattr and rejectattr filters.

Added support for loop.depth to figure out how deep inside a recursive loop the code is.

Disabled py_compile for pypy and python 3.

Released 2011-07-24, codename Convolution

Internal attributes now raise an internal attribute error now instead of returning an undefined. This fixes problems when passing undefined objects to Python semantics expecting APIs.

Traceback support now works properly for PyPy. (Tested with 1.4)

Implemented operator intercepting for sandboxed environments. This allows application developers to disable builtin operators for better security. (For instance limit the mathematical operators to actual integers instead of longs)

Groupby filter now supports dotted notation for grouping by attributes of attributes.

Scoped blocks now properly treat toplevel assignments and imports. Previously an import suddenly “disappeared” in a scoped block.

Automatically detect newer Python interpreter versions before loading code from bytecode caches to prevent segfaults on invalid opcodes. The segfault in earlier Jinja versions here was not a Jinja bug but a limitation in the underlying Python interpreter. If you notice Jinja segfaulting in earlier versions after an upgrade of the Python interpreter you don’t have to upgrade, it’s enough to flush the bytecode cache. This just no longer makes this necessary, Jinja will automatically detect these cases now.

The sum filter can now sum up values by attribute. This is a backwards incompatible change. The argument to the filter previously was the optional starting index which defaults to zero. This now became the second argument to the function because it’s rarely used.

Like sum, sort now also makes it possible to order items by attribute.

Like sum and sort, join now also is able to join attributes of objects as string.

The internal eval context now has a reference to the environment.

Added a mapping test to see if an object is a dict or an object with a similar interface.

Built documentation is no longer part of release.

Fixed extensions not loading properly with overlays.

Work around a bug in cpython for the debugger that causes segfaults on 64bit big-endian architectures.

Fixed an operator precedence error introduced in 2.5.2. Statements like “-foo.bar” had their implicit parentheses applied around the first part of the expression (“(-foo).bar”) instead of the more correct “-(foo.bar)”.

Improved setup.py script to better work with assumptions people might still have from it (--with-speedups).

Fixed a packaging error that excluded the new debug support.

StopIteration exceptions raised by functions called from templates are now intercepted and converted to undefineds. This solves a lot of debugging grief. (StopIteration is used internally to abort template execution)

Improved performance of macro calls slightly.

Babel extraction can now properly extract newstyle gettext calls.

Using the variable num in newstyle gettext for something else than the pluralize count will no longer raise a KeyError.

Removed builtin markup class and switched to markupsafe. For backwards compatibility the pure Python implementation still exists but is pulled from markupsafe by the Jinja developers. The debug support went into a separate feature called “debugsupport” and is disabled by default because it is only relevant for Python 2.4

Fixed an issue with unary operators having the wrong precedence.

Released 2010-05-29, codename Incoherence

Improved the sort filter (should have worked like this for a long time) by adding support for case insensitive searches.

Fixed a bug for getattribute constant folding.

Support for newstyle gettext translations which result in a nicer in-template user interface and more consistent catalogs.

It’s now possible to register extensions after an environment was created.

Fixed an error reporting bug for undefined.

Released 2010-04-13, codename Correlation

The environment template loading functions now transparently pass through a template object if it was passed to it. This makes it possible to import or extend from a template object that was passed to the template.

Added a ModuleLoader that can load templates from precompiled sources. The environment now features a method to compile the templates from a configured loader into a zip file or folder.

The _speedups C extension now supports Python 3.

Added support for autoescaping toggling sections and support for evaluation contexts.

Extensions have a priority now.

Fixed an error reporting bug on all python versions

Fixed an error reporting bug on Python 2.4

Released 2010-02-10, codename 3000 Pythons

Fixes issue with code generator that causes unbound variables to be generated if set was used in if-blocks and other small identifier problems.

Include tags are now able to select between multiple templates and take the first that exists, if a list of templates is given.

Fixed a problem with having call blocks in outer scopes that have an argument that is also used as local variable in an inner frame #360.

Greatly improved error message reporting #339

Implicit tuple expressions can no longer be totally empty. This change makes {% if %} a syntax error now. #364

Added support for translator comments if extracted via babel.

Added with-statement extension.

Experimental Python 3 support.

Fixes some smaller problems for Jinja on Jython.

Released 2009-09-13, codename Kong

Include statements can now be marked with ignore missing to skip non existing templates.

Priority of not raised. It’s now possible to write not foo in bar as an alias to foo not in bar like in python. Previously the grammar required parentheses (not (foo in bar)) which was odd.

Fixed a bug that caused syntax errors when defining macros or using the {% call %} tag inside loops.

Fixed a bug in the parser that made {{ foo[1, 2] }} impossible.

Made it possible to refer to names from outer scopes in included templates that were unused in the callers frame #327

Fixed a bug that caused internal errors if names where used as iteration variable and regular variable after the loop if that variable was unused before the loop. #331

Added support for optional scoped modifier to blocks.

Added support for line-comments.

Added the meta module.

Renamed (undocumented) attribute “overlay” to “overlayed” on the environment because it was clashing with a method of the same name.

Speedup extension is now disabled by default.

Fixed a translation error caused by looping over empty recursive loops.

Released 2008-11-23, codename Yasuzō

Fixed a bug with nested loops and the special loop variable. Before the change an inner loop overwrote the loop variable from the outer one after iteration.

Fixed a bug with the i18n extension that caused the explicit pluralization block to look up the wrong variable.

Fixed a limitation in the lexer that made {{ foo.0.0 }} impossible.

Index based subscribing of variables with a constant value returns an undefined object now instead of raising an index error. This was a bug caused by eager optimizing.

The i18n extension looks up foo.ugettext now followed by foo.gettext if an translations object is installed. This makes dealing with custom translations classes easier.

Fixed a confusing behavior with conditional extending. loops were partially executed under some conditions even though they were not part of a visible area.

Added sort filter that works like dictsort but for arbitrary sequences.

Fixed a bug with empty statements in macros.

Implemented a bytecode cache system.

The template context is now weakref-able

Inclusions and imports “with context” forward all variables now, not only the initial context.

Added a cycle helper called cycler.

Added a joining helper called joiner.

Added a compile_expression method to the environment that allows compiling of Jinja expressions into callable Python objects.

Fixed an escaping bug in urlize

Released 2008-07-17, codename Jinjavitus

The subscribing of objects (looking up attributes and items) changed from slightly. It’s now possible to give attributes or items a higher priority by either using dot-notation lookup or the bracket syntax. This also changed the AST slightly. Subscript is gone and was replaced with Getitem and Getattr.

Added support for preprocessing and token stream filtering for extensions. This would allow extensions to allow simplified gettext calls in template data and something similar.

Added TemplateStream.dump.

Added missing support for implicit string literal concatenation. {{ "foo" "bar" }} is equivalent to {{ "foobar" }}

else is optional for conditional expressions. If not given it evaluates to false.

Improved error reporting for undefined values by providing a position.

filesizeformat filter uses decimal prefixes now by default and can be set to binary mode with the second parameter.

Fixed bug in finalizer

First release of Jinja 2.

---

## Template Designer Documentation — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/templates/

**Contents:**
- Template Designer Documentation¶
- Synopsis¶
  - Template File Extension¶
- Variables¶
- Filters¶
- Tests¶
- Comments¶
- Whitespace Control¶
- Escaping¶
- Line Statements¶

This document describes the syntax and semantics of the template engine and will be most useful as reference to those creating Jinja templates. As the template engine is very flexible, the configuration from the application can be slightly different from the code presented here in terms of delimiters and behavior of undefined values.

A Jinja template is simply a text file. Jinja can generate any text-based format (HTML, XML, CSV, LaTeX, etc.). A Jinja template doesn’t need to have a specific extension: .html, .xml, or any other extension is just fine.

A template contains variables and/or expressions, which get replaced with values when a template is rendered; and tags, which control the logic of the template. The template syntax is heavily inspired by Django and Python.

Below is a minimal template that illustrates a few basics using the default Jinja configuration. We will cover the details later in this document:

The following example shows the default configuration settings. An application developer can change the syntax configuration from {% foo %} to <% foo %>, or something similar.

There are a few kinds of delimiters. The default Jinja delimiters are configured as follows:

{% ... %} for Statements

{{ ... }} for Expressions to print to the template output

{# ... #} for Comments not included in the template output

Line Statements and Comments are also possible, though they don’t have default prefix characters. To use them, set line_statement_prefix and line_comment_prefix when creating the Environment.

As stated above, any file can be loaded as a template, regardless of file extension. Adding a .jinja extension, like user.html.jinja may make it easier for some IDEs or editor plugins, but is not required. Autoescaping, introduced later, can be applied based on file extension, so you’ll need to take the extra suffix into account in that case.

Another good heuristic for identifying templates is that they are in a templates folder, regardless of extension. This is a common layout for projects.

Template variables are defined by the context dictionary passed to the template.

You can mess around with the variables in templates provided they are passed in by the application. Variables may have attributes or elements on them you can access too. What attributes a variable has depends heavily on the application providing that variable.

You can use a dot (.) to access attributes of a variable in addition to the standard Python __getitem__ “subscript” syntax ([]).

The following lines do the same thing:

It’s important to know that the outer double-curly braces are not part of the variable, but the print statement. If you access variables inside tags don’t put the braces around them.

If a variable or attribute does not exist, you will get back an undefined value. What you can do with that kind of value depends on the application configuration: the default behavior is to evaluate to an empty string if printed or iterated over, and to fail for every other operation.

For the sake of convenience, foo.bar in Jinja does the following things on the Python layer:

check for an attribute called bar on foo (getattr(foo, 'bar'))

if there is not, check for an item 'bar' in foo (foo.__getitem__('bar'))

if there is not, return an undefined object.

foo['bar'] works mostly the same with a small difference in sequence:

check for an item 'bar' in foo. (foo.__getitem__('bar'))

if there is not, check for an attribute called bar on foo. (getattr(foo, 'bar'))

if there is not, return an undefined object.

This is important if an object has an item and attribute with the same name. Additionally, the attr() filter only looks up attributes.

Variables can be modified by filters. Filters are separated from the variable by a pipe symbol (|) and may have optional arguments in parentheses. Multiple filters can be chained. The output of one filter is applied to the next.

For example, {{ name|striptags|title }} will remove all HTML Tags from variable name and title-case the output (title(striptags(name))).

Filters that accept arguments have parentheses around the arguments, just like a function call. For example: {{ listx|join(', ') }} will join a list with commas (str.join(', ', listx)).

The List of Builtin Filters below describes all the builtin filters.

Beside filters, there are also so-called “tests” available. Tests can be used to test a variable against a common expression. To test a variable or expression, you add is plus the name of the test after the variable. For example, to find out if a variable is defined, you can do name is defined, which will then return true or false depending on whether name is defined in the current template context.

Tests can accept arguments, too. If the test only takes one argument, you can leave out the parentheses. For example, the following two expressions do the same thing:

The List of Builtin Tests below describes all the builtin tests.

To comment-out part of a line in a template, use the comment syntax which is by default set to {# ... #}. This is useful to comment out parts of the template for debugging or to add information for other template designers or yourself:

In the default configuration:

a single trailing newline is stripped if present

other whitespace (spaces, tabs, newlines etc.) is returned unchanged

If an application configures Jinja to trim_blocks, the first newline after a template tag is removed automatically (like in PHP). The lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block. (Nothing will be stripped if there are other characters before the start of the block.)

With both trim_blocks and lstrip_blocks disabled (the default), block tags on their own lines will be removed, but a blank line will remain and the spaces in the content will be preserved. For example, this template:

With both trim_blocks and lstrip_blocks disabled, the template is rendered with blank lines inside the div:

With both trim_blocks and lstrip_blocks enabled, the template block lines are completely removed:

You can manually disable the lstrip_blocks behavior by putting a plus sign (+) at the start of a block:

Similarly, you can manually disable the trim_blocks behavior by putting a plus sign (+) at the end of a block:

You can also strip whitespace in templates by hand. If you add a minus sign (-) to the start or end of a block (e.g. a For tag), a comment, or a variable expression, the whitespaces before or after that block will be removed:

This will yield all elements without whitespace between them. If seq was a list of numbers from 1 to 9, the output would be 123456789.

If Line Statements are enabled, they strip leading whitespace automatically up to the beginning of the line.

By default, Jinja also removes trailing newlines. To keep single trailing newlines, configure Jinja to keep_trailing_newline.

You must not add whitespace between the tag and the minus sign.

It is sometimes desirable – even necessary – to have Jinja ignore parts it would otherwise handle as variables or blocks. For example, if, with the default syntax, you want to use {{ as a raw string in a template and not start a variable, you have to use a trick.

The easiest way to output a literal variable delimiter ({{) is by using a variable expression:

For bigger sections, it makes sense to mark a block raw. For example, to include example Jinja syntax in a template, you can use this snippet:

Minus sign at the end of {% raw -%} tag cleans all the spaces and newlines preceding the first character of your raw data.

If line statements are enabled by the application, it’s possible to mark a line as a statement. For example, if the line statement prefix is configured to #, the following two examples are equivalent:

The line statement prefix can appear anywhere on the line as long as no text precedes it. For better readability, statements that start a block (such as for, if, elif etc.) may end with a colon:

Line statements can span multiple lines if there are open parentheses, braces or brackets:

Since Jinja 2.2, line-based comments are available as well. For example, if the line-comment prefix is configured to be ##, everything from ## to the end of the line is ignored (excluding the newline sign):

The most powerful part of Jinja is template inheritance. Template inheritance allows you to build a base “skeleton” template that contains all the common elements of your site and defines blocks that child templates can override.

Sounds complicated but is very basic. It’s easiest to understand it by starting with an example.

This template, which we’ll call base.html, defines a simple HTML skeleton document that you might use for a simple two-column page. It’s the job of “child” templates to fill the empty blocks with content:

In this example, the {% block %} tags define four blocks that child templates can fill in. All the block tag does is tell the template engine that a child template may override those placeholders in the template.

block tags can be inside other blocks such as if, but they will always be executed regardless of if the if block is actually rendered.

A child template might look like this:

The {% extends %} tag is the key here. It tells the template engine that this template “extends” another template. When the template system evaluates this template, it first locates the parent. The extends tag should be the first tag in the template. Everything before it is printed out normally and may cause confusion. For details about this behavior and how to take advantage of it, see Null-Default Fallback. Also a block will always be filled in regardless of whether the surrounding condition is evaluated to be true or false.

The filename of the template depends on the template loader. For example, the FileSystemLoader allows you to access other templates by giving the filename. You can access templates in subdirectories with a slash:

But this behavior can depend on the application embedding Jinja. Note that since the child template doesn’t define the footer block, the value from the parent template is used instead.

You can’t define multiple {% block %} tags with the same name in the same template. This limitation exists because a block tag works in “both” directions. That is, a block tag doesn’t just provide a placeholder to fill - it also defines the content that fills the placeholder in the parent. If there were two similarly-named {% block %} tags in a template, that template’s parent wouldn’t know which one of the blocks’ content to use.

If you want to print a block multiple times, you can, however, use the special self variable and call the block with that name:

It’s possible to render the contents of the parent block by calling super(). This gives back the results of the parent block:

In the case of multiple levels of {% extends %}, super references may be chained (as in super.super()) to skip levels in the inheritance tree.

Rendering child.tmpl will give body: Hi from child. Hi from parent.

Rendering grandchild1.tmpl will give body: Hi from grandchild1.

Rendering grandchild2.tmpl will give body: Hi from grandchild2. Hi from parent.

Jinja allows you to put the name of the block after the end tag for better readability:

However, the name after the endblock word must match the block name.

Blocks can be nested for more complex layouts. By default, a block may not access variables from outside the block (outer scopes):

This example would output empty <li> items because item is unavailable inside the block. The reason for this is that if the block is replaced by a child template, a variable would appear that was not defined in the block or passed to the context.

Starting with Jinja 2.2, you can explicitly specify that variables are available in a block by setting the block to “scoped” by adding the scoped modifier to a block declaration:

When overriding a block, the scoped modifier does not have to be provided.

Blocks can be marked as required. They must be overridden at some point, but not necessarily by the direct child template. Required blocks may only contain space and comments, and they cannot be rendered directly.

Rendering page.txt or issue.txt will raise TemplateRuntimeError because they don’t override the body block. Rendering bug_report.txt will succeed because it does override the block.

When combined with scoped, the required modifier must be placed after the scoped modifier. Here are some valid examples:

extends, include, and import can take a template object instead of the name of a template to load. This could be useful in some advanced situations, since you can use Python code to load a template first and pass it in to render.

Note how extends is passed the variable with the template object that was passed to render, instead of a string.

When generating HTML from templates, there’s always a risk that a variable will include characters that affect the resulting HTML. There are two approaches:

manually escaping each variable; or

automatically escaping everything by default.

Jinja supports both. What is used depends on the application configuration. The default configuration is no automatic escaping; for various reasons:

Escaping everything except for safe values will also mean that Jinja is escaping variables known to not include HTML (e.g. numbers, booleans) which can be a huge performance hit.

The information about the safety of a variable is very fragile. It could happen that by coercing safe and unsafe values, the return value is double-escaped HTML.

If manual escaping is enabled, it’s your responsibility to escape variables if needed. What to escape? If you have a variable that may include any of the following chars (>, <, &, or ") you SHOULD escape it unless the variable contains well-formed and trusted HTML. Escaping works by piping the variable through the |e filter:

When automatic escaping is enabled, everything is escaped by default except for values explicitly marked as safe. Variables and expressions can be marked as safe either in:

The context dictionary by the application with markupsafe.Markup

The template, with the |safe filter.

If a string that you marked safe is passed through other Python code that doesn’t understand that mark, it may get lost. Be aware of when your data is marked safe and how it is processed before arriving at the template.

If a value has been escaped but is not marked safe, auto-escaping will still take place and result in double-escaped characters. If you know you have data that is already safe but not marked, be sure to wrap it in Markup or use the |safe filter.

Jinja functions (macros, super, self.BLOCKNAME) always return template data that is marked as safe.

String literals in templates with automatic escaping are considered unsafe because native Python strings are not safe.

A control structure refers to all those things that control the flow of a program - conditionals (i.e. if/elif/else), for-loops, as well as things like macros and blocks. With the default syntax, control structures appear inside {% ... %} blocks.

Loop over each item in a sequence. For example, to display a list of users provided in a variable called users:

As variables in templates retain their object properties, it is possible to iterate over containers like dict:

Python dicts may not be in the order you want to display them in. If order matters, use the |dictsort filter.

Inside of a for-loop block, you can access some special variables:

The current iteration of the loop. (1 indexed)

The current iteration of the loop. (0 indexed)

The number of iterations from the end of the loop (1 indexed)

The number of iterations from the end of the loop (0 indexed)

True if first iteration.

True if last iteration.

The number of items in the sequence.

A helper function to cycle between a list of sequences. See the explanation below.

Indicates how deep in a recursive loop the rendering currently is. Starts at level 1

Indicates how deep in a recursive loop the rendering currently is. Starts at level 0

The item from the previous iteration of the loop. Undefined during the first iteration.

The item from the following iteration of the loop. Undefined during the last iteration.

True if previously called with a different value (or not called at all).

Within a for-loop, it’s possible to cycle among a list of strings/variables each time through the loop by using the special loop.cycle helper:

Since Jinja 2.1, an extra cycle helper exists that allows loop-unbound cycling. For more information, have a look at the List of Global Functions.

Unlike in Python, it’s not possible to break or continue in a loop. You can, however, filter the sequence during iteration, which allows you to skip items. The following example skips all the users which are hidden:

The advantage is that the special loop variable will count correctly; thus not counting the users not iterated over.

If no iteration took place because the sequence was empty or the filtering removed all the items from the sequence, you can render a default block by using else:

Note that, in Python, else blocks are executed whenever the corresponding loop did not break. Since Jinja loops cannot break anyway, a slightly different behavior of the else keyword was chosen.

It is also possible to use loops recursively. This is useful if you are dealing with recursive data such as sitemaps or RDFa. To use loops recursively, you basically have to add the recursive modifier to the loop definition and call the loop variable with the new iterable where you want to recurse.

The following example implements a sitemap with recursive loops:

The loop variable always refers to the closest (innermost) loop. If we have more than one level of loops, we can rebind the variable loop by writing {% set outer_loop = loop %} after the loop that we want to use recursively. Then, we can call it using {{ outer_loop(...) }}

Please note that assignments in loops will be cleared at the end of the iteration and cannot outlive the loop scope. Older versions of Jinja had a bug where in some circumstances it appeared that assignments would work. This is not supported. See Assignments for more information about how to deal with this.

If all you want to do is check whether some value has changed since the last iteration or will change in the next iteration, you can use previtem and nextitem:

If you only care whether the value changed at all, using changed is even easier:

The if statement in Jinja is comparable with the Python if statement. In the simplest form, you can use it to test if a variable is defined, not empty and not false:

For multiple branches, elif and else can be used like in Python. You can use more complex Expressions there, too:

If can also be used as an inline expression and for loop filtering.

Macros are comparable with functions in regular programming languages. They are useful to put often used idioms into reusable functions to not repeat yourself (“DRY”).

Here’s a small example of a macro that renders a form element:

The macro can then be called like a function in the namespace:

If the macro was defined in a different template, you have to import it first.

Inside macros, you have access to three special variables:

If more positional arguments are passed to the macro than accepted by the macro, they end up in the special varargs variable as a list of values.

Like varargs but for keyword arguments. All unconsumed keyword arguments are stored in this special variable.

If the macro was called from a call tag, the caller is stored in this variable as a callable macro.

Macros also expose some of their internal details. The following attributes are available on a macro object:

The name of the macro. {{ input.name }} will print input.

A tuple of the names of arguments the macro accepts.

This is true if the macro accepts extra keyword arguments (i.e.: accesses the special kwargs variable).

This is true if the macro accepts extra positional arguments (i.e.: accesses the special varargs variable).

This is true if the macro accesses the special caller variable and may be called from a call tag.

If a macro name starts with an underscore, it’s not exported and can’t be imported.

Due to how scopes work in Jinja, a macro in a child template does not override a macro in a parent template. The following will output “LAYOUT”, not “CHILD”.

In some cases it can be useful to pass a macro to another macro. For this purpose, you can use the special call block. The following example shows a macro that takes advantage of the call functionality and how it can be used:

It’s also possible to pass arguments back to the call block. This makes it useful as a replacement for loops. Generally speaking, a call block works exactly like a macro without a name.

Here’s an example of how a call block can be used with arguments:

Filter sections allow you to apply regular Jinja filters on a block of template data. Just wrap the code in the special filter section:

Filters that accept arguments can be called like this:

Inside code blocks, you can also assign values to variables. Assignments at top level (outside of blocks, macros or loops) are exported from the template like top level macros and can be imported by other templates.

Assignments use the set tag and can have multiple targets:

Please keep in mind that it is not possible to set variables inside a block and have them show up outside of it. This also applies to loops. The only exception to that rule are if statements which do not introduce a scope. As a result the following template is not going to do what you might expect:

It is not possible with Jinja syntax to do this. Instead use alternative constructs like the loop else block or the special loop variable:

As of version 2.10 more complex use cases can be handled using namespace objects which allow propagating of changes across scopes:

Note that the obj.attr notation in the set tag is only allowed for namespace objects; attempting to assign an attribute on any other object will raise an exception.

Added in version 2.10: Added support for namespace objects

It’s possible to use set as a block to assign the content of the block to a variable. This can be used to create multi-line strings, since Jinja doesn’t support Python’s triple quotes (""", ''').

Instead of using an equals sign and a value, you only write the variable name, and everything until {% endset %} is captured.

Filters applied to the variable name will be applied to the block’s content.

Changed in version 2.10: Block assignment supports filters.

Added in version 2.8.

The extends tag can be used to extend one template from another. You can have multiple extends tags in a file, but only one of them may be executed at a time.

See the section about Template Inheritance above.

Blocks are used for inheritance and act as both placeholders and replacements at the same time. They are documented in detail in the Template Inheritance section.

The include tag renders another template and outputs the result into the current template.

The included template has access to context of the current template by default. Use without context to use a separate context instead. with context is also valid, but is the default behavior. See Import Context Behavior.

The included template can extend another template and override blocks in that template. However, the current template cannot override any blocks that the included template outputs.

Use ignore missing to ignore the statement if the template does not exist. It must be placed before a context visibility statement.

If a list of templates is given, each will be tried in order until one is not missing. This can be used with ignore missing to ignore if none of the templates exist.

A variable, with either a template name or template object, can also be passed to the statement.

Jinja supports putting often used code into macros. These macros can go into different templates and get imported from there. This works similarly to the import statements in Python. It’s important to know that imports are cached and imported templates don’t have access to the current template variables, just the globals by default. For more details about context behavior of imports and includes, see Import Context Behavior.

There are two ways to import templates. You can import a complete template into a variable or request specific macros / exported variables from it.

Imagine we have a helper module that renders forms (called forms.html):

The easiest and most flexible way to access a template’s variables and macros is to import the whole template module into a variable. That way, you can access the attributes:

Alternatively, you can import specific names from a template into the current namespace:

Macros and variables starting with one or more underscores are private and cannot be imported.

Changed in version 2.4: If a template object was passed to the template context, you can import from that object.

By default, included templates are passed the current context and imported templates are not. The reason for this is that imports, unlike includes, are cached; as imports are often used just as a module that holds macros.

This behavior can be changed explicitly: by adding with context or without context to the import/include directive, the current context can be passed to the template and caching is disabled automatically.

Here are two examples:

In Jinja 2.0, the context that was passed to the included template did not include variables defined in the template. As a matter of fact, this did not work:

The included template render_box.html is not able to access box in Jinja 2.0. As of Jinja 2.1, render_box.html is able to do so.

Jinja allows basic expressions everywhere. These work very similarly to regular Python; even if you’re not working with Python you should feel comfortable with it.

The simplest form of expressions are literals. Literals are representations for Python objects such as strings and numbers. The following literals exist:

Everything between two double or single quotes is a string. They are useful whenever you need a string in the template (e.g. as arguments to function calls and filters, or just to extend or include a template).

Integers are whole numbers without a decimal part. The ‘_’ character can be used to separate groups for legibility.

Floating point numbers can be written using a ‘.’ as a decimal mark. They can also be written in scientific notation with an upper or lower case ‘e’ to indicate the exponent part. The ‘_’ character can be used to separate groups for legibility, but cannot be used in the exponent part.

Everything between two brackets is a list. Lists are useful for storing sequential data to be iterated over. For example, you can easily create a list of links using lists and tuples for (and with) a for loop:

Tuples are like lists that cannot be modified (“immutable”). If a tuple only has one item, it must be followed by a comma (('1-tuple',)). Tuples are usually used to represent items of two or more elements. See the list example above for more details.

A dict in Python is a structure that combines keys and values. Keys must be unique and always have exactly one value. Dicts are rarely used in templates; they are useful in some rare cases such as the xmlattr() filter.

true is always true and false is always false.

The special constants true, false, and none are indeed lowercase. Because that caused confusion in the past, (True used to expand to an undefined variable that was considered false), all three can now also be written in title case (True, False, and None). However, for consistency, (all Jinja identifiers are lowercase) you should use the lowercase versions.

Jinja allows you to calculate with values. This is rarely useful in templates but exists for completeness’ sake. The following operators are supported:

Adds two objects together. Usually the objects are numbers, but if both are strings or lists, you can concatenate them this way. This, however, is not the preferred way to concatenate strings! For string concatenation, have a look-see at the ~ operator. {{ 1 + 1 }} is 2.

Subtract the second number from the first one. {{ 3 - 2 }} is 1.

Divide two numbers. The return value will be a floating point number. {{ 1 / 2 }} is {{ 0.5 }}.

Divide two numbers and return the truncated integer result. {{ 20 // 7 }} is 2.

Calculate the remainder of an integer division. {{ 11 % 7 }} is 4.

Multiply the left operand with the right one. {{ 2 * 2 }} would return 4. This can also be used to repeat a string multiple times. {{ '=' * 80 }} would print a bar of 80 equal signs.

Raise the left operand to the power of the right operand. {{ 2**3 }} would return 8.

Unlike Python, chained pow is evaluated left to right. {{ 3**3**3 }} is evaluated as (3**3)**3 in Jinja, but would be evaluated as 3**(3**3) in Python. Use parentheses in Jinja to be explicit about what order you want. It is usually preferable to do extended math in Python and pass the results to render rather than doing it in the template.

This behavior may be changed in the future to match Python, if it’s possible to introduce an upgrade path.

Compares two objects for equality.

Compares two objects for inequality.

true if the left hand side is greater than the right hand side.

true if the left hand side is greater or equal to the right hand side.

true if the left hand side is lower than the right hand side.

true if the left hand side is lower or equal to the right hand side.

For if statements, for filtering, and if expressions, it can be useful to combine multiple expressions.

For x and y, if x is false, then the value is x, else y. In a boolean context, this will be treated as True if both operands are truthy.

For x or y, if x is true, then the value is x, else y. In a boolean context, this will be treated as True if at least one operand is truthy.

For not x, if x is false, then the value is True, else False.

Prefer negating is and in using their infix notation: foo is not bar instead of not foo is bar; foo not in bar instead of not foo in bar. All other expressions require prefix notation: not (foo and bar).

Parentheses group an expression. This is used to change evaluation order, or to make a long expression easier to read or less ambiguous.

The following operators are very useful but don’t fit into any of the other two categories:

Perform a sequence / mapping containment test. Returns true if the left operand is contained in the right. {{ 1 in [1, 2, 3] }} would, for example, return true.

Converts all operands into strings and concatenates them.

{{ "Hello " ~ name ~ "!" }} would return (assuming name is set to 'John') Hello John!.

Call a callable: {{ post.render() }}. Inside of the parentheses you can use positional arguments and keyword arguments like in Python:

{{ post.render(user, full=true) }}.

Get an attribute of an object. (See Variables)

It is also possible to use inline if expressions. These are useful in some situations. For example, you can use this to extend from one template if a variable is defined, otherwise from the default layout template:

The general syntax is <do something> if <something is true> else <do something else>.

The else part is optional. If not provided, the else block implicitly evaluates into an Undefined object (regardless of what undefined in the environment is set to):

You can also use any of the methods defined on a variable’s type. The value returned from the method invocation is used as the value of the expression. Here is an example that uses methods defined on strings (where page.title is a string):

This works for methods on user-defined types. For example, if variable f of type Foo has a method bar defined on it, you can do the following:

Operator methods also work as expected. For example, % implements printf-style for strings:

Although you should prefer the .format method for that case (which is a bit contrived in the context of rendering a template):

Return the absolute value of the argument.

Get an attribute of an object. foo|attr("bar") works like foo.bar, but returns undefined instead of falling back to foo["bar"] if the attribute doesn’t exist.

See Notes on subscriptions for more details.

A filter that batches items. It works pretty much like slice just the other way round. It returns a list of lists with the given number of items. If you provide a second parameter this is used to fill up missing items. See this example:

Capitalize a value. The first character will be uppercase, all others lowercase.

Centers the value in a field of a given width.

If the value is undefined it will return the passed default value, otherwise the value of the variable:

This will output the value of my_variable if the variable was defined, otherwise 'my_variable is not defined'. If you want to use default with variables that evaluate to false you have to set the second parameter to true:

Changed in version 2.11: It’s now possible to configure the Environment with ChainableUndefined to make the default filter work on nested elements and attributes that may contain undefined values in the chain without getting an UndefinedError.

Sort a dict and yield (key, value) pairs. Python dicts may not be in the order you want to display them in, so sort them first.

Replace the characters &, <, >, ', and " in the string with HTML-safe sequences. Use this if you need to display text that might contain such characters in HTML.

If the object has an __html__ method, it is called and the return value is assumed to already be safe for HTML.

s – An object to be converted to a string and escaped.

A Markup string with the escaped text.

Format the value like a ‘human-readable’ file size (i.e. 13 kB, 4.1 MB, 102 Bytes, etc). Per default decimal prefixes are used (Mega, Giga, etc.), if the second parameter is set to True the binary prefixes are used (Mebi, Gibi).

Return the first item of a sequence.

Convert the value into a floating point number. If the conversion doesn’t work it will return 0.0. You can override this default using the first parameter.

Enforce HTML escaping. This will probably double escape variables.

Apply the given values to a printf-style format string, like string % values.

In most cases it should be more convenient and efficient to use the % operator or str.format().

Group a sequence of objects by an attribute using Python’s itertools.groupby(). The attribute can use dot notation for nested access, like "address.city". Unlike Python’s groupby, the values are sorted first so only one group is returned for each unique value.

For example, a list of User objects with a city attribute can be rendered in groups. In this example, grouper refers to the city value of the group.

groupby yields namedtuples of (grouper, list), which can be used instead of the tuple unpacking above. grouper is the value of the attribute, and list is the items with that value.

You can specify a default value to use if an object in the list does not have the given attribute.

Like the sort() filter, sorting and grouping is case-insensitive by default. The key for each group will have the case of the first item in that group of values. For example, if a list of users has cities ["CA", "NY", "ca"], the “CA” group will have two values. This can be disabled by passing case_sensitive=True.

Changed in version 3.1: Added the case_sensitive parameter. Sorting and grouping is case-insensitive by default, matching other filters that do comparisons.

Changed in version 3.0: Added the default parameter.

Changed in version 2.6: The attribute supports dot notation for nested access.

Return a copy of the string with each line indented by 4 spaces. The first line and blank lines are not indented by default.

width – Number of spaces, or a string, to indent by.

first – Don’t skip indenting the first line.

blank – Don’t skip indenting empty lines.

Changed in version 3.0: width can be a string.

Changed in version 2.10: Blank lines are not indented by default.

Rename the indentfirst argument to first.

Convert the value into an integer. If the conversion doesn’t work it will return 0. You can override this default using the first parameter. You can also override the default base (10) in the second parameter, which handles input with prefixes such as 0b, 0o and 0x for bases 2, 8 and 16 respectively. The base is ignored for decimal numbers and non-string values.

Return an iterator over the (key, value) items of a mapping.

x|items is the same as x.items(), except if x is undefined an empty iterator is returned.

This filter is useful if you expect the template to be rendered with an implementation of Jinja in another programming language that does not have a .items() method on its mapping type.

Added in version 3.1.

Return a string which is the concatenation of the strings in the sequence. The separator between elements is an empty string per default, you can define it with the optional parameter:

It is also possible to join certain attributes of an object:

Added in version 2.6: The attribute parameter was added.

Return the last item of a sequence.

Note: Does not work with generators. You may want to explicitly convert it to a list:

Return the number of items in a container.

Convert the value into a list. If it was a string the returned list will be a list of characters.

Convert a value to lowercase.

Applies a filter on a sequence of objects or looks up an attribute. This is useful when dealing with lists of objects but you are really only interested in a certain value of it.

The basic usage is mapping on an attribute. Imagine you have a list of users but you are only interested in a list of usernames:

You can specify a default value to use if an object in the list does not have the given attribute.

Alternatively you can let it invoke a filter by passing the name of the filter and the arguments afterwards. A good example would be applying a text conversion filter on a sequence:

Similar to a generator comprehension such as:

Changed in version 2.11.0: Added the default parameter.

Added in version 2.7.

Return the largest item from the sequence.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Get the object with the max value of this attribute.

Return the smallest item from the sequence.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Get the object with the min value of this attribute.

Pretty print a variable. Useful for debugging.

Return a random item from the sequence.

Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.

If no test is specified, each object will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.

If no test is specified, the attribute’s value will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Return a copy of the value with all occurrences of a substring replaced with a new one. The first argument is the substring that should be replaced, the second is the replacement string. If the optional third argument count is given, only the first count occurrences are replaced:

Reverse the object or return an iterator that iterates over it the other way round.

Round the number to a given precision. The first parameter specifies the precision (default is 0), the second the rounding method:

'common' rounds either up or down

'ceil' always rounds up

'floor' always rounds down

If you don’t specify a method 'common' is used.

Note that even if rounded to 0 precision, a float is returned. If you need a real integer, pipe it through int:

Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.

Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.

If no test is specified, each object will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.

If no test is specified, the attribute’s value will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Slice an iterator and return a list of lists containing those items. Useful if you want to create a div containing three ul tags that represent columns:

If you pass it a second argument it’s used to fill missing values on the last iteration.

Sort an iterable using Python’s sorted().

reverse – Sort descending instead of ascending.

case_sensitive – When sorting strings, sort upper and lower case separately.

attribute – When sorting objects or dicts, an attribute or key to sort by. Can use dot notation like "address.city". Can be a list of attributes like "age,name".

The sort is stable, it does not change the relative order of elements that compare equal. This makes it is possible to chain sorts on different attributes and ordering.

As a shortcut to chaining when the direction is the same for all attributes, pass a comma separate list of attributes.

Changed in version 2.11.0: The attribute parameter can be a comma separated list of attributes, e.g. "age,name".

Changed in version 2.6: The attribute parameter was added.

Convert an object to a string if it isn’t already. This preserves a Markup string rather than converting it back to a basic string, so it will still be marked as safe and won’t be escaped again.

Strip SGML/XML tags and replace adjacent whitespace by one space.

Returns the sum of a sequence of numbers plus the value of parameter ‘start’ (which defaults to 0). When the sequence is empty it returns start.

It is also possible to sum up only certain attributes:

Changed in version 2.6: The attribute parameter was added to allow summing up over attributes. Also the start parameter was moved on to the right.

Return a titlecased version of the value. I.e. words will start with uppercase letters, all remaining characters are lowercase.

Serialize an object to a string of JSON, and mark it safe to render in HTML. This filter is only for use in HTML documents.

The returned string is safe to render in HTML documents and <script> tags. The exception is in HTML attributes that are double quoted; either use single quotes or the |forceescape filter.

value – The object to serialize to JSON.

indent – The indent parameter passed to dumps, for pretty-printing the value.

Added in version 2.9.

Strip leading and trailing characters, by default whitespace.

Return a truncated copy of the string. The length is specified with the first parameter which defaults to 255. If the second parameter is true the filter will cut the text at length. Otherwise it will discard the last word. If the text was in fact truncated it will append an ellipsis sign ("..."). If you want a different ellipsis sign than "..." you can specify it using the third parameter. Strings that only exceed the length by the tolerance margin given in the fourth parameter will not be truncated.

The default leeway on newer Jinja versions is 5 and was 0 before but can be reconfigured globally.

Returns a list of unique items from the given iterable.

The unique items are yielded in the same order as their first occurrence in the iterable passed to the filter.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Filter objects with unique values for this attribute.

Convert a value to uppercase.

Quote data for use in a URL path or query using UTF-8.

Basic wrapper around urllib.parse.quote() when given a string, or urllib.parse.urlencode() for a dict or iterable.

value – Data to quote. A string will be quoted directly. A dict or iterable of (key, value) pairs will be joined as a query string.

When given a string, “/” is not quoted. HTTP servers treat “/” and “%2F” equivalently in paths. If you need quoted slashes, use the |replace("/", "%2F") filter.

Added in version 2.7.

Convert URLs in text into clickable links.

This may not recognize links in some situations. Usually, a more comprehensive formatter, such as a Markdown library, is a better choice.

Works on http://, https://, www., mailto:, and email addresses. Links with trailing punctuation (periods, commas, closing parentheses) and leading punctuation (opening parentheses) are recognized excluding the punctuation. Email addresses that include header fields are not recognized (for example, mailto:address@example.com?cc=copy@example.com).

value – Original text containing URLs to link.

trim_url_limit – Shorten displayed URL values to this length.

nofollow – Add the rel=nofollow attribute to links.

target – Add the target attribute to links.

rel – Add the rel attribute to links.

extra_schemes – Recognize URLs that start with these schemes in addition to the default behavior. Defaults to env.policies["urlize.extra_schemes"], which defaults to no extra schemes.

Changed in version 3.0: The extra_schemes parameter was added.

Changed in version 3.0: Generate https:// links for URLs without a scheme.

Changed in version 3.0: The parsing rules were updated. Recognize email addresses with or without the mailto: scheme. Validate IP addresses. Ignore parentheses and brackets in more cases.

Changed in version 2.8: The target parameter was added.

Count the words in that string.

Wrap a string to the given width. Existing newlines are treated as paragraphs to be wrapped separately.

s – Original text to wrap.

width – Maximum length of wrapped lines.

break_long_words – If a word is longer than width, break it across lines.

break_on_hyphens – If a word contains hyphens, it may be split across lines.

wrapstring – String to join each wrapped line. Defaults to Environment.newline_sequence.

Changed in version 2.11: Existing newlines are treated as paragraphs wrapped separately.

Changed in version 2.11: Added the break_on_hyphens parameter.

Changed in version 2.7: Added the wrapstring parameter.

Create an SGML/XML attribute string based on the items in a dict.

Values that are neither none nor undefined are automatically escaped, safely allowing untrusted user input.

User input should not be used as keys to this filter. If any key contains a space, / solidus, > greater-than sign, or = equals sign, this fails with a ValueError. Regardless of this, user input should never be used as keys to this filter, or must be separately validated first.

Results in something like this:

As you can see it automatically prepends a space in front of the item if the filter returned something unless the second parameter is false.

Changed in version 3.1.4: Keys with / solidus, > greater-than sign, or = equals sign are not allowed.

Changed in version 3.1.3: Keys with spaces are not allowed.

Return true if the object is a boolean value.

Added in version 2.11.

Return whether the object is callable (i.e., some kind of function).

Note that classes are callable, as are instances of classes with a __call__() method.

Return true if the variable is defined:

See the default() filter for a simple way to set undefined variables.

Check if a variable is divisible by a number.

Check if the value is escaped.

Return true if the variable is even.

Return true if the object is False.

Added in version 2.11.

Check if a filter exists by name. Useful if a filter may be optionally available.

Added in version 3.0.

Return true if the object is a float.

Added in version 2.11.

Check if value is in seq.

Added in version 2.10.

Return true if the object is an integer.

Added in version 2.11.

Check if it’s possible to iterate over an object.

Return true if the variable is lowercased.

Return true if the object is a mapping (dict etc.).

Added in version 2.6.

Return true if the variable is none.

Return true if the variable is a number.

Return true if the variable is odd.

Check if an object points to the same memory address than another object:

Return true if the variable is a sequence. Sequences are variables that are iterable.

Return true if the object is a string.

Check if a test exists by name. Useful if a test may be optionally available.

Added in version 3.0.

Return true if the object is True.

Added in version 2.11.

Like defined() but the other way round.

Return true if the variable is uppercased.

The following functions are available in the global scope by default:

Return a list containing an arithmetic progression of integers. range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0. When step is given, it specifies the increment (or decrement). For example, range(4) and range(0, 4, 1) return [0, 1, 2, 3]. The end point is omitted! These are exactly the valid indices for a list of 4 elements.

This is useful to repeat a template block multiple times, e.g. to fill a list. Imagine you have 7 users in the list but you want to render three empty items to enforce a height with CSS:

Generates some lorem ipsum for the template. By default, five paragraphs of HTML are generated with each paragraph between 20 and 100 words. If html is False, regular text is returned. This is useful to generate simple contents for layout testing.

A convenient alternative to dict literals. {'foo': 'bar'} is the same as dict(foo='bar').

Cycle through values by yielding them one at a time, then restarting once the end is reached.

Similar to loop.cycle, but can be used outside loops or across multiple loops. For example, render a list of folders and files in a list, alternating giving them “odd” and “even” classes.

items – Each positional argument will be yielded in the order given for each cycle.

Added in version 2.1.

Return the current item. Equivalent to the item that will be returned next time next() is called.

Return the current item, then advance current to the next item.

Resets the current item to the first item.

A tiny helper that can be used to “join” multiple sections. A joiner is passed a string and will return that string every time it’s called, except the first time (in which case it returns an empty string). You can use this to join things:

Added in version 2.1.

Creates a new container that allows attribute assignment using the {% set %} tag:

The main purpose of this is to allow carrying a value from within a loop body to an outer scope. Initial values can be provided as a dict, as keyword arguments, or both (same behavior as Python’s dict constructor):

Changed in version 3.2: Namespace attributes can be assigned to in multiple assignment.

Added in version 2.10.

The following sections cover the built-in Jinja extensions that may be enabled by an application. An application could also provide further extensions not covered by this documentation; in which case there should be a separate document explaining said extensions.

If the i18n Extension is enabled, it’s possible to mark text in the template as translatable. To mark a section as translatable, use a trans block:

Inside the block, no statements are allowed, only text and simple variable tags.

Variable tags can only be a name, not attribute access, filters, or other expressions. To use an expression, bind it to a name in the trans tag for use in the block.

To bind more than one expression, separate each with a comma (,).

To pluralize, specify both the singular and plural forms separated by the pluralize tag.

By default, the first variable in a block is used to determine whether to use singular or plural form. If that isn’t correct, specify the variable used for pluralizing as a parameter to pluralize.

When translating blocks of text, whitespace and linebreaks result in hard to read and error-prone translation strings. To avoid this, a trans block can be marked as trimmed, which will replace all linebreaks and the whitespace surrounding them with a single space and remove leading and trailing whitespace.

This results in This is %(book_title)s. You should read it! in the translation file.

If trimming is enabled globally, the notrimmed modifier can be used to disable it for a block.

Added in version 2.10: The trimmed and notrimmed modifiers have been added.

If the translation depends on the context that the message appears in, the pgettext and npgettext functions take a context string as the first argument, which is used to select the appropriate translation. To specify a context with the {% trans %} tag, provide a string as the first token after trans.

Added in version 3.1: A context can be passed to the trans tag to use pgettext and npgettext.

It’s possible to translate strings in expressions with these functions:

_(message): Alias for gettext.

gettext(message): Translate a message.

ngettext(singular, plural, n): Translate a singular or plural message based on a count variable.

pgettext(context, message): Like gettext(), but picks the translation based on the context string.

npgettext(context, singular, plural, n): Like npgettext(), but picks the translation based on the context string.

You can print a translated string like this:

To use placeholders, use the format filter.

Always use keyword arguments to format, as other languages may not use the words in the same order.

If New Style Gettext calls are activated, using placeholders is easier. Formatting is part of the gettext call instead of using the format filter.

The ngettext function’s format string automatically receives the count as a num parameter in addition to the given parameters.

If the expression-statement extension is loaded, a tag called do is available that works exactly like the regular variable expression ({{ ... }}); except it doesn’t print anything. This can be used to modify lists:

If the application enables the Loop Controls, it’s possible to use break and continue in loops. When break is reached, the loop is terminated; if continue is reached, the processing is stopped and continues with the next iteration.

Here’s a loop that skips every second item:

Likewise, a loop that stops processing after the 10th iteration:

Note that loop.index starts with 1, and loop.index0 starts with 0 (See: For).

If the Debug Extension is enabled, a {% debug %} tag will be available to dump the current context as well as the available filters and tests. This is useful to see what’s available to use in the template without setting up a debugger.

Added in version 2.3.

The with statement makes it possible to create a new inner scope. Variables set within this scope are not visible outside of the scope.

Because it is common to set variables at the beginning of the scope, you can do that within the with statement. The following two examples are equivalent:

An important note on scoping here. In Jinja versions before 2.9 the behavior of referencing one variable to another had some unintended consequences. In particular one variable could refer to another defined in the same with block’s opening statement. This caused issues with the cleaned up scoping behavior and has since been improved. In particular in newer Jinja versions the following code always refers to the variable a from outside the with block:

In earlier Jinja versions the b attribute would refer to the results of the first attribute. If you depend on this behavior you can rewrite it to use the set tag:

In older versions of Jinja (before 2.9) it was required to enable this feature with an extension. It’s now enabled by default.

Added in version 2.4.

If you want you can activate and deactivate the autoescaping from within the templates.

After an endautoescape the behavior is reverted to what it was before.

In older versions of Jinja (before 2.9) it was required to enable this feature with an extension. It’s now enabled by default.

---

## Sandbox — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/sandbox/

**Contents:**
- Sandbox¶
- Security Considerations¶
- API¶
- Operator Intercepting¶

The Jinja sandbox can be used to render untrusted templates. Access to attributes, method calls, operators, mutating data structures, and string formatting can be intercepted and prohibited.

A sandboxed environment can be useful, for example, to allow users of an internal reporting system to create custom emails. You would document what data is available in the templates, then the user would write a template using that information. Your code would generate the report data and pass it to the user’s sandboxed template to render.

The sandbox alone is not a solution for perfect security. Keep these things in mind when using the sandbox.

Templates can still raise errors when compiled or rendered. Your code should attempt to catch errors instead of crashing.

It is possible to construct a relatively small template that renders to a very large amount of output, which could correspond to a high use of CPU or memory. You should run your application with limits on resources such as CPU and memory to mitigate this.

Jinja only renders text, it does not understand, for example, JavaScript code. Depending on how the rendered template will be used, you may need to do other postprocessing to restrict the output.

Pass only the data that is relevant to the template. Avoid passing global data, or objects with methods that have side effects. By default the sandbox prevents private and internal attribute access. You can override is_safe_attribute() to further restrict attributes access. Decorate methods with unsafe() to prevent calling them from templates when passing objects as data. Use ImmutableSandboxedEnvironment to prevent modifying lists and dictionaries.

The sandboxed environment. It works like the regular environment but tells the compiler to generate sandboxed code. Additionally subclasses of this environment may override the methods that tell the runtime what attributes or functions are safe to access.

If the template tries to access insecure code a SecurityError is raised. However also other exceptions may occur during the rendering so the caller has to ensure that all exceptions are caught.

default callback table for the binary operators. A copy of this is available on each instance of a sandboxed environment as binop_table

default callback table for the unary operators. A copy of this is available on each instance of a sandboxed environment as unop_table

a set of binary operators that should be intercepted. Each operator that is added to this set (empty by default) is delegated to the call_binop() method that will perform the operator. The default operator callback is specified by binop_table.

The following binary operators are interceptable: //, %, +, *, -, /, and **

The default operation form the operator table corresponds to the builtin function. Intercepted calls are always slower than the native operator call, so make sure only to intercept the ones you are interested in.

Added in version 2.6.

a set of unary operators that should be intercepted. Each operator that is added to this set (empty by default) is delegated to the call_unop() method that will perform the operator. The default operator callback is specified by unop_table.

The following unary operators are interceptable: +, -

The default operation form the operator table corresponds to the builtin function. Intercepted calls are always slower than the native operator call, so make sure only to intercept the ones you are interested in.

Added in version 2.6.

The sandboxed environment will call this method to check if the attribute of an object is safe to access. Per default all attributes starting with an underscore are considered private as well as the special attributes of internal python objects as returned by the is_internal_attribute() function.

Check if an object is safely callable. By default callables are considered safe unless decorated with unsafe().

This also recognizes the Django convention of setting func.alters_data = True.

For intercepted binary operator calls (intercepted_binops()) this function is executed instead of the builtin operator. This can be used to fine tune the behavior of certain operators.

Added in version 2.6.

For intercepted unary operator calls (intercepted_unops()) this function is executed instead of the builtin operator. This can be used to fine tune the behavior of certain operators.

Added in version 2.6.

Works exactly like the regular SandboxedEnvironment but does not permit modifications on the builtin mutable objects list, set, and dict by using the modifies_known_mutable() function.

Raised if a template tries to do something insecure if the sandbox is enabled.

Marks a function or method as unsafe.

Test if the attribute given is an internal python attribute. For example this function returns True for the func_code attribute of python objects. This is useful if the environment method is_safe_attribute() is overridden.

This function checks if an attribute on a builtin mutable object (list, dict, set or deque) or the corresponding ABCs would modify it if called.

If called with an unsupported object, False is returned.

For performance, Jinja outputs operators directly when compiling. This means it’s not possible to intercept operator behavior by overriding SandboxEnvironment.call by default, because operator special methods are handled by the Python interpreter, and might not correspond with exactly one method depending on the operator’s use.

The sandbox can instruct the compiler to output a function to intercept certain operators instead. Override SandboxedEnvironment.intercepted_binops and SandboxedEnvironment.intercepted_unops with the operator symbols you want to intercept. The compiler will replace the symbols with calls to SandboxedEnvironment.call_binop() and SandboxedEnvironment.call_unop() instead. The default implementation of those methods will use SandboxedEnvironment.binop_table and SandboxedEnvironment.unop_table to translate operator symbols into operator functions.

For example, the power (**) operator can be disabled:

---

## Native Python Types — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/nativetypes/

**Contents:**
- Native Python Types¶
- Examples¶
- Sandboxed Native Environment¶
- API¶

The default Environment renders templates to strings. With NativeEnvironment, rendering a template produces a native Python type. This is useful if you are using Jinja outside the context of creating text files. For example, your code may have an intermediate step where users may use templates to define values that will then be passed to a traditional string environment.

Adding two values results in an integer, not a string with a number:

Rendering list syntax produces a list:

Rendering something that doesn’t look like a Python literal produces a string:

Rendering a Python object produces that object as long as it is the only node:

You can combine SandboxedEnvironment and NativeEnvironment to get both behaviors.

An environment that renders templates to native Python types.

block_start_string (str)

block_end_string (str)

variable_start_string (str)

variable_end_string (str)

comment_start_string (str)

comment_end_string (str)

line_statement_prefix (str | None)

line_comment_prefix (str | None)

newline_sequence (te.Literal['\n', '\r\n', '\r'])

keep_trailing_newline (bool)

extensions (Sequence[str | Type[Extension]])

undefined (Type[Undefined])

finalize (Callable[[...], Any] | None)

autoescape (bool | Callable[[str | None], bool])

loader (BaseLoader | None)

bytecode_cache (BytecodeCache | None)

source (str | Template)

block_start_string (str)

block_end_string (str)

variable_start_string (str)

variable_end_string (str)

comment_start_string (str)

comment_end_string (str)

line_statement_prefix (str | None)

line_comment_prefix (str | None)

newline_sequence (te.Literal['\n', '\r\n', '\r'])

keep_trailing_newline (bool)

extensions (Sequence[str | Type[Extension]])

undefined (Type[Undefined])

finalize (Callable[[...], Any] | None)

autoescape (bool | Callable[[str | None], bool])

Render the template to produce a native Python type. If the result is a single node, its value is returned. Otherwise, the nodes are concatenated as strings. If the result can be parsed with ast.literal_eval(), the parsed value is returned. Otherwise, the string is returned.

---

## Integration — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/integration/

**Contents:**
- Integration¶
- Flask¶
- Django¶
- Babel¶
- Pylons¶

The Flask web application framework, also maintained by Pallets, uses Jinja templates by default. Flask sets up a Jinja environment and template loader for you, and provides functions to easily render templates from view functions.

Django supports using Jinja as its template engine, see https://docs.djangoproject.com/en/stable/topics/templates/#support-for-template-engines.

Jinja provides support for extracting gettext messages from templates via a Babel extractor entry point called jinja2.ext.babel_extract. The support is implemented as part of the i18n Extension extension.

Gettext messages are extracted from both trans tags and code expressions.

To extract gettext messages from templates, the project needs a Jinja section in its Babel extraction method mapping file:

The syntax related options of the Environment are also available as configuration values in the mapping file. For example, to tell the extractor that templates use % as line_statement_prefix you can use this code:

Extensions may also be defined by passing a comma separated list of import paths as the extensions value. The i18n extension is added automatically.

Template syntax errors are ignored by default. The assumption is that tests will catch syntax errors in templates. If you don’t want to ignore errors, add silent = false to the settings.

It’s easy to integrate Jinja into a Pylons application.

The template engine is configured in config/environment.py. The configuration for Jinja looks something like this:

After that you can render Jinja templates by using the render_jinja function from the pylons.templating module.

Additionally it’s a good idea to set the Pylons c object to strict mode. By default attribute access on missing attributes on the c object returns an empty string and not an undefined object. To change this add this to config/environment.py:

---

## Jinja — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/

**Contents:**
- Jinja¶

Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.

---

## Jinja — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/

**Contents:**
- Jinja¶

Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.

---

## Changes — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/changes/

**Contents:**
- Changes¶
- Version 3.1.6¶
- Version 3.1.5¶
- Version 3.1.4¶
- Version 3.1.3¶
- Version 3.1.2¶
- Version 3.1.1¶
- Version 3.1.0¶
- Version 3.0.3¶
- Version 3.0.2¶

The |attr filter does not bypass the environment’s attribute lookup, allowing the sandbox to apply its checks. GHSA-cpwx-vrp4-4pq7

The sandboxed environment handles indirect calls to str.format, such as by passing a stored reference to a filter that calls its argument. GHSA-q2x7-8rv6-6q7h

Escape template name before formatting it into error messages, to avoid issues with names that contain f-string syntax. #1792, GHSA-gmj6-6f8f-6699

Sandbox does not allow clear and pop on known mutable sequence types. #2032

Calling sync render for an async template uses asyncio.run. #1952

Avoid unclosed auto_aiter warnings. #1960

Return an aclose-able AsyncGenerator from Template.generate_async. #1960

Avoid leaving root_render_func() unclosed in Template.generate_async. #1960

Avoid leaving async generators unclosed in blocks, includes and extends. #1960

The runtime uses the correct concat function for the current environment when calling block references. #1701

Make |unique async-aware, allowing it to be used after another async-aware filter. #1781

|int filter handles OverflowError from scientific notation. #1921

Make compiling deterministic for tuple unpacking in a {% set ... %} call. #2021

Fix dunder protocol (copy/pickle/etc) interaction with Undefined objects. #2025

Fix copy/pickle support for the internal missing object. #2027

Environment.overlay(enable_async) is applied correctly. #2061

The error message from FileSystemLoader includes the paths that were searched. #1661

PackageLoader shows a clearer error message when the package does not contain the templates directory. #1705

Improve annotations for methods returning copies. #1880

urlize does not add mailto: to values like @a@b. #1870

Tests decorated with @pass_context` can be used with the |select filter. #1624

Using set for multiple assignment (a, b = 1, 2) does not fail when the target is a namespace attribute. #1413

Using set in all branches of {% if %}{% elif %}{% else %} blocks does not cause the variable to be considered initially undefined. #1253

The xmlattr filter does not allow keys with / solidus, > greater-than sign, or = equals sign, in addition to disallowing spaces. Regardless of any validation done by Jinja, user input should never be used as keys to this filter, or must be separately validated first. GHSA-h75v-3vvj-5mfj

Fix compiler error when checking if required blocks in parent templates are empty. #1858

xmlattr filter does not allow keys with spaces. GHSA-h5c8-rqwp-cp95

Make error messages stemming from invalid nesting of {% trans %} blocks more helpful. #1918

Add parameters to Environment.overlay to match __init__. #1645

Handle race condition in FileSystemBytecodeCache. #1654

The template filename on Windows uses the primary path separator. #1637

Drop support for Python 3.6. #1534

Remove previously deprecated code. #1544

WithExtension and AutoEscapeExtension are built-in now.

contextfilter and contextfunction are replaced by pass_context. evalcontextfilter and evalcontextfunction are replaced by pass_eval_context. environmentfilter and environmentfunction are replaced by pass_environment.

Markup and escape should be imported from MarkupSafe.

Compiled templates from very old Jinja versions may need to be recompiled.

Legacy resolve mode for Context subclasses is no longer supported. Override resolve_or_missing instead of resolve.

unicode_urlencode is renamed to url_quote.

Add support for native types in macros. #1510

The {% trans %} tag can use pgettext and npgettext by passing a context string as the first token in the tag, like {% trans "title" %}. #1430

Update valid identifier characters from Python 3.6 to 3.7. #1571

Filters and tests decorated with @async_variant are pickleable. #1612

Add items filter. #1561

Subscriptions ([0], etc.) can be used after filters, tests, and calls when the environment is in async mode. #1573

The groupby filter is case-insensitive by default, matching other comparison filters. Added the case_sensitive parameter to control this. #1463

Windows drive-relative path segments in template names will not result in FileSystemLoader and PackageLoader loading from drive-relative paths. #1621

Fix traceback rewriting internals for Python 3.10 and 3.11. #1535

Fix how the native environment treats leading and trailing spaces when parsing values on Python 3.10. #1537

Improve async performance by avoiding checks for common types. #1514

Revert change to hash(Node) behavior. Nodes are hashed by id again #1521

PackageLoader works when the package is a single module file. #1512

Fix a loop scoping bug that caused assignments in nested loops to still be referenced outside of it. #1427

Make compile_templates deterministic for filter and import names. #1452, 1453

Revert an unintended change that caused Undefined to act like StrictUndefined for the in operator. #1448

Imported macros have access to the current template globals in async environments. #1494

PackageLoader will not include a current directory (.) path segment. This allows loading templates from the root of a zip import. #1467

Update MarkupSafe dependency to >= 2.0. #1418

Mark top-level names as exported so type checking understands imports in user projects. #1426

Fix some types that weren’t available in Python 3.6.0. #1433

The deprecation warning for unneeded autoescape and with_ extensions shows more relevant context. #1429

Fixed calling deprecated jinja2.Markup without an argument. Use markupsafe.Markup instead. #1438

Calling sync render for an async template uses asyncio.new_event_loop This fixes a deprecation that Python 3.10 introduces. #1443

Drop support for Python 2.7 and 3.5.

Bump MarkupSafe dependency to >=1.1.

Bump Babel optional dependency to >=2.1.

Remove code that was marked deprecated.

Add type hinting. #1412

Use PEP 451 API to load templates with PackageLoader. #1168

Fix a bug that caused imported macros to not have access to the current template’s globals. #688

Add ability to ignore trim_blocks using +%}. #1036

Fix a bug that caused custom async-only filters to fail with constant input. #1279

Fix UndefinedError incorrectly being thrown on an undefined variable instead of Undefined being returned on NativeEnvironment on Python 3.10. #1335

Blocks can be marked as required. They must be overridden at some point, but not necessarily by the direct child. #1147

Deprecate the autoescape and with extensions, they are built-in to the compiler. #1203

The urlize filter recognizes mailto: links and takes extra_schemes (or env.policies["urlize.extra_schemes"]) to recognize other schemes. It tries to balance parentheses within a URL instead of ignoring trailing characters. The parsing in general has been updated to be more efficient and match more cases. URLs without a scheme are linked as https:// instead of http://. #522, 827, 1172, #1195

Filters that get attributes, such as map and groupby, can use a false or empty value as a default. #1331

Fix a bug that prevented variables set in blocks or loops from being accessed in custom context functions. #768

Fix a bug that caused scoped blocks from accessing special loop variables. #1088

Update the template globals when calling Environment.get_template(globals=...) even if the template was already loaded. #295

Do not raise an error for undefined filters in unexecuted if-statements and conditional expressions. #842

Add is filter and is test tests to test if a name is a registered filter or test. This allows checking if a filter is available in a template before using it. Test functions can be decorated with @pass_environment, @pass_eval_context, or @pass_context. #842, #1248

Support pgettext and npgettext (message contexts) in i18n extension. #441

The |indent filter’s width argument can be a string to indent by. #1167

The parser understands hex, octal, and binary integer literals. #1170

Undefined.__contains__ (in) raises an UndefinedError instead of a TypeError. #1198

Undefined is iterable in an async environment. #1294

NativeEnvironment supports async mode. #1362

Template rendering only treats \n, \r\n and \r as line breaks. Other characters are left unchanged. #769, 952, 1313

|groupby filter takes an optional default argument. #1359

The function and filter decorators have been renamed and unified. The old names are deprecated. #1381

pass_context replaces contextfunction and contextfilter.

pass_eval_context replaces evalcontextfunction and evalcontextfilter

pass_environment replaces environmentfunction and environmentfilter.

Async support no longer requires Jinja to patch itself. It must still be enabled with Environment(enable_async=True). #1390

Overriding Context.resolve is deprecated, override resolve_or_missing instead. #1380

Improve the speed of the urlize filter by reducing regex backtracking. Email matching requires a word character at the start of the domain part, and only word characters in the TLD. #1343

Fix a bug that caused callable objects with __getattr__, like Mock to be treated as a contextfunction(). #1145

Update wordcount filter to trigger Undefined methods by wrapping the input in soft_str(). #1160

Fix a hang when displaying tracebacks on Python 32-bit. #1162

Showing an undefined error for an object that raises AttributeError on access doesn’t cause a recursion error. #1177

Revert changes to PackageLoader from 2.10 which removed the dependency on setuptools and pkg_resources, and added limited support for namespace packages. The changes caused issues when using Pytest. Due to the difficulty in supporting Python 2 and PEP 451 simultaneously, the changes are reverted until 3.0. #1182

Fix line numbers in error messages when newlines are stripped. #1178

The special namespace() assignment object in templates works in async environments. #1180

Fix whitespace being removed before tags in the middle of lines when lstrip_blocks is enabled. #1138

NativeEnvironment doesn’t evaluate intermediate strings during rendering. This prevents early evaluation which could change the value of an expression. #1186

Fix a bug that prevented looking up a key after an attribute ({{ data.items[1:] }}) in an async template. #1141

Drop support for Python 2.6, 3.3, and 3.4. This will be the last version to support Python 2.7 and 3.5.

Added a new ChainableUndefined class to support getitem and getattr on an undefined object. #977

Allow {%+ syntax (with NOP behavior) when lstrip_blocks is disabled. #748

Added a default parameter for the map filter. #557

Exclude environment globals from meta.find_undeclared_variables(). #931

Float literals can be written with scientific notation, like 2.56e-3. #912, #922

Int and float literals can be written with the ‘_’ separator for legibility, like 12_345. #923

Fix a bug causing deadlocks in LRUCache.setdefault. #1000

The trim filter takes an optional string of characters to trim. #828

A new jinja2.ext.debug extension adds a {% debug %} tag to quickly dump the current context and available filters and tests. #174, #798, 983

Lexing templates with large amounts of whitespace is much faster. #857, #858

Parentheses around comparisons are preserved, so {{ 2 * (3 < 5) }} outputs “2” instead of “False”. #755, #938

Add new boolean, false, true, integer and float tests. #824

The environment’s finalize function is only applied to the output of expressions (constant or not), not static template data. #63

When providing multiple paths to FileSystemLoader, a template can have the same name as a directory. #821

Always return Undefined when omitting the else clause in a {{ 'foo' if bar }} expression, regardless of the environment’s undefined class. Omitting the else clause is a valid shortcut and should not raise an error when using StrictUndefined. #710, #1079

Fix behavior of loop control variables such as length and revindex0 when looping over a generator. #459, 751, 794, #993

Async support is only loaded the first time an environment enables it, in order to avoid a slow initial import. #765

In async environments, the |map filter will await the filter call if needed. #913

In for loops that access loop attributes, the iterator is not advanced ahead of the current iteration unless length, revindex, nextitem, or last are accessed. This makes it less likely to break groupby results. #555, #1101

In async environments, the loop attributes length and revindex work for async iterators. #1101

In async environments, values from attribute/property access will be awaited if needed. #1101

PackageLoader doesn’t depend on setuptools or pkg_resources. #970

PackageLoader has limited support for PEP 420 namespace packages. #1097

Support os.PathLike objects in FileSystemLoader and ModuleLoader. #870

NativeTemplate correctly handles quotes between expressions. "'{{ a }}', '{{ b }}'" renders as the tuple ('1', '2') rather than the string '1, 2'. #1020

Creating a NativeTemplate directly creates a NativeEnvironment instead of a default Environment. #1091

After calling LRUCache.copy(), the copy’s queue methods point to the correct queue. #843

Compiling templates always writes UTF-8 instead of defaulting to the system encoding. #889

|wordwrap filter treats existing newlines as separate paragraphs to be wrapped individually, rather than creating short intermediate lines. #175

Add break_on_hyphens parameter to |wordwrap filter. #550

Cython compiled functions decorated as context functions will be passed the context. #1108

When chained comparisons of constants are evaluated at compile time, the result follows Python’s behavior of returning False if any comparison returns False, rather than only the last one. #1102

Tracebacks for exceptions in templates show the correct line numbers and source for Python >= 3.7. #1104

Tracebacks for template syntax errors in Python 3 no longer show internal compiler frames. #763

Add a DerivedContextReference node that can be used by extensions to get the current context and local variables such as loop. #860

Constant folding during compilation is applied to some node types that were previously overlooked. #733

TemplateSyntaxError.source is not empty when raised from an included template. #457

Passing an Undefined value to get_template (such as through extends, import, or include), raises an UndefinedError consistently. select_template will show the undefined message in the list of attempts rather than the empty string. #1037

TemplateSyntaxError can be pickled. #1117

Fix a typo in Babel entry point in setup.py that was preventing installation.

Fix Python 3.7 deprecation warnings.

Using range in the sandboxed environment uses xrange on Python 2 to avoid memory use. #933

Use Python 3.7’s better traceback support to avoid a core dump when using debug builds of Python 3.7. #1050

SandboxedEnvironment securely handles str.format_map in order to prevent code execution through untrusted format strings. The sandbox already handled str.format.

Added a new extension node called OverlayScope which can be used to create an unoptimized scope that will look up all variables from a derived context.

Added an in test that works like the in operator. This can be used in combination with reject and select.

Added previtem and nextitem to loop contexts, providing access to the previous/next item in the loop. If such an item does not exist, the value is undefined.

Added changed(*values) to loop contexts, providing an easy way of checking whether a value has changed since the last iteration (or rather since the last call of the method)

Added a namespace function that creates a special object which allows attribute assignment using the set tag. This can be used to carry data across scopes, e.g. from a loop body to code that comes after the loop.

Added a trimmed modifier to {% trans %} to strip linebreaks and surrounding whitespace. Also added a new policy to enable this for all trans blocks.

The random filter is no longer incorrectly constant folded and will produce a new random choice each time the template is rendered. #478

Added a unique filter. #469

Added min and max filters. #475

Added tests for all comparison operators: eq, ne, lt, le, gt, ge. #665

import statement cannot end with a trailing comma. #617, #618

indent filter will not indent blank lines by default. #685

Add reverse argument for dictsort filter. #692

Add a NativeEnvironment that renders templates to native Python types instead of strings. #708

Added filter support to the block set tag. #489

tojson filter marks output as safe to match documented behavior. #718

Resolved a bug where getting debug locals for tracebacks could modify template context.

Fixed a bug where having many {% elif ... %} blocks resulted in a “too many levels of indentation” error. These blocks now compile to native elif ..: instead of else: if ..: #759

Fixed custom context behavior in fast resolve mode #675

Restored the original repr of the internal _GroupTuple because this caused issues with ansible and it was an unintended change. #654

Added back support for custom contexts that override the old resolve method since it was hard for people to spot that this could cause a regression.

Correctly use the buffer for the else block of for loops. This caused invalid syntax errors to be caused on 2.x and completely wrong behavior on Python 3 #669

Resolve an issue where the {% extends %} tag could not be used with async environments. #668

Reduce memory footprint slightly by reducing our unicode database dump we use for identifier matching on Python 3 #666

Fixed autoescaping not working for macros in async compilation mode. #671

Solved some warnings for string literals. #646

Increment the bytecode cache version which was not done due to an oversight before.

Corrected bad code generation and scoping for filtered loops. #649

Resolved an issue where top-level output silencing after known extend blocks could generate invalid code when blocks where contained in if statements. #651

Made the truncate.leeway default configurable to improve compatibility with older templates.

Restored the use of blocks in macros to the extend that was possible before. On Python 3 it would render a generator repr instead of the block contents. #645

Set a consistent behavior for assigning of variables in inner scopes when the variable is also read from an outer scope. This now sets the intended behavior in all situations however it does not restore the old behavior where limited assignments to outer scopes was possible. For more information and a discussion see #641

Resolved an issue where block scoped would not take advantage of the new scoping rules. In some more exotic cases a variable overridden in a local scope would not make it into a block.

Change the code generation of the with statement to be in line with the new scoping rules. This resolves some unlikely bugs in edge cases. This also introduces a new internal With node that can be used by extensions.

Fixed a regression that caused for loops to not be able to use the same variable for the target as well as source iterator. #640

Add support for a previously unknown behavior of macros. It used to be possible in some circumstances to explicitly provide a caller argument to macros. While badly buggy and unintended it turns out that this is a common case that gets copy pasted around. To not completely break backwards compatibility with the most common cases it’s now possible to provide an explicit keyword argument for caller if it’s given an explicit default. #642

Resolved a regression with call block scoping for macros. Nested caller blocks that used the same identifiers as outer macros could refer to the wrong variable incorrectly.

Released 2017-01-07, codename Derivation

Change cache key definition in environment. This fixes a performance regression introduced in 2.8.

Added support for generator_stop on supported Python versions (Python 3.5 and later)

Corrected a long standing issue with operator precedence of math operations not being what was expected.

Added support for Python 3.6 async iterators through a new async mode.

Added policies for filter defaults and similar things.

Urlize now sets “rel noopener” by default.

Support attribute fallback for old-style classes in 2.x.

Support toplevel set statements in extend situations.

Restored behavior of Cycler for Python 3 users.

Subtraction now follows the same behavior as other operators on undefined values.

map and friends will now give better error messages if you forgot to quote the parameter.

Depend on MarkupSafe 0.23 or higher.

Improved the truncate filter to support better truncation in case the string is barely truncated at all.

Change the logic for macro autoescaping to be based on the runtime autoescaping information at call time instead of macro define time.

Ported a modified version of the tojson filter from Flask to Jinja and hooked it up with the new policy framework.

Block sets are now marked safe by default.

On Python 2 the asciification of ASCII strings can now be disabled with the compiler.ascii_str policy.

Tests now no longer accept an arbitrary expression as first argument but a restricted one. This means that you can now properly use multiple tests in one expression without extra parentheses. In particular you can now write foo is divisibleby 2 or foo is divisibleby 3 as you would expect.

Greatly changed the scoping system to be more consistent with what template designers and developers expect. There is now no more magic difference between the different include and import constructs. Context is now always propagated the same way. The only remaining differences is the defaults for with context and without context.

The with and autoescape tags are now built-in.

Added the new select_autoescape function which helps configuring better autoescaping easier.

Fixed a runtime error in the sandbox when attributes of async generators were accessed.

Fixed the for_qs flag for urlencode.

Fixed regression when applying int to non-string values.

SECURITY: if the sandbox mode is used format expressions are now sandboxed with the same rules as in Jinja. This solves various information leakage problems that can occur with format strings.

Released 2015-07-26, codename Replacement

Added target parameter to urlize function.

Added support for followsymlinks to the file system loader.

The truncate filter now counts the length.

Added equalto filter that helps with select filters.

Changed cache keys to use absolute file names if available instead of load names.

Fixed loop length calculation for some iterators.

Changed how Jinja enforces strings to be native strings in Python 2 to work when people break their default encoding.

Added make_logging_undefined which returns an undefined object that logs failures into a logger.

If unmarshalling of cached data fails the template will be reloaded now.

Implemented a block set tag.

Default cache size was increased to 400 from a low 50.

Fixed is number test to accept long integers in all Python versions.

Changed is number to accept Decimal as a number.

Added a check for default arguments followed by non-default arguments. This change makes {% macro m(x, y=1, z) %} a syntax error. The previous behavior for this code was broken anyway (resulting in the default value being applied to y).

Add ability to use custom subclasses of jinja2.compiler.CodeGenerator and jinja2.runtime.Context by adding two new attributes to the environment (code_generator_class and context_class). #404

Added support for context/environment/evalctx decorator functions on the finalize callback of the environment.

Escape query strings for urlencode properly. Previously slashes were not escaped in that place.

Add ‘base’ parameter to ‘int’ filter.

Security issue: Corrected the security fix for the cache folder. This fix was provided by RedHat.

Prefix loader was not forwarding the locals properly to inner loaders. This is now fixed.

Security issue: Changed the default folder for the filesystem cache to be user specific and read and write protected on UNIX systems. See Debian bug 734747 for more information.

Fixed a bug with call_filter not working properly on environment and context filters.

Fixed lack of Python 3 support for bytecode caches.

Reverted support for defining blocks in included templates as this broke existing templates for users.

Fixed some warnings with hashing of undefineds and nodes if Python is run with warnings for Python 3.

Added support for properly hashing undefined objects.

Fixed a bug with the title filter not working on already uppercase strings.

Released 2013-05-20, codename Translation

Choice and prefix loaders now dispatch source and template lookup separately in order to work in combination with module loaders as advertised.

Fixed filesizeformat.

Added a non-silent option for babel extraction.

Added urlencode filter that automatically quotes values for URL safe usage with utf-8 as only supported encoding. If applications want to change this encoding they can override the filter.

Added keep-trailing-newline configuration to environments and templates to optionally preserve the final trailing newline.

Accessing last on the loop context no longer causes the iterator to be consumed into a list.

Python requirement changed: 2.6, 2.7 or >= 3.3 are required now, supported by same source code, using the “six” compatibility library.

Allow contextfunction and other decorators to be applied to __call__.

Added support for changing from newline to different signs in the wordwrap filter.

Added support for ignoring memcache errors silently.

Added support for keeping the trailing newline in templates.

Added finer grained support for stripping whitespace on the left side of blocks.

Added map, select, reject, selectattr and rejectattr filters.

Added support for loop.depth to figure out how deep inside a recursive loop the code is.

Disabled py_compile for pypy and python 3.

Released 2011-07-24, codename Convolution

Internal attributes now raise an internal attribute error now instead of returning an undefined. This fixes problems when passing undefined objects to Python semantics expecting APIs.

Traceback support now works properly for PyPy. (Tested with 1.4)

Implemented operator intercepting for sandboxed environments. This allows application developers to disable builtin operators for better security. (For instance limit the mathematical operators to actual integers instead of longs)

Groupby filter now supports dotted notation for grouping by attributes of attributes.

Scoped blocks now properly treat toplevel assignments and imports. Previously an import suddenly “disappeared” in a scoped block.

Automatically detect newer Python interpreter versions before loading code from bytecode caches to prevent segfaults on invalid opcodes. The segfault in earlier Jinja versions here was not a Jinja bug but a limitation in the underlying Python interpreter. If you notice Jinja segfaulting in earlier versions after an upgrade of the Python interpreter you don’t have to upgrade, it’s enough to flush the bytecode cache. This just no longer makes this necessary, Jinja will automatically detect these cases now.

The sum filter can now sum up values by attribute. This is a backwards incompatible change. The argument to the filter previously was the optional starting index which defaults to zero. This now became the second argument to the function because it’s rarely used.

Like sum, sort now also makes it possible to order items by attribute.

Like sum and sort, join now also is able to join attributes of objects as string.

The internal eval context now has a reference to the environment.

Added a mapping test to see if an object is a dict or an object with a similar interface.

Built documentation is no longer part of release.

Fixed extensions not loading properly with overlays.

Work around a bug in cpython for the debugger that causes segfaults on 64bit big-endian architectures.

Fixed an operator precedence error introduced in 2.5.2. Statements like “-foo.bar” had their implicit parentheses applied around the first part of the expression (“(-foo).bar”) instead of the more correct “-(foo.bar)”.

Improved setup.py script to better work with assumptions people might still have from it (--with-speedups).

Fixed a packaging error that excluded the new debug support.

StopIteration exceptions raised by functions called from templates are now intercepted and converted to undefineds. This solves a lot of debugging grief. (StopIteration is used internally to abort template execution)

Improved performance of macro calls slightly.

Babel extraction can now properly extract newstyle gettext calls.

Using the variable num in newstyle gettext for something else than the pluralize count will no longer raise a KeyError.

Removed builtin markup class and switched to markupsafe. For backwards compatibility the pure Python implementation still exists but is pulled from markupsafe by the Jinja developers. The debug support went into a separate feature called “debugsupport” and is disabled by default because it is only relevant for Python 2.4

Fixed an issue with unary operators having the wrong precedence.

Released 2010-05-29, codename Incoherence

Improved the sort filter (should have worked like this for a long time) by adding support for case insensitive searches.

Fixed a bug for getattribute constant folding.

Support for newstyle gettext translations which result in a nicer in-template user interface and more consistent catalogs.

It’s now possible to register extensions after an environment was created.

Fixed an error reporting bug for undefined.

Released 2010-04-13, codename Correlation

The environment template loading functions now transparently pass through a template object if it was passed to it. This makes it possible to import or extend from a template object that was passed to the template.

Added a ModuleLoader that can load templates from precompiled sources. The environment now features a method to compile the templates from a configured loader into a zip file or folder.

The _speedups C extension now supports Python 3.

Added support for autoescaping toggling sections and support for evaluation contexts.

Extensions have a priority now.

Fixed an error reporting bug on all python versions

Fixed an error reporting bug on Python 2.4

Released 2010-02-10, codename 3000 Pythons

Fixes issue with code generator that causes unbound variables to be generated if set was used in if-blocks and other small identifier problems.

Include tags are now able to select between multiple templates and take the first that exists, if a list of templates is given.

Fixed a problem with having call blocks in outer scopes that have an argument that is also used as local variable in an inner frame #360.

Greatly improved error message reporting #339

Implicit tuple expressions can no longer be totally empty. This change makes {% if %} a syntax error now. #364

Added support for translator comments if extracted via babel.

Added with-statement extension.

Experimental Python 3 support.

Fixes some smaller problems for Jinja on Jython.

Released 2009-09-13, codename Kong

Include statements can now be marked with ignore missing to skip non existing templates.

Priority of not raised. It’s now possible to write not foo in bar as an alias to foo not in bar like in python. Previously the grammar required parentheses (not (foo in bar)) which was odd.

Fixed a bug that caused syntax errors when defining macros or using the {% call %} tag inside loops.

Fixed a bug in the parser that made {{ foo[1, 2] }} impossible.

Made it possible to refer to names from outer scopes in included templates that were unused in the callers frame #327

Fixed a bug that caused internal errors if names where used as iteration variable and regular variable after the loop if that variable was unused before the loop. #331

Added support for optional scoped modifier to blocks.

Added support for line-comments.

Added the meta module.

Renamed (undocumented) attribute “overlay” to “overlayed” on the environment because it was clashing with a method of the same name.

Speedup extension is now disabled by default.

Fixed a translation error caused by looping over empty recursive loops.

Released 2008-11-23, codename Yasuzō

Fixed a bug with nested loops and the special loop variable. Before the change an inner loop overwrote the loop variable from the outer one after iteration.

Fixed a bug with the i18n extension that caused the explicit pluralization block to look up the wrong variable.

Fixed a limitation in the lexer that made {{ foo.0.0 }} impossible.

Index based subscribing of variables with a constant value returns an undefined object now instead of raising an index error. This was a bug caused by eager optimizing.

The i18n extension looks up foo.ugettext now followed by foo.gettext if an translations object is installed. This makes dealing with custom translations classes easier.

Fixed a confusing behavior with conditional extending. loops were partially executed under some conditions even though they were not part of a visible area.

Added sort filter that works like dictsort but for arbitrary sequences.

Fixed a bug with empty statements in macros.

Implemented a bytecode cache system.

The template context is now weakref-able

Inclusions and imports “with context” forward all variables now, not only the initial context.

Added a cycle helper called cycler.

Added a joining helper called joiner.

Added a compile_expression method to the environment that allows compiling of Jinja expressions into callable Python objects.

Fixed an escaping bug in urlize

Released 2008-07-17, codename Jinjavitus

The subscribing of objects (looking up attributes and items) changed from slightly. It’s now possible to give attributes or items a higher priority by either using dot-notation lookup or the bracket syntax. This also changed the AST slightly. Subscript is gone and was replaced with Getitem and Getattr.

Added support for preprocessing and token stream filtering for extensions. This would allow extensions to allow simplified gettext calls in template data and something similar.

Added TemplateStream.dump.

Added missing support for implicit string literal concatenation. {{ "foo" "bar" }} is equivalent to {{ "foobar" }}

else is optional for conditional expressions. If not given it evaluates to false.

Improved error reporting for undefined values by providing a position.

filesizeformat filter uses decimal prefixes now by default and can be set to binary mode with the second parameter.

Fixed bug in finalizer

First release of Jinja 2.

---

## Native Python Types — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/nativetypes/

**Contents:**
- Native Python Types¶
- Examples¶
- Sandboxed Native Environment¶
- API¶

The default Environment renders templates to strings. With NativeEnvironment, rendering a template produces a native Python type. This is useful if you are using Jinja outside the context of creating text files. For example, your code may have an intermediate step where users may use templates to define values that will then be passed to a traditional string environment.

Adding two values results in an integer, not a string with a number:

Rendering list syntax produces a list:

Rendering something that doesn’t look like a Python literal produces a string:

Rendering a Python object produces that object as long as it is the only node:

You can combine SandboxedEnvironment and NativeEnvironment to get both behaviors.

An environment that renders templates to native Python types.

block_start_string (str)

block_end_string (str)

variable_start_string (str)

variable_end_string (str)

comment_start_string (str)

comment_end_string (str)

line_statement_prefix (str | None)

line_comment_prefix (str | None)

newline_sequence (te.Literal['\n', '\r\n', '\r'])

keep_trailing_newline (bool)

extensions (Sequence[str | Type[Extension]])

undefined (Type[Undefined])

finalize (Callable[[...], Any] | None)

autoescape (bool | Callable[[str | None], bool])

loader (BaseLoader | None)

bytecode_cache (BytecodeCache | None)

source (str | Template)

block_start_string (str)

block_end_string (str)

variable_start_string (str)

variable_end_string (str)

comment_start_string (str)

comment_end_string (str)

line_statement_prefix (str | None)

line_comment_prefix (str | None)

newline_sequence (te.Literal['\n', '\r\n', '\r'])

keep_trailing_newline (bool)

extensions (Sequence[str | Type[Extension]])

undefined (Type[Undefined])

finalize (Callable[[...], Any] | None)

autoescape (bool | Callable[[str | None], bool])

Render the template to produce a native Python type. If the result is a single node, its value is returned. Otherwise, the nodes are concatenated as strings. If the result can be parsed with ast.literal_eval(), the parsed value is returned. Otherwise, the string is returned.

---

## Template Designer Documentation — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/templates/

**Contents:**
- Template Designer Documentation¶
- Synopsis¶
  - Template File Extension¶
- Variables¶
- Filters¶
- Tests¶
- Comments¶
- Whitespace Control¶
- Escaping¶
- Line Statements¶

This document describes the syntax and semantics of the template engine and will be most useful as reference to those creating Jinja templates. As the template engine is very flexible, the configuration from the application can be slightly different from the code presented here in terms of delimiters and behavior of undefined values.

A Jinja template is simply a text file. Jinja can generate any text-based format (HTML, XML, CSV, LaTeX, etc.). A Jinja template doesn’t need to have a specific extension: .html, .xml, or any other extension is just fine.

A template contains variables and/or expressions, which get replaced with values when a template is rendered; and tags, which control the logic of the template. The template syntax is heavily inspired by Django and Python.

Below is a minimal template that illustrates a few basics using the default Jinja configuration. We will cover the details later in this document:

The following example shows the default configuration settings. An application developer can change the syntax configuration from {% foo %} to <% foo %>, or something similar.

There are a few kinds of delimiters. The default Jinja delimiters are configured as follows:

{% ... %} for Statements

{{ ... }} for Expressions to print to the template output

{# ... #} for Comments not included in the template output

Line Statements and Comments are also possible, though they don’t have default prefix characters. To use them, set line_statement_prefix and line_comment_prefix when creating the Environment.

As stated above, any file can be loaded as a template, regardless of file extension. Adding a .jinja extension, like user.html.jinja may make it easier for some IDEs or editor plugins, but is not required. Autoescaping, introduced later, can be applied based on file extension, so you’ll need to take the extra suffix into account in that case.

Another good heuristic for identifying templates is that they are in a templates folder, regardless of extension. This is a common layout for projects.

Template variables are defined by the context dictionary passed to the template.

You can mess around with the variables in templates provided they are passed in by the application. Variables may have attributes or elements on them you can access too. What attributes a variable has depends heavily on the application providing that variable.

You can use a dot (.) to access attributes of a variable in addition to the standard Python __getitem__ “subscript” syntax ([]).

The following lines do the same thing:

It’s important to know that the outer double-curly braces are not part of the variable, but the print statement. If you access variables inside tags don’t put the braces around them.

If a variable or attribute does not exist, you will get back an undefined value. What you can do with that kind of value depends on the application configuration: the default behavior is to evaluate to an empty string if printed or iterated over, and to fail for every other operation.

For the sake of convenience, foo.bar in Jinja does the following things on the Python layer:

check for an attribute called bar on foo (getattr(foo, 'bar'))

if there is not, check for an item 'bar' in foo (foo.__getitem__('bar'))

if there is not, return an undefined object.

foo['bar'] works mostly the same with a small difference in sequence:

check for an item 'bar' in foo. (foo.__getitem__('bar'))

if there is not, check for an attribute called bar on foo. (getattr(foo, 'bar'))

if there is not, return an undefined object.

This is important if an object has an item and attribute with the same name. Additionally, the attr() filter only looks up attributes.

Variables can be modified by filters. Filters are separated from the variable by a pipe symbol (|) and may have optional arguments in parentheses. Multiple filters can be chained. The output of one filter is applied to the next.

For example, {{ name|striptags|title }} will remove all HTML Tags from variable name and title-case the output (title(striptags(name))).

Filters that accept arguments have parentheses around the arguments, just like a function call. For example: {{ listx|join(', ') }} will join a list with commas (str.join(', ', listx)).

The List of Builtin Filters below describes all the builtin filters.

Beside filters, there are also so-called “tests” available. Tests can be used to test a variable against a common expression. To test a variable or expression, you add is plus the name of the test after the variable. For example, to find out if a variable is defined, you can do name is defined, which will then return true or false depending on whether name is defined in the current template context.

Tests can accept arguments, too. If the test only takes one argument, you can leave out the parentheses. For example, the following two expressions do the same thing:

The List of Builtin Tests below describes all the builtin tests.

To comment-out part of a line in a template, use the comment syntax which is by default set to {# ... #}. This is useful to comment out parts of the template for debugging or to add information for other template designers or yourself:

In the default configuration:

a single trailing newline is stripped if present

other whitespace (spaces, tabs, newlines etc.) is returned unchanged

If an application configures Jinja to trim_blocks, the first newline after a template tag is removed automatically (like in PHP). The lstrip_blocks option can also be set to strip tabs and spaces from the beginning of a line to the start of a block. (Nothing will be stripped if there are other characters before the start of the block.)

With both trim_blocks and lstrip_blocks disabled (the default), block tags on their own lines will be removed, but a blank line will remain and the spaces in the content will be preserved. For example, this template:

With both trim_blocks and lstrip_blocks disabled, the template is rendered with blank lines inside the div:

With both trim_blocks and lstrip_blocks enabled, the template block lines are completely removed:

You can manually disable the lstrip_blocks behavior by putting a plus sign (+) at the start of a block:

Similarly, you can manually disable the trim_blocks behavior by putting a plus sign (+) at the end of a block:

You can also strip whitespace in templates by hand. If you add a minus sign (-) to the start or end of a block (e.g. a For tag), a comment, or a variable expression, the whitespaces before or after that block will be removed:

This will yield all elements without whitespace between them. If seq was a list of numbers from 1 to 9, the output would be 123456789.

If Line Statements are enabled, they strip leading whitespace automatically up to the beginning of the line.

By default, Jinja also removes trailing newlines. To keep single trailing newlines, configure Jinja to keep_trailing_newline.

You must not add whitespace between the tag and the minus sign.

It is sometimes desirable – even necessary – to have Jinja ignore parts it would otherwise handle as variables or blocks. For example, if, with the default syntax, you want to use {{ as a raw string in a template and not start a variable, you have to use a trick.

The easiest way to output a literal variable delimiter ({{) is by using a variable expression:

For bigger sections, it makes sense to mark a block raw. For example, to include example Jinja syntax in a template, you can use this snippet:

Minus sign at the end of {% raw -%} tag cleans all the spaces and newlines preceding the first character of your raw data.

If line statements are enabled by the application, it’s possible to mark a line as a statement. For example, if the line statement prefix is configured to #, the following two examples are equivalent:

The line statement prefix can appear anywhere on the line as long as no text precedes it. For better readability, statements that start a block (such as for, if, elif etc.) may end with a colon:

Line statements can span multiple lines if there are open parentheses, braces or brackets:

Since Jinja 2.2, line-based comments are available as well. For example, if the line-comment prefix is configured to be ##, everything from ## to the end of the line is ignored (excluding the newline sign):

The most powerful part of Jinja is template inheritance. Template inheritance allows you to build a base “skeleton” template that contains all the common elements of your site and defines blocks that child templates can override.

Sounds complicated but is very basic. It’s easiest to understand it by starting with an example.

This template, which we’ll call base.html, defines a simple HTML skeleton document that you might use for a simple two-column page. It’s the job of “child” templates to fill the empty blocks with content:

In this example, the {% block %} tags define four blocks that child templates can fill in. All the block tag does is tell the template engine that a child template may override those placeholders in the template.

block tags can be inside other blocks such as if, but they will always be executed regardless of if the if block is actually rendered.

A child template might look like this:

The {% extends %} tag is the key here. It tells the template engine that this template “extends” another template. When the template system evaluates this template, it first locates the parent. The extends tag should be the first tag in the template. Everything before it is printed out normally and may cause confusion. For details about this behavior and how to take advantage of it, see Null-Default Fallback. Also a block will always be filled in regardless of whether the surrounding condition is evaluated to be true or false.

The filename of the template depends on the template loader. For example, the FileSystemLoader allows you to access other templates by giving the filename. You can access templates in subdirectories with a slash:

But this behavior can depend on the application embedding Jinja. Note that since the child template doesn’t define the footer block, the value from the parent template is used instead.

You can’t define multiple {% block %} tags with the same name in the same template. This limitation exists because a block tag works in “both” directions. That is, a block tag doesn’t just provide a placeholder to fill - it also defines the content that fills the placeholder in the parent. If there were two similarly-named {% block %} tags in a template, that template’s parent wouldn’t know which one of the blocks’ content to use.

If you want to print a block multiple times, you can, however, use the special self variable and call the block with that name:

It’s possible to render the contents of the parent block by calling super(). This gives back the results of the parent block:

In the case of multiple levels of {% extends %}, super references may be chained (as in super.super()) to skip levels in the inheritance tree.

Rendering child.tmpl will give body: Hi from child. Hi from parent.

Rendering grandchild1.tmpl will give body: Hi from grandchild1.

Rendering grandchild2.tmpl will give body: Hi from grandchild2. Hi from parent.

Jinja allows you to put the name of the block after the end tag for better readability:

However, the name after the endblock word must match the block name.

Blocks can be nested for more complex layouts. By default, a block may not access variables from outside the block (outer scopes):

This example would output empty <li> items because item is unavailable inside the block. The reason for this is that if the block is replaced by a child template, a variable would appear that was not defined in the block or passed to the context.

Starting with Jinja 2.2, you can explicitly specify that variables are available in a block by setting the block to “scoped” by adding the scoped modifier to a block declaration:

When overriding a block, the scoped modifier does not have to be provided.

Blocks can be marked as required. They must be overridden at some point, but not necessarily by the direct child template. Required blocks may only contain space and comments, and they cannot be rendered directly.

Rendering page.txt or issue.txt will raise TemplateRuntimeError because they don’t override the body block. Rendering bug_report.txt will succeed because it does override the block.

When combined with scoped, the required modifier must be placed after the scoped modifier. Here are some valid examples:

extends, include, and import can take a template object instead of the name of a template to load. This could be useful in some advanced situations, since you can use Python code to load a template first and pass it in to render.

Note how extends is passed the variable with the template object that was passed to render, instead of a string.

When generating HTML from templates, there’s always a risk that a variable will include characters that affect the resulting HTML. There are two approaches:

manually escaping each variable; or

automatically escaping everything by default.

Jinja supports both. What is used depends on the application configuration. The default configuration is no automatic escaping; for various reasons:

Escaping everything except for safe values will also mean that Jinja is escaping variables known to not include HTML (e.g. numbers, booleans) which can be a huge performance hit.

The information about the safety of a variable is very fragile. It could happen that by coercing safe and unsafe values, the return value is double-escaped HTML.

If manual escaping is enabled, it’s your responsibility to escape variables if needed. What to escape? If you have a variable that may include any of the following chars (>, <, &, or ") you SHOULD escape it unless the variable contains well-formed and trusted HTML. Escaping works by piping the variable through the |e filter:

When automatic escaping is enabled, everything is escaped by default except for values explicitly marked as safe. Variables and expressions can be marked as safe either in:

The context dictionary by the application with markupsafe.Markup

The template, with the |safe filter.

If a string that you marked safe is passed through other Python code that doesn’t understand that mark, it may get lost. Be aware of when your data is marked safe and how it is processed before arriving at the template.

If a value has been escaped but is not marked safe, auto-escaping will still take place and result in double-escaped characters. If you know you have data that is already safe but not marked, be sure to wrap it in Markup or use the |safe filter.

Jinja functions (macros, super, self.BLOCKNAME) always return template data that is marked as safe.

String literals in templates with automatic escaping are considered unsafe because native Python strings are not safe.

A control structure refers to all those things that control the flow of a program - conditionals (i.e. if/elif/else), for-loops, as well as things like macros and blocks. With the default syntax, control structures appear inside {% ... %} blocks.

Loop over each item in a sequence. For example, to display a list of users provided in a variable called users:

As variables in templates retain their object properties, it is possible to iterate over containers like dict:

Python dicts may not be in the order you want to display them in. If order matters, use the |dictsort filter.

Inside of a for-loop block, you can access some special variables:

The current iteration of the loop. (1 indexed)

The current iteration of the loop. (0 indexed)

The number of iterations from the end of the loop (1 indexed)

The number of iterations from the end of the loop (0 indexed)

True if first iteration.

True if last iteration.

The number of items in the sequence.

A helper function to cycle between a list of sequences. See the explanation below.

Indicates how deep in a recursive loop the rendering currently is. Starts at level 1

Indicates how deep in a recursive loop the rendering currently is. Starts at level 0

The item from the previous iteration of the loop. Undefined during the first iteration.

The item from the following iteration of the loop. Undefined during the last iteration.

True if previously called with a different value (or not called at all).

Within a for-loop, it’s possible to cycle among a list of strings/variables each time through the loop by using the special loop.cycle helper:

Since Jinja 2.1, an extra cycle helper exists that allows loop-unbound cycling. For more information, have a look at the List of Global Functions.

Unlike in Python, it’s not possible to break or continue in a loop. You can, however, filter the sequence during iteration, which allows you to skip items. The following example skips all the users which are hidden:

The advantage is that the special loop variable will count correctly; thus not counting the users not iterated over.

If no iteration took place because the sequence was empty or the filtering removed all the items from the sequence, you can render a default block by using else:

Note that, in Python, else blocks are executed whenever the corresponding loop did not break. Since Jinja loops cannot break anyway, a slightly different behavior of the else keyword was chosen.

It is also possible to use loops recursively. This is useful if you are dealing with recursive data such as sitemaps or RDFa. To use loops recursively, you basically have to add the recursive modifier to the loop definition and call the loop variable with the new iterable where you want to recurse.

The following example implements a sitemap with recursive loops:

The loop variable always refers to the closest (innermost) loop. If we have more than one level of loops, we can rebind the variable loop by writing {% set outer_loop = loop %} after the loop that we want to use recursively. Then, we can call it using {{ outer_loop(...) }}

Please note that assignments in loops will be cleared at the end of the iteration and cannot outlive the loop scope. Older versions of Jinja had a bug where in some circumstances it appeared that assignments would work. This is not supported. See Assignments for more information about how to deal with this.

If all you want to do is check whether some value has changed since the last iteration or will change in the next iteration, you can use previtem and nextitem:

If you only care whether the value changed at all, using changed is even easier:

The if statement in Jinja is comparable with the Python if statement. In the simplest form, you can use it to test if a variable is defined, not empty and not false:

For multiple branches, elif and else can be used like in Python. You can use more complex Expressions there, too:

If can also be used as an inline expression and for loop filtering.

Macros are comparable with functions in regular programming languages. They are useful to put often used idioms into reusable functions to not repeat yourself (“DRY”).

Here’s a small example of a macro that renders a form element:

The macro can then be called like a function in the namespace:

If the macro was defined in a different template, you have to import it first.

Inside macros, you have access to three special variables:

If more positional arguments are passed to the macro than accepted by the macro, they end up in the special varargs variable as a list of values.

Like varargs but for keyword arguments. All unconsumed keyword arguments are stored in this special variable.

If the macro was called from a call tag, the caller is stored in this variable as a callable macro.

Macros also expose some of their internal details. The following attributes are available on a macro object:

The name of the macro. {{ input.name }} will print input.

A tuple of the names of arguments the macro accepts.

This is true if the macro accepts extra keyword arguments (i.e.: accesses the special kwargs variable).

This is true if the macro accepts extra positional arguments (i.e.: accesses the special varargs variable).

This is true if the macro accesses the special caller variable and may be called from a call tag.

If a macro name starts with an underscore, it’s not exported and can’t be imported.

Due to how scopes work in Jinja, a macro in a child template does not override a macro in a parent template. The following will output “LAYOUT”, not “CHILD”.

In some cases it can be useful to pass a macro to another macro. For this purpose, you can use the special call block. The following example shows a macro that takes advantage of the call functionality and how it can be used:

It’s also possible to pass arguments back to the call block. This makes it useful as a replacement for loops. Generally speaking, a call block works exactly like a macro without a name.

Here’s an example of how a call block can be used with arguments:

Filter sections allow you to apply regular Jinja filters on a block of template data. Just wrap the code in the special filter section:

Filters that accept arguments can be called like this:

Inside code blocks, you can also assign values to variables. Assignments at top level (outside of blocks, macros or loops) are exported from the template like top level macros and can be imported by other templates.

Assignments use the set tag and can have multiple targets:

Please keep in mind that it is not possible to set variables inside a block and have them show up outside of it. This also applies to loops. The only exception to that rule are if statements which do not introduce a scope. As a result the following template is not going to do what you might expect:

It is not possible with Jinja syntax to do this. Instead use alternative constructs like the loop else block or the special loop variable:

As of version 2.10 more complex use cases can be handled using namespace objects which allow propagating of changes across scopes:

Note that the obj.attr notation in the set tag is only allowed for namespace objects; attempting to assign an attribute on any other object will raise an exception.

Added in version 2.10: Added support for namespace objects

It’s possible to use set as a block to assign the content of the block to a variable. This can be used to create multi-line strings, since Jinja doesn’t support Python’s triple quotes (""", ''').

Instead of using an equals sign and a value, you only write the variable name, and everything until {% endset %} is captured.

Filters applied to the variable name will be applied to the block’s content.

Changed in version 2.10: Block assignment supports filters.

Added in version 2.8.

The extends tag can be used to extend one template from another. You can have multiple extends tags in a file, but only one of them may be executed at a time.

See the section about Template Inheritance above.

Blocks are used for inheritance and act as both placeholders and replacements at the same time. They are documented in detail in the Template Inheritance section.

The include tag renders another template and outputs the result into the current template.

The included template has access to context of the current template by default. Use without context to use a separate context instead. with context is also valid, but is the default behavior. See Import Context Behavior.

The included template can extend another template and override blocks in that template. However, the current template cannot override any blocks that the included template outputs.

Use ignore missing to ignore the statement if the template does not exist. It must be placed before a context visibility statement.

If a list of templates is given, each will be tried in order until one is not missing. This can be used with ignore missing to ignore if none of the templates exist.

A variable, with either a template name or template object, can also be passed to the statement.

Jinja supports putting often used code into macros. These macros can go into different templates and get imported from there. This works similarly to the import statements in Python. It’s important to know that imports are cached and imported templates don’t have access to the current template variables, just the globals by default. For more details about context behavior of imports and includes, see Import Context Behavior.

There are two ways to import templates. You can import a complete template into a variable or request specific macros / exported variables from it.

Imagine we have a helper module that renders forms (called forms.html):

The easiest and most flexible way to access a template’s variables and macros is to import the whole template module into a variable. That way, you can access the attributes:

Alternatively, you can import specific names from a template into the current namespace:

Macros and variables starting with one or more underscores are private and cannot be imported.

Changed in version 2.4: If a template object was passed to the template context, you can import from that object.

By default, included templates are passed the current context and imported templates are not. The reason for this is that imports, unlike includes, are cached; as imports are often used just as a module that holds macros.

This behavior can be changed explicitly: by adding with context or without context to the import/include directive, the current context can be passed to the template and caching is disabled automatically.

Here are two examples:

In Jinja 2.0, the context that was passed to the included template did not include variables defined in the template. As a matter of fact, this did not work:

The included template render_box.html is not able to access box in Jinja 2.0. As of Jinja 2.1, render_box.html is able to do so.

Jinja allows basic expressions everywhere. These work very similarly to regular Python; even if you’re not working with Python you should feel comfortable with it.

The simplest form of expressions are literals. Literals are representations for Python objects such as strings and numbers. The following literals exist:

Everything between two double or single quotes is a string. They are useful whenever you need a string in the template (e.g. as arguments to function calls and filters, or just to extend or include a template).

Integers are whole numbers without a decimal part. The ‘_’ character can be used to separate groups for legibility.

Floating point numbers can be written using a ‘.’ as a decimal mark. They can also be written in scientific notation with an upper or lower case ‘e’ to indicate the exponent part. The ‘_’ character can be used to separate groups for legibility, but cannot be used in the exponent part.

Everything between two brackets is a list. Lists are useful for storing sequential data to be iterated over. For example, you can easily create a list of links using lists and tuples for (and with) a for loop:

Tuples are like lists that cannot be modified (“immutable”). If a tuple only has one item, it must be followed by a comma (('1-tuple',)). Tuples are usually used to represent items of two or more elements. See the list example above for more details.

A dict in Python is a structure that combines keys and values. Keys must be unique and always have exactly one value. Dicts are rarely used in templates; they are useful in some rare cases such as the xmlattr() filter.

true is always true and false is always false.

The special constants true, false, and none are indeed lowercase. Because that caused confusion in the past, (True used to expand to an undefined variable that was considered false), all three can now also be written in title case (True, False, and None). However, for consistency, (all Jinja identifiers are lowercase) you should use the lowercase versions.

Jinja allows you to calculate with values. This is rarely useful in templates but exists for completeness’ sake. The following operators are supported:

Adds two objects together. Usually the objects are numbers, but if both are strings or lists, you can concatenate them this way. This, however, is not the preferred way to concatenate strings! For string concatenation, have a look-see at the ~ operator. {{ 1 + 1 }} is 2.

Subtract the second number from the first one. {{ 3 - 2 }} is 1.

Divide two numbers. The return value will be a floating point number. {{ 1 / 2 }} is {{ 0.5 }}.

Divide two numbers and return the truncated integer result. {{ 20 // 7 }} is 2.

Calculate the remainder of an integer division. {{ 11 % 7 }} is 4.

Multiply the left operand with the right one. {{ 2 * 2 }} would return 4. This can also be used to repeat a string multiple times. {{ '=' * 80 }} would print a bar of 80 equal signs.

Raise the left operand to the power of the right operand. {{ 2**3 }} would return 8.

Unlike Python, chained pow is evaluated left to right. {{ 3**3**3 }} is evaluated as (3**3)**3 in Jinja, but would be evaluated as 3**(3**3) in Python. Use parentheses in Jinja to be explicit about what order you want. It is usually preferable to do extended math in Python and pass the results to render rather than doing it in the template.

This behavior may be changed in the future to match Python, if it’s possible to introduce an upgrade path.

Compares two objects for equality.

Compares two objects for inequality.

true if the left hand side is greater than the right hand side.

true if the left hand side is greater or equal to the right hand side.

true if the left hand side is lower than the right hand side.

true if the left hand side is lower or equal to the right hand side.

For if statements, for filtering, and if expressions, it can be useful to combine multiple expressions.

For x and y, if x is false, then the value is x, else y. In a boolean context, this will be treated as True if both operands are truthy.

For x or y, if x is true, then the value is x, else y. In a boolean context, this will be treated as True if at least one operand is truthy.

For not x, if x is false, then the value is True, else False.

Prefer negating is and in using their infix notation: foo is not bar instead of not foo is bar; foo not in bar instead of not foo in bar. All other expressions require prefix notation: not (foo and bar).

Parentheses group an expression. This is used to change evaluation order, or to make a long expression easier to read or less ambiguous.

The following operators are very useful but don’t fit into any of the other two categories:

Perform a sequence / mapping containment test. Returns true if the left operand is contained in the right. {{ 1 in [1, 2, 3] }} would, for example, return true.

Converts all operands into strings and concatenates them.

{{ "Hello " ~ name ~ "!" }} would return (assuming name is set to 'John') Hello John!.

Call a callable: {{ post.render() }}. Inside of the parentheses you can use positional arguments and keyword arguments like in Python:

{{ post.render(user, full=true) }}.

Get an attribute of an object. (See Variables)

It is also possible to use inline if expressions. These are useful in some situations. For example, you can use this to extend from one template if a variable is defined, otherwise from the default layout template:

The general syntax is <do something> if <something is true> else <do something else>.

The else part is optional. If not provided, the else block implicitly evaluates into an Undefined object (regardless of what undefined in the environment is set to):

You can also use any of the methods defined on a variable’s type. The value returned from the method invocation is used as the value of the expression. Here is an example that uses methods defined on strings (where page.title is a string):

This works for methods on user-defined types. For example, if variable f of type Foo has a method bar defined on it, you can do the following:

Operator methods also work as expected. For example, % implements printf-style for strings:

Although you should prefer the .format method for that case (which is a bit contrived in the context of rendering a template):

Return the absolute value of the argument.

Get an attribute of an object. foo|attr("bar") works like foo.bar, but returns undefined instead of falling back to foo["bar"] if the attribute doesn’t exist.

See Notes on subscriptions for more details.

A filter that batches items. It works pretty much like slice just the other way round. It returns a list of lists with the given number of items. If you provide a second parameter this is used to fill up missing items. See this example:

Capitalize a value. The first character will be uppercase, all others lowercase.

Centers the value in a field of a given width.

If the value is undefined it will return the passed default value, otherwise the value of the variable:

This will output the value of my_variable if the variable was defined, otherwise 'my_variable is not defined'. If you want to use default with variables that evaluate to false you have to set the second parameter to true:

Changed in version 2.11: It’s now possible to configure the Environment with ChainableUndefined to make the default filter work on nested elements and attributes that may contain undefined values in the chain without getting an UndefinedError.

Sort a dict and yield (key, value) pairs. Python dicts may not be in the order you want to display them in, so sort them first.

Replace the characters &, <, >, ', and " in the string with HTML-safe sequences. Use this if you need to display text that might contain such characters in HTML.

If the object has an __html__ method, it is called and the return value is assumed to already be safe for HTML.

s – An object to be converted to a string and escaped.

A Markup string with the escaped text.

Format the value like a ‘human-readable’ file size (i.e. 13 kB, 4.1 MB, 102 Bytes, etc). Per default decimal prefixes are used (Mega, Giga, etc.), if the second parameter is set to True the binary prefixes are used (Mebi, Gibi).

Return the first item of a sequence.

Convert the value into a floating point number. If the conversion doesn’t work it will return 0.0. You can override this default using the first parameter.

Enforce HTML escaping. This will probably double escape variables.

Apply the given values to a printf-style format string, like string % values.

In most cases it should be more convenient and efficient to use the % operator or str.format().

Group a sequence of objects by an attribute using Python’s itertools.groupby(). The attribute can use dot notation for nested access, like "address.city". Unlike Python’s groupby, the values are sorted first so only one group is returned for each unique value.

For example, a list of User objects with a city attribute can be rendered in groups. In this example, grouper refers to the city value of the group.

groupby yields namedtuples of (grouper, list), which can be used instead of the tuple unpacking above. grouper is the value of the attribute, and list is the items with that value.

You can specify a default value to use if an object in the list does not have the given attribute.

Like the sort() filter, sorting and grouping is case-insensitive by default. The key for each group will have the case of the first item in that group of values. For example, if a list of users has cities ["CA", "NY", "ca"], the “CA” group will have two values. This can be disabled by passing case_sensitive=True.

Changed in version 3.1: Added the case_sensitive parameter. Sorting and grouping is case-insensitive by default, matching other filters that do comparisons.

Changed in version 3.0: Added the default parameter.

Changed in version 2.6: The attribute supports dot notation for nested access.

Return a copy of the string with each line indented by 4 spaces. The first line and blank lines are not indented by default.

width – Number of spaces, or a string, to indent by.

first – Don’t skip indenting the first line.

blank – Don’t skip indenting empty lines.

Changed in version 3.0: width can be a string.

Changed in version 2.10: Blank lines are not indented by default.

Rename the indentfirst argument to first.

Convert the value into an integer. If the conversion doesn’t work it will return 0. You can override this default using the first parameter. You can also override the default base (10) in the second parameter, which handles input with prefixes such as 0b, 0o and 0x for bases 2, 8 and 16 respectively. The base is ignored for decimal numbers and non-string values.

Return an iterator over the (key, value) items of a mapping.

x|items is the same as x.items(), except if x is undefined an empty iterator is returned.

This filter is useful if you expect the template to be rendered with an implementation of Jinja in another programming language that does not have a .items() method on its mapping type.

Added in version 3.1.

Return a string which is the concatenation of the strings in the sequence. The separator between elements is an empty string per default, you can define it with the optional parameter:

It is also possible to join certain attributes of an object:

Added in version 2.6: The attribute parameter was added.

Return the last item of a sequence.

Note: Does not work with generators. You may want to explicitly convert it to a list:

Return the number of items in a container.

Convert the value into a list. If it was a string the returned list will be a list of characters.

Convert a value to lowercase.

Applies a filter on a sequence of objects or looks up an attribute. This is useful when dealing with lists of objects but you are really only interested in a certain value of it.

The basic usage is mapping on an attribute. Imagine you have a list of users but you are only interested in a list of usernames:

You can specify a default value to use if an object in the list does not have the given attribute.

Alternatively you can let it invoke a filter by passing the name of the filter and the arguments afterwards. A good example would be applying a text conversion filter on a sequence:

Similar to a generator comprehension such as:

Changed in version 2.11.0: Added the default parameter.

Added in version 2.7.

Return the largest item from the sequence.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Get the object with the max value of this attribute.

Return the smallest item from the sequence.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Get the object with the min value of this attribute.

Pretty print a variable. Useful for debugging.

Return a random item from the sequence.

Filters a sequence of objects by applying a test to each object, and rejecting the objects with the test succeeding.

If no test is specified, each object will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Filters a sequence of objects by applying a test to the specified attribute of each object, and rejecting the objects with the test succeeding.

If no test is specified, the attribute’s value will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Return a copy of the value with all occurrences of a substring replaced with a new one. The first argument is the substring that should be replaced, the second is the replacement string. If the optional third argument count is given, only the first count occurrences are replaced:

Reverse the object or return an iterator that iterates over it the other way round.

Round the number to a given precision. The first parameter specifies the precision (default is 0), the second the rounding method:

'common' rounds either up or down

'ceil' always rounds up

'floor' always rounds down

If you don’t specify a method 'common' is used.

Note that even if rounded to 0 precision, a float is returned. If you need a real integer, pipe it through int:

Mark the value as safe which means that in an environment with automatic escaping enabled this variable will not be escaped.

Filters a sequence of objects by applying a test to each object, and only selecting the objects with the test succeeding.

If no test is specified, each object will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Filters a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding.

If no test is specified, the attribute’s value will be evaluated as a boolean.

Similar to a generator comprehension such as:

Added in version 2.7.

Slice an iterator and return a list of lists containing those items. Useful if you want to create a div containing three ul tags that represent columns:

If you pass it a second argument it’s used to fill missing values on the last iteration.

Sort an iterable using Python’s sorted().

reverse – Sort descending instead of ascending.

case_sensitive – When sorting strings, sort upper and lower case separately.

attribute – When sorting objects or dicts, an attribute or key to sort by. Can use dot notation like "address.city". Can be a list of attributes like "age,name".

The sort is stable, it does not change the relative order of elements that compare equal. This makes it is possible to chain sorts on different attributes and ordering.

As a shortcut to chaining when the direction is the same for all attributes, pass a comma separate list of attributes.

Changed in version 2.11.0: The attribute parameter can be a comma separated list of attributes, e.g. "age,name".

Changed in version 2.6: The attribute parameter was added.

Convert an object to a string if it isn’t already. This preserves a Markup string rather than converting it back to a basic string, so it will still be marked as safe and won’t be escaped again.

Strip SGML/XML tags and replace adjacent whitespace by one space.

Returns the sum of a sequence of numbers plus the value of parameter ‘start’ (which defaults to 0). When the sequence is empty it returns start.

It is also possible to sum up only certain attributes:

Changed in version 2.6: The attribute parameter was added to allow summing up over attributes. Also the start parameter was moved on to the right.

Return a titlecased version of the value. I.e. words will start with uppercase letters, all remaining characters are lowercase.

Serialize an object to a string of JSON, and mark it safe to render in HTML. This filter is only for use in HTML documents.

The returned string is safe to render in HTML documents and <script> tags. The exception is in HTML attributes that are double quoted; either use single quotes or the |forceescape filter.

value – The object to serialize to JSON.

indent – The indent parameter passed to dumps, for pretty-printing the value.

Added in version 2.9.

Strip leading and trailing characters, by default whitespace.

Return a truncated copy of the string. The length is specified with the first parameter which defaults to 255. If the second parameter is true the filter will cut the text at length. Otherwise it will discard the last word. If the text was in fact truncated it will append an ellipsis sign ("..."). If you want a different ellipsis sign than "..." you can specify it using the third parameter. Strings that only exceed the length by the tolerance margin given in the fourth parameter will not be truncated.

The default leeway on newer Jinja versions is 5 and was 0 before but can be reconfigured globally.

Returns a list of unique items from the given iterable.

The unique items are yielded in the same order as their first occurrence in the iterable passed to the filter.

case_sensitive – Treat upper and lower case strings as distinct.

attribute – Filter objects with unique values for this attribute.

Convert a value to uppercase.

Quote data for use in a URL path or query using UTF-8.

Basic wrapper around urllib.parse.quote() when given a string, or urllib.parse.urlencode() for a dict or iterable.

value – Data to quote. A string will be quoted directly. A dict or iterable of (key, value) pairs will be joined as a query string.

When given a string, “/” is not quoted. HTTP servers treat “/” and “%2F” equivalently in paths. If you need quoted slashes, use the |replace("/", "%2F") filter.

Added in version 2.7.

Convert URLs in text into clickable links.

This may not recognize links in some situations. Usually, a more comprehensive formatter, such as a Markdown library, is a better choice.

Works on http://, https://, www., mailto:, and email addresses. Links with trailing punctuation (periods, commas, closing parentheses) and leading punctuation (opening parentheses) are recognized excluding the punctuation. Email addresses that include header fields are not recognized (for example, mailto:address@example.com?cc=copy@example.com).

value – Original text containing URLs to link.

trim_url_limit – Shorten displayed URL values to this length.

nofollow – Add the rel=nofollow attribute to links.

target – Add the target attribute to links.

rel – Add the rel attribute to links.

extra_schemes – Recognize URLs that start with these schemes in addition to the default behavior. Defaults to env.policies["urlize.extra_schemes"], which defaults to no extra schemes.

Changed in version 3.0: The extra_schemes parameter was added.

Changed in version 3.0: Generate https:// links for URLs without a scheme.

Changed in version 3.0: The parsing rules were updated. Recognize email addresses with or without the mailto: scheme. Validate IP addresses. Ignore parentheses and brackets in more cases.

Changed in version 2.8: The target parameter was added.

Count the words in that string.

Wrap a string to the given width. Existing newlines are treated as paragraphs to be wrapped separately.

s – Original text to wrap.

width – Maximum length of wrapped lines.

break_long_words – If a word is longer than width, break it across lines.

break_on_hyphens – If a word contains hyphens, it may be split across lines.

wrapstring – String to join each wrapped line. Defaults to Environment.newline_sequence.

Changed in version 2.11: Existing newlines are treated as paragraphs wrapped separately.

Changed in version 2.11: Added the break_on_hyphens parameter.

Changed in version 2.7: Added the wrapstring parameter.

Create an SGML/XML attribute string based on the items in a dict.

Values that are neither none nor undefined are automatically escaped, safely allowing untrusted user input.

User input should not be used as keys to this filter. If any key contains a space, / solidus, > greater-than sign, or = equals sign, this fails with a ValueError. Regardless of this, user input should never be used as keys to this filter, or must be separately validated first.

Results in something like this:

As you can see it automatically prepends a space in front of the item if the filter returned something unless the second parameter is false.

Changed in version 3.1.4: Keys with / solidus, > greater-than sign, or = equals sign are not allowed.

Changed in version 3.1.3: Keys with spaces are not allowed.

Return true if the object is a boolean value.

Added in version 2.11.

Return whether the object is callable (i.e., some kind of function).

Note that classes are callable, as are instances of classes with a __call__() method.

Return true if the variable is defined:

See the default() filter for a simple way to set undefined variables.

Check if a variable is divisible by a number.

Check if the value is escaped.

Return true if the variable is even.

Return true if the object is False.

Added in version 2.11.

Check if a filter exists by name. Useful if a filter may be optionally available.

Added in version 3.0.

Return true if the object is a float.

Added in version 2.11.

Check if value is in seq.

Added in version 2.10.

Return true if the object is an integer.

Added in version 2.11.

Check if it’s possible to iterate over an object.

Return true if the variable is lowercased.

Return true if the object is a mapping (dict etc.).

Added in version 2.6.

Return true if the variable is none.

Return true if the variable is a number.

Return true if the variable is odd.

Check if an object points to the same memory address than another object:

Return true if the variable is a sequence. Sequences are variables that are iterable.

Return true if the object is a string.

Check if a test exists by name. Useful if a test may be optionally available.

Added in version 3.0.

Return true if the object is True.

Added in version 2.11.

Like defined() but the other way round.

Return true if the variable is uppercased.

The following functions are available in the global scope by default:

Return a list containing an arithmetic progression of integers. range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0. When step is given, it specifies the increment (or decrement). For example, range(4) and range(0, 4, 1) return [0, 1, 2, 3]. The end point is omitted! These are exactly the valid indices for a list of 4 elements.

This is useful to repeat a template block multiple times, e.g. to fill a list. Imagine you have 7 users in the list but you want to render three empty items to enforce a height with CSS:

Generates some lorem ipsum for the template. By default, five paragraphs of HTML are generated with each paragraph between 20 and 100 words. If html is False, regular text is returned. This is useful to generate simple contents for layout testing.

A convenient alternative to dict literals. {'foo': 'bar'} is the same as dict(foo='bar').

Cycle through values by yielding them one at a time, then restarting once the end is reached.

Similar to loop.cycle, but can be used outside loops or across multiple loops. For example, render a list of folders and files in a list, alternating giving them “odd” and “even” classes.

items – Each positional argument will be yielded in the order given for each cycle.

Added in version 2.1.

Return the current item. Equivalent to the item that will be returned next time next() is called.

Return the current item, then advance current to the next item.

Resets the current item to the first item.

A tiny helper that can be used to “join” multiple sections. A joiner is passed a string and will return that string every time it’s called, except the first time (in which case it returns an empty string). You can use this to join things:

Added in version 2.1.

Creates a new container that allows attribute assignment using the {% set %} tag:

The main purpose of this is to allow carrying a value from within a loop body to an outer scope. Initial values can be provided as a dict, as keyword arguments, or both (same behavior as Python’s dict constructor):

Changed in version 3.2: Namespace attributes can be assigned to in multiple assignment.

Added in version 2.10.

The following sections cover the built-in Jinja extensions that may be enabled by an application. An application could also provide further extensions not covered by this documentation; in which case there should be a separate document explaining said extensions.

If the i18n Extension is enabled, it’s possible to mark text in the template as translatable. To mark a section as translatable, use a trans block:

Inside the block, no statements are allowed, only text and simple variable tags.

Variable tags can only be a name, not attribute access, filters, or other expressions. To use an expression, bind it to a name in the trans tag for use in the block.

To bind more than one expression, separate each with a comma (,).

To pluralize, specify both the singular and plural forms separated by the pluralize tag.

By default, the first variable in a block is used to determine whether to use singular or plural form. If that isn’t correct, specify the variable used for pluralizing as a parameter to pluralize.

When translating blocks of text, whitespace and linebreaks result in hard to read and error-prone translation strings. To avoid this, a trans block can be marked as trimmed, which will replace all linebreaks and the whitespace surrounding them with a single space and remove leading and trailing whitespace.

This results in This is %(book_title)s. You should read it! in the translation file.

If trimming is enabled globally, the notrimmed modifier can be used to disable it for a block.

Added in version 2.10: The trimmed and notrimmed modifiers have been added.

If the translation depends on the context that the message appears in, the pgettext and npgettext functions take a context string as the first argument, which is used to select the appropriate translation. To specify a context with the {% trans %} tag, provide a string as the first token after trans.

Added in version 3.1: A context can be passed to the trans tag to use pgettext and npgettext.

It’s possible to translate strings in expressions with these functions:

_(message): Alias for gettext.

gettext(message): Translate a message.

ngettext(singular, plural, n): Translate a singular or plural message based on a count variable.

pgettext(context, message): Like gettext(), but picks the translation based on the context string.

npgettext(context, singular, plural, n): Like npgettext(), but picks the translation based on the context string.

You can print a translated string like this:

To use placeholders, use the format filter.

Always use keyword arguments to format, as other languages may not use the words in the same order.

If New Style Gettext calls are activated, using placeholders is easier. Formatting is part of the gettext call instead of using the format filter.

The ngettext function’s format string automatically receives the count as a num parameter in addition to the given parameters.

If the expression-statement extension is loaded, a tag called do is available that works exactly like the regular variable expression ({{ ... }}); except it doesn’t print anything. This can be used to modify lists:

If the application enables the Loop Controls, it’s possible to use break and continue in loops. When break is reached, the loop is terminated; if continue is reached, the processing is stopped and continues with the next iteration.

Here’s a loop that skips every second item:

Likewise, a loop that stops processing after the 10th iteration:

Note that loop.index starts with 1, and loop.index0 starts with 0 (See: For).

If the Debug Extension is enabled, a {% debug %} tag will be available to dump the current context as well as the available filters and tests. This is useful to see what’s available to use in the template without setting up a debugger.

Added in version 2.3.

The with statement makes it possible to create a new inner scope. Variables set within this scope are not visible outside of the scope.

Because it is common to set variables at the beginning of the scope, you can do that within the with statement. The following two examples are equivalent:

An important note on scoping here. In Jinja versions before 2.9 the behavior of referencing one variable to another had some unintended consequences. In particular one variable could refer to another defined in the same with block’s opening statement. This caused issues with the cleaned up scoping behavior and has since been improved. In particular in newer Jinja versions the following code always refers to the variable a from outside the with block:

In earlier Jinja versions the b attribute would refer to the results of the first attribute. If you depend on this behavior you can rewrite it to use the set tag:

In older versions of Jinja (before 2.9) it was required to enable this feature with an extension. It’s now enabled by default.

Added in version 2.4.

If you want you can activate and deactivate the autoescaping from within the templates.

After an endautoescape the behavior is reverted to what it was before.

In older versions of Jinja (before 2.9) it was required to enable this feature with an extension. It’s now enabled by default.

---

## Frequently Asked Questions — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/faq/

**Contents:**
- Frequently Asked Questions¶
- Why is it called Jinja?¶
- How fast is Jinja?¶
- Isn’t it a bad idea to put logic in templates?¶
- Why is HTML escaping not the default?¶

“Jinja” is a Japanese Shinto shrine, or temple, and temple and template share a similar English pronunciation. It is not named after the city in Uganda.

Jinja is relatively fast among template engines because it compiles and caches template code to Python code, so that the template does not need to be parsed and interpreted each time. Rendering a template becomes as close to executing a Python function as possible.

Jinja also makes extensive use of caching. Templates are cached by name after loading, so future uses of the template avoid loading. The template loading itself uses a bytecode cache to avoid repeated compiling. The caches can be external to persist across restarts. Templates can also be precompiled and loaded as fast Python imports.

We dislike benchmarks because they don’t reflect real use. Performance depends on many factors. Different engines have different default configurations and tradeoffs that make it unclear how to set up a useful comparison. Often, database access, API calls, and data processing have a much larger effect on performance than the template engine.

Without a doubt you should try to remove as much logic from templates as possible. With less logic, the template is easier to understand, has fewer potential side effects, and is faster to compile and render. But a template without any logic means processing must be done in code before rendering. A template engine that does that is shipped with Python, called string.Template, and while it’s definitely fast it’s not convenient.

Jinja’s features such as blocks, statements, filters, and function calls make it much easier to write expressive templates, with very few restrictions. Jinja doesn’t allow arbitrary Python code in templates, or every feature available in the Python language. This keeps the engine easier to maintain, and keeps templates more readable.

Some amount of logic is required in templates to keep everyone happy. Too much logic in the template can make it complex to reason about and maintain. It’s up to you to decide how your application will work and balance how much logic you want to put in the template.

Jinja provides a feature that can be enabled to escape HTML syntax in rendered templates. However, it is disabled by default.

Jinja is a general purpose template engine, it is not only used for HTML documents. You can generate plain text, LaTeX, emails, CSS, JavaScript, configuration files, etc. HTML escaping wouldn’t make sense for any of these document types.

While automatic escaping means that you are less likely have an XSS problem, it also requires significant extra processing during compiling and rendering, which can reduce performance. Jinja uses MarkupSafe for escaping, which provides optimized C code for speed, but it still introduces overhead to track escaping across methods and formatting.

---

## Switching From Other Template Engines — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/en/stable/switching/

**Contents:**
- Switching From Other Template Engines¶
- Django¶
  - Method Calls¶
  - Filter Arguments¶
  - Tests¶
  - Loops¶
  - Cycle¶
- Mako¶

This is a brief guide on some of the differences between Jinja syntax and other template languages. See Template Designer Documentation for a comprehensive guide to Jinja syntax and features.

If you have previously worked with Django templates, you should find Jinja very familiar. Many of the syntax elements look and work the same. However, Jinja provides some more syntax elements, and some work a bit differently.

This section covers the template changes. The API, including extension support, is fundamentally different so it won’t be covered here.

Django supports using Jinja as its template engine, see https://docs.djangoproject.com/en/stable/topics/templates/#support-for-template-engines.

In Django, methods are called implicitly, without parentheses.

In Jinja, using parentheses is required for calls, like in Python. This allows you to pass variables to the method, which is not possible in Django. This syntax is also used for calling macros.

In Django, one literal value can be passed to a filter after a colon.

In Jinja, filters can take any number of positional and keyword arguments in parentheses, like function calls. Arguments can also be variables instead of literal values.

In addition to filters, Jinja also has “tests” used with the is operator. This operator is not the same as the Python operator.

In Django, the special variable for the loop context is called forloop, and the empty is used for no loop items.

In Jinja, the special variable for the loop context is called loop, and the else block is used for no loop items.

In Django, the {% cycle %} can be used in a for loop to alternate between values per loop.

In Jinja, the loop context has a cycle method.

A cycler can also be assigned to a variable and used outside or across loops with the cycle() global function.

You can configure Jinja to look more like Mako:

With an environment configured like that, Jinja should be able to interpret a small subset of Mako templates without any changes.

Jinja does not support embedded Python code, so you would have to move that out of the template. You could either process the data with the same code before rendering, or add a global function or filter to the Jinja environment.

The syntax for defs (which are called macros in Jinja) and template inheritance is different too.

The following Mako template:

Looks like this in Jinja with the above configuration:

---

## Switching From Other Template Engines — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/switching/

**Contents:**
- Switching From Other Template Engines¶
- Django¶
  - Method Calls¶
  - Filter Arguments¶
  - Tests¶
  - Loops¶
  - Cycle¶
- Mako¶

This is a brief guide on some of the differences between Jinja syntax and other template languages. See Template Designer Documentation for a comprehensive guide to Jinja syntax and features.

If you have previously worked with Django templates, you should find Jinja very familiar. Many of the syntax elements look and work the same. However, Jinja provides some more syntax elements, and some work a bit differently.

This section covers the template changes. The API, including extension support, is fundamentally different so it won’t be covered here.

Django supports using Jinja as its template engine, see https://docs.djangoproject.com/en/stable/topics/templates/#support-for-template-engines.

In Django, methods are called implicitly, without parentheses.

In Jinja, using parentheses is required for calls, like in Python. This allows you to pass variables to the method, which is not possible in Django. This syntax is also used for calling macros.

In Django, one literal value can be passed to a filter after a colon.

In Jinja, filters can take any number of positional and keyword arguments in parentheses, like function calls. Arguments can also be variables instead of literal values.

In addition to filters, Jinja also has “tests” used with the is operator. This operator is not the same as the Python operator.

In Django, the special variable for the loop context is called forloop, and the empty is used for no loop items.

In Jinja, the special variable for the loop context is called loop, and the else block is used for no loop items.

In Django, the {% cycle %} can be used in a for loop to alternate between values per loop.

In Jinja, the loop context has a cycle method.

A cycler can also be assigned to a variable and used outside or across loops with the cycle() global function.

You can configure Jinja to look more like Mako:

With an environment configured like that, Jinja should be able to interpret a small subset of Mako templates without any changes.

Jinja does not support embedded Python code, so you would have to move that out of the template. You could either process the data with the same code before rendering, or add a global function or filter to the Jinja environment.

The syntax for defs (which are called macros in Jinja) and template inheritance is different too.

The following Mako template:

Looks like this in Jinja with the above configuration:

---

## Tips and Tricks — Jinja Documentation (3.1.x)

**URL:** https://jinja.palletsprojects.com/tricks/

**Contents:**
- Tips and Tricks¶
- Null-Default Fallback¶
- Alternating Rows¶
- Highlighting Active Menu Items¶
- Accessing the parent Loop¶

This part of the documentation shows some tips and tricks for Jinja templates.

Jinja supports dynamic inheritance and does not distinguish between parent and child template as long as no extends tag is visited. While this leads to the surprising behavior that everything before the first extends tag including whitespace is printed out instead of being ignored, it can be used for a neat trick.

Usually child templates extend from one template that adds a basic HTML skeleton. However it’s possible to put the extends tag into an if tag to only extend from the layout template if the standalone variable evaluates to false, which it does by default if it’s not defined. Additionally a very basic skeleton is added to the file so that if it’s indeed rendered with standalone set to True a very basic HTML skeleton is added:

If you want to have different styles for each row of a table or list you can use the cycle method on the loop object:

cycle can take an unlimited number of strings. Each time this tag is encountered the next item from the list is rendered.

Often you want to have a navigation bar with an active navigation item. This is really simple to achieve. Because assignments outside of blocks in child templates are global and executed before the layout template is evaluated it’s possible to define the active menu item in the child template:

The layout template can then access active_page. Additionally it makes sense to define a default for that variable:

The special loop variable always points to the innermost loop. If it’s desired to have access to an outer loop it’s possible to alias it:

---
