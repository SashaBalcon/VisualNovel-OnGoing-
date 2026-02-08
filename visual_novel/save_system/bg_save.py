import pygame 
import os
from save_system.saved_data import total_saves
from save_system.branches import BgRegistry, ImportBranches

class BgSaving:
    def __init__(self, screen):
        #general settings...
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        #grid settings
        self.cols = 3
        self.rows = 2
        self.cell_width = (self.screen_width // self.cols)
        self.cell_height = (self.screen_height // self.rows) - 10

    def LoadingBackground(self,bg_string):
        """
        Loads a background image from a folder.
        Example: self.LoadingBackground('day1_anime', 'frame57.png')
        """
        #get the sub folder name
        bg_key = BgRegistry(bg_string)
        bg_upper_folder = ""

        for char in bg_key:
            if char == "_":
                break
            else:
                bg_upper_folder = bg_upper_folder + char

        image_path = os.path.join(bg_upper_folder, bg_key, bg_string)
        image_path = os.path.abspath(image_path)

        current_img = pygame.image.load(image_path).convert()
        current_img = pygame.transform.scale(current_img, (self.cell_width - 100, self.cell_height - 175))
        return current_img

    def renderPicture(self):
        """
        This creates the pictures to place ontop of the grid
        """
        text = "frame57.png"
        current_img = self.LoadingBackground(text)

        x = self.cell_width + 50 
        y = (self.cell_height - 70) + 100 
        self.screen.blit(current_img, (x, y))

        #for row in range(self.rows):
            #for col in range(self.cols):


    def renderGrid(self, slot_num):
        """
        This creates the grid for the slots that are used to represent the saves
        """
        #default settings
        slot_index = slot_num

        for row in range(self.rows):
                for col in range(self.cols):
                    gap_between_cells = 70 
                    x = col * self.cell_width
                    y = row * (self.cell_height - gap_between_cells)

                    rect = pygame.Rect(x + 50, y + 100, self.cell_width - 100, self.cell_height - 175)
                    pygame.draw.rect(self.screen, self.button_color, rect, border_radius = 10)

                    slot_index += 1
                    self.slot_rects.append((rect, slot_index))

                    # Text for slot label
                    saves = total_saves()
                    slot_key = f"save{slot_index}.pkl"

                    if slot_key in saves and saves[slot_key] == 'saved':
                            label_text = f"Slot {slot_index}: Saved"
                    else:
                            label_text = f"Slot {slot_index}: Empty"

                    # Render the label
                    label_surface = self.text_font.render(label_text, True, self.white)

                    # Position the label centered horizontally below the panel
                    label_rect = label_surface.get_rect()
                    label_rect.centerx = rect.centerx
                    label_rect.top = rect.bottom + 10

                    self.screen.blit(label_surface, label_rect)


        

        
            

    
