from prettytable import PrettyTable

#Names: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki

#Generate the normalized linear approximation table given the S-box

#Header column and row for table
table = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6","7"])

#S-box
S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]

#Normalized Linear Approximation table loop
for x in range(8): #Input
    #reset counter and values
    counter = 0
    NLrow = [x, 0, 0, 0, 0, 0, 0, 0, 0]
    for y in range(8): #Output
        for i in range(8): #NL calculation
            #XOR operation
            Xval = (x & i).bit_count() % 2
            Yval = (y & S[i]).bit_count() % 2
            Outxor = Xval ^ Yval
            #Increment if the probability statement is true
            if Outxor == 0:
                counter +=1
        NLrow[y+1] = counter - 4 #Normalize output and add entry
        counter = 0
    #Add normalized outputs for a single input to the table
    table.add_row(NLrow)

print(table)

