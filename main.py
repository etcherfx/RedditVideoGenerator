import json
import random
import subprocess
import time

from moviepy.editor import *

import reddit
import screenshot

file_cfg: str = "config.json"
config: dict = {}

if os.path.exists(file_cfg):
    with open(file_cfg) as c:
        config = json.loads(c.read())
    c.close()

directories = [config["General"]["OutputDirectory"],
               config["General"]["BackgroundDirectory"],
               config["General"]["VoiceoverDirectory"],
               config["Screenshots"]["Directory"]
               ]

for directory in directories:
    if not os.path.exists(directory):
        os.mkdir(directory)


def createVideo():
    outputDir = config["General"]["OutputDirectory"]

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = config["Reddit"]["NumberOfPostsToSelectFrom"]
        script = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script)

    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"]
    bgPrefix = config["General"]["BackgroundFilePrefix"]
    bgCount = int(config["General"]["BackgroundVideos"])
    bgIndex = random.randint(0, bgCount-1)
    backgroundVideo = VideoFileClip(filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", audio=False).subclip(0,
                                                                                                      script.getDuration())
    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
        ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w - marginSize))
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay],
        size=backgroundVideo.size).set_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile,
        codec='mpeg4',
        threads=threads,
        bitrate=bitrate
    )
    print(f"Video completed in {time.time() - startTime}")

    # Preview in VLC for approval before uploading
    if (config["General"]["PreviewBeforeUpload"]):
        vlcPath = config["General"]["VLCPath"]
        p = subprocess.Popen([vlcPath, outputFile])
        print("Waiting for video review. Type anything to continue")
        wait = input()

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")


if __name__ == "__main__":
    createVideo()
