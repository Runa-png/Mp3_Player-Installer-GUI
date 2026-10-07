import requests
from mutagen.mp3 import MP3
from mutagen.id3 import APIC

def writeAlbumArt(mp3Location, spotifyTrackId):
    spotifyUrl = f"https://open.spotify.com/track/{spotifyTrackId}"

    response = requests.get(
        "https://open.spotify.com/oembed",
        params={"url": spotifyUrl}
    )

    if response.status_code != 200:
        print("Failed to get Spotify artwork")
        return 

    imageUrl = response.json().get("thumbnail_url")

    if not imageUrl:
        print("Spotify returned no artwork")
        return 

    imageResponse = requests.get(imageUrl)

    if imageResponse.status_code != 200:
        print("Failed to download artwork")
        return 

    audio = MP3(mp3Location)

    try:
        audio.add_tags()
    except:
        pass

    # Remove existing album artwork
    audio.tags.delall("APIC:")

    # Add Spotify artwork
    audio.tags.add(
        APIC(
            encoding=3,
            mime=imageResponse.headers.get("Content-Type", "image/jpeg"),
            type=3,
            desc="Cover",
            data=imageResponse.content
        )
    )

    audio.save()
    return 
