#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from socket import *
from threading import Thread
from random import randrange

# About Window
class AboutDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Fsociety Chat 1.0 - About", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(350, 100)
        self.set_border_width(5)
        
        label = Gtk.Label("\nDeveloped by:\n\nSamuel Paz\nhttps://github.com/samuelpaz\n")
        label.set_justify(Gtk.Justification.CENTER)
        box = self.get_content_area()
        box.add(label)
        self.show_all()

# Nickname Entry Window        
class NicknameDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Enter a Nickname")

        self.set_default_size(350, 100)
        self.set_border_width(5)
        self.grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        self.add(self.grid)
        
        #generate a default nickname
        self.default_user = "User" + str(randrange(1111, 9999))
        self.create_nick_entry()
        self.create_buttons()
        
    def create_nick_entry(self):
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_text(self.default_user)
        self.entry.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.entry, 0, 0, 4, 1)
        
    def create_buttons(self):
        self.button1 = Gtk.Button.new_with_label("Confirm")
        self.button1.connect("clicked", self.on_click_me_clicked)
        self.grid.attach(self.button1, 0, 1, 2, 1)
        
        self.button2 = Gtk.Button.new_with_label("Cancel")
        self.button2.connect("clicked", self.on_click_me_clicked2)
        self.grid.attach_next_to(self.button2, self.button1, Gtk.PositionType.RIGHT, 2, 1)
        
    # Buttons Events
    def on_click_me_clicked(self, widget):
        if self.entry.get_text() != "" :
            client_socket.send(bytes(self.entry.get_text(), "utf8"))
        else:
            client_socket.send(bytes(self.default_user, "utf8"))
        self.destroy()
        
    def on_click_me_clicked2(self, widget):
        client_socket.send(bytes(self.default_user, "utf8"))
        self.destroy()
        
# Main Window
class TextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Fsociety Chat 1.0")

        self.set_default_size(650, 450)
        self.set_border_width(5)
        
        self.connect("destroy", self.on_closing)

        self.grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        self.add(self.grid)
        self.create_textview()
        self.create_buttons()
        self.create_textsend()
        self.create_menubar()

        self.receive_thread = Thread(target = self.receive, args=())
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
    def create_menubar(self):
        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        self.grid.attach(menubar, 0, 0, 6, 1)

        menuitem = Gtk.MenuItem(label="File")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="Quit")
        menuitem.connect("activate", self.on_closing)
        menu.append(menuitem)

        menuitem = Gtk.MenuItem(label="Help")
        menubar.append(menuitem)

        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="About")
        menuitem.connect("activate", self.about_win)
        menu.append(menuitem)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 6, 1)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(" Welcome to [Fsociety Chat] Server.\n\n")
        scrolledwindow.add(self.textview)

    def create_buttons(self):
        self.button = Gtk.Button.new_with_label("Send")
        self.button.connect("clicked", self.on_click_me_clicked)
        self.grid.attach(self.button, 0, 3, 1, 1)

    def create_textsend(self):
        self.entry = Gtk.Entry()
        self.entry.set_text("type message here...")
        self.entry.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.entry, 1, 3, 5, 1)

    # Buttons and Connection Events
    def on_click_me_clicked(self, widget):
        client_socket.send(bytes(self.entry.get_text(), "utf8"))
        self.entry.set_text("")

    def receive(self):
        while True:
            try:
                msg = client_socket.recv(BUFFSIZE).decode("utf8")
                self.textbuffer.insert_at_cursor(msg + "\n")
            except OSError:
                break
     
    # Call About Window           
    def about_win(self, widget):
        dialog = AboutDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
        dialog.destroy()

                
    # Closing Client
    def on_closing(self, widget):
        client_socket.send(bytes("/quit", "utf8"))
        client_socket.close()
        Gtk.main_quit()


# Default Buffsize, address and port
BUFFSIZE = 1024
ADDR = ("127.0.0.1", 33000)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

win = TextViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
nick = NicknameDialog()
nick.show_all()
Gtk.main()
