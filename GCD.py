import math
from prettytable import PrettyTable

#NAMES: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki

#PURPOSE: To find the greatest common divisor of two numbers. A divsion algorithm table will be created to show steps taken and the final postive a and b values.

# take input from the user
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

# obtain the greatest common divisor of the two numbers
gcd = math.gcd(a, b)

# initalize all values for the divsion algorithm table
u1 = 1
v1 = 0
u2 = 0
v2 = 1
u3 = a
v3 = b
q = 0

# temp U values for use when calculating V alues
temp_u1 = 0
temp_u2 = 0
temp_u3 = 0


# Create headers for the table
table = PrettyTable(["u1", "v1", "u2", "v2", "u3", "v3", "q"])
table.add_row([u1, v1, u2, v2, u3, v3, q])

# While v3 is not 0, continue to loop through the divsion algorithm.
while v3 != 0:
    temp_u1 = u1
    temp_u2 = u2
    temp_u3 = u3
    q = u3 // v3
    u1 = v1
    v1 = temp_u1 - q * v1
    u2 = v2
    v2 = temp_u2 - q * v2
    u3 = v3
    v3 = temp_u3 - q * v3
    table.add_row([u1, v1, u2, v2, u3, v3, q])

print(table)


 