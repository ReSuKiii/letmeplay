import psutil
import time
from pygetwindow import getWindowsWithTitle
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import ctypes

def is_osu_running():
    """Check if osu! is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'osu!.exe':
            return True
    return False

def is_playing_map():
    """Check if osu! is running and currently playing a map."""
    windows = getWindowsWithTitle('osu!')
    for window in windows:
        if 'osu!' in window.title and '-' in window.title:
            return True
    return False

def set_discord_notification_mute(mute):
    """Mute or unmute Discord notifications."""
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Discord.exe":
            volume.SetMute(mute, None)

def show_notification(title, message):
    """Windows notification."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def main():
    try:
        was_playing_map = False
        running = True
        
        # Notify that the program is running for the skeptical people
        show_notification("LetMePlay", "LetMePlay is running, new top play incoming.")
        
        while running:
            osu_running = is_osu_running()
            playing_map = osu_running and is_playing_map()
            
            if playing_map and not was_playing_map:
                set_discord_notification_mute(True)
                print("Playing a map, Discord notifications muted.")
            elif not playing_map and was_playing_map:
                set_discord_notification_mute(False)
                print("Not playing a map, Discord notifications unmuted.")
            
            was_playing_map = playing_map
            
            time.sleep(3)  
            
            # Check if osu! has been closed
            if not is_osu_running():
                running = False
    
    except KeyboardInterrupt:
        # that shit wouldn't work for some unknown reasons, fixed tho
        set_discord_notification_mute(False)
        print("\nExiting... Discord notifications unmuted.")
        show_notification("LetMePlay", "LetMePlay has stopped.")

if __name__ == "__main__":
    main()
