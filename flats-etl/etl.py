import pandas as pd
import numpy as np
import re 

from unidecode import unidecode

# Map district in Kraków to integers.
# For details see:
# https://en.wikipedia.org/wiki/Districts_of_Krak%C3%B3w
districts = {'stare miasto': 1,
             'grzegórzki': 2,
             'prądnik czerwony': 3,
             'prądnik biały': 4,
             'krowodrza': 5,
             'bronowice': 6,
             'zwierzyniec': 7,
             'dębniki': 8,
             'łagiewniki': 9,
             'borek fałęcki': 9,
             'swoszowice': 10,
             'podgórze duchackie': 11,
             'bieżanów': 12,
             'prokocim': 12,
             'podgórze': 13,
             'czyżyny': 14,
             'mistrzejowice': 15,
             'bieńczyce': 16,
             'wzgórza krzesławickie': 17,
             'nowa huta': 18}

# Remove polish characters from key names
for key in list(districts.keys()):
    districts[unidecode(key)] = districts.pop(key)

# Translate data from polish to english.
translation = {'Cena': 'Price',
               'Lokalizacja': 'Location',
               'Data dodania': 'Date',
               'Na sprzedaż przez': 'Seller',
               'Rodzaj nieruchomości': 'Property',
               'Liczba pokoi': 'Rooms',
               'Liczba łazienek': 'Bathrooms',
               'Wielkość (m2)': 'Area',
               'Parking': 'Parking',
               'Tytuł': 'Title',
               'Opis': 'Description',
               'Link': 'Link'}             

def remove_polish_characters(x):
    """
    Remove polsih chars

    Examples
    --------    
    >>> remove_polish_characters('ąćęłńóśźż')
    'acelnoszz'

    """
    if pd.isnull(x):
        return x
    else:
        x = unidecode(x)
        return x

def parse_price(x):
    """
    Convert string with price to a integer value.

    Parameters
    ----------
    x : str
        Row from price column.

    Returns
    -------
    int :
        Price of the property.

    Example
    -------
    >>> parse_price('349\xa0000 zł')
    349000
    >>> parse_price('349 000 zł')
    349000
    >>> parse_price('349\xa0000')
    349000
    >>> parse_price('349000')    
    349000
    >>> parse_price(349000)    
    349000
    >>> parse_price(349000.1235)
    349000
    >>> parse_price(np.nan)
    nan
    >>> parse_price('Proszę o kontakt')
    nan

    """
    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.replace('\xa0', '')
            x = x.replace('zł', '')
            x = x.replace(' ', '')
            x = x.strip()
            try:
                x = int(x)                
            except ValueError:
                x = np.nan
            return x    
        elif isinstance(x, int):
            return x
        elif isinstance(x, float):
            x = int(x)
            return x
        else:
            return np.nan

