import os
from tkinter import Tk, Text, Menu, Scrollbar, filedialog, messagebox, constants
from PIL import Image, ImageTk


#------------------------------------------------------------------------------
# Constant definitions
#------------------------------------------------------------------------------

# Constant defs for file types
PLAT_FILE_TYPES = [
    ("All Files", "*.*"),
    ("C Header File", "*.h*"),
    ("C Source File", "*.c*"),
    ("Cascading Style Sheet File", "*.css*"),
    ("Configuration File", "*.conf*"),
    ("C# File", "*.cs*"),
    ("C++ Header File", "*.hpp*"),
    ("C++ Source File", "*.cpp*"),
    ("HTML File", "*.html*"),
    ("JavaScript File", "*.js*"),
    ("JSON File", "*.json*"),
    ("PHP File", "*.php*"),
    ("Python File", "*.py*"),
    ("Shell Script File", "*.sh*"),
    ("Text File", "*.txt*"),
    ("Yet Another Markup Language File", "*.yaml*")
]

# Constant for files
PLAT_NAME_SHORT = "Platinum"
PLAT_NAME_FULL = "Platinum Text Editor"
PLAT_DEFAULT_FILE_NAME = "untitled"
PLAT_DEFAULT_FILE_EXT = ".txt"

# Constants for styling
PADDING_TEXT_X = 8
PADDING_TEXT_Y = 8

# Ported constants from tkinter
# -anchor and -sticky
N='n'
S='s'
W='w'
E='e'
NW='nw'
SW='sw'
NE='ne'
SE='se'
NS='ns'
EW='ew'
NSEW='nsew'
CENTER='center'

# -fill
NONE='none'
X='x'
Y='y'
BOTH='both'

# -side
LEFT='left'
TOP='top'
RIGHT='right'
BOTTOM='bottom'

# -orient
HORIZONTAL='horizontal'
VERTICAL='vertical'

END = 'end'

#------------------------------------------------------------------------------
# Static/Global definitions
#------------------------------------------------------------------------------

# Prefixed with underscore
_file_name = PLAT_DEFAULT_FILE_NAME
_file_ext = PLAT_DEFAULT_FILE_EXT
_file_path = None
_text_change = False
_win_root = None
_win_text = None
_win_scrollbar = None

#------------------------------------------------------------------------------
# Function definitions
#------------------------------------------------------------------------------

# Open file at specified path
# Returns a handle
def file_open():
    global _file_path, _win_text
    
    try:
        opened_file = filedialog.askopenfilename(defaultextension=PLAT_DEFAULT_FILE_EXT, filetypes=PLAT_FILE_TYPES)

        if opened_file == None or opened_file == "":
            return

        win_text_area_reset()

        with open(opened_file, "r") as file:
            _win_text.insert(1.0, file.read())
            file.close()
            _file_path = opened_file
            win_root_set_title("{} - {}".format(PLAT_NAME_SHORT,_file_path))
    except:
        messagebox.showerror("{} - Error".format(PLAT_NAME_SHORT), "Error opening file")

# Save changes to a file
def file_save():
    global _file_path, _win_text
    text = _win_text.get(1.0, END)

    if _file_path == None or _file_path == "":
        return

    try:
        file = open(_file_path, "w")
        file.write(text)
        file.close()
    except:
        messagebox.showerror("{} - Error".format(PLAT_NAME_SHORT), "Error during Save")


# Save a file as a specific file type
def file_save_as():
    global _file_path, _win_text
    text = _win_text.get(1.0, END)

    try:
        saved_file = filedialog.asksaveasfilename(initialfile="{}{}".format(PLAT_DEFAULT_FILE_NAME,PLAT_DEFAULT_FILE_EXT), defaultextension=PLAT_DEFAULT_FILE_EXT, filetypes=PLAT_FILE_TYPES)
        
        if saved_file == None or saved_file == "":
            return
        
        file = open(saved_file, "w")
        file.write(text)
        file.close()
        _file_path = saved_file
    except:
        messagebox.showerror("{} - Error".format(PLAT_NAME_SHORT), "Error during Save As")

