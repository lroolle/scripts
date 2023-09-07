import argparse
import os
import re

import requests
from bs4 import BeautifulSoup


def download_episode(url, dir):
    if is_valid_xiaoyuzhou_episode_url(url):
        audio_url, episode_title, podcast_name = get_episode_info(url)
        file_extension = get_audio_file_extension(audio_url)

        if not file_extension:
            raise ValueError(f"Cannot get file extension for url {audio_url}")

        audio_file_path = build_episode_file_path(dir, podcast_name, episode_title, file_extension)
        # Ensure the directory exists
        os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
        print(f"Downloading episode {episode_title}")
        download_file(audio_url, audio_file_path)
    else:
        raise ValueError(f"URL is not a valid episode: {url}")


def is_valid_xiaoyuzhou_episode_url(url):
    pattern = r"^https?://(?:www\.)?xiaoyuzhoufm\.com/episode/([0-9a-f]{24})"
    return bool(re.match(pattern, url))


def get_audio_file_extension(audio_file_url):
    supported_extensions = [".mp3", ".m4a", ".wav", ".ogg", ".flac", ".ape"]
    for ext in supported_extensions:
        if audio_file_url.endswith(ext):
            return ext
    return ""


def get_episode_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract audio URL
    audio_url_tag = soup.find("meta", {"property": "og:audio"})
    if audio_url_tag:
        audio_url = audio_url_tag["content"]
    else:
        raise ValueError("Cannot find audio URL")

    # Extract episode title
    episode_title_tag = soup.find("meta", {"property": "og:title"})
    if episode_title_tag:
        episode_title = episode_title_tag["content"]
    else:
        raise ValueError("Cannot find episode title")

    # Extract podcast name
    podcast_name_tag = soup.find(class_="podcast-title")
    if podcast_name_tag:
        podcast_name = podcast_name_tag.text.strip()
    else:
        podcast_name = "Unknown Podcast Name"

    return audio_url, episode_title, podcast_name


def build_episode_file_path(dir, podcast_name, episode_title, file_extension):
    podcast_dir = os.path.join(dir, podcast_name)
    return os.path.join(podcast_dir, episode_title + file_extension)


def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(description="Download episodes from xiaoyuzhoufm.com")
    parser.add_argument("--url", type=str, help="URL of the episode to download")
    parser.add_argument("--dir", type=str, help="Directory where the episode will be saved")

    args = parser.parse_args()

    try:
        download_episode(args.url, args.dir)
        print(f"Episode downloaded successfully to {args.dir}")
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
