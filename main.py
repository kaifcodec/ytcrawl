import argparse
from helpers import extract_video_id
from scraper import YTScraper

def main():
    parser = argparse.ArgumentParser(description="YouTube Comment Scraper")
    parser.add_argument("input", help="YouTube video URL or ID")
    parser.add_argument("--output", default="comments.json")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--minimal", action="store_true", help="Remove 'type' key from JSON output")

    args = parser.parse_args()
    video_id = extract_video_id(args.input)

    if not video_id:
        print("Invalid YouTube URL or ID")
        return

    app = YTScraper(video_id, args.output, verbose=args.verbose, minimal=args.minimal)
    app.start(limit=args.limit)

if __name__ == "__main__":
    main()
