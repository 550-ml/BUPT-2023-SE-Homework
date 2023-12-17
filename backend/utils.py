"""
Title: Utility Functions for Central Air Conditioning System
Module Description:
    This module contains various utility functions that are used across the central air conditioning system.
    These functions provide essential calculations and helper routines that support the system's main functionality.
    Key utilities include temperature recovery calculations, time conversions, and other common operations needed by \
    different parts of the air conditioning system.

Main Algorithms:
    - Temperature Recovery: Calculates the recovery rate of the room temperature.
    - Time-based Calculations: Provides helper functions for time conversions and calculations relevant to the \
        air conditioning operations.
    - General Utility Functions: Includes other miscellaneous functions that support the system's operations.

Interface Description:
    - recover_temp(room: Room): Calculates the temperature recovery for a given room based on certain parameters.

Development Record:
    Creator: Lisheng Gong
    Creation Date: 2023/12/01
    Modifier: Lisheng Gong
    Modification Date: 2023/12/17
    Modification Content:
        - add preamble notes
    Version: 3.0.0
"""


from datetime import datetime

from room import Room


def recover_temp(room: Room):
    recover_per_min = 0.5

    if room.end_time == 0:
        return 0

    room_current_temp = room.current_temp
    room_initial_temp = room.initial_env_temp

    if room_current_temp == room_initial_temp:
        return 0

    time_now = datetime.now()
    end_time = room.end_time
    duration = (time_now - end_time).total_seconds()

    temp_should_recover = duration / 10 * recover_per_min
    if room.last_off_temp + temp_should_recover >= room_initial_temp:
        room.current_temp = room.initial_env_temp
    else:
        room.current_temp = room.last_off_temp + temp_should_recover


def current_temp(room: Room, time_now):
    recover_per_min = 0.5

    room_current_temp = room.current_temp
    end_time = room.end_time
    duration = (time_now - end_time).total_seconds()

    temp_should_recover = duration % 60 * recover_per_min
    return room_current_temp + temp_should_recover
