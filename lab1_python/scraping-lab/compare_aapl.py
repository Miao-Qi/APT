import json

data_file = []
with open('aapl.json') as f:
    for line in f:
        data_file.append(line.strip())
		
dump_data_file = []
with open('output_aapl') as f:
    for line in f:
        dump_data_file.append(line.strip())		

for counter in range(0,len(data_file)):
  if data_file[counter] != dump_data_file[counter]:
    print "dump_line:{}\nfile_line:{}\ncounter:{}".format(dump_data_file[counter],data_file[counter],counter)
    print "data_file_len:",len(data_file[counter])
    print "dump_file_len:",len(dump_data_file[counter])
