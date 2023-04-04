import json
import markdown_to_text
import os
import praw
import re
import time

from videoscript import VideoScript

with open("config.json") as c:
    config = json.load(c)
    subReddit = config["Reddit"]["Subreddit"]
    clientID = config["Reddit"]["ClientID"]
    clientSecret = config["Reddit"]["ClientSecret"]
    userAgent = config["Reddit"]["UserAgent"]
    redditURL = config["Reddit"]["URL"]
c.close()

if not __name__ == "__main__":

    def getContent(outputDir, postOptionCount) -> VideoScript:
        reddit = __getReddit()
        existingPostIds = __getExistingPostIds(outputDir)

        now = int(time.time())
        autoSelect = postOptionCount == 0
        posts = []

        for submission in reddit.subreddit(subReddit).top(time_filter="day", limit=postOptionCount * 3):
            if (f"{submission.id}.mp4" in existingPostIds or submission.over_18):
                continue
            hoursAgoPosted = (now - submission.created_utc) / 3600
            print(
                f"[{len(posts) + 1}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago")
            posts.append(submission)
            if (autoSelect or len(posts) >= postOptionCount):
                break

        if (autoSelect):
            return __getContentFromPost(posts[0])
        else:
            postSelection = int(input("Please enter an ID: "))
            selectedPost = posts[postSelection - 1]
            return __getContentFromPost(selectedPost)


    def getContentFromId(outputDir, submissionId) -> VideoScript:
        reddit = __getReddit()
        existingPostIds = __getExistingPostIds(outputDir)

        if (submissionId in existingPostIds):
            print("Video already exists!")
            exit()
        try:
            submission = reddit.submission(submissionId)
        except:
            print(f"Submission with id '{submissionId}' not found!")
            exit()
        return __getContentFromPost(submission)


    def __getReddit():
        return praw.Reddit(
            client_id= clientID,
            client_secret=clientSecret,
            user_agent=userAgent
        )


    def __getContentFromPost(submission) -> VideoScript:
        content = VideoScript(submission.url, submission.title, submission.id)
        print(f"Creating video for post: {submission.title}")
        print(f"Url: {submission.url}")

        failedAttempts = 0
        for comment in submission.comments:
            if (content.addCommentScene(markdown_to_text.markdown_to_text(comment.body), comment.id)):
                failedAttempts += 1
            if (content.canQuickFinish() or (failedAttempts > 2 and content.canBeFinished())):
                break
        return content


    def __getExistingPostIds(outputDir):
        files = os.listdir(outputDir)
        # I'm sure anyone knowledgable on python hates this. I had some weird 
        # issues and frankly didn't care to troubleshoot. It works though...
        files = [f for f in files if os.path.isfile(outputDir + '/' + f)]
        return [re.sub(r'.*?-', '', file) for file in files]
