from table_extract import *
from table_extract import extract_tables

def test1():
    data = extract_tables('https://en.wikipedia.org/wiki/List_of_animal_names',['Animal','Collateral adjective'],'Collateral adjective',' ')[0]
    assert len(data) == 211

def test2():
    data = extract_tables('https://en.wikipedia.org/wiki/List_of_animal_sounds',['Animal','Description'],'Description',',')[0]
    assert len(data) == 89
