# YTCrawl
A lightweight CLI tool to extract YouTube comment data without the overhead. Built for speed, complex pattern recognition.

<div align="center">
  <img src="https://github.com/user-attachments/assets/43b50e12-9952-468e-bbbb-5e594cdae001" width="900" height="420" alt="kaifcodec's ytcrawl repository banner"/>
</div>


## Features

- Fetch paginated comments from a YouTube video
- Support for standard URLs, short links, and YouTube Shorts
- Extract:
  - `author` name
  - `text` of the comment
  - `reply_count`
  - `likes` count
  - `pfp_url` (author profile picture)
- Modular architecture for easier maintenance
- Export comments to `JSON`

## Requirements

- `Python 3.x`
- `requests`

Install dependencies:

```bash
pip install requests
```

## Usage

Run the script by passing a YouTube URL or Video ID as a positional argument:

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### CLI Arguments

| Argument | Description | Default |
| --- | --- | --- |
| `input` | YouTube video URL, Shorts URL, or ID | (Required) |
| `--limit` | Number of comment pages to fetch | `5` |
| `--output` | Target JSON filename | `comments.json` |
| `-v`, `--verbose` | Print author `pfp_url` in the console | `False` |
| `--minimal` | Remove `type` key from the saved `JSON` file | `False` |

## How it works

- `helpers.py`: Logic for `extract_video_id` and `JSON` I/O operations.
- `scraper.py`: Manages `requests.Session` and `YTScraper` orchestration.
- `parser.py`: Uses `CommentParser` to scrape `youtubei/v1/next` JSON payloads.
- `generator.py`: Generates the initial continuation token.

## Example Output

```text
Page 1...
[standard] User123: Nice video!
        └── Reply count(s): 5
        └── Like count(s): 42
```

## TODO

- Add threaded replies support
- Add `CSV` export support
- Improve request handling and performance
