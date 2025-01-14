import vimeo

# Initialize the Vimeo Client
client = vimeo.VimeoClient(
    token='YOUR_ACCESS_TOKEN',
    key='YOUR_CLIENT_IDENTIFIER',
    secret="YOUR_CLIENT_SECRET"
)

def get_team_library_videos():
    # Fetch all videos uploaded by the org.
    videos = []
    uri = '/me/videos'
    while uri:
        response = client.get(uri)
        data = response.json()
        videos.extend(data['data'])
        uri = data['paging'].get('next')
    return videos

def get_existing_albums():
    # Fetch all existing albums (folders) on Vimeo.
    albums = {}
    uri = 'me/albums' # replace with correct uri
    while uri:
        response = client.get(uri)
        data = response.json()
        for album in data['data']:
            albums[album['name']] = album['uri']
        uri = data['paging'].get('next')
    return albums

def add_video_to_album(video_uri, album_uri):
    # Add a video to an existing album.
    response = client.put(f"{album_uri}/videos/{video_uri.split('/')[-1]}")
    if response.status_code == 204:
        print(f"Video {video_uri} added to album {album_uri}")
    else:
        print(f"Failed to add video {video_uri} to album {album_uri}")

def organize_team_library_videos():
    # Organize videos from the Team Library into existing albums based on video names
    videos = get_team_library_videos()
    albums = get_existing_albums()

    for video in videos:
        video_name = video['name']
        video_uri = video['uri']

        # match video to album name
        # test and customize logic based on naming conventions
        album_name = video_name.split()[0] # Example: use the first word as the album name

        if album_name in albums:
            add_video_to_album(video_uri, albums[album_name])
        else:
            print(f"No matching album found for video: {video_name}")

# Run
if __name__ == "__main__":
    organize_team_library_videos()