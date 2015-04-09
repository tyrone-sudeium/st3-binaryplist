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
    view.substr(Region(0,19)) == '6270 6c69 7374 3030')

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
    # print('on_load')
    if is_binary_plist(view):
      view.run_command('binary_plist_toggle')
    
  def on_post_save(self, view):
    # print('on_post_save')
    # Convert back to XML
    if view.get_status('is_binary_plist'):
      view.run_command('binary_plist_toggle', {'force_to':True})

  def on_new(self, view):
    pass
    # print('on_new')

  def on_clone(self, view):
    pass
    # print('on_clone')

  def on_pre_close(self, view):
    pass
    # print('on_pre_close')

  def on_close(self, view):
    pass
    # print('on_close')

  def on_pre_save(self, view):
    pass
    # print('on_pre_save')

  def on_modified(self, view):
    freshly_written = view.settings().get('freshly_written')
    if freshly_written and is_binary_plist(view):
      view.run_command('binary_plist_toggle')
      view.settings().erase('freshly_written')


  def on_activated(self, view):
    pass
    # print('on_activated')

class BinaryPlistToggleCommand(TextCommand):
  def to_xml_plist(self, edit, view):
    """Reads in the view's file, converts it to XML and replaces the view's
    buffer with the XML text."""
    file_name = view.file_name()
    if file_name and file_name != '' and os.path.isfile(file_name) == True:
      with open(file_name, 'rb') as fp:
        pl = plistlib.load(fp)
      full_text = plistlib.dumps(pl).decode('utf-8')
      view.set_encoding('UTF-8')
      # print("view.size()={0}".format(view.size()))
      view.replace(edit, Region(0, view.size()), full_text)
      view.end_edit(edit)
      view.set_status('is_binary_plist', 'Saving As Binary Property List')
      view.set_scratch(True)

  def to_binary_plist(self, view):
    """Converts the view's XML text back to a binary plist and writes it out
    to the view's file."""
    file_name = view.file_name()
    if file_name and file_name != '' and os.path.isfile(file_name) == True:
      bytes = view.substr(Region(0, view.size())).encode('utf-8')
      try:
        pl = plistlib.loads(bytes, fmt=plistlib.FMT_XML)
        with open(file_name, 'wb') as fp:
          plistlib.dump(pl, fp, fmt=plistlib.FMT_BINARY)
          view.settings().set('freshly_written', True)
      except Exception as e:
        sublime.error_message(str(e))
        raise e

  def run(self, edit, force_to=False):
    if is_binary_plist(self.view) and not force_to:
      self.to_xml_plist(edit, self.view)
      if not is_syntax_set(self.view):
        self.view.set_syntax_file(SYNTAX_FILE)
    else:
      self.to_binary_plist(self.view)
