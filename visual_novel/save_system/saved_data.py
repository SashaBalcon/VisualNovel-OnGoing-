import pickle
import os
import importlib

from save_system import save_data 
from save_system.branches import SceneRegistry, ImportBranches, BgRegistry

SAVES = os.path.join(os.path.dirname(__file__), 'saves')

def save_game(file_name, overwrite=False):
    """
    Serializes the data and also
    Makes it so you can overwrite a file with a new file
    """
    print(f"save_game called with file_name={file_name}, overwrite={overwrite}")
    if not os.path.exists(SAVES):
        os.makedirs(SAVES)

    file_path = os.path.join(SAVES, f"{file_name}.pkl")

    if os.path.exists(file_path) and not overwrite:
        return False

    with open(file_path, 'wb') as file:
        pickle.dump(save_data.save_data_dict, file)
    
    return True


def load_game(file_name):
    """
    This function takes the data and than loads it from save_data_dict into a pkl file
    """
    file_path = os.path.join(SAVES, f"{file_name}.pkl")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)

        save_data.save_data_dict.clear()
        save_data.save_data_dict.update(data)

        return save_data.save_data_dict

def total_saves():
    """
    This function creates the total amount of saves you can have and 
    than manually checks if the file is empty or saved and assigns it with 'empty' or 'saved'

    """
    full_slots = {}
    actual_slots = {}
    empty_or_saved = {}

    for i in range(1, 31):
        file_name = f"save{i}.pkl"
        file_path = f"{SAVES}/{file_name}"
        
        full_slots[file_name] = file_path

    for file in os.listdir(SAVES):
        file_path = os.path.join(SAVES, file)
        if os.path.isfile(file_path):
            actual_slots[file] = file_path

    for file in full_slots:
        if file in actual_slots:
            empty_or_saved[file] = 'saved'
        else:
            empty_or_saved[file] = 'empty'

    return(empty_or_saved)


def load_UI(slot_index, day):
    """
    Is designed to load a saved game state from a file and return all the critical data 
    needed to resume the game at the exact point where the player left off.
    """

    file_name = f"save{slot_index}"
    load_game(file_name)

    file_path = os.path.join(SAVES, f"save{slot_index}.pkl")
    if os.path.exists(file_path):

        #returning the file path
        scene_name = save_data.save_data_dict['current_scene']
        module = SceneRegistry(scene_name)

        #returning the text index
        text_idx = save_data.save_data_dict['txt_idx']

        #returning the friendship_points
        friendship = save_data.save_data_dict['friendship_points']

        #general_flags
        general_flags = save_data.save_data_dict['general_flags']

        #day specific flags
        day_num = f"day{day}_flags"
        day_specific = save_data.save_data_dict.get(day_num, {})

        #return cards
        cards_gained = save_data.save_data_dict['card_gained']

        #get the associated background
        current_bg = sava_data.save_data_dict['current_bg']

        print(f"{module}, {text_idx}, {friendship}, {general_flags}, {day_specific}, {cards_gained}, {slot_img}, {current_bg}")

        return module, text_idx, friendship, general_flags, day_specific, cards_gained, slot_img, current_bg
