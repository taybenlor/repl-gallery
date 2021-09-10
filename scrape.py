import csv
import requests
import json
import re
import sys
import pathlib
from time import sleep
from datetime import datetime


class URLException(Exception):
    def __init__(self, url):
        self.message = "Invalid URL"
        self.url = url


class DownloadException(Exception):
    def __init__(self, message, request):
        self.message = message
        self.request = request


def get_url_cover(url):
    """
    Gets the cover image for the repl. Because requests will follow redirects
    we also use this as a way to get the canonical url. This is important since
    students might rename their project. Without this the oembed API will fail.
    """
    try:
        page_request = requests.get(url)
    except:
        raise URLException(url)

    # Rate limit
    if page_request.status_code == 429:
        wait = int(page_request.headers.get('Retry-After', '30')) + 1
        print(f'Hit rate limit, waiting {wait} seconds...')
        sleep(wait)
        return get_url_cover(url)

    if page_request.status_code != 200:
        raise DownloadException('Error with request', page_request)

    m = re.search(
        '<meta.*?property="og:image"[^c]*?content="(.+?)".*?( /)?>', page_request.text)

    if m is not None:
        return page_request.url, m.group(1)
    else:
        return page_request.url, None


def get_oembed_data(url):
    """
    Uses the Replit OEmbed API to get metadata about the replit. The only data
    thats really used is the project name, and the user name. But handy!
    """
    embed_request = requests.get(
        f'https://replit.com/data/oembed/?format=json&url={url}')

    # Rate limit
    if embed_request.status_code == 429:
        wait = int(embed_request.headers.get('Retry-After', '30')) + 1
        print(f'Hit rate limit, waiting {wait} seconds...')
        sleep(wait)
        return get_oembed_data(url)

    if embed_request.status_code != 200:
        raise DownloadException('Error with request', embed_request)

    return embed_request.json()


def get_data(url):
    url, cover = get_url_cover(url)
    data = get_oembed_data(url)

    if cover is not None:
        data['poster_url'] = cover

    return data


def read_file(file, url_column):
    reader = csv.reader(file)
    for row in reader:
        url = row[url_column]
        try:
            data = get_data(url)
            yield data
            print(f'Retrieved data for {url}', json.dumps(data))
        except DownloadException as e:
            print(f'Error getting {url}',
                  e.request.status_code, e.request.text)
        except URLException as e:
            print(f'Error getting {url} invalid URL')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} INPUTFILE [COLUMN]')
        print()
        print('INPUTFILE - a CSV file that contains repl.it URLs')
        print('COLUMN - the column (0-indexed) that contains the URL')
        print()
        print('Use a header row with a URL field for column auto-detection')
        print('Otherwise this script will ask for the url column if not passed')
        sys.exit()

    filename = sys.argv[1]
    if len(sys.argv) > 2:
        column = sys.argv[2]
    else:
        column = None

    projects = []
    with open(filename) as datafile:
        has_header = csv.Sniffer().has_header(datafile.read(2048))
        datafile.seek(0)
        reader = csv.reader(datafile)
        if has_header:
            header = [h.lower() for h in reader.__next__()]
            print('Detected Header')
            print('\n'.join([f'{i}: {h}' for i, h in enumerate(header)]))
            if 'url' in header:
                column = header.index('url')
                print(f'Automatically using {column}:url')

        if column is None:
            column = int(input('Which column contains the URL? '))

        for i, row in enumerate(reader):
            url = row[column]
            try:
                data = get_data(url)
                data["id"] = i
                projects.append(data)
                print(f'Retrieved data for {url}', json.dumps(data))
            except DownloadException as e:
                print(f'Error getting {url}',
                      e.request.status_code, e.request.text)
            except URLException as e:
                print(f'Error getting {url} invalid URL')

    cwd = pathlib.Path(__file__).parent.absolute()
    with open(cwd / 'src' / '_data' / 'projects.json', 'w') as datafile:
        json.dump(projects, datafile)
