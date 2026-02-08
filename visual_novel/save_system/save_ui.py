import os
import sys
import pygame

from save_system import save_data
from save_system.saved_data import total_saves, save_game, load_game, load_UI
from save_system.save_ui_button import SaveButtons
from save_system.branches import SceneRegistry
from save_system.bg_save import BgSaving

class SaveUI(SaveButtons, BgSaving):
    def __init__(self, screen, previous_scene, text_idx, day_index = 1):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.previous_scene = previous_scene
        self.text_idx = text_idx

        self.clicked_load = False
        self.clicked_save = False

        self.instructions_open = False
        self.overwrite_save = False
        self.show_two_option_popup = False

        self.clock = pygame.time.Clock()
        self.slot_num = 0

        self.day_index = day_index
        self.just_closed_popup = False

        super().__init__(self.screen)
        BgSaving.__init__(self, self.screen)

        self.action = None
    
    def run(self):
        running = True
        mouse = pygame.mouse.get_pos() 
        self.slot_rects = []

        while running:
            if self.just_closed_popup:
                self.just_closed_popup = False
                continue

            self.screen.fill(self.black)
            saves = total_saves()

            self.renderGrid(self.slot_num)
            self.renderButtons()
            self.renderPicture()

            #arrow buttons
            if self.slot_num > 0:
                #left
                pygame.draw.rect(self.screen, self.button_color, self.left_rect)
                self.screen.blit(self.arrow_left, self.text_left_arrow)

            if self.slot_num < 30:
                #right
                pygame.draw.rect(self.screen, self.button_color, self.right_rect)
                self.screen.blit(self.arrow_right, self.text_right_arrow)

            #1 Option popup
            if self.instructions_open:
                pygame.draw.rect(self.screen, (154, 159, 142), self.rect_message)
                self.screen.blit(self.message, self.message_surface_rect)

                pygame.draw.rect(self.screen, (88, 117, 113), self.ok_rect)
                self.screen.blit(self.ok_surface, self.ok_surface_rect)

            #2 Option popup
            if self.show_two_option_popup:
                pygame.draw.rect(self.screen, (154, 159, 142), self.rect_message)
                self.screen.blit(self.message, self.message_surface_rect)

                pygame.draw.rect(self.screen, (88, 117, 113), self.no_rect)
                self.screen.blit(self.no, self.no_surface_rect)

                pygame.draw.rect(self.screen, (88, 117, 113), self.yes_rect)
                self.screen.blit(self.yes, self.yes_surface_rect)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = event.pos

                    event_consumed = False
                    

                    #close Option 2 popup
                    if self.show_two_option_popup:
                        if self.no_rect.collidepoint(mouse):
                            self.overwrite_save = True
                            self.show_two_option_popup = False
                            self.pending_slot = None
                            self.action = None
                            event_consumed = True
                            continue  # skip rest of loop for this event

                        elif self.yes_rect.collidepoint(mouse):
                            if self.action == 'save' and self.pending_slot is not None:
                                slot_name = f"save{self.pending_slot}"
                                save_game(slot_name, overwrite=True)
                            self.overwrite_save = False
                            self.show_two_option_popup = False
                            self.pending_slot = None
                            self.action = None
                            event_consumed = True
                            continue
                        
                    if not event_consumed:
                        #back button
                        if self.back_rect.collidepoint(mouse):
                            module = SceneRegistry(self.previous_scene)
                            getattr(module, self.previous_scene)(self.screen, self.text_idx)
                            running = False

                        #save button
                        if self.save_rect.collidepoint(mouse):
                            self.clicked_save = True
                            self.action = 'save'
                            saves = total_saves()

                        #load button
                        if self.load_rect.collidepoint(mouse):
                            self.clicked_load = True
                            self.action = 'load'

                        #arrow buttons
                        if self.slot_num > 0:
                            if self.left_rect.collidepoint(mouse):
                                self.slot_num = self.slot_num - 6
                                self.renderGrid(self.slot_num)

                        if self.slot_num < 30:
                            if self.right_rect.collidepoint(mouse):
                                self.slot_num = self.slot_num + 6
                                self.renderGrid(self.slot_num)
                
                        #close Option 1 popup
                        if self.instructions_open:
                            if self.ok_rect.collidepoint(mouse):
                                self.clicked_load = False
                                self.clicked_save = False
                                self.instructions_open = False
                                self.just_closed_popup = True

                    if not event_consumed:
                        if not self.show_two_option_popup and not self.instructions_open and not self.just_closed_popup:
                            for rect, slot_index in self.slot_rects:
                                if rect.collidepoint(mouse):

                                    slot_name = f"save{slot_index}"
                                    slot_file = f"{slot_name}.pkl"
                                    saves = total_saves()

                                #instructions for clicking
                                    #if save or load hasn't been pressed first
                                    if not self.clicked_load and not self.clicked_save:
                                        self.RectMessages(1)
                                        self.instructions_open = True

                                    elif self.action == 'save':
                                        if saves.get(slot_file) == 'saved' and not self.overwrite_save:
                                            # Save already exists, ask for confirmation
                                            self.RectMessages(2)
                                            self.show_two_option_popup = True
                                            self.overwrite_save = False
                                            self.pending_slot = slot_index
                                        elif saves.get(slot_file) == 'saved' and self.overwrite_save:
                                            # User confirmed overwrite via popup
                                            save_game(slot_name, overwrite=True)
                                            self.overwrite_save = False
                                            self.pending_slot = None
                                            self.action = None
                                        else:
                                            # Either slot is empty or already confirmed overwrite
                                            save_game(slot_name, overwrite=True)
                                            self.overwrite_save = False
                                            self.action = None

                                    elif self.action == 'load':
                                        module, text_idx, friendship, general_flags, day_specific, cards_gained, current_bg = load_UI(slot_index, self.day_index)

                                        scene_name = save_data.save_data_dict['current_scene']

                                        print(save_data.save_data_dict['slot_images'])
                                        scene_instance = getattr(module, scene_name)(self.screen, text_idx, friendship, general_flags, day_specific)
                                        scene_instance.run()
                                        running = False
                                        self.action = None
                                        self.clicked_load = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

