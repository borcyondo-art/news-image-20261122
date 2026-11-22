#!/usr/bin/env python3
"""News image for Sunday 22 November 2026.

Draws one 1024x1024 PNG procedurally with the Python standard library
only: flat geometric shapes plus a small 5x7 bitmap font defined below.
No network, no external files, no randomness. Two runs write
byte-identical files.

Stories (all reported in the news cycle of 22 November 2026; see
README.md for sources and dates):
  lead  COP31 climate talks in Antalya still without a deal, in overtime
  1     Ukraine: local ceasefire proposal to evacuate civilians
  2     Yemen: strikes on Hodeidah port, UN aid-lifeline warning
  3     EU: proposed long-term budget EUR 204bn below the plan
  4     France: sixth Saturday of cost-of-living protests
  5     Sport: Australia beat England in the T20 opener at the MCG
"""
import os
import struct
import zlib

W, H = 1024, 1024

# --- palette ---
PAPER = (246, 241, 227)
WHITE = (255, 255, 255)
INK = (22, 35, 63)
NAVY = (22, 35, 63)
NAVY2 = (30, 48, 84)
TEAL = (14, 124, 123)
TEAL_D = (9, 92, 91)
RED = (192, 57, 43)
RED_D = (150, 40, 30)
AMBER = (232, 160, 32)
AMBER_L = (250, 205, 110)
SKY = (168, 208, 230)
SKY_L = (220, 233, 242)
GREEN = (62, 124, 79)
GREEN_L = (140, 190, 140)
BLUE = (52, 110, 170)
SAND = (233, 220, 180)
GREY = (110, 116, 128)
GREY_L = (210, 208, 198)
YELLOW = (245, 205, 48)
BROWN = (120, 82, 50)

# --- 5x7 bitmap font (glyphs drawn for this entry) ---
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def line(self, x0, y0, x1, y1, c, th=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            self.rect(x - th // 2, y - th // 2, th, th, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, th=3):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - th) ** 2 <= d2 <= r * r:
                    self.set(xx, yy, c)

    def triangle(self, p0, p1, p2, c):
        pts = (p0, p1, p2)
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            nodes = []
            for i in range(3):
                a, b = pts[i], pts[(i + 1) % 3]
                if (a[1] <= yy < b[1]) or (b[1] <= yy < a[1]):
                    t = (yy - a[1]) / (b[1] - a[1])
                    nodes.append(a[0] + t * (b[0] - a[0]))
            nodes.sort()
            for k in range(0, len(nodes) - 1, 2):
                for xx in range(int(nodes[k]), int(nodes[k + 1]) + 1):
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s.upper():
            g = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def ctext(self, cx, y, s, scale, c):
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, c)

    def to_png(self):
        raw = b''.join(b'\x00' + bytes(self.px[y * self.w * 3:(y + 1) * self.w * 3])
                       for y in range(self.h))
        comp = zlib.compress(raw, 9)

        def chunk(kind, data):
            out = struct.pack('>I', len(data)) + kind + data
            out += struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
            return out

        ihdr = struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)
        return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
                + chunk(b'IDAT', comp) + chunk(b'IEND', b''))


# --- lead scene ---------------------------------------------------------
def draw_earth(cv, cx, cy, r):
    cv.circle(cx, cy, r, BLUE)
    cv.ring(cx, cy, r, NAVY, 4)
    for (lx, ly, lr) in [(cx - 40, cy - 36, 28), (cx + 28, cy - 50, 22),
                         (cx + 46, cy + 26, 24), (cx - 46, cy + 40, 20),
                         (cx + 4, cy + 56, 16)]:
        cv.circle(lx, ly, lr, GREEN)
    cv.circle(cx - 6, cy - r + 8, 13, WHITE)
    cv.circle(cx - 6, cy + r - 8, 11, WHITE)


