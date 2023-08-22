# yt-interactive-downloader

## Setup

1. Set some environment variable for this app in `yt-interactive-downloader/.env`.
```bash
YOUTUBE_API={YOUR_YOUTUBE_API_KEY}
EXTERNAL_SERVER={REMOTE SERVER NAME}  # OPTIONAL
PATH_TO_DOWNLOAD={YOUR_PATH_TO_DOWNLOAD}  # if this is not set, this is set to `.`
```
2. Using `rye`, call `rye sync`.
3. Call `rye run app` to start this app.