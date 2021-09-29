from os import F_OK
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import re, os, webbrowser
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

wiki_table_class = "wikitable sortable" # html class attribute for bs parsing. achived by inspect wiki pages and find the table class in the pages"
table_header = 'th' # html table header class

def get_page_content(page_url:str):
    """
    Download a page by url and return it content
    """
    response = requests.get(page_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f'[{response.status_code}] {response.reason}')

def gen_regex_filter(strings:list):
    """
    Generate an or regex by list of words
    """
    regex_str = '(' + '|'.join(strings) + ')'
    return re.compile(regex_str)

def filter_ABC_rows(table):
    """
    Drop all A-B-C rows in table
    """
    for header in table.find_all("th",{"colspan":7}):
        header.parent.decompose()

def get_tables(page_content:str,columns:list) -> list:
    """
    Return only the tables from the page content wuth th relvant columns
    """
    page_soup = BeautifulSoup(page_content, 'html.parser')

    # find tables 
    tables = page_soup.find_all('table',{'class':wiki_table_class})

    # filter tables by the relvant columns
    reg = gen_regex_filter(columns)
    relvant_tables = list(filter(lambda t: (len(t.findChildren(table_header,recursive=True,text=reg)) == len(columns)), tables))

    # drop A-B-C tables
    for table in relvant_tables:
        filter_ABC_rows(table)
        
    return relvant_tables

def extract_tables_data(tables,columns,key,delimeter) -> list[pd.DataFrame]:
    """
    Extract tables into data using pandas
    """
    data_frames = []

    # extract data from each table
    for t in tables:
        df=pd.read_html(str(t))

        # get the relvat columns only
        df = df[0][columns]

        # generate series list
        series_list = []
        for col in columns:            
            if col!=key:

            # trim notes from series
                s = df[col].str.replace(r'\[.*?\]',"").str.replace(r' \([^()]*\)', '')
                series_list.append(s)
        
        # trim and split by space charcater in the key column
        key_s = df[key].str.replace(r'\[.*?\]',"").str.replace(r' \([^()]*\)', '').str.split(delimeter)

        # merge to one dataframe
        df = key_s.to_frame().join(series_list)

        # explode the multi values by the key
        df = df.explode(key)

        # group by the key and add to data frames list
        grouped_df = df.groupby(key, as_index=False).agg(lambda x : ', '.join(x))
        data_frames.append(grouped_df)
    
    return data_frames

def write_to_html(html_name,data:list):
    """
    Write data to html files
    """
    for i,data_frame in enumerate(data):
        html_file_name = '{}_{}.html'.format(html_name.replace('.html',''),i)
        html_file_path = os.path.join(os.getcwd(),html_file_name)
        with open(html_file_path,'w+') as html_file:
            html_file.write(data_frame.to_html())

        webbrowser.open_new_tab('file:///'+html_file_path)

def extract_tables(url:str,fields:list,key:str,delimeter:str) -> list[pd.DataFrame]:
    page_content = get_page_content(url)
    tables = get_tables(page_content,fields)
    data = extract_tables_data(tables,fields,key,delimeter)
    return data
