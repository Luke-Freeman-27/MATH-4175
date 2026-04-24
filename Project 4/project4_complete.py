"""
MATH 4175 - Project 4 complete differential workflow.

This script computes:
1) 8x8 DDT for the project S-box
2) Three differential trails from x' = 000001 to H-differences
   001, 011, 111 (Tr1, Tr2, Tr3)
3) Total propagation ratios R1, R2, R3
4) Filtering of right 4-tuples
5) c1/c2/c3 counters, weighted score C, and recovered K4 last 3 bits
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from prettytable import PrettyTable


S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]
INV_S = [0] * 8
for _x, _y in enumerate(S):
    INV_S[_y] = _x

# Given 4-tuples from project statement (x, y, x*, y*)
FOUR_TUPLES = [
    ("100111", "100100", "100110", "111110"),
    ("000111", "110010", "000110", "110110"),
    ("001100", "111001", "001101", "100000"),
    ("011000", "011101", "011001", "011111"),
    ("001000", "001101", "001001", "000011"),
    ("011010", "101001", "011011", "101000"),
]


@dataclass
class Trail:
    name: str
    target_h_diff: int
    b_round1: int
    e_after_p1: int
    b_round2: int
    h_diff: int
    probability: float
    ratio_fraction: str


def bits6(v: int) -> str:
    return format(v, "06b")


def build_ddt() -> list[list[int]]:
    ddt = [[0 for _ in range(8)] for _ in range(8)]
    for a in range(8):
        for x in range(8):
            b = S[x] ^ S[x ^ a]
            ddt[a][b] += 1
    return ddt


def split6(v: int) -> tuple[int, int]:
    return ((v >> 3) & 0b111, v & 0b111)


def join6(top3: int, bot3: int) -> int:
    return (top3 << 3) | bot3


def permute_6_bits(v: int) -> int:
    """
    Permutation wiring used for this Project 4 differential workflow.
    """
    b = [(v >> i) & 1 for i in range(5, -1, -1)]
    p = [b[5], b[4], b[3], b[2], b[1], b[0]]
    out = 0
    for bit in p:
        out = (out << 1) | bit
    return out


def round_transitions(input_diff: int, ddt: list[list[int]]) -> list[tuple[int, int, float]]:
    a_top, a_bot = split6(input_diff)
    transitions = []
    for b_top in range(8):
        c_top = ddt[a_top][b_top]
        if c_top == 0:
            continue
        for b_bot in range(8):
            c_bot = ddt[a_bot][b_bot]
            if c_bot == 0:
                continue
            b_out = join6(b_top, b_bot)
            p_out = permute_6_bits(b_out)
            prob = (c_top / 8.0) * (c_bot / 8.0)
            transitions.append((b_out, p_out, prob))
    return transitions


def as_fraction(prob: float) -> str:
    mapping = {
        1.0: "1",
        0.5: "1/2",
        0.25: "1/4",
        0.125: "1/8",
        0.0625: "1/16",
        0.03125: "1/32",
        0.015625: "1/64",
    }
    return mapping.get(prob, f"{prob:.6f}")


def best_trail_to_target(
    name: str, start_diff: int, target_h_diff: int, ddt: list[list[int]]
) -> Trail:
    best = None
    for b1, e1, p1 in round_transitions(start_diff, ddt):
        for b2, h2, p2 in round_transitions(e1, ddt):
            if h2 != target_h_diff:
                continue
            p = p1 * p2
            if best is None or p > best[0]:
                best = (p, b1, e1, b2, h2)
    if best is None:
        raise ValueError(f"No nonzero trail found for target H'={bits6(target_h_diff)}")
    p, b1, e1, b2, h2 = best
    return Trail(
        name=name,
        target_h_diff=target_h_diff,
        b_round1=b1,
        e_after_p1=e1,
        b_round2=b2,
        h_diff=h2,
        probability=p,
        ratio_fraction=as_fraction(p),
    )


def total_ratio_for_target(start_diff: int, target_h_diff: int, ddt: list[list[int]]) -> float:
    total = 0.0
    for _, e1, p1 in round_transitions(start_diff, ddt):
        for _, h2, p2 in round_transitions(e1, ddt):
            if h2 == target_h_diff:
                total += p1 * p2
    return total


def filter_right_tuples(rows: list[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
    # Keep tuples where top-half ciphertext difference is 000.
    out = []
    for row in rows:
        _, y, _, y_star = row
        y_diff = int(y, 2) ^ int(y_star, 2)
        if (y_diff >> 3) == 0:
            out.append(row)
    return out


def counter_for_guess(
    guess_k4_last3: int,
    tuples: list[tuple[str, str, str, str]],
    trail_target_hdiff_low3: int,
) -> int:
    c = 0
    for _, y, _, y_star in tuples:
        c_low = int(y, 2) & 0b111
        c_star_low = int(y_star, 2) & 0b111
        h_low = INV_S[c_low ^ guess_k4_last3]
        h_star_low = INV_S[c_star_low ^ guess_k4_last3]
        if (h_low ^ h_star_low) == trail_target_hdiff_low3:
            c += 1
    return c


def print_ddt(ddt: list[list[int]]) -> None:
    t = PrettyTable([" ", "0", "1", "2", "3", "4", "5", "6", "7"])
    for a in range(8):
        t.add_row([a] + ddt[a])
    print("=== Part 1: Difference Distribution Table ===")
    print(t)
    print()


def print_trails(trails: list[Trail]) -> None:
    print("=== Part 2: Three Differential Trails ===")
    for tr in trails:
        print(f"{tr.name}: target H'={bits6(tr.target_h_diff)}")
        print(
            "  "
            f"Round1 B'={bits6(tr.b_round1)} -> E'={bits6(tr.e_after_p1)}, "
            f"Round2 B'={bits6(tr.b_round2)} -> H'={bits6(tr.h_diff)}"
        )
        print(f"  trail ratio = {tr.ratio_fraction} ({tr.probability:.6f})")
    print()


def print_total_ratios(trails: list[Trail], ratio_fn: Callable[[int], float]) -> None:
    print("=== Part 3: Total Propagation Ratios ===")
    for tr in trails:
        total = ratio_fn(tr.target_h_diff)
        print(f"{tr.name}: R = {as_fraction(total)} ({total:.6f})")
    print()


def print_filtering(selected: list[tuple[str, str, str, str]]) -> None:
    print("=== Part 4: Filtering Right 4-tuples ===")
    print("Selected tuples (x, y, x*, y*):")
    for row in selected:
        print(" ", row)
    print()


def print_counters_and_key(trails: list[Trail], selected: list[tuple[str, str, str, str]]) -> None:
    print("=== Part 5: Counters c1/c2/c3 and Weighted C ===")
    ratios = [tr.probability for tr in trails]
    counts = []
    for tr in trails:
        target_low3 = tr.target_h_diff & 0b111
        counts.append([counter_for_guess(k, selected, target_low3) for k in range(8)])

    table = PrettyTable(
        ["K4(last3)", "c1", "c2", "c3", "C = R1*c1 + R2*c2 + R3*c3"]
    )
    best_k = 0
    best_c = -1.0
    for k in range(8):
        weighted = ratios[0] * counts[0][k] + ratios[1] * counts[1][k] + ratios[2] * counts[2][k]
        table.add_row([format(k, "03b"), counts[0][k], counts[1][k], counts[2][k], f"{weighted:.6f}"])
        if weighted > best_c:
            best_c = weighted
            best_k = k

    print(table)
    print(f"\nRecovered K4 last 3 bits: {format(best_k, '03b')}")


def main() -> None:
    ddt = build_ddt()
    start_diff = 0b000001

    # Required trail endpoints:
    # Tr1 -> H6 (001), Tr2 -> H5,H6 (011), Tr3 -> H4,H5,H6 (111)
    targets = [0b000001, 0b000011, 0b000111]
    names = ["Tr1", "Tr2", "Tr3"]
    trails = [
        best_trail_to_target(names[i], start_diff, targets[i], ddt)
        for i in range(3)
    ]

    selected = filter_right_tuples(FOUR_TUPLES)

    print_ddt(ddt)
    print_trails(trails)
    print_total_ratios(trails, lambda target: total_ratio_for_target(start_diff, target, ddt))
    print_filtering(selected)
    print_counters_and_key(trails, selected)


if __name__ == "__main__":
    main()
