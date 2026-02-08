
save_data_dict = {

    'current_scene' : 'C1', #updated with every scene

    'general_flags' : {'mary_intro' : False #true, false
    },

    'day1_flags' : {'main_choice' : 'hangout', #hangout, go to work, stay home
                    'stay_home_meal': 'grocery_store'  # grocery_store, mcronalds

    },

    
    'friendship_points' : {'Sammy' : 0, 'Aleksa' : 0, 'Lyle' : 0, 'Winston' : 0, 'Mary' : 0},

    'card_gained' : {'Sammy' : False, 'Aleksa' : False, 'Lyle' : False, 'Winston' : False, 'Mary' : False},

    'txt_idx' : 0,

    'current_bg' : 'frame57.png',  

    'save_slot_bgs' : {}

    }


def UpdatePoints(friend, points):
    global save_data_dict
    if friend in save_data_dict['friendship_points']:
        save_data_dict['friendship_points'][friend] += points

def UpdateTextIdx(text_num):
    global save_data_dict
    save_data_dict['txt_idx'] = text_num

def UpdateGeneralFlags(flag, updated):
    global save_data_dict
    if flag in save_data_dict['general_flags']:
        save_data_dict['general_flags'][flag] = updated

def UpdateDay1Flags(flag, updated):
    global save_data_dict
    if flag in save_data_dict['day1_flags']:
        save_data_dict['day1_flags'][flag] = updated

def UpdateScene(scene_name):
    global save_data_dict
    save_data_dict['current_scene'] = scene_name

def CardGained(flag, card):
    global save_data_dict
    save_data_dict['card_gained'][flag] = updated

def CurrentBg(img_path):
    global save_data_dict
    save_data_dict['current_bg'] = img_path







    
