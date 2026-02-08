import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from save_system.save_data import UpdateDay1Flags, UpdateScene, UpdateTextIdx
from template import Template
from save_system.save_ui import SaveUI
from game_state import game_state
from print_text import SlowText

'''
If you select the first option after initial choice 1
'''

class C1C1(Template):
    def __init__(self, screen, text_idx = 0, friendship = None, general_flags = None, day1_flags = None):
        self.screen = screen

        super().__init__()

        #save system updates
        UpdateScene('C1C1')
        UpdateDay1Flags('stay_home_meal', 'grocery_store')

        self.scene3_bg = pygame.image.load('day1/day1_anime/night.png').convert_alpha()
        self.scene3_bg = pygame.transform.smoothscale(self.scene3_bg, (self.screen_width, self.screen_height))

        self.new_bg = pygame.image.load('day1/day1_anime/grocery_store.png').convert_alpha()
        self.new_bg = pygame.transform.smoothscale(self.new_bg, (self.screen_width, self.screen_height))

        self.mary = pygame.image.load('day1/day1_anime/mary.png').convert_alpha()

        original_rect = self.mary.get_rect()
        desired_width = 1500
        aspect_ratio = original_rect.height / original_rect.width
        desired_height = int(desired_width * aspect_ratio)

        self.mary = pygame.transform.smoothscale(self.mary, (desired_width, desired_height))
        self.show_mary = False

        self.delay = 1500
        self.delay2 = 2000

        self.text_idx = text_idx
        self.text_funcs = [self.text1, self.text2, self.text3, self.text4, self.text5, self.text6, self.text7, self.text8, self.text9,
        self.text10, self.text11, self.text12]

        self.start_time = pygame.time.get_ticks()
        self.popup_visible = False

        self.clock = pygame.time.Clock()

        self.text_funcs[self.text_idx]()
        self.run()

    def text1(self):
        text = "(The drive to the grocery store was short and uneventful. You walk by the usual shelves, picking up ingredients on the way—milk, eggs, eggplant, cereal— it's not long before you have almost every ingredient on the list. But, somehow, you can't seem to find the pasta- you could've sworn there was a whole shelf last time you came here.)"

        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    def text2(self):
        text = "(It's not in the produce aisle-- not in the baking section. It's not even in the weird middle row with seasonal stuff and patio chairs.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
    
    def text3(self):
        text = "(Minutes pass. Maybe more? You realize you've been pacing in a wide loop. Same shelves, the same ingredients, and the same cashier who chews on her gum a little too loudly.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    
    def text4(self):
        text = "??? : You look lost."

        #save system updates
        UpdateTextIdx(self.text_idx)
        
        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (255, 182, 193))
        self.text_idx += 1
        self.add_to_back_log(text, color = (255, 182, 193))


    def text5(self):
        text = "(You turn. A young woman is behind you—closer than expected, smiling softly.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.show_mary = True

    
    def text6(self):
        text = "??? : You've passed the same aisle four times. What are you looking for? Maybe I can help?"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (255, 182, 193))
        self.text_idx += 1
        self.add_to_back_log(text, color = (255, 182, 193))


    def text7(self):
        text = "You : Oh, uhh, I can't seem to find the pasta aisle. I could've sworn there was a whole section somewhere around here, but well..."
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    
    def text8(self):
        text = "??? : It's right over here- let me show you"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40, colored = (255, 182, 193))
        self.text_idx += 1
        self.add_to_back_log(text, color = (255, 182, 193))


    def text9(self):
        text = "(She guides you to the aisle—it's exactly where you already looked. You're sure it wasn't there before. You mumble a thanks. She smiles, waves, and drifts off toward the fruit section, her basket still mostly empty.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)
        self.show_mary = False

    
    def text10(self):
        text = "(You're not the happiest with yourself, but you found what you came here for. You put the pasta in your basket, check out through the express aisle, and walk back to your apartment.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    
    def text11(self):
        text = "(As you get home, you set your grocery bags down. Quickly, you cook something simple with the pasta you found.)"
        
        #save system updates
        UpdateTextIdx(self.text_idx)

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)

    
    def text12(self):
        text = "(The moment you crawl into bed, your eyes close—and you're gone, deep asleep.)"

        self.slow_text = SlowText(text, pos=(self.text_bar_rect.x + 20, self.text_bar_rect.y + 10), line_length=self.text_bar_rect.width - 40)
        self.text_idx += 1
        self.add_to_back_log(text)


    def run(self):
        running = True

        text_run = True
        text_pressed = False
        log_show = False
        self.text_fully_rendered = False

        while running:
            self.screen.blit(self.new_bg, (0,0 ))
            mouse = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time

            #see if you should run everything yet or if it's still loading
            if elapsed > self.delay:
                self.available = True
            else:
                self.available = False

            if self.available:

                if self.show_mary:
                    mary_rect = self.mary.get_rect()
                    mary_rect.bottomright = (self.screen_width - 80, self.screen_height)
                    self.screen.blit(self.mary, mary_rect)

                #draw button and text bar ui
                self.draw_buttons()
                
                #words
                if elapsed > self.delay2 and text_run:
                    self.slow_text.update()
                    self.slow_text.Draw(self.screen)
                if self.text_idx >= len(self.slow_text.text):  
                    self.text_fully_rendered = True
                    text_run = False
                
                #if space bar has been pressed or text bar has been clicked move on to the next line...
                if text_pressed:
                    if self.text_idx < len(self.text_funcs):
                        self.text_funcs[self.text_idx]() 
                        text_run = True
                    else:
                        pass
                    text_pressed = False

                if log_show:
                    pygame.draw.rect(self.screen, self.button_color, self.popup)
                    self.back_log_hist()
                    pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                    self.screen.blit(self.x, self.x_text_rect)

                #popup
            if self.popup_visible:
                pygame.draw.rect(self.screen, self.button_color, self.popup)
                pygame.draw.rect(self.screen, self.button_color2, self.mini_x)
                self.screen.blit(self.x, self.x_text_rect)

                #exit button
                pygame.draw.rect(self.screen, self.button_color2, self.button_rect)
                self.screen.blit(self.quit_button, self.text_rect_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #If the space key is pressed down skip dailougue loading
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        else:
                            text_pressed = True
                            text_run = True
                            self.text_fully_rendered = False
                    
                    if event.key in (pygame.K_F11, pygame.K_ESCAPE):
                        game_state.toggle_fullscreen()
                        self.screen = game_state.screen
                        self.width, self.height = game_state.width, game_state.height

                if event.type == pygame.MOUSEBUTTONDOWN:

                #If the text_box is pressed down skip dailougue loading
                    if self.text_bar_rect.collidepoint(mouse):
                        if not self.text_fully_rendered:
                            self.slow_text.UpdateFast()
                            self.text_fully_rendered = True
                        else:
                            text_pressed = True
                            text_run = True
                            self.text_fully_rendered = False

                    #save button instructions
                    if self.save_rect.collidepoint(mouse):
                        previous_scene = 'C1C1'
                        save_screen = SaveUI(self.screen, previous_scene, self.text_idx, 1)
                        save_screen.run()

                    #run rest of collide instructions
                    self.collide_instructions(event, mouse)
                    
            self.clock.tick(60)
            pygame.display.flip()
            
