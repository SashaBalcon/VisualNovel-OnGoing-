import pygame
import sys
import os

#get image path
current_directory = os.path.dirname(__file__)
image_path = os.path.join(current_directory, "inventory_images")

class Inventory():
    def __init__(self):

        #what items they should start w
        self.items = {
            "pencil" : {"count" : 2, "image" : "pencil.png"},
            "notebook" : {"count": 1, "image" : "notebook.png"},
            "iphone" : {"count": 1, "image" : "iphone.png"}
            }
        
        self.capacity = 25
        self.taken_slots = 3
        self.slots = []

        for item in range(self.capacity):
            self.slots.append(ItemSlot())

        self.listener = None

    #notifys user of changes
    def notify(self):
        if self.listener != None:
            self.listener.refresh()

    #adds smt to inventory
    def add_items(self, item_type, amount = 1):
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amount = amount
                    if add_amount > item_type.stack_size - slot.amount:
                        add_amount = item_type.stack_size - slot.amount
                    slot.amount += add_amount
                    amount -= add_amount
                    if amount <= 0:
                        self.notify()
                        return 0
            for slot in self.slots:
                if slot.type == None:
                    slot.type == item_type()
                    if item_type.stack_size < amount:
                        pass




    #removes smt from inventory
    def remove_items(self, item_type, amount = 1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found += amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    continue
                elif slot.ammount == amount:
                    found += amount
                    slot.type = None
                    self.notify()
                    return found
                else:
                    found += amount
                    slot.amount -= amount
                    self.notify()
                    return found
        return found

    #notifies how many of the item the user has
    def has(self, item_type, amount = 1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                found += amount
                if found >= amount:
                    return True
        return False

    #returns the first slot of where an item is
    def get_index(self):
        pass

    #for error bugging
    def string(self):
        pass
    
    #how many slots are left
    def get_free_slots(self):
        pass

    #returns total weight
    def is_full(self):
        pass

    #total value for the inventory
    def get_value(self):
        pass
    
        

class ItemSlot():
    def __init__(self):
        self.type = None
        self.amount = 0

class ItemType():
    def __init__(self, name, icon, stack_size = 1):
        self.name = name
        self.icon = icon
        self.icon = pygame.image.load(image_path + "/" + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size


'''
Sources:
https://stackoverflow.com/questions/44809610/how-do-i-make-a-visual-inventory-in-pygame
https://www.geeksforgeeks.org/how-to-create-a-pop-up-in-pygame-with-pgu/
https://www.youtube.com/watch?v=1q_0l71Ln7I
'''