def file_close(set_title = True):
    global _win_text, _file_path

    if set_title == True:
        win_root_set_title("{}".format(PLAT_NAME_FULL))
    _win_text.delete(1.0, END)

    if _file_path == None or _file_path == "":
        pass
    else:
        try:
            with open(_file_path, "r") as file:
                file.close()
                _file_path = None
        except:
            messagebox.showerror("{} - Error".format(PLAT_NAME_SHORT), "Error closing file")

# Start new file
# Returns a handle
def file_new():
    global _win_root, _win_text

    win_root_set_title("{} - {}{}".format(PLAT_NAME_SHORT,PLAT_DEFAULT_FILE_NAME,PLAT_DEFAULT_FILE_EXT))
    _win_text.delete(1.0, END)
    _file_path = "./{}{}".format(PLAT_DEFAULT_FILE_NAME,PLAT_DEFAULT_FILE_EXT)

def plat_about():
    messagebox.showinfo("About Platinum", "Platinum is a multiplatform text editor written by a developer for developers.")

def plat_help():
    messagebox.showinfo("Platinum Help", "There will be help here, eventually...")

def plat_set_file(name, ext):
    global _file_name, _file_ext

    _file_name = name
    _file_ext = ext

# Destroys a window; will end program if root is destroyed
def win_destroy(win):
    win.destroy()

# Destroys the root window; will end program
def win_root_destroy():
    global _win_root

    _win_root.destroy()

# Add menu bar to root
def win_root_add_menu():
    global _win_root

    menu_main = Menu(_win_root)

    # Submenu File
    submenu_file = Menu(menu_main, tearoff=False, activebackground="DodgerBlue")
    submenu_file.add_command(label="New File", command=file_new)
    submenu_file.add_command(label="Open File", command=file_open)
    submenu_file.add_command(label="Save File", command=file_save)
    submenu_file.add_command(label="Save File As", command=file_save_as)
    submenu_file.add_command(label="Close File", command=file_close)
    submenu_file.add_command(label="Exit", command=win_root_destroy)
    menu_main.add_cascade(label="File", menu=submenu_file)

    submenu_about = Menu(menu_main, tearoff=False, activebackground="DodgerBlue")
    submenu_about.add_command(label="Help", command=plat_help)
    submenu_about.add_command(label="About", command=plat_about)
    menu_main.add_cascade(label="About", menu=submenu_about)

    _win_root.config(menu=menu_main)

def win_root_bind_keys():
    global _win_root
    
    #_win_root.bind("<Control-C>", txt_copy)
    #_win_root.bind("<Control-X>", txt_cut)
    #_win_root.bind("<Control-V>", txt_paste)

def win_root_set_title(text):
    global _win_root

    _win_root.title(text)

def win_text_area_init():
    global _win_root, _win_text, _win_scrollbar

    _win_text = Text(_win_root, font=("Courier New", 12), padx=PADDING_TEXT_X, pady=PADDING_TEXT_Y)
    _win_text.grid(sticky=NSEW)
    _win_text.pack(fill=BOTH, expand=True)

    _win_scrollbar = Scrollbar(_win_text, orient=VERTICAL)
    _win_scrollbar.pack(side=RIGHT, fill=Y)
    _win_scrollbar.config(command=_win_text.yview)
    _win_text.config(yscrollcommand=_win_scrollbar.set)

def win_text_area_reset():
    global _win_text

    _win_text.delete(1.0, END)

# Spawn the root window
# Returns the root
def win_root_init():
    global _win_root

    _win_root = Tk()
    _win_root.title("Platinum")
    _win_root.geometry('800x600')
    _win_root.resizable(1, 1)

    ico = ImageTk.PhotoImage(Image.open('./img/icon_16.png'))
    _win_root.iconphoto(True, ico)

def txt_copy():
    global _win_text

    _win_text.event_generate("<<Copy>>")

def txt_cut():
    global _win_text

    _win_text.event_generate("<<Cut>>")

def txt_paste():
    global _win_text

    _win_text.event_generate("<<Paste>>")

def txt_select_all():
    global _win_text

    _win_text.event_generate("<<Control-Keypress-A>>")

def txt_delete():
    global _win_text

    _win_text.event_generate("KP_Delete")


def main():
    global _win_root, _win_text

    win_root_init()
    win_root_add_menu()
    win_text_area_init()

    _win_root.update()
    _win_root.mainloop()


if __name__ == "__main__":
    main()