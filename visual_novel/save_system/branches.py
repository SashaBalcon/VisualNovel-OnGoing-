import sys
import os
import importlib

def SceneRegistry(previous_scene):
    """
    This function's purpose is to find the module that the key is in
    
    Returns: the key that the value is from (aka the scene)
    """
    scene_registry = {
        
                #day 1 scenes
                    
                    "C1" : "day1.c1",
                    "C1_1" : "day1.c1",
                    "C1C1" : "day1.c1c1",
                    "C1C2" : "day1.c1c2",
                    "C3" : "day1.c3",
                    "C3S2" : "day1.c3",
                    "Choice3_1" : "day1.choice3",
                    "C3C1" : "day1.c3c12",
                    "C3C2" : "day1.c3c12",
                    "C3C12S1" : "day1.c3c12",
                    "Choice1_1" : "day1.choice1_1",
                    "C3C12C1" : "day1.c3c12c12",
                    "C3C12C2" : "day1.c3c12c12",
                    "Choice3_12_12" : "day1.c3c12choice12",
                    "Choice3_1" : "day1.choice3",
                    "C3C12C12C1" : "day1.c3c12c12c1",
                    "C3C12C12C2" : "day1.c3c12c12c2",
                    "C3C12C12C12C12C1" : "day1.c3c12c12c12c12c1",
                    "extra_choice" : "day1.c3c12c12c12c12c1",
                    "sea_slugs" : "day1.c3c12c12c12c12c1",
                    "C3C12C12C12C12C2" : "day1.c3c12c12c12c12c2",
                    "Choice3_12_12_12_12" : "day1.c3c12c12c12choice12",
                    "Choice3_12_12_12" : "day1.c3c12c12choice12",
                    "Scene1_1" : "day1.scene1_1",
                    "SlugLiar" : "day1.slug_liar",
                    "yay_slugs" : "day1.slug_liar",
                    "ew_slugs" : "day1.slug_liar",
                    "StartMaryConvo" : "day1.start_mary_convo",
                    "NoTalk" : "day1.start_mary_convo",
                    "Talk" : "day1.start_mary_convo",
                    "YesOrNo" : "day1.yes_or_no_McRonalds",
                    "No" : "day1.yes_or_no_McRonalds",
                    "Yes" : "day1.yes_or_no_McRonalds"}

    for key, value in scene_registry.items():
        if key == previous_scene:
            module = ImportBranches(value)
            return module

def BgRegistry(current_bg):
    """
    This function's purpose is to find the module that the key is in
    
    Returns: the key that the value is from (aka the background)
    """
    bg_registry =  {
        
            #day 1 backgrounds
                    
                "day1_anime" : ["frame57.png", "aquirium.png", "grocery_store.png", "night.png", "park.png", "mcronalds.png"]
    }
                    
    for key, value_list in bg_registry.items():
        if current_bg in value_list:
            return key

def ImportBranches(module_name):
    """
    Links the module to this .py file so it can access it
    
    returns: Returns the linked module
    """
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    module = importlib.import_module(module_name)
    return module
