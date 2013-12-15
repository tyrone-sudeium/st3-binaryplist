BinaryPlist
===========

I'm an Objective-C developer by trade and a Ruby developer at heart, so excuse
my poor python skills.  This is my take at a plist plugin for Sublime Text 3
that should make working with plists feel a lot more first-class.  It provides:

* Automatic conversion of binary plist to XML.  You can then edit the XML file
  in Sublime and it will automatically convert back to binary when you save.
* Cross platform support.  The solution is pure python.  No calls to the
  command line, no foreign-function shenanigans, just 100% python goodness.
* Plist syntax highlighting from [TextMate][4].

The python plist support is taken from the [Python 3.4 standard library][5], 
with a few modifications to support running in the Python 3.3 that ships with
Sublime Text 3.  This library therefore has a heavy dependency on Python 3.x
which is why it'll probably never work with Sublime Text 2.  Seriously, just
use Sublime Text 3, it's awesome.