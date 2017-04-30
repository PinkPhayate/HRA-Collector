import csv
def writeCsv(list, filename):
  with open(filename, 'w') as f:
      writer = csv.writer(f, lineterminator='\n')
      writer.writerow(list)
