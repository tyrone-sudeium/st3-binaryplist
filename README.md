BinaryPlist
===========

I'm an Objective-C developer by trade and a Ruby developer at heart, so excuse
my poor python skills.  This is my take at a plist plugin for Sublime Text 3
that should make working with plists feel a lot more first-class.  It provides:

* Automatic conversion of binary plist to XML.  You can then edit the XML file
  in Sublime and it will automatically convert back to binary when you save.
* Cross platform support. The solution is pure python. No calls to the
  command line, no foreign-function shenanigans, just 100% python goodness.
* Plist syntax highlighting from [TextMate][1].

The python plist support is taken from the [Python 3.4 standard library][2], 
with a few modifications to support running in the Python 3.3 that ships with
Sublime Text 3.  This library therefore has a heavy dependency on Python 3.x
which is why it'll probably never work with Sublime Text 2.  Seriously, just
use Sublime Text 3, it's awesome.

Why?
=========

[Sublime Text][3] is by far my favourite text editor.  It has a fantastic 
package manager in [Package Control][4] which allows you to manage the 
installation of plugins that extend the functionality of Sublime.  Sublime 
doesn't support binary plists out of the box, but a kind sir by the name of 
[relikd][5] made a plugin that can convert to and from binary plist.  I have a
couple of problems with his implementation, though:

1. The UX leaves a lot to be desired.  It requires you to manually press some
   arcane key combination to toggle between binary (useless) and XML (useful).
   I can't imagine any situation where'd you _want_ to edit the binary in a
   binary plist by hand, so why open it as binary by default?
2. Internally, it just calls the `plutil` command line tool that ships with
   OS X.  This means it requires OS X to work.  Ideally, this should be an
   entirely python native solution, which would work on any platform, on the
   off-chance you encounter a plist file on a non-Apple computer.  Having to 
   start up a command line app doesn't strike me as particularly efficient
   either.
3. It doesn't ship with a plist syntax definition.  XML plists can of course
   just use the built-in XML highlighter, but that isn't nearly as strict as
   plists are, and it doesn't support the "old-style" plist format which you
   sometimes still see.

[1]: https://github.com/textmate/property-list.tmbundle/tree/textmate-1.x
[2]: http://hg.python.org/cpython/file/default/Lib/plistlib.py
[3]: http://www.sublimetext.com/3
[4]: https://sublime.wbond.net/
[5]: https://github.com/relikd/Plist-Binary_sublime
