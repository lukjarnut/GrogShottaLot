from logging import NullHandler, critical
from tkinter.font import BOLD
from turtle import position
from warnings import catch_warnings
import PySimpleGUI as sg
import random

weather_tab = [
    "Normal (0)",
    "Light Glare/Light Smoke (-20)",
    "Fog/Glare/Radiation Storm (-50)",
    "Heavy Fog/Dust Storm/Heavy Storm (-50)",
    "Night Time/Powerful Glare (-100)",
    "Total Darkness/Blinding Glare(-150)"
]

weather_dict = {
    "Normal (0)": 0,
    "Light Glare/Light Smoke (-20)": -20,
    "Fog/Glare/Radiation Storm (-50)": -50,
    "Heavy Fog/Dust Storm/Heavy Storm (-50)": -50,
    "Night Time/Powerful Glare (-100)": -100,
    "Total Darkness/Blinding Glare(-150)": -150
}

covers_tab = [
    "No cover",
    "Quarter Cover (-25)",
    "Half Cover (-50)",
    "3/4 Cover (-75)",
    "Full Cover (imposiburu)"
]

covers_dict = {
    "No cover": 0,
    "Quarter Cover (-25)": -25,
    "Half Cover (-50)": -50,
    "3/4 Cover (-75)": -75,
    "Full Cover (imposiburu)": -100
}

ranges_tab = [
    "Base (up to 1x)  0",
    "Mid (1.1 - 2x)  -25",
    "Long (2.1 - 3x)  -50",
    "Extreme (3.1 - 4x)  -100",
    "Impossible (4.1 - 5x)  -150"
]

ranges_dict = {
    "Base (up to 1x)  0": 0,
    "Mid (1.1 - 2x)  -25": -25,
    "Long (2.1 - 3x)  -50": -50,
    "Extreme (3.1 - 4x)  -100": -100,
    "Impossible (4.1 - 5x)  -150": -150
}

ammo_tab = [
    "1 (no burst mode)",
    "2 (penalty: -10, with set-up: 0)",
    "3-4 (penalty -25, with set-up: -10)",
    "5-6 (penalty -50, with set-up: -20)",
    "7-8 (penalty -75, with set-up: -35)",
    "9-10 (penalty -100, with set-up: -50)"
]

attack_count_dict = {
    "1 (no burst mode)": 1,
    "2 (penalty: -10, with set-up: 0)": 1,
    "3-4 (penalty -25, with set-up: -10)": 2,
    "5-6 (penalty -50, with set-up: -20)": 3,
    "7-8 (penalty -75, with set-up: -35)": 4,
    "9-10 (penalty -100, with set-up: -50)": 5
}

ammo_pen_ns = {
    "1 (no burst mode)": 0,
    "2 (penalty: -10, with set-up: 0)": -10,
    "3-4 (penalty -25, with set-up: -10)": -25,
    "5-6 (penalty -50, with set-up: -20)": -50,
    "7-8 (penalty -75, with set-up: -35)": -75,
    "9-10 (penalty -100, with set-up: -50)": -100
}

ammo_pen_s = {
    "1 (no burst mode)": 0,
    "2 (penalty: -10, with set-up: 0)": 0,
    "3-4 (penalty -25, with set-up: -10)": -10,
    "5-6 (penalty -50, with set-up: -20)": -20,
    "7-8 (penalty -75, with set-up: -35)": -35,
    "9-10 (penalty -100, with set-up: -50)": -50
}

Inputs = [
    [sg.Text("Weather:")],
    [sg.Combo(weather_tab, default_value = "Normal (0)", readonly = True, key='weather')],
    [sg.Text("Cover:")],
    [sg.Combo(covers_tab, default_value = "No cover", readonly = True, key='cover')],
    [sg.Text("Range:")],
    [sg.Combo(ranges_tab, default_value = "Base (up to 1x)  0", readonly = True, key='range')],
    [sg.Text("Ammo:")],
    [sg.Combo(ammo_tab, default_value = "1 (no burst mode)", readonly = True, key='ammo'), sg.Checkbox("set-up", key = "set-up")],
    [sg.Text("Ability modifier:"), sg.Input(key='ability', size=(5,1), default_text="0")],
    [sg.Text("Fighting Stance modifier: "), sg.Input(size=(5,1), key='stance', default_text="0")],
    [sg.Text("Enemy Armor: "), sg.Input(size=(5,1), key='e_armor', default_text="0")],
    [sg.Text("Damage Resistance Mod: "), sg.Input(size=(5,1), key='dmg_res', default_text="0")],
    [sg.Text("Crit Chance: "), sg.Input(size=(5,1),  key='cc', default_text="0")]
    ]

