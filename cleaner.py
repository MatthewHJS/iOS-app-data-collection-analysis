import csv

'''
cleaner.py 

Goes through a .csv file, takes all the rows that has a value in the name field and writes it to another .csv file. 
I use this python code to remove all the rows with None values i gave them in the crawler, i find this solution to be easier
because of the parent filler etc. 

Input -> .csv file to be cleaner
Output -> new .csv file with removed None rows

'''

def clean_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            if row[1].strip(): 
                writer.writerow(row)

input_file = 'leaf_leaf_apps.csv'
output_file = 'leaf_leaf_apps1.csv'

clean_csv(input_file, output_file)

print(f"Cleaned data has been written to {output_file}.")
