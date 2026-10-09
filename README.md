BinaryPlist
===========

This is my take at a plist plugin for Sublime Text 4 that should make working 
with plists feel a lot more first-class.  It provides:

* Automatic conversion of binary plist to XML.  You can then edit the XML file
  in Sublime and it will automatically convert back to binary when you save.
* Cross platform support. The solution is pure python. No calls to the
  command line, no foreign-function shenanigans, just 100% python goodness.
* Plist syntax highlighting from [TextMate][1].

The python plist support is taken from the [Python 3.14 standard library][2], 
matching the Python 3.14 that ships with Sublime Text 4 build 4205 (2026-Apr-23).

Why?
=========

[Sublime Text][3] is by far my favourite text editor.  It has a fantastic 
package manager in [Package Control][4] which allows you to manage the 
installation of plugins that extend the functionality of Sublime.  Sublime 
doesn't support binary plists out of the box, but a kind sir by the name of 
[relikd][5] made a plugin that can convert to and from binary plist. I
believe this plugin improves on that one in a few key ways:

1. A more hands-off UX. The other plugin requires you to manually press some
   arcane key combination to toggle between binary (useless) and XML (useful).
   I can't imagine any situation where'd you _want_ to edit the binary in a
   binary plist by hand, which is why this one just opens as binary by default.
2. This plugin uses a plist implementation entirely implemented in Python, which 
   means it works on any platform that Sublime Text works on. The other plugin 
   calls out to the `plutil` command line tool built into macOS which 
   unfortunately means it only works on Macs. I also believe a pure python 
   implementation will have less runtime overhead than spawning a `plutil` 
   process.
4. This plugin ships with a plist syntax definition. XML plists can of course
   just use the built-in XML highlighter, but that isn't nearly as strict as
   plists are, and it doesn't support the "old-style" plist format which you
   sometimes still see.

[1]: https://github.com/textmate/property-list.tmbundle/tree/textmate-1.x
[2]: https://github.com/python/cpython/blob/v3.14.8/Lib/plistlib.py
[3]: https://www.sublimetext.com
[4]: https://packagecontrol.io/
[5]: https://github.com/relikd/Plist-Binary_sublime

### Features
  - round-trip of control chars like Backspace  `\x08` by quoting their symbolic representation `␈` in PUA Unicode chars (≝`󿿾␈󿿿` or `uFFFFE` `uFFFFF`, user-configurable)
    - ⚠data loss: arbitrary escaping is NOT supported, so if the source document contains the same escaped control chars used to escape actual control chars, those will be unescaped on save
  - supports `UID`s with two configurable escape schemes
    - `<dict><key>CF$UID</key><integer>123</integer></dict>` "dict-escaped" (standard Apple)
    - `<integer>٠123</integer>` shorter and nicer "prefix-escaped"

### Configure

  - run `Preferences: BinaryPlist Settings: Default+User` command to open default and user `BinaryPlist.sublime-settings` for a list of available settings, including seting custom control escape characters, indentation and newline density…
