# uses winrt to get the song name and artist name from the Windows APIs
# and prints them to a file

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackInfo as np
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionMediaProperties as media
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as status
import winrt

def main():
    # Get all the attributes of `media`
    print()



if __name__ == "__main__":
    main()
else:
    print(f"{__name__}: Don't import me! Thanks, Bye.")