Rolls = [
    [sg.Text("Ammo modifier:")],
    [sg.Input(size = (4,1), key = "ammo_count", default_text="0"), sg.Text("d"), sg.Input(size = (4,1), key = "ammo_dice", default_text="0"), sg.Text("+"), sg.Input(size = (4,1), key = "ammo_mod", default_text="0")],
    [sg.Text("Weapon modifier:")],
    [sg.Input(size = (4,1), key = "weapon_count", default_text="0"), sg.Text("d"), sg.Input(size = (4,1), key = "weapon_dice", default_text="0"), sg.Text("+"), sg.Input(size = (4,1), key = "weapon_mod", default_text="0")]
]

Output_box = [
    [sg.Multiline(" ", s = (30, 20), key = "output")],
    [sg.Button("CLEAR", enable_events=True, key="clear")]
]


layout = [
    [sg.Frame("Inputs", Inputs), sg.Frame("Rolls", Rolls), sg.Frame("Output", Output_box)],
    [sg.Button("ATTACK", enable_events=True, key="submit")]
]
#create window

window = sg.Window("LiczDemydź", layout=layout)

def to_int(value):
    if value == None:
        return 0
    else:
        return int(value)

def main(event):
    try:
        if event == "submit":

                weather_mod = weather_dict[values['weather']]
                if values['cover'] == "No cover":
                    cover_mod = 0
                else:
                    cover_mod = covers_dict[values['cover']]

                range_mod = ranges_dict[values['range']]
                ability_mod = to_int(values['ability'])

                if values['set-up'] == True:
                    ammo_pen = ammo_pen_s[values['ammo']]
                else:
                    ammo_pen = ammo_pen_ns[values['ammo']]

                attack_count = attack_count_dict[values['ammo']]
                stance_mod = to_int(values['stance'])
                e_armor = to_int(values['e_armor'])
                dmg_resistance_mod = 1 - (to_int(values['dmg_res'])/100)
                cc_mod = to_int(values['cc'])
                ammo_count = to_int(values['ammo_count'])
                ammo_dice = to_int(values['ammo_dice'])
                ammo_mod = to_int(values['ammo_mod'])
                weapon_count = to_int(values['weapon_count'])
                weapon_dice = to_int(values['weapon_dice'])
                weapon_mod = to_int(values['weapon_mod'])

                for i in range(0,attack_count):
                    ammo_rolls = []
                    weapon_rolls = []
                    
                    for i in range(0,ammo_count):
                        ammo_rolls.append(random.randint(1,ammo_dice))

                    for i in range(0,weapon_count):
                        weapon_rolls.append(random.randint(1,weapon_dice))

                    roll = random.randint(1,100)

                    if cover_mod == -100:
                       window["output"].print("You want to shoot through wall?", end = "\n")
                       window["output"].print("REALLY?", end = '\n', text_color = 'red', font="bold")
                    else:   
                        if roll > 100 - cc_mod:
                            damage = "{:.0f}".format(2 * (sum(ammo_rolls) + ammo_mod + sum(weapon_rolls) + weapon_mod) * dmg_resistance_mod)
                            window["output"].print("CRIT \n damage:" + str(damage), end = '\n', text_color = 'red', font="bold")
                        else:
                            attack = roll + ability_mod - e_armor + weather_mod + ammo_pen + stance_mod + cover_mod + range_mod
                            damage = "{:.0f}".format((sum(ammo_rolls) + ammo_mod + sum(weapon_rolls) + weapon_mod) * dmg_resistance_mod)              
                        
                            window["output"].print("roll: " + str(roll), end=' ')
                            window["output"].print("attack: " + str(attack), end='\n')
                            window["output"].print("damage: " + str(damage) + "\n" + \
                                "ammo rols:" + str(ammo_rolls) + "\n" + \
                                "weapon rols:" + str(weapon_rolls) + "\n" + \
                                "weather mod: " + str(weather_mod) + "\n" + \
                                "cover mod: " + str(cover_mod) + "\n" + \
                                "range mod: " + str(range_mod) + "\n" + \
                                "ability mod: " + str(ability_mod) + "\n" + \
                                "burst penalty: " + str(ammo_pen) + "\n" + \
                                "stance mod: " + str(stance_mod) + "\n" + \
                                "damage resistance mod: " + str("{:.2f}".format(dmg_resistance_mod)) + "\n")
                window["output"].print("======================", end = "\n") 
        elif event == "clear":
            window["output"].update(' ');   
    except ValueError:
        window["output"].print("Not all data given/Wrong type", end = "\n", text_color = 'red')
        window["output"].print("======================", end = "\n")
#main loop
while True:
    event, values = window.Read()
    if event == sg.WIN_CLOSED:
        break;
    else:
        main(event)
window.close()
