"""
MATH 4175 — Project 3 (full helper script)

Bit convention for 6-bit strings in the handout table:
  Leftmost character is P1 (resp. C1); rightmost is P6 (C6).

S-box (hex): x -> S[x]
Permutation after each S-layer (B -> D, same F -> G):
  D1=B1, D2=B3, D3=B5, D4=B2, D5=B4, D6=B6
"""

from __future__ import annotations

S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]

INV_S = [0] * 8
for x, y in enumerate(S):
    INV_S[y] = x

PAIRS = [
    ("100111", "100100"),
    ("000111", "110010"),
    ("001100", "111001"),
    ("011000", "011101"),
    ("001000", "001101"),
    ("011010", "101001"),
]


def nl_minus4(a: int, b: int) -> int:
    """Table entry NL(a,b) - 4 for the project S-box."""
    cnt = 0
    for i in range(8):
        if ((a & i).bit_count() + (b & S[i]).bit_count()) % 2 == 0:
            cnt += 1
    return cnt - 4


def eps(a: int, b: int) -> float:
    """Bias epsilon(a,b) = (NL(a,b) - 4) / 8."""
    return nl_minus4(a, b) / 8.0


def perm6(mask: list[int]) -> list[int]:
    m = mask
    return [m[0], m[2], m[4], m[1], m[3], m[5]]


def pack3(bits: list[int]) -> int:
    return (bits[0] << 2) | (bits[1] << 1) | bits[2]


def unpack3(v: int) -> list[int]:
    return [(v >> 2) & 1, (v >> 1) & 1, v & 1]


def print_lat_prettytable() -> None:
    from prettytable import PrettyTable

    t = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6", "7"])
    for a in range(8):
        row = [a] + [nl_minus4(a, b) for b in range(8)]
        t.add_row(row)
    print(t)


def piling_two_parallel(e1: float, e2: float) -> float:
    """Piling-up lemma for XOR of two independent-ish S-box approximations (same round)."""
    return 2.0 * e1 * e2


def plaintext_p1245_mask() -> list[int]:
    """Mask g with g·P = P1 XOR P2 XOR P4 XOR P5 (P1 = leftmost char)."""
    m = [0] * 6
    for idx in (0, 1, 3, 4):  # P1..P6 at indices 0..5
        m[idx] = 1
    return m


def round_s_layer(mask6: list[int]) -> list[tuple[int, int, float]]:
    """Enumerate nonzero (b_top, b_bot, eps_round) for one S layer given input mask."""
    a1 = pack3(mask6[0:3])
    a2 = pack3(mask6[3:6])
    out = []
    for b1 in range(8):
        n1 = nl_minus4(a1, b1)
        if n1 == 0:
            continue
        e1 = n1 / 8.0
        for b2 in range(8):
            n2 = nl_minus4(a2, b2)
            if n2 == 0:
                continue
            e2 = n2 / 8.0
            er = piling_two_parallel(e1, e2)
            out.append((b1, b2, er))
    return out


def apply_s_output(b1: int, b2: int) -> list[int]:
    return unpack3(b1) + unpack3(b2)


def k4_counters() -> None:
    print("Problem 4 — count of (P1^P2^P4^P5^H1 == 0) over 6 pairs\n")
    print("Guess K4 on C1 C2 C3 (bits xor J1 J2 J3), MSB..LSB = first three bits as in diagram order.\n")
    for guess in range(8):
        gbits = unpack3(guess)
        z = 0
        for pt, ct in PAIRS:
            pb = [1 if c == "1" else 0 for c in pt]
            cb = [1 if c == "1" else 0 for c in ct]
            j0 = cb[0] ^ gbits[0]
            j1 = cb[1] ^ gbits[1]
            j2 = cb[2] ^ gbits[2]
            jv = pack3([j0, j1, j2])
            hv = INV_S[jv]
            h1 = (hv >> 2) & 1  # MSB of S^{-1}(J) = H1 in project diagram
            t = pb[0] ^ pb[1] ^ pb[3] ^ pb[4] ^ h1
            if t == 0:
                z += 1
        print(f"  K4[1..3] = {guess}  ({gbits[0]}{gbits[1]}{gbits[2]})  zeros: {z}/6")


def main() -> None:
    print("=== Problem 1: Normalized LAT (entry = NL(a,b) - 4) ===\n")
    print_lat_prettytable()

    print("\n=== Problem 2/3 sketch (one valid 2-round stack) ===\n")
    print("Start mask on A (after K1) for P1+P2+P4+P5:")
    m0 = plaintext_p1245_mask()
    print(" ", m0, "-> S11 mask a=", pack3(m0[0:3]), " S12 mask a=", pack3(m0[3:6]))
    print("Row 6 of LAT only allows b=4 on BOTH S-boxes (NL=-4, eps=-1/2 each).")
    b1 = b2 = 4
    e_r1 = piling_two_parallel(eps(6, 4), eps(6, 4))
    print(f"After round-1 S-boxes: (b1,b2)=({b1},{b2}), round-1 stacked bias = 2*eps*eps = {e_r1}")
    B = apply_s_output(b1, b2)
    E = perm6(B)
    print("B (output of S boxes) mask bits:", B)
    print("E = perm(B) (input mask to round-2 S after K2):", E)
    a21, a22 = pack3(E[0:3]), pack3(E[3:6])
    print(f"Round 2 active S-box input masks: {a21} and {a22}")
    # pick (2,2) on both: NL values row4 col2 = 2, row2 col2 = -2
    c1, c2 = 2, 2
    print(f"Example second-round choice: (b_top,b_bot)=({c1},{c2}) "
          f"(NL={nl_minus4(a21,c1)} and {nl_minus4(a22,c2)})")
    e_r2 = piling_two_parallel(eps(a21, c1), eps(a22, c2))
    F = apply_s_output(c1, c2)
    G = perm6(F)
    print("F mask:", F, "G = perm(F) (mask before K3, on H wires):", G)
    print(f"Round-2 stacked bias = {e_r2}")
    e_tot = 2.0 * e_r1 * e_r2
    print(f"Total trail bias (2 rounds, piling-up across rounds): 2 * {e_r1} * {e_r2} = {e_tot}")
    print("(Use this style in your PDF; adjust (b_top,b_bot) if your instructor wants a different G mask.)")

    print("\n=== Problem 4/5: Counters ===\n")
    k4_counters()


if __name__ == "__main__":
    main()
