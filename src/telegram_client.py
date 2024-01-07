import configparser
import tkinter as tk

import ttkbootstrap as ttb
from ttkbootstrap.constants import *


# Manipulate with screen size
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Setting configuration values

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone=0
username=""

root = tk.Tk()
root.attributes('-fullscreen', True)
style= ttb.Style(theme="darkly")
style.theme_use()

 # Bind Escape key to toggle fullscreenpylint
root.bind("<Escape>", toggle_fullscreen) 
toggle_fullscreen()

#Initialize gui elements
phone_entry = ttb.Entry(root)
code_entry = ttb.Entry(root)
password_entry = ttb.Entry(root)
username_entry = ttb.Entry(root)
