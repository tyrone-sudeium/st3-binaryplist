# Changelog
All notable changes to this project will be documented in this file

[unreleased]: https://github.com/tyrone-sudeium/st3-binaryplist/compare/1.0.1...HEAD
## [Unreleased]
<!-- - ✨ __Added__ -->
  <!-- + new features -->
<!-- - Δ __Changed__ -->
  <!-- + changes in existing functionality -->
<!-- - 🐞 __Fixed__ -->
  <!-- + bug fixes -->
<!-- - 💩 __Deprecated__ -->
  <!-- + soon-to-be removed features -->
<!-- - 🗑️ __Removed__ -->
  <!-- + now removed features -->
<!-- - 🔒 __Security__ -->
  <!-- + vulnerabilities -->

- ✨ __Added__
  + support for round-trip of control chars like Backspace  `\x08` by quoting their symbolic representation `␈` in PUA Unicode chars (≝`󿿾␈󿿿` or `uFFFFE` `uFFFFF`)
    + user-configurable escape "quotes" by setting `esc_pre` and `esc_pos` values in `BinaryPlist.sublime-settings`
    - ⚠data loss: arbitrary escaping is NOT supported,so if the source document contains the same escaped control chars used to escape actual control chars, those will be unescaped on save
  + supports `UID`
  + support for configuring key/value newline separator, indent char, and max line lenght value
  + user commands to open preferences and changelog
  + alternative `UID` encoding option for better reading/editing experience (optional, user-customizable prefix):
    - `<integer>٠123</integer>` instead of
    - `<dict><key>CF$UID</key><integer>123</integer></dict>`
- Δ __Changed__
  - slightly denser layout, removes newlines between `key`s and `value`s and increases max line length from 80 to 120
- 🐞 __Fixed__
  + buggy `UID` support, the Python std library only supported `UID` at the top level(?), not in dictionaries or arrays
  + wrong defaults in user config template
  + corruption on save when settings were changed between load and save. Strictly use configs when the document was loaded
  + corruption on save when using custom UID escape mode (all ints were saved as UIDs)
- 🗑️ __Removed__
  - support for older Sublime Text versions due to requires Python 3.14, included since Sublime Text build 4205 (2026-Apr-23)

[1.0.1]: https://github.com/tyrone-sudeium/st3-binaryplist/releases/tag/1.0.1
## [1.0.1]

- 🐞 __Fixed__
  + negative integers
