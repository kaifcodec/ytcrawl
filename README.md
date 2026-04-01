# YTCrawl
A lightweight CLI tool to extract YouTube comment data without the overhead. Built for speed,  complex pattern recognition.

## Features

- Fetch paginated comments from a YouTube video
- Extract:
  - Author name
  - Comment text
  - Reply count
  - Like count
- Handles inconsistent YouTube JSON structures

## Requirements

- Python 3.x
- requests

Install dependencies:

```
pip install requests
```

## Usage

Run the script:

```
python main.py
```

Enter the video ID when prompted:

```
Enter YouTube Video ID: dQw4w9WgXcQ
```

To control how many pages of comments are fetched, modify the `limit` parameter in:

```
app.start(limit=5)
```

Increase or decrease the value based on how many comment pages are needed.

## How it works

- Generates an initial continuation token
- Sends requests to YouTube's internal `youtubei/v1/next` endpoint
- Parses deeply nested JSON responses
- Iterates through comment pages

## Example Output

```
[standard] User123: Nice video!
     └── Reply count(s): 5
     └── Like count(s): 42
```

## TODO

- Export comments to JSON or CSV
- Add threaded replies support
- Add CLI arguments
- Improve request handling and performance
