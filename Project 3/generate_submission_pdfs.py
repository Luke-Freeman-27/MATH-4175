"""Generate submission PDFs for MATH 4175 Project 3."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

S = [0x6, 0x5, 0x1, 0x0, 0x3, 0x2, 0x7, 0x4]


def nl_minus4(a: int, b: int) -> int:
    count = 0
    for i in range(8):
        if ((a & i).bit_count() + (b & S[i]).bit_count()) % 2 == 0:
            count += 1
    return count - 4


def make_lat_pdf(out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, h - 50, "MATH 4175 Project 3 - Problem 1")
    c.setFont("Helvetica", 11)
    c.drawString(50, h - 70, "Names: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki")
    c.drawString(50, h - 90, "Normalized LAT entries: NL(a,b)-4 for a,b in {0..7}")

    headers = ["a\\b"] + [str(i) for i in range(8)]
    y = h - 130
    x0 = 70
    dx = 50
    c.setFont("Courier-Bold", 11)
    for col, text in enumerate(headers):
        c.drawString(x0 + col * dx, y, f"{text:>3}")
    y -= 22
    c.setFont("Courier", 11)
    for a in range(8):
        row = [a] + [nl_minus4(a, b) for b in range(8)]
        for col, val in enumerate(row):
            c.drawString(x0 + col * dx, y, f"{val:>3}")
        y -= 20

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 70, "Generated automatically from project S-box.")
    c.save()


def make_trail_pdf(out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, h - 50, "MATH 4175 Project 3 - Problem 2 Trail Sketch")
    c.setFont("Helvetica", 11)
    c.drawString(50, h - 70, "Names: Luke Freeman, Yoshwan Pathipati, Diego Penadillo, Hiren Sai Vellanki")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, h - 105, "Chosen linear trail (mask summary):")
    c.setFont("Helvetica", 10)
    lines = [
        "Start plaintext mask: P1 xor P2 xor P4 xor P5  -> (1,1,0,1,1,0)",
        "Round 1: S11 uses a=6->b=4, S12 uses a=6->b=4  (NL=-4 each)",
        "After permutation: B=(1,0,0,1,0,0) -> E=(1,0,0,0,1,0)",
        "Round 2: S21 uses a=4->b=2 (NL=+2), S22 uses a=2->b=2 (NL=-2)",
        "After permutation: F=(0,1,0,0,1,0) -> G=(0,0,1,1,0,0)",
        "Total bias in write-up: epsilon_total = -1/8",
    ]
    y = h - 125
    for line in lines:
        c.drawString(60, y, f"- {line}")
        y -= 16

    # Simple SPN block sketch
    top = h - 260
    c.setFont("Helvetica-Bold", 10)
    c.drawString(55, top + 90, "P bits")
    c.drawString(180, top + 90, "Round 1 S-boxes")
    c.drawString(325, top + 90, "Permutation")
    c.drawString(440, top + 90, "Round 2 S-boxes")
    c.drawString(560, top + 90, "G/H wires")

    c.rect(170, top + 30, 110, 50)
    c.rect(430, top + 30, 110, 50)
    c.drawString(185, top + 58, "S11: 6->4")
    c.drawString(185, top + 42, "S12: 6->4")
    c.drawString(445, top + 58, "S21: 4->2")
    c.drawString(445, top + 42, "S22: 2->2")

    c.line(90, top + 55, 170, top + 55)
    c.line(280, top + 55, 340, top + 55)
    c.line(370, top + 55, 430, top + 55)
    c.line(540, top + 55, 600, top + 55)
    c.drawString(345, top + 58, "perm")

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 75, "Attach this with your final typed report PDF.")
    c.drawString(50, 62, "If your instructor wants a hand-drawn version, redraw this same trail and export to PDF.")
    c.save()


def make_report_pdf(source_txt: Path, out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=letter)
    w, h = letter
    c.setFont("Helvetica", 10)
    y = h - 50
    for raw in source_txt.read_text(encoding="utf-8").splitlines():
        line = raw.expandtabs(4)
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = h - 50
        # soft-wrap long lines
        while len(line) > 105:
            c.drawString(40, y, line[:105])
            line = line[105:]
            y -= 13
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = h - 50
        c.drawString(40, y, line)
        y -= 13
    c.save()


def make_code_pdf(py_files: list[Path], out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=letter)
    w, h = letter
    c.setFont("Courier", 8)
    y = h - 40
    for py_file in py_files:
        header = f"===== {py_file.name} ====="
        if y < 60:
            c.showPage()
            c.setFont("Courier", 8)
            y = h - 40
        c.drawString(30, y, header)
        y -= 12
        for idx, raw in enumerate(py_file.read_text(encoding="utf-8").splitlines(), start=1):
            line = f"{idx:>3}: {raw}"
            while len(line) > 130:
                if y < 40:
                    c.showPage()
                    c.setFont("Courier", 8)
                    y = h - 40
                c.drawString(30, y, line[:130])
                line = "     " + line[130:]
                y -= 10
            if y < 40:
                c.showPage()
                c.setFont("Courier", 8)
                y = h - 40
            c.drawString(30, y, line)
            y -= 10
        y -= 12
    c.save()


def main() -> None:
    root = Path(__file__).parent
    make_lat_pdf(root / "Project3_P1_LAT.pdf")
    make_trail_pdf(root / "Project3_P2_Trail.pdf")
    make_report_pdf(root / "Project3_Report.txt", root / "Project3_P3_P6_Report.pdf")
    make_code_pdf(
        [root / "NLATCalculation.py", root / "project3_complete.py"],
        root / "Project3_Code.pdf",
    )
    print("Generated PDFs:")
    print(" - Project3_P1_LAT.pdf")
    print(" - Project3_P2_Trail.pdf")
    print(" - Project3_P3_P6_Report.pdf")
    print(" - Project3_Code.pdf")


if __name__ == "__main__":
    main()
