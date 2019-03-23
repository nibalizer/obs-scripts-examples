# OBS-Studio python scripts
# Copyright (C) 2018 IBM
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

source_name = ""
visible = True

# ------------------------------------------------------------


def refresh_pressed(props, prop):
    """
    Called when the 'refresh' button defined below is pressed
    """
    print("Refresh Pressed")
    blink()


def blink():
    global source_name
    global visible

    source = obs.obs_get_source_by_name(source_name)
    text = "Hello World"
    if source is not None:
        visible = not visible
        obs.obs_source_set_enabled(source, visible)

# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()
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

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global source_name

    source_name = obs.obs_data_get_string(settings, "source")

def script_load(settings):
	obs.timer_add(blink, 1000)  # blink every second
