# OBS-Studio python scripts
# Copyright (C) 2018-2019 IBM
# Copyright (C) 2018 Jim

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# blink_visible.py
# Very basic script that switches a source from visible to not in a loop
# This is 99% me playing with the api

import obspython as obs

import requests


source_name = ""
visible = True
match_history = False
match_history_data = {"Z": [0,0], "P": [0,0], "T": [0,0]}
game_state = 'nostate'

# ------------------------------------------------------------

def blink():
    global source_name
    global match_history
    global match_history_data
    global game_state
    url = "http://127.0.0.1:6119/game"
    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        r = requests.get(url).json()
        player_name = r['players'][1]['name']
        player_race = r['players'][1]['race']
        text = "OPPONENT: {0}\nRACE: {1}\n".format(player_name, player_race)
        current_game_state = r['players'][0]['result']
        print(r)
        if current_game_state != game_state:
            game_state = current_game_state
            if current_game_state in ['Victory', 'Defeat']:
                if current_game_state == 'Victory':
                    idx = 0 # victory
                elif current_game_state == 'Defeat':
                    idx = 1 # defeat

                if player_race[0] == "Z":
                    match_history_data['Z'][idx] += 1
                if player_race[0] == "T":
                    match_history_data['T'][idx] += 1
                if player_race[0] == "P":
                    match_history_data['P'][idx] += 1

        if match_history:
            text += "vZ: {0}, vP: {1}, vT: {2}".format(match_history_data['Z'],
                                                           match_history_data['P'],
                                                           match_history_data['T'])
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        
# ------------------------------------------------------------

def refresh_pressed(props, prop):
    global match_history_data
    match_history_data = {"Z": [0,0], "P": [0,0], "T": [0,0]}
    blink()

# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()

    mh = obs.obs_properties_add_bool(props, "match_history", "Show Match History")

    p = obs.obs_properties_add_list(props, "source", "Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)

    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_int(props,
                               "blink_rate",
                               "Blink Rate(ms)",
                               1000,
                               10000,
                               1)
    obs.obs_properties_add_button(props, "button", "Reset Match History", refresh_pressed)

    return props

# ------------------------------------------------------------

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global source_name
    global match_history
    global match_history_data 



    source_name = obs.obs_data_get_string(settings, "source")
    obs.timer_remove(blink)
    blink_rate = obs.obs_data_get_int(settings, "blink_rate")
    # blink is actually refresh, do it every blink_rate ms
    obs.timer_add(blink, blink_rate)
    match_history = obs.obs_data_get_bool(settings, "match_history")
