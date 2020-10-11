# flats in cracow

## Project goal
The goal of this project is to build a model to predict flat prices in Cracow, PL from scratch.

### Methods
* Machine learning
* Data visualization
* Web scraping

### Technologies
* Python
* Matplotlib
* Pandas
* Jupyter
* Scrapy
* Scikit-Learn

## Project description
The flow of the project is as follows: first data is scraped from the web and saved to memory untouched. Next the data is prepared for further analysis. This step would include things such as extracting information about the property. In the next step the data is read into a Jupyter Notebook where it is cleaned, transformed and analyzed. Lastly we build models and evaluate their performance against a baseline model.

## Analysis & Notebooks
All notebooks are saved in ```flats-notebooks``` in ```.ipynb``` and ```.pdf``` formats.


## Getting started
1. Clone this repo:
    ```
    git clone https://github.com/besiobu/flats-in-cracow.git
    ```
2. Install the requirements:
    ```
    pip3 install -r requirements.txt    
    ```
3. Run:
    ```
    python3 setup.py
    ```
    This creates a directory for scraped links:
    ```
    flats-data/urls
    ``` 
    and a directory for the actual property listings:
    ```
    flats-data/listings
    ```
4. Go to ```flats-scrapy``` and run: 
    ```
    python3 scrape_links.py
    ```
    The scraped links will be saved in ```flats-data/urls```. 
5. Go to ```flats-scrapy``` and run: 
    ```
    python3 scrape_listings.py
    ```
    The data scraped of the page will be saved in ```flats-data/listings```.
6. To process the scraped data go to ```flats-etl``` and run: 
    ```
    python3 etl.py
    ```
    This will generate a file in ```flats-data``` called ```raw_data.csv```.
7. Next you should run the notebooks ```flats-notebooks``` according to the their numbering.
8. The last notebook trains all the models that are saved to ```flats-models```.