Module format specification
===========================

All ints are 8 byte (even on 32bit platforms)

All strings are preceded by their length (8 bytes) + value

List of ints is preceded by 8byte length as int, then ints
List of strings is preceded by 8byte length as int, then strings
List of objects is preceded by 8byte length, then, for each:
  2 byte type ('ci', 'cs' additionally to all the ones below)
  wrapped item (like below and Int and Str)

Spec is as follows:

magic number (Int) 0xBABACACA
version number (Int) 13 for now
module name (Str)
number of exports (Int)
exported names (Str for each) of length <number of exports>
number of all items (Int)
for each item serialization with first two bytes being the type:

"bf" - builtin function, followed by name (Str)
"bt" - builtin type, followed by name (Str)
"ut" - user type

  name (Str)
  number of elements (Int)
  for each element serialized version

"uf" - user function

  name (Str)
  varnames (List[Int])
  arglist (List[Str])
  defaults (List[Int])
  constants (List)
  bytecode (Str)
