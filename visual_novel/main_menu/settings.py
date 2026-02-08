import tkinter as tk
from style import header_start_buttons

'''
This opens a tkinker window that has settings on it 
'''

class open_settings:
    def __init__(self, start_options):
        self.start_options = start_options
        self.root = tk.Toplevel(start_options)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.overrideredirect(True)

        button_frame = tk.Frame(self.root, bg = "#9A9F8E")
        button_frame.place(relx=0.5, rely = 0.5, anchor = "center")

        lighting = tk.Button(button_frame,
                             text = "Lighting",
                             command = self.lighting,
                             **header_start_buttons)
        
        resolution = tk.Button(button_frame,
                               text = "Resolution",
                               command = self.resolution,
                               **header_start_buttons)

        back = tk.Button(button_frame,
                         text = "Back",
                         command = self.back,
                         **header_start_buttons)
        
        lighting.pack(pady = 10, padx = 10)
        resolution.pack(pady = 10, padx = 10)
        back.pack(pady = 10, padx = 10)
        
    def back(self):
        self.start_options.deiconify()
    def lighting(self):
        return None
    def resolution(self):
        return None
    