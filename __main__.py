import argparse

from table_extract import extract_tables,write_to_html

parser = argparse.ArgumentParser(description='Extract fields from wiki page tables')
parser.add_argument('--url',help='Wiki page to download tables',default="https://en.wikipedia.org/wiki/List_of_animal_names")
parser.add_argument('-f','--fields', nargs='+', help='Fields to extract', default=['Animal','Collateral adjective'])
parser.add_argument('-k','--key', help='Key column to group by', default='Collateral adjective')
parser.add_argument('--html', help='html file name to write data to')
parser.add_argument('-d','--delimeter', help='Delimeter to seprate key values',default=' ')
args = parser.parse_args()

def main():

    # validate key
    if args.key not in args.fields:
        raise ValueError('Key must be some of the fields to extract')

    data = extract_tables(args.url,args.fields,args.key,args.delimeter)

    # write to html
    if args.html:
        write_to_html(args.html,data)
    else:
        for data_frame in data:
            print(data_frame)

if __name__=="__main__":
    main()