# nolang
A language experiment

## General Goals

Take the good parts of Python, get rid of the bad ones and learn from other
languages

## Decisions Taken So Far

Here is why certain things were decided this way for now:

### Immutable Module Scope

Unlike Python the global scope is immutable.  The only thing that can be done
on the global scope is introduce explicit bindings which in themselves can be
mutable.

### Semicolons / Braces

Instead of using indentation based syntax like in Python we go with braces and
semicolons like in Rust.

The reason this is preferrable over no semicolons and indentation based syntax:

* easier to write editor support for
* clear ends of blocks (allows better syntax for anonymous functions)
* supports trivial minification in places where this matters
* permits easy code generation

### Main Function

When a file is executed as a script the function named `main` is executed as
entry point.  This lets us used an immutable global scope and solves a lot of
issues with the entry point file being different like in Python

### Bindings

Imports and globals are impemented as bindings.  A binding is a completely
transparent "proxy" that gives access to the underlying value.  A binding can
be of one of the following types:

* global immutable: a binding that points to a value that cannot be overridden
* contextual immutable: a binding that resolves to the current context and cannot be overridden
* contextual mutable: a binding that resolves to data in the current context and can be modified

A binding is initialized once (either on the global context or the current local
context) through a callback.  It's guaranteed that this is only executed once.

Pseudocode:

```
binding LANG: str = ContextBinding(lambda: os.environ['LANG'])
```

When `LANG` is accessed it works exactly like any other variable.  On first
access per context however that value will be initialized by calling the
function.  If it's overridden it will be overridden for the current context
only in this case.

### Context Management

A context is automatically created and can be overridden.  A context can be
created in two modes: isolated or non isolated.  If a context is created
in an isolated way then all context bindings that are set to be isolated will
be recreated.  Non isolated bindings will be inherited.

```
binding current_user: User = ContextBinding(
  lambda: get_user_from_request_or_something(),
  isolated=true)

with new_context(isolated=true) {
  /* because this is created isolated, the current_user init function
     will be called again.  It's not inherited into this context. */
}
```
