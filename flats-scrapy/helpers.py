from datetime import datetime
from os import getcwd, listdir
from os.path import isfile, join
from pathlib import Path

def unix_ts():
    """
    Get unix timestamp

    Returns
    -------
    int : Unix timestamp in milliseconds.

    """

    start = datetime(1970, 1, 1)
    now = datetime.now()
    dt = now - start
    ts = int(dt.total_seconds() * 1000)

    return ts

def make_directory(dirtype, path):
    """
    Create directory to store crawled pages.

    """

    ts = unix_ts()

    if dirtype == 'urls':
        path = '/'.join([path, 'urls', str(ts), 'pages', ''])
    elif dirtype == 'listings':
        path = '/'.join([path, 'listings', str(ts), 'pages', ''])        
    else:
        raise ValueError(f'{dirtype} is not a valid input.')

    Path(path).mkdir(parents=True)
    
    path = path.split('/')
    path = path[0:-2]
    path = '/'.join(path)

    return path

def get_urls_from_txt(path):
    """
    Extract urls from text files.

    Notes
    -----
    For each folder open *.txt file and read all urls.
    """

    files_to_open = []

    for f in listdir(path):
        if f.endswith('.txt'):
            full_path = join(path, f)
            files_to_open.append(full_path)

    links = []

    for file_path in files_to_open:
        with open(file_path, 'r') as f:
            content = f.readlines()
            for link in content:
                links.append(link.strip())

    return links        

def get_urls(path):
    """
    Get list of unique urls to scrape.
    """

    path = f'{path}/urls'
    all_urls = set()
    folders = listdir(path)

    for folder in folders:
        time = int(folder) / 1000
        time = datetime.fromtimestamp(time)
        today = datetime.now()    

        if today.date() == time.date():
            path_to_urls = f'{path}/{folder}'
            print(f'Extracting links scraped on {time.date()} from {path_to_urls}.')
            links = get_urls_from_txt(path_to_urls)

            for link in links:
                all_urls.add(link)

    all_urls = list(all_urls)
    print(f'{len(all_urls)} unique urls to scrape.')
    
    return all_urls
