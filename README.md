# Wiki Columns extractor
Extract fields from wiki page tables

## Requirments
`BeautifulSoup4
requests
pandas
lxml
html5lib
webbrowser`

`pytest (optional)`

## Usage

`python __main__.py [-h] [--url URL] [-f FIELDS] [-k KEY] [--html HTML]`

    optional arguments:

    --url URL             
        Wiki page to download tables (default: https://en.wikipedia.org/wiki/List_of_animal_names)

    -f [FIELDS ...], --fields [FIELDS ...]
        Fields to extract (default: ['Animal','Collateral adjective'])

    -k KEY, --key KEY     
        Key column to group by (default: 'Collateral adjective')

    --html HTML           
        Html file(s) name to write data to. File(s) will be in the execute dir.

    -d DELIMETER, --delimetter DELIMETER
        Delimeter character that seprate between values in the key column (default: ' ')

## Test
- `pytest` required!

`pytest __test__.py`
