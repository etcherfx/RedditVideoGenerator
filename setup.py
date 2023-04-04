import json
import os

configDir = "config/"
configFile = "config.json"
configFilePath = os.path.join(configDir, configFile)

if not os.path.exists(configDir):
    os.makedirs(configDir)
if not os.path.exists(configFilePath):
    preview_before_upload = input("Preview before upload (True/False): ").lower() == "true"
    vlc_path = input("VLC path: ")
    output_directory = input("Output directory: ")
    background_directory = input("Background directory: ")
    voiceover_directory = input("Voiceover directory: ")
    background_file_prefix = input("Background file prefix: ")
    background_videos = int(input("Number of background videos: "))
    margin_size = int(input("Margin size: "))
    bitrate = input("Bitrate: ")
    threads = int(input("Number of threads: "))
    reddit_url = input("Reddit URL: ")
    num_posts_to_select_from = int(input("Number of posts to select from: "))
    subreddit = input("Subreddit: ")
    client_id = input("Client ID: ")
    client_secret = input("Client secret: ")
    user_agent = input("User agent: ")
    screenshots_directory = input("Screenshots directory: ")
    screenshots_width = int(input("Screenshots width: "))
    screenshots_height = int(input("Screenshots height: "))

    config = {
        "General": {
            "PreviewBeforeUpload": preview_before_upload,
            "VLCPath": vlc_path,
            "OutputDirectory": output_directory,
            "BackgroundDirectory": background_directory,
            "VoiceoverDirectory": voiceover_directory,
            "BackgroundFilePrefix": background_file_prefix,
            "BackgroundVideos": background_videos
        },
        "Video": {
            "MarginSize": margin_size,
            "Bitrate": bitrate,
            "Threads": threads
        },
        "Reddit": {
            "URL": reddit_url,
            "NumberOfPostsToSelectFrom": num_posts_to_select_from,
            "Subreddit": subreddit,
            "ClientID": client_id,
            "ClientSecret": client_secret,
            "UserAgent": user_agent
        },
        "Screenshots": {
            "Directory": screenshots_directory,
            "Width": screenshots_width,
            "Height": screenshots_height
        }
    }

    with open(configFilePath, "w") as c:
        json.dump(config, c, indent=2)
