#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 16:56:41 2025

@author: peppermintbalcon
"""

import tkinter as tk


class Inventory:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title("Backpack")
        self.window.overrideredirect(True)

        self.window.lift()
        self.window.attributes("-topmost", True)
        self.window.after_idle(self.window.attributes, '-topmost', False)
        
        #the player should start with these items 
        self.items = {
            "pencil" : {"count" : 2, "image" : "pencil.png"},
            "notebook" : {"count": 1, "image" : "notebook.png"},
            "iphone" : {"count": 1, "image" : "iphone.png"}
            }
        
        self.images = {}
        self.buttons = {}
        
        exit_button = tk.Button(self.window,
                                text= "Exit",
                                command= self.exit_inv,
                                font=("Comic Sans MS", 12),
                                fg="#2C325B")
        
        exit_button.grid(row = 5, column = 4, pady = 2)
        
        #call the function
        self.render_inventory()
        
    def exit_inv(self):
        if self.window:  # Check if the window still exists
            self.window.destroy()
    
    def add_items(self, items):
        
        #for every item in the list you call
        for item in items:
            #check if the item is already in the dict
            if item in self.items:
                #increase count by one
                self.items[item]["count"] += 1
            elif len(self.items) < 25:
                #make new inventory slot
                self.items[item] = {"count" : 1, "image" : item + ".png"}
            else:
                #not enough storage left
                print("How many pockets do you think you have? Not enough to hold ", item)
                
        self.render_inventory()
    
    def remove_item(self, item):
        try:
            if item not in self.items:
                raise No_Item_In_Inventory(item)
            
            self.items.pop(item)
        except No_Item_In_Inventory as e:
            self.show_error(e.message)
            
        self.render_inventory()
            
        
    def render_empty(self, row, column):
        for _ in range(len(self.items), 25):
            btn = tk.Button(
                image=self.images["empty"],
                borderwidth=0
        
                )
            btn.grid(row=row, column=column, padx=10, pady=5)
            
            #to move to the next column

            column += 1
            
            #When it reaches 5 it switches to the next row
            if column > 4:
                column = 0
                row += 1
            
    def render_inventory(self):
        if not self.window or not self.window.winfo_exists():
            return
        
        row = 0
        column = 0
        
        #sets what empty is if not loaded
        if "empty" not in self.images:
            self.images["empty"] = tk.PhotoImage(file="empty.png")
        
        #loading images if not loaded yet
        for item_name, data in self.items.items():
            if item_name not in self.images:
                img = tk.PhotoImage(file = data["image"])
                self.images[item_name] = img
            
                #button for the images
                btn = tk.Button(
                    image = img,
                    borderwidth=0,
                    command= lambda item = item_name: self.clicked(item) #makes it so clicked() is part of the button  
                    )
                
                #positions buttons in a grid layout
                btn.grid(row = row, column = column, padx = 10, pady = 5)
                
                #stores the btn in the dictionary for buttons
                self.buttons[item_name] = btn
            
            column += 1
            
            if column > 4: 
                column = 0
                row += 1
            
        self.render_empty(row, column)
        
        #to run a message when clicked
    def clicked(self, item_name):
        
        #makes basic window
        clicked = tk.Toplevel(self.window)
        clicked.geometry("250x150")
        clicked.resizable(False, False)
        clicked.overrideredirect(True)
        
        bg_image = tk.PhotoImage(file="paper_background.png")
        
        bg_label = tk.Label(clicked, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        
        bg_label.image = bg_image
        
        count = self.items[item_name]["count"]
        
        label = tk.Label(clicked,
                         text = "Item: " + str(item_name + "\nCount: " + str(count)),
                         font = ("Comic Sans MS", 16),
                         fg ="#2C325B"
                         )
        
        button = tk.Button(clicked,
                        text = "Ok",
                        command = clicked.destroy,
                        font = ("Comic Sans MS", 12),
                        fg = "#2C325B",
            )
        
       
        label.pack(pady = 20)
        button.pack(pady = 20)
    
    def show_error(self, message):
        #makes basic window
        show_error_pop = tk.Toplevel(self.window)
        show_error_pop.geometry("250x150")
        show_error_pop.resizable(False, False)
        show_error_pop.overrideredirect(True)
        
        bg_image = tk.PhotoImage(file="paper_background.png")
        
        bg_label = tk.Label(show_error_pop, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        
        bg_label.image = bg_image
        
        label = tk.Label(show_error_pop,
                         text = "You forgot to pick the item up.",
                         font = ("Comic Sans MS", 16),
                         fg ="#2C325B" 
                         )
        
        button = tk.Button(show_error_pop,
                        text = "Ok",
                        command = show_error_pop.destroy,
                        font = ("Comic Sans MS", 12),
                        fg = "#2C325B",
            )
        
        label.pack(pady = 20)
        button.pack(pady = 20)
        
        
class No_Item_In_Inventory(Exception):
    def __init__(self, item):
        self.item = item
        self.message = "Next time remember to actually take your " + str(item)
        super().__init__(self.message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x200")

    inv = Inventory(root)

    # Add item button to test adding an item
    def add_pencil():
        inv.add_items(["pencil"])

    root.mainloop()
        
'''
Sources:
    https://docs.python.org/3/library/tkinter.messagebox.html
    https://www.geeksforgeeks.org/python-tkinter-tutorial/ 
    https://realpython.com/python-gui-tkinter/
    https://www.geeksforgeeks.org/python-tkinter-toplevel-widget/
    https://www.youtube.com/watch?v=tpwu5Zb64lQ&t=308s
    https://www.reddit.com/r/Python/comments/z8cvus/list_of_fonts_for_tkinter/?rdt=47931
    https://htmlcolorcodes.com
    https://stackoverflow.com/questions/56983976/how-to-setup-a-background-image-on-a-tk-toplevel
    https://stackoverflow.com/questions/69208259/stop-a-tkinter-subwindow-from-topleve-being-resized
    https://stackoverflow.com/questions/29857757/transparent-backgrounds-on-buttons-in-tkinter
    https://stackoverflow.com/questions/31085533/how-to-remove-just-the-window-border
    
'''
