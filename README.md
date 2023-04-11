<div align ="center">

<img src="projectInfo/icon.png" width="180">

# RedditVideoGenerator

<span style="font-size:18px;">A program that generates a .mp4 video automatically by querying a post on a subreddit and grabbing several comments. </span>

</div>

## Links

- [Releases](https://github.com/etcherfx/RedditVideoGenerator/releases)

## Projects Used

- [RedditVideoGenerator](https://github.com/Shifty-The-Dev/RedditVideoGenerator)

## Usage

- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
- Register with Reddit to create and API application [here](https://www.reddit.com/prefs/apps/)
- Use the credentials from the previous step to update `config/defaultConfig.json` lines 20-22
- Rename `defaultConfig.json` to `config.json`
- Start the application:
  ```
  python main.py
  ```
- Alternatively you can run this command to create a video for a specific post:
  ```
  python main.py <reddit-post-id>
  ```
