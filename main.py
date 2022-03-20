import asyncio
import time
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.storage.streams import \
    DataReader, Buffer, InputStreamOptions

# Code stolen from
# https://stackoverflow.com/a/66037406

async def get_media_info():
    sessions = await MediaManager.request_async()

    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    current_session = sessions.get_current_session()
    sessionsarray = sessions.get_sessions()
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    return None

async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

def ExportInfo(title, artist):
    # Encode info.txt as utf-8
    with open('title.txt', 'w', encoding='utf-8') as f:
        f.write(title)
    with open('artist.txt', 'w', encoding='utf-8') as f:
        f.write(artist)

def main():
    while True:
        current_media_info = asyncio.run(get_media_info())
        titlefile = open('title.txt', 'r', encoding='utf-8')
        artistfile = open('artist.txt', 'r', encoding='utf-8')
        if current_media_info == None and titlefile.read() != '' and artistfile.read() != '':
            title = ""
            artist = ""
            ExportInfo(title, artist)
            with open('media_thumb.png', 'wb+') as fobj:
                with open ('default.png', 'rb') as f:
                    fobj.write(f.read())
            continue
        elif current_media_info == None:
            continue
        
        #print(current_media_info)

        title = current_media_info['title']
        artist = current_media_info['artist']

        if titlefile.read() != title or artistfile.read() != artist:

            ExportInfo(title, artist)

        try:
            # create the current_media_info dict with the earlier code first
            thumb_stream_ref = current_media_info['thumbnail']

            # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
            thumb_read_buffer = Buffer(5000000)

            # copies data from data stream reference into buffer created above
            asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))

            # reads data (as bytes) from buffer
            buffer_reader = DataReader.from_buffer(thumb_read_buffer)
            byte_buffer = buffer_reader.read_bytes(thumb_read_buffer.length)

            with open('media_thumb.png', 'wb+') as fobj:
                fobj.write(bytearray(byte_buffer))

        except AttributeError:
            with open('media_thumb.png', 'wb+') as fobj:
                with open ('default.png', 'rb') as f:
                    fobj.write(f.read())

        time.sleep(1)

if __name__ == '__main__':
    main()

        
