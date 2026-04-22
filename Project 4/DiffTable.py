from prettytable import PrettyTable

# Problem 1: Make a difference distribution table, analogous to Difference Distribution Table given in the slide 7 of section 4.4 in class notes, for the given S-box. Remember that you table should be an 8 × 8 table.

#Names: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki

# Header labels for prettytable.
table = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6","7"])

#S-box
S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]    

# Difference distribution table loop:
# x -> input difference a′
# y -> output difference b′
# i -> S-box input value

for x in range(8):  # input difference a′
    counter = 0
    Drow = [x, 0, 0, 0, 0, 0, 0, 0, 0]
    for y in range(8):  # output difference b′
        for i in range(8):  # iterate all S-box inputs i in {0..7}
            # Compute S(i) XOR S(i XOR a′) and check if it equals b′.
            Sxor = S[i] ^ S[i ^ x]
            if Sxor == y:
                counter +=1
        # Entry is the count of matches for this input difference a′ and output difference b′.
        Drow[y+1] = counter
        counter = 0
    # Append one completed row for this input difference a′.
    table.add_row(Drow)

print(table)