#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk, calendar, locale
from datetime import datetime
from gobject import idle_add, timeout_add_seconds, source_remove
from loginmanager import ThomeLogin
COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2
locale.setlocale(locale.LC_ALL, 'mk_MK.utf8')

class LoginUI(object):
  def __init__(self):
    pass
class MonthButton(gtk.Button):
  def __init__(self, name, trafic, callback):
    super(MonthButton, self).__init__()
    self.trafic = trafic
    myencoding= locale.getpreferredencoding()
    month = calendar.month_abbr[name]
    self.set_label("%s [_%s]" %(month.decode(myencoding), name))
    self.connect("clicked", callback,  name, trafic)
    self.set_normal()
    self.set_size_request(10, 10)
    self.show()
  def set_selected(self):
    self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))    
  def set_normal(self):
    self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("gray"))
    self.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("yellow"))
class window (gtk.Window):
  def gui_constructor(self):
    self.after_login_box.set_visible(False)
    self.traffic_view.set_visible(False)
  def calendar_buttons_cb(self, widget, month, total):
    self.totaL_bandwidth = total
    self.set_calendar_month(month)
    self.set_statistics()
  def set_statistics(self):
    self.usage_total.set_text("%s Мб" %(self.get_totaL_bandwidth()))
    # TODO: limit manager.
    self.left_total.set_text("%s Мб" %(str(int(102400  - self.totaL_bandwidth))))
  def get_totaL_bandwidth(self):
    return str(int(self.totaL_bandwidth))
  def copy_band_clicked_cb(self, widget):
    clipboard = gtk.clipboard_get()
    clipboard.set_text(self.get_totaL_bandwidth)
    clipboard.store()
  def username_input_activate_cb(self, widget):
    user_text = self.username_input.get_text()        
    if user_text != "":
      self.password_input.grab_focus()
  def username_input_icon_press_cb(self, widget, entry_icon, event):
    if entry_icon == 1:
      widget.set_text("")
      widget.grab_focus()
  def password_input_activate_cb(self, widget):
    pass_text = self.password_input.get_text()        
    if pass_text != "":
      self.toggle_user_login()
  def password_input_icon_press_cb(self, widget, entry_icon, event):
    if entry_icon == 1:
      if not widget.get_visibility():
	widget.set_property("visibility", True)
      else:
	widget.set_property("visibility", False)
  def login_btn_clicked_cb(self, widget):
    self.toggle_user_login()
  def disconnect_user(self):
    self.login_box.set_visible(True)
    self.login_btn.set_label("Најави")
    self.login_btn.grab_focus()
    self.testLogin.disconnect()
  def toggle_user_login(self):
    if not self.is_connected:
      self.testLogin.set_username(self.username_input.get_text())
      self.testLogin.set_password(self.password_input.get_text())
      if self.testLogin.login():	
	self.login_user()
	self.is_connected = True    
	self.display_username.set_markup('<span size="xx-large" color="blue">%s</span>' %(self.testLogin.get_username()))
	self.after_login_box.set_visible(True)
	self.login_btn.set_image(self.disconnect_img)
	self.traffic_view.set_visible(True)
	self.fill_month_buttons()
	# On login, set to the current month.
	self.set_calendar_month(datetime.now().month)
	self.set_statistics()
	self.status_msg.set_text("")
      else:
	self.status_msg.set_markup("<span color='red'>Внесовте погрешна лозинка.</span>")
    else:
      self.after_login_box.set_visible(False)
      self.disconnect_user()
      self.is_connected = False
      self.login_btn.set_image(self.connect_img)
      self.traffic_view.set_visible(False)
      # Cleaning up the month buttons.
      self.months_select.foreach(self.months_select.remove)
  def login_user(self):
    '''Logs the user on.'''

    self.login_box.set_visible(False)
    self.login_btn.set_label("Одјави")
  def set_months(self):
    '''Sets the months in their places.'''

    pass
  def set_calendar_month(self, month):
    '''TODO:Sets the... '''
    self.month_buttons
    self.month_buttons[self.calendar.get_date()[1]].set_normal()
    self.calendar.select_month(month, self.current_year)
    self.month_name.set_text(calendar.month_name[month])
    self.month_buttons[self.calendar.get_date()[1]].set_selected()    
  def fill_month_buttons(self):
    # Create an accelgroup and add it to the window
    accel_group = gtk.AccelGroup()    
    for i in xrange(self.month_range[0], self.month_range[1]+1):
      btn = MonthButton(i, self.testLogin.get_month(i), self.calendar_buttons_cb)
      #key, mod = gtk.accelerator_parse(str(i))
      #accel_group.connect_group(i, gtk.gdk.MOD1_MASK, gtk.ACCEL_LOCKED, self.do_it)
      key, mod = gtk.accelerator_parse(str(i))
      btn.add_accelerator("activate", accel_group, gtk.gdk.CONTROL_MASK, key, gtk.ACCEL_VISIBLE)
      #a = gtk.Alignment(0, 1, 0, 0)
      self.month_buttons[i] = btn
      self.months_select.add(self.month_buttons[i])
    self.add_accel_group(accel_group)
    self.totaL_bandwidth = self.testLogin.get_month(datetime.now().month)
  def start_builder(self):
    '''Loads the builder stuff.'''	  
    dic = {"copy_band_clicked_cb" : self.copy_band_clicked_cb, "destroy" : self.destroy,
    "username_input_activate_cb" : self.username_input_activate_cb,
    "username_input_icon_press_cb" : self.username_input_icon_press_cb,
    "password_input_activate_cb" : self.password_input_activate_cb,
    "password_input_icon_press_cb" : self.password_input_icon_press_cb,
    "login_btn_clicked_cb" : self.login_btn_clicked_cb}
    gladefile = "gui.xml"
    self.builder = gtk.Builder()
    self.builder.add_from_file(gladefile)
    self.builder.connect_signals(dic)

    self.usage_lb = self.builder.get_object("usage_lb")
    self.usage_total = self.builder.get_object("usage_total")
    self.left_total = self.builder.get_object("left_total")
    self.calendar = self.builder.get_object("calendar1")
    self.months_select = self.builder.get_object("months_select")
    self.month_name_lb = self.builder.get_object("self.month_name_lb")
    self.month_name = self.builder.get_object("month_name")
    self.login_box = self.builder.get_object("login_box")
    self.username_input = self.builder.get_object("username_input")
    self.username_input_icon_press_cb = self.builder.get_object("username_input_icon_press_cb")    
    self.password_input = self.builder.get_object("password_input")
    self.password_input_icon_press_cb = self.builder.get_object("password_input_icon_press_cb")    
    self.login_btn = self.builder.get_object("login_btn")
    self.status_msg = self.builder.get_object("status_msg")    
    self.connect_img = self.builder.get_object("connect_img")
    self.disconnect_img = self.builder.get_object("disconnect_img")
    self.after_login_box = self.builder.get_object("after_login_box")
    self.display_username = self.builder.get_object("display_username")
    self.traffic_view = self.builder.get_object("traffic_view")
  def destroy(self, widget):
    gtk.main_quit()
  def __init__(self):
    super(window, self).__init__()
    self.testLogin = ThomeLogin()
    self.store = None
    self.is_connected = False    
    self.totaL_bandwidth = 0
    # TODO: get end from current month.
    self.month_range = (4, 10)
    self.current_year = datetime.now().year
    self.month_buttons = {}
    self.start_builder()	              
    self.gui_constructor()
    self = self.builder.get_object("window1")   
    self.show()
    
def main ():
  p = window()
  gtk.main()
if __name__ == "__main__":
  main()