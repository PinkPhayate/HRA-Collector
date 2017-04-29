def writeCsv(list, filename):
  with open('./../Resource/rid_list.csv', 'w') as f:
      writer = csv.writer(f, lineterminator='\n')
      writer.writerow(list)