def draw_lead(cv):
    cv.rect(0, 148, W, 364, SKY_L)
    cv.rect(0, 148, W, 6, TEAL)
    cv.rect(0, 462, W, 50, SAND)
    cv.circle(392, 216, 32, AMBER)
    cv.ring(392, 216, 38, AMBER, 3)
    for bx, bh in [(330, 116), (362, 92)]:
        cv.rect(bx, 462 - bh, 26, bh, GREY)
        cv.rect(bx - 3, 462 - bh - 8, 32, 8, INK)
    cv.circle(343, 312, 15, GREY)
    cv.circle(375, 330, 19, GREY)
    cv.circle(343, 292, 11, GREY)
    draw_earth(cv, 200, 322, 102)
    cv.circle(392, 402, 32, WHITE)
    cv.ring(392, 402, 32, INK, 4)
    cv.line(392, 402, 392, 380, INK, 4)
    cv.line(392, 402, 410, 402, INK, 4)
    cv.rect(56, 188, 288, 50, RED)
    cv.ctext(200, 201, "NO DEAL YET", 4, WHITE)
    cv.text(448, 172, "COP31 - ANTALYA", 3, TEAL_D)
    cv.text(448, 202, "STILL", 7, NAVY)
    cv.text(448, 254, "NO DEAL", 7, RED)
    cv.text(448, 318, "TALKS RUN INTO OVERTIME.", 3, INK)
    cv.text(448, 346, "FOSSIL FUELS AND CLIMATE", 3, INK)
    cv.text(448, 374, "CASH DIVIDE NEARLY", 3, INK)
    cv.text(448, 402, "200 NATIONS.", 3, INK)
    cv.rect(448, 440, 420, 4, AMBER)


def panel_frame(cv, x, y, w, h, tag, tag_bg):
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, 40, tag_bg)
    cv.text(x + 16, y + 9, tag, 3, WHITE)
    cv.rect(x, y + 40, w, 3, INK)


# --- compact pictograms: art zone is (ax, ay) .. (ax+300, ay+92) -------
def art_ukraine(cv, ax, ay):
    # Ukrainian flag (blue over yellow) + houses by the river
    cv.rect(ax + 14, ay + 8, 5, 76, BROWN)
    cv.rect(ax + 19, ay + 8, 78, 26, BLUE)
    cv.rect(ax + 19, ay + 34, 78, 26, YELLOW)
    cv.rect(ax + 130, ay + 58, 34, 26, SAND)
    cv.triangle((ax + 126, ay + 58), (ax + 147, ay + 38), (ax + 168, ay + 58), RED_D)
    cv.rect(ax + 190, ay + 58, 34, 26, SAND)
    cv.triangle((ax + 186, ay + 58), (ax + 207, ay + 38), (ax + 228, ay + 58), RED_D)
    cv.rect(ax + 248, ay + 58, 34, 26, SAND)
    cv.triangle((ax + 244, ay + 58), (ax + 265, ay + 38), (ax + 286, ay + 58), RED_D)
    cv.rect(ax + 8, ay + 84, 284, 8, BLUE)


def art_yemen(cv, ax, ay):
    cv.rect(ax + 16, ay + 10, 9, 66, INK)
    cv.rect(ax + 16, ay + 10, 76, 9, INK)
    cv.line(ax + 25, ay + 19, ax + 48, ay + 58, INK, 4)
    cv.rect(ax + 48, ay + 56, 22, 16, AMBER)
    cv.rect(ax + 118, ay + 56, 108, 24, RED_D)
    cv.rect(ax + 118, ay + 46, 108, 10, INK)
    for cx0, cc in [(124, TEAL), (154, AMBER), (184, GREEN)]:
        cv.rect(ax + cx0, ay + 18, 26, 28, cc)
    cv.rect(ax + 8, ay + 80, 284, 10, BLUE)
    cv.triangle((ax + 252, ay + 8), (ax + 274, ay + 46), (ax + 230, ay + 46), YELLOW)
    cv.text(ax + 249, ay + 20, "!", 3, INK)


def art_eu(cv, ax, ay):
    base = ay + 86
    for i, bh in enumerate((66, 48, 30)):
        cv.rect(ax + 22 + i * 44, base - bh, 32, bh, (TEAL, BLUE, GREY)[i])
    cv.line(ax + 18, ay + 8, ax + 160, ay + 44, RED, 5)
    cv.triangle((ax + 160, ay + 44), (ax + 140, ay + 34), (ax + 144, ay + 56), RED)
    cv.circle(ax + 226, ay + 42, 32, AMBER)
    cv.ring(ax + 226, ay + 42, 32, AMBER_L, 3)
    cv.ctext(ax + 226, ay + 30, "EUR", 3, INK)


