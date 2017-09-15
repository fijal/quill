
Easy beginnings
===============

The basic way to run a quill program is as follows::

   quill program.q

In some examples the program might contain import statements, of form roughly
``import foo.bar``. What does that do? It would insert into local namespace
an object (or module) ``bar``, from package ``foo``. How exactly the packages
are being made visible is described in later sections. Packages ``core`` and
``std`` are special and always visible. The import can have three forms::

  import foo
  import foo.bar
  import foo{bar,baz}

The first one is equivalent to "put ``foo`` into global namespace. Then you
can write ``foo.bar`` anywhere, provided ``foo`` exports symbol (or module)
``bar``. Second one let's you import directly name ``bar`` without needing
to say ``foo.bar``. The third form is a short for ``import foo.bar`` followed
by ``import foo.baz`` and has the exact same effect.

By default the packages available would be all the packages installed, imported
in the latest version. If you want to be more specific about the versions,
you need to have a ``spec file``, which is described below.

Authoring a package
===================

Every now and again you might want to provide a piece of software that's more
complicated than a single file. In this case, we require you to write
a package, but don't worry it's not that complicated.

The package looks more or less like that:

  package_dir/
  package_dir/index.q
  package_dir/entrypoint/
  package_dir/entrypoint/<some exec>.q
  package_dir/spec

The ``entrypoint`` directory and ``index.q`` are optional, but you have to have
at least one of those. ``index.q`` specifies what modules should be imported when
compiling the package. ``entrypoint/*.q`` is a place to put executables that
are exported by that package.

The main way to run the entrypoint, without compilation would be to run::

  quill package_dir/entrypoint/foo.q

Which will run ``foo.q``. Inside packages there is a special module for imports
called ``self``. Imagine we have directory structure like this::

  bamboozle/bob.q
  bamboozle/entrypoint/run.q

Then if ``bob.q`` contains::

  def do_bob_things() {
      return 3
  }

We can run ``quill bamboozle/entrypoint/run.q`` with ``run.q`` containing::

  import self.bob

  def main() {
      print(bob.do_bob_things())
  }

Which ideally should print 3.

Spec file
=========

XXX

Compiling a package
===================

XXX

Installing a package
====================

XXX