def extract_currency(x):
    """
    Exctract currency from price column.

    Examples
    --------
    >>> extract_currency('123000zł')
    'pln'

    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()            
            if 'zł' in x or 'zł' in x or 'pln' in x:
                return 'pln'
            else:
                return np.nan
        else:
            return np.nan               
        
def parse_bathrooms(x):    
    """
    Extract first digit from string 
    describing the number of bathrooms.

    Parameters
    ----------
    x : str
        String describing the number of bathrooms.
    
    Returns
    -------
    int :
        The number of bathrooms or nan.

    Examples
    --------
    >>> parse_bathrooms('1 łazienka')
    1
    >>> parse_bathrooms('2 łazienki')
    2
    >>> parse_bathrooms('4')
    4
    >>> parse_bathrooms(3)    
    3

    """
    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = [s for s in x if s.isdigit()]
            if x:
                return int(x[0])
            else:
                return np.nan
        elif isinstance(x, int):
            return x
        elif isinstance(x, float):
            return int(x)
        else:
            return np.nan
                    
def parse_rooms(x):
    """
    
    Extract first digit in string 
    describing the number of bathrooms.

    Parameters
    ----------
    x : str
        Row of rooms column.
    
    Returns
    -------
    int
        The number of rooms in the property.

    Examples
    --------
    >>> parse_rooms('2 pokoje')
    2
    >>> parse_rooms('5')    
    5
    >>> parse_rooms('3')    
    3

    """
        
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            # Check for special
            # cases first
            x = x.lower()
            if 'kawalerka' in x:
                return 1
            elif 'garsoniera' in x:
                return 1
            else:
                # If not special case extract
                # first digit in string.
                x = [s for s in x if s.isdigit()]
                if x:
                    return int(x[0])
                else:
                    return np.nan
        elif isinstance(x, float):
            return int(x)
        elif isinstance(x, int):
            return x
        else:
            return np.nan
        
def extract_city(x):
    """
    Extract city from location column.

    Parameters
    ----------
    x : str
        Row of location column.        

    Returns
    -------
    str :
        Kraków if the property is 
        located in Kraków else nan.

    Examples
    --------
    >>> extract_city('Piotra Stachiewicza, Kraków-Krowodrza, Kraków')
    'kraków'
    >>> extract_city('os. Na Stoku, Kraków-Nowa Huta, Kraków')
    'kraków'
    >>> extract_city('Modlniczka, Wielka Wieś, krakowski')
    nan
    >>> extract_city('random string')
    nan

    """
    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.split(',')        
            x = [s.strip().lower() for s in x]
            if 'kraków' in x or 'krakow' in x or 'cracow' in x:
                return 'kraków'
            else:
                return np.nan
        else:
            return np.nan

def extract_district(x):
    """
    Extract district from location column.

    Parameters
    ----------
    x : str
        Row from location column.

    Returns
    -------
    str :
        The district where the property is located.

    Examples
    --------
    >>> extract_district('Piotra Stachiewicza, Kraków-Krowodrza, Kraków')
    'krowodrza'
    >>> extract_district('os. Na Stoku, Kraków-Nowa Huta, Kraków')
    'nowa huta'
    >>> extract_district('Modlniczka, Wielka Wieś, krakowski')
    nan
    >>> extract_city('random string')
    nan

    """
    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            x = x.replace('kraków', '')            
            x = x.replace(',', ' ')
            x = x.replace('-', ' ')
            x = x.replace('.', ' ')
            x = x.split(' ')
            x = [s.replace(' ', '') for s in x if s != '']
            x = ' '.join(x)
            if x == '':
                return np.nan
            else:
                for key in districts:
                    if key in x:
                        return key
                return np.nan            

def parse_seller(x):
    """
    Translate seller column to english.
    """
    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'agencja' in x:
                return 'realtor'
            elif 'właściciel' in x:
                return 'owner'
            else:
                return np.nan
        else:
            return np.nan                

def parse_property(x):
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'dom' in x:
                return 'house'
            elif 'mieszkanie' in x:
                return 'flat'
            else:
                return np.nan
        else:
            return np.nan

def parse_parking(x):
    """
    Translate parking column.

    Examples
    --------
    >>> parse_parking('garaż')
    'garage'
    >>> parse_parking('Ulica')
    'street'
    >>> parse_parking('Brak')
    'no parking'
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'garaż' in x:
                return 'garage'
            elif 'kryty' in x:
                return 'covered'
            elif 'ulica' in x:
                return 'street'
            elif 'brak' in x:
                return 'no parking'
            else:
                return np.nan
        else:
            return np.nan

def extract_garden(x):
    """
    Check if property has garden.

    Examples
    --------
    >>> extract_garden('piękny ogrod')    
    True
    >>> extract_garden('piękny dom')    
    False
    >>> extract_garden('1223')    
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()            
            if 'ogrod' in x:
                return True
            else:
                return False
        else:
            return False

def extract_balcony(x):
    """
    Check if property has balcony.

    Examples
    --------
    >>> extract_balcony('Mieszkanie z pięknym balkonem')    
    True
    >>> extract_balcony('Brzydkie mieszkanie')    
    False

    """
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()            
            if 'balkon' in x:
                return True
            else:
                return False
        else:
            return False    

def extract_terrace(x):
    """
    Check if property has terrace.

    Examples
    --------
    >>> extract_terrace('Mieszkanie z tarasem')    
    True
    >>> extract_terrace('Brzydkie mieszkanie')    
    False
    >>> extract_terrace('125')    
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()            
            if 'taras' in x:
                return True
            else:
                return False
        else:
            return False    

def extract_basement(x):
    """
    Check if property has a basement.

    Examples
    --------    
    >>> extract_basement('Mieszkanie z przynależną piwnica')
    True
    >>> extract_basement('Pierwsze pietro')
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()            
            if 'piwnica' in x:
                return True
            else:
                return False
        else:
            return False    
            
def extract_new(x):
    """
    Check if property is new.

    Examples
    --------    
    >>> extract_new('Nowe mieszkanie')
    True
    >>> extract_new('Stare mieszkanie')
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'nowe' in x or 'nowa' in x:
                return True
            else:
                return False
        else:
            return False                

def extract_block(x):
    """
    Check if property is in an block.

    Examples
    --------
    >>> extract_block('Piękne mieszkanie w bloku xxx')
    True
    >>> extract_block(123)
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'bloku' in x:
                return True
            else:
                return False
        else:
            return False        

def extract_town_house(x):
    """
    Check if property is in a town house.

    Examples
    --------
    >>> extract_town_house('Małe mieszkanie w kamienicy')
    True
    >>> extract_town_house('Duże mieszkanie w bloku')
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'kamienica' in x or 'kamienicy' in x:
                return True
            else:
                return False
        else:
            return False    


