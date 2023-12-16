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

    temp_should_recover = duration / 60 * recover_per_min
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
