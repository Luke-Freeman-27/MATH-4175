# Difference Distribution Table

# Names: Diego Penadillo, Luke Freeman, Yoshwan Pathipati, Hiren Sai Vellanki

# Setup the table
from prettytable import PrettyTable
table = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6","7"])

#S-box
S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]

#Initialize variables
yout = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
NDrow = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]

#Creates Difference Distribution Table
for j in range(8):
    for i in range(8):
        xstar = i ^ j
        ystar = S[xstar]
        y = S[i]
        yout[i] = y ^ ystar
        NDrow[yout[i] + 1] += 1
    NDrow[0] = j
    table.add_row(NDrow)
    NDrow = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]


print(table)