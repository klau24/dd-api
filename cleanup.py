import os
import csv

def cleanup():
    dir = os.chdir('./data')
    files = os.listdir(dir)
    for file in files:
        if file.endswith('.csv'):
            with open(file, 'r') as input_file:
                csv_reader = csv.reader(x.replace('\0', 'NULL') for x in input_file)
                rows = list(csv_reader)

            for i in range(len(rows)):
                rows[i] = [cell.replace('"', '') for cell in rows[i]]
                
            with open(file, 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                for row in rows:
                    csv_writer.writerow(row)

if __name__ == "__main__":
    cleanup()