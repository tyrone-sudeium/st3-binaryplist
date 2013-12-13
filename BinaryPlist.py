import sublime
from sublime import Region
import os
import sublime_plugin
from sublime_plugin import EventListener
from sublime_plugin import TextCommand
from .plistlib import plistlib
import collections

# GLOBAL STUFF
SYNTAX_FILE = 'Packages/BinaryPlist/Property_List.tmLanguage'

def is_syntax_set(view=None):
  if view is None:
    view = sublime.active_window().active_view()
  return 'Property_List.tmLanguage' in view.settings().get('syntax')

def is_binary_plist(view):
  return (view.substr(Region(0,8)) == 'bplist00' or 
    view.substr(Region(0,20)) == '6270 6c69 7374 3030')

def keys_to_strings(data):
  if isinstance(data, bytes):
      return data.decode('utf-8')
  elif isinstance(data, collections.Mapping):
      return dict(map(keys_to_strings, data.items()))
  elif isinstance(data, collections.Iterable):
      return type(data)(map(keys_to_strings, data))
  else:
      return data


class BinaryPlistCommand(EventListener):
  def on_load(self, view):
    # Check if binary, convert to XML, mark as "was binary"
    if is_binary_plist(view):
      view.run_command('binary_plist_toggle')
      if not is_syntax_set(view):
        view.set_syntax_file(SYNTAX_FILE)
    
  def on_post_save(self, view):
    # Convert back to XML
    if view.settings().get('is_binary_plist'):
      view.run_command('binary_plist_toggle', force_to=True)

class BinaryPlistToggleCommand(TextCommand):
  def to_xml_plist(self, edit, view):
    file_name = view.file_name()
    if file_name and file_name != '' and os.path.isfile(file_name) == True:
      with open(file_name, 'rb') as fp:
        pl = plistlib.load(fp)
        full_text = plistlib.dumps(pl).decode('utf-8')
        view.set_encoding('UTF-8')
        view.replace(edit, Region(0, view.size()), full_text)
        view.sel().clear()
        view.sel().add(sublime.Region(0))
        view.end_edit(edit)
        view.settings().set('is_binary_plist', True)

  def run(self, edit, **args):
    if is_binary_plist(self.view) or args['force_to']:
      self.to_xml_plist(edit, self.view)
    else:
      print("Not binary plist")
