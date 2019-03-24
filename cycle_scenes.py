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

# cycle_scenes.py
# Very basic script that changes the active scene every few seconds. The next scene selection is random.
# This is 99% me playing with the api

import obspython as obs
import random

# ------------------------------------------------------------

def cycle():

    scenes = obs.obs_frontend_get_scenes()
    current_scene = obs.obs_frontend_get_current_scene()
    scenes.remove(current_scene)
    obs.obs_frontend_set_current_scene(random.choice(scenes))

# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "cycle_rate", "Cycle Rate(ms)", 10000, 1000000, 1000);
    return props

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """

    obs.timer_remove(cycle);
    blink_rate = obs.obs_data_get_int(settings, "cycle_rate")
    obs.timer_add(cycle, blink_rate)  # Change scene every cycle_rate ms
