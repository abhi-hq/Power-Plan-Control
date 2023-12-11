import keyboard
import subprocess
import psutil
import json

def set_power_profile(profile_guid):
    subprocess.run(['powercfg', '/setactive', profile_guid], shell=True)

#power profiles with key combinations
power_profiles = {
    'Saver': 'Alt+1',
    'Balanced': 'Alt+2',
    'Performance': 'Alt+3',
}

profile_file = 'last_profiles.json'

# another one to map the GUIDs of the profiles
profile_guids = {
    'Saver': 'a1841308-3541-4fab-bc81-f71556f20b4a',
    'Balanced': '381b4222-f694-41f0-9685-ff5bb260df2e',
    'Performance': '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
}

def read_last_profiles(): #reading the last profiles set in the json file and loading accordingly
    try:
        with open(profile_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'Battery': 'Saver', 'Charging': 'Balanced'} 

# write the last used profiles to the file
def write_last_profiles(last_profiles):
    with open(profile_file, 'w') as file:
        json.dump(last_profiles, file)

# changin profile based on the key basically mapping key combo and profiles
def change_power_profile():
    for profile, key_combo in power_profiles.items():
        if keyboard.is_pressed(key_combo):
            last_profiles = read_last_profiles()
            if is_on_battery():
                last_profiles['Battery'] = profile
            else:
                last_profiles['Charging'] = profile
            write_last_profiles(last_profiles)
            set_power_profile(profile_guids[profile])


# checking battery status
def is_on_battery():
    battery = psutil.sensors_battery()
    return not battery.power_plugged

# changing profiles based on charge status and also using key combo to set
def change_profile_based_on_power_status():
    last_profiles = read_last_profiles()
    battery_profile = profile_guids[last_profiles['Battery']]
    charging_profile = profile_guids[last_profiles['Charging']]
    if is_on_battery():
        set_power_profile(battery_profile)
        print(f"Changed power profile to {last_profiles['Battery']} (On Battery)")
    else:
        set_power_profile(charging_profile)
        print(f"Changed power profile to {last_profiles['Charging']} (Charging)")

# mapping the combo to profiles
for key_combo in power_profiles.values():
    keyboard.add_hotkey(key_combo, change_power_profile)

prev_power_plugged = is_on_battery() #initialization 

# change based on status
def handle_power_status_change():
    change_profile_based_on_power_status()

#a listener to always track the battery status
while True:
    current_power_plugged = is_on_battery()
    if current_power_plugged != prev_power_plugged:
        handle_power_status_change()
        prev_power_plugged = current_power_plugged