def extract_apartment(x):
    """
    Check if property is an apartment.

    Examples
    --------
    >>> extract_apartment('Apartament na sprzedaż')
    True
    >>> extract_apartment('Kawalerka na sprzedaż')    
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'apartament' in x or 'apartamencie' in x:
                return True
            else:
                return False
        else:
            return False    

def extract_studio(x):
    """
    Check if property is studio flat.

    Examples
    --------
    >>> extract_studio('Kawalerka na sprzedaż')    
    True
    >>> extract_studio('Apartament na sprzedaż')
    False
    """

    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'kawalerka' in x or 'kawaler' in x:
                return True
            else:
                return False
        else:
            return False                

def extract_bus_stops(x):
    """
    Check is property has bus stops nearby.

    Examples
    --------
    >>> extract_bus_stops('Blisko przystanki komunkacji miejskiej')
    True

    """    
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = x.lower()
            if 'miejskiej' in x:
                return True
            else:
                return False
        else:
            return False        

def parse_title(x):
    """
    Remove non letters from title.

    Examples
    --------
    >>> parse_title('Piękne mieszkanie !!!')
    'piękne mieszkanie'

    """
    if pd.isnull(x):
        return x
    else:
        if isinstance(x, str):
            x = re.sub(r'\W+', ' ', x)        
            x = x.strip()
            x = x.lower()
            return x
        else:
            return x

def count_missing(df):
    """
    Count missing values in dataframe.

    Returns
    -------
    DataFrame : Dataframe with % of missing values.

    """
    count = np.round(df.isna().sum() / len(df) * 100, 2)
    return count.to_frame(name='NaN %')

def translate_cols(df):
    """
    Translate column names to english.
    """

    df = df.rename(columns=translation)    
    return df

def get_data(path):
    """
    Read csv from path.
    """

    if not isinstance(path, str):
        print(f'{path} is not a string')        
        return
    else:
        try:
            data = pd.read_csv(path)
        except FileNotFoundError:
            print(f'{path} does not exist.')
            return
        else:
            print(f'Data read.')
            return data



def transform(in_path, out_path, prefix='raw'):

    if isinstance(in_path, list):
        dfs = list()
        for path in in_path:
            try:
                tmp = get_data(path=path)
            except pd.errors.EmptyDataError:
                pass
            else:
                dfs.append(tmp)
        df = pd.concat(dfs)
        df = df.reset_index(drop=True)
    elif isinstance(in_path, str):
        df = get_data(path=in_path)
    else:
        print(f'in_path should be string or list, got {type(in_path)} instead.')
        return

    df = translate_cols(df)

    nrows_before = len(df)
    print(f'Rows before transforming {nrows_before}.')
    print('Missing before processing:')    
    print(count_missing(df))

    text_cols = ['Title', 'Location', 'Description']
    df['Full Text'] = df[text_cols].apply(lambda x: ' '.join(map(str, x)), axis=1)
    df['Full Text'] = df['Full Text'].apply(remove_polish_characters)

    # Parse
    df['Amount'] = df['Price'].apply(parse_price)
    df['Bathrooms'] = df['Bathrooms'].apply(parse_bathrooms)    
    df['Rooms'] = df['Rooms'].apply(parse_rooms)
    df['Seller'] = df['Seller'].apply(parse_seller)    
    df['Property'] = df['Property'].apply(parse_property)    
    df['Parking'] = df['Parking'].apply(parse_parking)
    df['Title'] = df['Title'].apply(parse_title)

    # Extract
    df['City'] = df['Location'].apply(extract_city)    
    df['Currency'] = df['Price'].apply(extract_currency)    

    df['District'] = df['Full Text'].apply(extract_district)    
    df['Garden'] = df['Full Text'].apply(extract_garden)
    df['Balcony'] = df['Full Text'].apply(extract_balcony)
    df['Terrace'] = df['Full Text'].apply(extract_terrace)
    df['Basement'] = df['Full Text'].apply(extract_basement)
    df['New'] = df['Full Text'].apply(extract_new)
    df['Estate'] =  df['Full Text'].apply(extract_block)
    df['Townhouse'] = df['Full Text'].apply(extract_town_house)
    df['Apartment'] = df['Full Text'].apply(extract_apartment)
    df['Bus stops'] = df['Full Text'].apply(extract_bus_stops)
    df['Studio'] = df['Full Text'].apply(extract_studio)    

    # Remove useles columns
    df = df.drop(['Price'], axis=1)

    df['Date'] = pd.to_datetime(df['Date'])    

    # Reorrder
    cols = ['Date',  'City', 'District', 'Amount', 'Currency', 
            'Property', 'Seller', 'Area', 'Rooms', 'Bathrooms', 
            'Parking', 'Garden', 'Balcony', 'Terrace', 'Basement', 
            'New', 'Estate', 'Townhouse', 'Apartment', 'Bus stops',
            'Studio', 'Title', 'Description', 'Link']

    df = df[cols]

    print('Missing after processing:')
    print(count_missing(df))

    nrows_after = len(df)
    print(f'Rows remaining {nrows_after}.')
    print(f'Dropped {nrows_before - nrows_after}.')    

    out_path += f'{prefix}_data.csv'

    df.to_csv(out_path, index=False, line_terminator='\n')

if __name__ == '__main__':

    import doctest    
    doctest.testmod()        