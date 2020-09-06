from etl import transform
from os import listdir
from os.path import isfile

# Path to folder with scraped data
path_listings = '/home/dev/Desktop/house-pricing/data/listings'

# Output path
path_cleaned = '../flats-data/'

files_to_open = list()

# Gather files
for folder in listdir(path_listings):
    path_scrape = f'{path_listings}/{folder}'
    for f in listdir(path_scrape):
        path = f'{path_listings}/{folder}/{f}'
        if isfile(path) and path.endswith('.csv'):
            files_to_open.append(path)

print(files_to_open)

# Create cleaned dataset.
transform(in_path=files_to_open, 
          out_path=path_cleaned)