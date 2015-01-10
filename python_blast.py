#Input file name: "blast.txt", output file name: "select.txt"
#Runing with the command: python python_blast.py
#The first step is to build the database according to the -ALGNMENTS-.
datadict = {} #To build the database of the "ref|...|" based on the ALGNMENTS part
list_buffer = []
count = 1
filelines = 8253
Begin_ref_flag = 0
End_ref_flag = 0
Filled_finish_flag = 0
file_read = open("blast.txt","r")
while count < filelines :
	line_string = file_read.readline()
	if count >= 406 : #Begin of the ALIGNMENTS parts
		line_list = (line_string.strip()).split(' ')
		line_list_length = len(line_list)
		line_list_1_length = len(line_list[0])
		#To allocate the buffer list to restore the "ref|...|" and the corresponding "Gaps = ..."
		if line_list_1_length > 0 and line_list[0][0] == '>' :
			End_ref_flag += 1
		if End_ref_flag != Begin_ref_flag :
			Begin_ref_flag += 1
			list_buffer = []
			Filled_finish_flag = 0
		if line_list_1_length > 0 and line_list[0][0:4] == '>ref' :
			list_buffer.append(line_list[0][1:])
		if line_list_1_length > 0 and line_list[0][0:3] == 'ref' :
			list_buffer.append(line_list[0])
		if line_list_1_length > 0 and line_list[0] == 'Identities' :
			list_buffer.append(line_list[10]) #The value of "Gaps" is at the line_list[10]
		if len(list_buffer) != 0 and list_buffer[len(list_buffer)-1][0] != 'r' :
			Filled_finish_flag += 1
		if Filled_finish_flag == 1 :
			for i in range(len(list_buffer)-1) :
				datadict.setdefault(list_buffer[i],list_buffer[len(list_buffer)-1])
	count += 1
file_read.close()
#Finish building the database

#The second step is to search the "Gaps" values for the "ref|...|" items in the database and proceed the print. 
count = 1
file_read = open("blast.txt","r")
file_write = open("select.txt","w")
while count < filelines :
	line_string = file_read.readline()
	line_list = (line_string.strip()).split(' ')
	line_list_length = len(line_list)
	line_list_1_length = len(line_list[0])
	if line_list_1_length >= 3 and line_list[0][0:3] == 'ref' :
		if line_list[line_list_length-1][0] >= '0' and line_list[line_list_length-1][0] <= '9' and float(line_list[line_list_length-1]) < 1e-100 : #Only the E-value < 1e-100 is output
			file_write.write(line_list[0] + ' ' + datadict[line_list[0]] + ' ' + line_list[line_list_length-1] + '\n')
		#if line_list[line_list_length-1][0] >= '0' and line_list[line_list_length-1][0] <= '9': #all will be output
		    #file_write.write(line_list[0] + ' ' + datadict[line_list[0]] + ' ' + line_list[line_list_length-1] + '\n')
	count += 1
file_read.close()
file_write.close()
#Finish writing the contents into file