def art_france(cv, ax, ay, wide=True):
    for i, px in enumerate((30, 84, 138)):
        cv.circle(ax + px, ay + 40, 17, INK if i % 2 == 0 else BROWN)
        cv.rect(ax + px - 20, ay + 58, 40, 30, YELLOW if i % 2 == 0 else GREY_L)
    cv.rect(ax + 236, ay + 6, 5, 58, BROWN)
    cv.rect(ax + 196, ay + 6, 72, 32, WHITE)
    cv.text(ax + 204, ay + 13, "FAIR", 3, RED)


def art_sport(cv, ax, ay):
    for sx in (30, 44, 58):
        cv.rect(ax + sx, ay + 30, 7, 52, AMBER_L)
    cv.rect(ax + 26, ay + 24, 44, 7, AMBER)
    cv.line(ax + 120, ay + 82, ax + 158, ay + 22, BROWN, 11)
    cv.line(ax + 120, ay + 82, ax + 158, ay + 22, AMBER_L, 4)
    cv.circle(ax + 212, ay + 34, 17, RED)
    cv.ring(ax + 212, ay + 34, 17, WHITE, 2)


def main():
    cv = Canvas(W, H, PAPER)
    cv.rect(0, 0, W, 148, NAVY)
    cv.rect(0, 0, W, 8, AMBER)
    cv.ctext(W // 2, 22, "WORLD NEWS IN ONE IMAGE", 3, AMBER_L)
    cv.ctext(W // 2, 56, "SUNDAY 22 NOVEMBER 2026", 6, WHITE)
    cv.rect(312, 118, 400, 4, AMBER)

    draw_lead(cv)

    gap, top, ph = 8, 520, 226
    pw = (W - 4 * gap) // 3
    row1 = [
        ("UKRAINE", TEAL, art_ukraine,
         "CEASEFIRE PLAN", ["PAUSES PROPOSED", "TO MOVE CIVILIANS"]),
        ("YEMEN", RED_D, art_yemen,
         "PORT STRIKES", ["UN WARNS AID", "LIFELINE AT RISK"]),
        ("EUROPE", BLUE, art_eu,
         "BUDGET CUT", ["204BN EUROS LESS", "FOR 2028-34"]),
    ]
    for i, (tag, bg, fn, head, sub) in enumerate(row1):
        x = gap + i * (pw + gap)
        panel_frame(cv, x, top, pw, ph, tag, bg)
        fn(cv, x + 14, top + 46)
        cv.ctext(x + pw // 2, top + 146, head, 3, INK)
        cv.ctext(x + pw // 2, top + 176, sub[0], 3, TEAL_D)
        cv.ctext(x + pw // 2, top + 200, sub[1], 3, TEAL_D)

    top2, ph2 = 754, 214
    pw2 = (W - 3 * gap) // 2
    panel_frame(cv, gap, top2, pw2, ph2, "FRANCE", NAVY2)
    art_france(cv, gap + 12, top2 + 52)
    cv.text(gap + 300, top2 + 78, "PROTESTS,", 3, INK)
    cv.text(gap + 300, top2 + 104, "WEEK 6", 3, INK)
    cv.text(gap + 300, top2 + 142, "COST OF", 3, TEAL_D)
    cv.text(gap + 300, top2 + 168, "LIVING", 3, TEAL_D)
    cv.text(gap + 300, top2 + 194, "MARCHES", 3, TEAL_D)

    x2 = 2 * gap + pw2
    panel_frame(cv, x2, top2, pw2, ph2, "SPORT", GREEN)
    art_sport(cv, x2 + 12, top2 + 52)
    cv.text(x2 + 268, top2 + 84, "AUSTRALIA", 3, INK)
    cv.text(x2 + 268, top2 + 110, "WIN T20", 3, INK)
    cv.text(x2 + 268, top2 + 148, "CHASED 188,", 3, TEAL_D)
    cv.text(x2 + 268, top2 + 174, "CHAUDHARY 66", 3, TEAL_D)

    cv.rect(0, 976, W, 48, NAVY)
    cv.ctext(W // 2, 992, "NEWS REPORTED ON 22 NOVEMBER 2026", 3, WHITE)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(cv.to_png())


if __name__ == "__main__":
    main()
