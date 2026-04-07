"""Problem 1: build the normalized LAT (entries NL(a,b)-4) for the project S-box."""

from prettytable import PrettyTable  # type: ignore[reportMissingImports]

#Names: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki

# Header labels for a,b in hexadecimal 0..7.
table = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6","7"])

#S-box
S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]

# NLAT loop:
#   x -> input mask a
#   y -> output mask b
#   i -> S-box input value
for x in range(8):  # input mask a
    counter = 0
    NLrow = [x, 0, 0, 0, 0, 0, 0, 0, 0]
    for y in range(8):  # output mask b
        for i in range(8):  # iterate all S-box inputs i in {0..7}
            # Compute parity(a·i) and parity(b·S(i)).
            Xval = (x & i).bit_count() % 2
            Yval = (y & S[i]).bit_count() % 2
            Outxor = Xval ^ Yval
            # Count matches where a·i XOR b·S(i) = 0.
            if Outxor == 0:
                counter +=1
        # Entry is NL(a,b)-4 for l=3.
        NLrow[y+1] = counter - 4
        counter = 0
    # Append one completed row for this input mask a.
    table.add_row(NLrow)

print(table)

