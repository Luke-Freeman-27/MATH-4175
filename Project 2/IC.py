#NAMES: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki

#PURPOSE: Vigenere cipher cryptanalysis - IC analysis, key recovery, and decryption.

# Open file and read ciphertext
# File is one line of text with no newline characters.
file = open("ciphertext.md", "r")
ciphertext = file.read().strip().upper()
file.close()

# PART 1: Index of Coincidence analysis for m = 6, 7, 8

print("PART 1: Index of Coincidence Analysis")

# Formatting for the table output
for m in [6, 7, 8]:
    print(f"\n{'='*40}")
    print(f"m = {m}")
    print(f"{'='*40}")

    # Split the ciphertext into m substrings (cosets)
    substrings = []
    for i in range(m):
        substring = ""
        for j in range(i, len(ciphertext), m):
            substring += ciphertext[j]
        substrings.append(substring)

    # Calculate and print the Index of Coincidence for each substring
    ic_values = []
    for i in range(m):
        substring = substrings[i]
        n = len(substring)
        freq = {}
        # Count the frequency of each letter in the substring
        for ch in substring:
            freq[ch] = freq.get(ch, 0) + 1
        ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
        ic_values.append(ic)
        print(f"  y{i+1}: IC = {ic:.4f}  (length = {n})")

    # Calculate the average IC for all substrings
    avg_ic = sum(ic_values) / len(ic_values)
    print(f"  Average IC = {avg_ic:.4f}")

# PART 2: Key recovery using mutual IC / frequency correlation (m = 7)

print("\n\nPART 2: Frequency Analysis Table & Key Recovery")

# English letter frequencies (a=0, b=1, ..., z=25)
ENGLISH_FREQ = [
    0.0817, 0.0149, 0.0278, 0.0425, 0.1202, 0.0223, 0.0202, 0.0609,
    0.0697, 0.0015, 0.0077, 0.0403, 0.0241, 0.0675, 0.0751, 0.0193,
    0.0010, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015,
    0.0197, 0.0007
]

m = 7

# Split into 7 cosets, same as before
substrings = []
for i in range(m):
    substring = ""
    for j in range(i, len(ciphertext), m):
        substring += ciphertext[j]
    substrings.append(substring)

# Empty string to build the keyword
keyword = ""

# For each coset, compute M_g for all shifts g and find the best one
for i, sub in enumerate(substrings):
    n = len(sub)

    # Count letter frequencies in this coset
    counts = [0] * 26
    for ch in sub:
        if ch.isalpha():
            counts[ord(ch) - ord('A')] += 1

    # Compute M_g for each possible shift g (0=A, 1=B, ..., 25=Z)
    mg_values = []
    for g in range(26):
        mg = sum((counts[j] / n) * ENGLISH_FREQ[(j - g) % 26] for j in range(26))
        mg_values.append(mg)

    # Find the shift g that maximizes M_g
    best_g = mg_values.index(max(mg_values))
    key_letter = chr(best_g + ord('A'))
    keyword += key_letter

    # Print top 5 candidate shifts for this coset
    ranked = sorted(range(26), key=lambda g: mg_values[g], reverse=True)
    print(f"\n{'='*40}")
    print(f"y{i+1} (length={n}):")
    print(f"  {'Shift (g)':<12} {'Key Letter':<12} {'M_g':>8}")
    print(f"  {'-'*35}")
    for g in ranked[:5]:
        marker = " <-- best" if g == best_g else ""
        print(f"  {g:<12} {chr(g + ord('A')):<12} {mg_values[g]:>8.5f}{marker}")

print(f"\n{'='*40}")
print(f"Keyword: {keyword}")

# PART 3: Decrypt the ciphertext using the recovered keyword

print("\n\nPART 3: Decryption using keyword:", keyword)
print("="*40)

# Convert the keyword letters into their indexes (0=A, 1=B, ..., 25=Z)
key = [ord(k) - ord('A') for k in keyword]

plaintext = ""

# Decrypt each letter in the ciphertext
for i, ch in enumerate(ciphertext):
    if ch.isalpha():
        p = (ord(ch) - ord('A') - key[i % len(key)]) % 26
        plaintext += chr(p + ord('a'))
    else:
        plaintext += ch

# Output the decrypted plaintext
print("\nRaw decrypted text:")
print(plaintext)