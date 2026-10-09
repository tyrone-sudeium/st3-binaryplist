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
  if view is None: view = sublime.active_window().active_view()
  return 'Property_List.tmLanguage' in view.settings().get('syntax')

def is_binary_plist(view):
  return (view.substr(Region(0, 8)) == 'bplist00' \
    or    view.substr(Region(0,19)) == '6270 6c69 7374 3030')

def keys_to_strings(data):
  if   isinstance(data,            bytes    ): return      data.decode('utf-8')
  elif isinstance(data,collections.Mapping  ): return       dict(map(keys_to_strings, data.items()))
  elif isinstance(data,collections.Iterable ): return type(data)(map(keys_to_strings, data        ))
  else:                                        return      data


class BinaryPlistCommand(EventListener):
  def on_load(self, view): # Check if binary, convert to XML, mark as "was binary"
    # print('on_load')
    if is_binary_plist(view): view.run_command('binary_plist_toggle')

  def on_post_save(self, view): # Convert back to XML
    # print('on_post_save')
    if view.get_status('is_binary_plist'): view.run_command('binary_plist_toggle',{'force_to':True})

  def on_new      (self, view):
    pass # print('on_new')
  def on_clone    (self, view):
    pass # print('on_clone')
  def on_pre_close(self, view):
    pass # print('on_pre_close')
  def on_close    (self, view):
    pass # print('on_close')
  def on_pre_save(self, view):
    pass # print('on_pre_save')
  def on_modified(self, view):
    if is_binary_plist(view): view.run_command('binary_plist_toggle')
  def on_activated(self, view):
    pass # print('on_activated')

class BinaryPlistToggleCommand(TextCommand):
  def to_xml_plist(self, edit, view):
    """Reads in the view's file, converts it to XML and replaces the view's buffer with the XML text."""
    file_name = view.file_name()
    if file_name and file_name != '' and os.path.isfile(file_name) == True:
      with open(file_name, 'rb') as fp:
        pl = plistlib.load(fp)
      ctrld = {}
      cfg = sublime.load_settings("BinaryPlist.sublime-settings")
      cv= view.settings() # Save pre/pos values to document's vars so that you can't change them after load and corrupt on save
      esc_pre= cfg.get("esc_pre"     ,None); esc_pre=esc_pre if isinstance(esc_pre,str) else None; cv.set('𝐁Plist.esc_pre'    ,esc_pre)
      esc_pos= cfg.get("esc_pos"     ,None); esc_pos=esc_pos if isinstance(esc_pos,str) else None; cv.set('𝐁Plist.esc_pos'    ,esc_pos)
      indent = cfg.get("indent"      ,None); indent =indent  if isinstance(indent ,str) else None; cv.set('𝐁Plist.indent'     ,indent)
      sep_kv = cfg.get("key_val_sep" ,None); sep_kv =sep_kv  if isinstance(sep_kv ,str) else None; cv.set('𝐁Plist.key_val_sep',sep_kv)
      max_ll = cfg.get("max_line_len",None); max_ll =max_ll  if isinstance(max_ll ,int) else None; cv.set('𝐁Plist.max_line_len',max_ll)
      uidict = cfg.get("uidict"      ,None); uidict =uidict  if isinstance(uidict,bool) else None; cv.set('𝐁Plist.uidict'      ,uidict)
      q_uid  = cfg.get("q_uid"       ,None); q_uid  =q_uid   if isinstance(q_uid  ,str) else None; cv.set('𝐁Plist.q_uid'       ,q_uid)
      is_warn= cfg.get("warn_dupe",True)

      full_text = plistlib.dumps(pl,esc_pre=esc_pre,esc_pos=esc_pos, indent=indent, sep_kv=sep_kv, max_line_len=max_ll, uidict=uidict,q_uid=q_uid, ctrld=ctrld).decode('utf-8')
      msg_status = '⇩Binary PList'
      msg_extra = []
      if ctrld.get('is_ctrl',False): msg_extra += ["␛Controls"]
      if ctrld.get('is_uid' ,False): msg_extra += ["u🆔"]
      if msg_extra: msg_status += " with ❗" + " ".join(msg_extra) + ", see end of file…"
      if ctrld.get('is_dupe',False) and is_warn: sublime.message_dialog("This file contains the same escaped control chars used to escape actual control chars!\n\nIf you save the file, these replacement chars will be unescaped and thus lost!")
      # print("view.size()={0}".format(view.size()))
      view.replace (edit, Region(0, view.size()), full_text)
      view.end_edit(edit)
      view.set_status('is_binary_plist', msg_status)
      view.set_scratch(True)

  def to_binary_plist(self, view):
    """Converts the view's XML text back to a binary plist and writes it out to the view's file."""
    file_name = view.file_name()
    if file_name and file_name != '' and os.path.isfile(file_name) == True:
      bytes = view.substr(Region(0, view.size())).encode('utf-8')
      try:
        cv= view.settings() # only use view settings to avoid config updates corrupting saves with different escapes
        uidict    = cv.get("𝐁Plist.uidict"      ,None); uidict  = uidict  if isinstance(uidict,bool) else None
        q_uid     = cv.get("𝐁Plist.q_uid"       ,None); q_uid   = q_uid   if isinstance(q_uid ,str ) else None

        pl = plistlib.loads(bytes, fmt=plistlib.FMT_XML, uidict=uidict,q_uid=q_uid)
        with open(file_name, 'wb') as fp:
          ctrld = {}
          esc_pre = cv.get("𝐁Plist.esc_pre"     ,None); esc_pre = esc_pre if isinstance(esc_pre,str) else None
          esc_pos = cv.get("𝐁Plist.esc_pos"     ,None); esc_pos = esc_pos if isinstance(esc_pos,str) else None
          indent  = cv.get("𝐁Plist.indent"      ,None); indent  = indent  if isinstance(indent ,str) else None
          sep_kv  = cv.get("𝐁Plist.key_val_sep" ,None); sep_kv  = sep_kv  if isinstance(sep_kv ,str) else None
          max_ll  = cv.get("𝐁Plist.max_line_len",None); max_ll  = max_ll  if isinstance(max_ll ,int) else None

          plistlib.dump(pl, fp, fmt=plistlib.FMT_BINARY, esc_pre=esc_pre,esc_pos=esc_pos, indent=indent, sep_kv=sep_kv, max_line_len=max_ll, uidict=uidict,q_uid=q_uid, ctrld=ctrld)
      except Exception as e:
        sublime.error_message(str(e))
        raise e

  def run(self, edit, force_to=False):
    if self.view.encoding() == 'UTF-8':
      if is_binary_plist(self.view) and not force_to:
        self.to_xml_plist(edit, self.view)
        if not is_syntax_set(self.view):
          self.view.set_syntax_file(SYNTAX_FILE)
      else: self.to_binary_plist(self.view)
    else:   self.view.set_encoding('UTF-8')
