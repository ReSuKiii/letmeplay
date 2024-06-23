import psutil # checking running processes
import time
from pygetwindow import getWindowsWithTitle # checking window titles
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume # controlling audio sessions
import ctypes # showing Windows notifications



def is_osu_running():
    """Check if osu! is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'osu!.exe':
            return True
    return False
# This basically iterate trough all processes and check if the name of the process is 'osu!.exe'. 
# If it is, it returns True, otherwise False. 


def is_playing_map():
    """Check if osu! is running and currently playing a map."""
    windows = getWindowsWithTitle('osu!')
    for window in windows:
        if 'osu!' in window.title and '-' in window.title:
            return True
    return False
# The same goes for the window title 
# If a window title contains both osu! and a dash (-), it indicates that a map is being played.
# If it does, it returns True, otherwise False. 

def set_discord_notification_mute(mute):
    """Mute or unmute Discord notifications."""
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Discord.exe":
            volume.SetMute(mute, None)
# This function iterates through all audio sessions and mutes or unmutes those associated with Discord.exe.
# If the session is related to Discord, it mutes or unmutes it based on the value of the mute parameter.


def show_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)
# This is for the Windows notification, it uses ctypes.windll.user32.MessageBoxW to show a message box.
# The title and message are passed as arguments to the function.
# The 0x40 | 0x1 flags are used to display the message box as a notification.

def main():
    try:
        was_playing_map = False
        running = True
        show_notification("LetMePlay", "LetMePlay is running, new top play incoming.")
# Initializes a flag (was_playing_map) to track the previous state and a running flag (running). It also shows a notification that the script is running.   
# The flags are used to determine if the script should mute or unmute Discord notifications based on the current and previous states.     
        
        while running:
            osu_running = is_osu_running()
            playing_map = osu_running and is_playing_map() # if osu is running and a map is being played
            
            if playing_map and not was_playing_map:
                set_discord_notification_mute(True)
                print("Playing a map, Discord notifications muted.")
            elif not playing_map and was_playing_map:
                set_discord_notification_mute(False)
                print("Not playing a map, Discord notifications unmuted.")
            
            was_playing_map = playing_map
            
            time.sleep(3)  
            
            if not is_osu_running():
                running = False                
# This is the main logic of the script, which continuously monitors the state of osu! and Discord to mute or unmute notifications accordingly.
# In this loop, it checks if osu! is running and if a map is being played.
# If a map is being played and the previous state was not playing a map, it mutes Discord notifications.
# If a map is not being played and the previous state was playing a map, it unmutes Discord notifications.
# The script then waits for 3 seconds before repeating the process.
# If osu! is not running, the script stops.
    
    except KeyboardInterrupt:
        # that shit wouldn't work for some unknown reasons, fixed tho
        set_discord_notification_mute(False)
        print("\nExiting... Discord notifications unmuted.")
        show_notification("LetMePlay", "LetMePlay has stopped.")
    

if __name__ == "__main__":
    main()

# To all my fellow programmers out here, if you have any suggestions please tell me ^^
# I'm still learning and i know this can be done in so many better ways  
