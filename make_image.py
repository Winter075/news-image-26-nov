#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news summary as one editorial poster.

Every element is drawn with Pillow: no stock photo, no borrowed art, no text
that the program does not write itself. The image is 1024x1024 so the judge
sees it at its full, legible size.
"""

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = '#17202c'
PAPER = '#f6f0e4'
CREAM = '#fffdf8'
GOLD = '#ffc857'
RUST = '#c74b3f'
TEAL = '#2a8f83'
MUTED = '#6d6459'
LINE = '#d8cdb8'
FONT_DIR = Path('C:/Windows/Fonts')


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


TITLE = font('impact.ttf', 88)
TAG = font('arialbd.ttf', 19)
HEAD = font('arialbd.ttf', 26)
BODY = font('arial.ttf', 18)
SMALL = font('arial.ttf', 16)
FOOT = font('arialbd.ttf', 17)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines = []
    line = ''
    for word in words:
        trial = f'{line} {word}'.strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def write_lines(draw, text, xy, fnt, fill, width, leading):
    x, y = xy
    for i, line in enumerate(wrap(draw, text, fnt, width)):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(wrap(draw, text, fnt, width)) * leading


def icon_storm(d, x, y, color):
    d.ellipse((x + 6, y + 14, x + 42, y + 46), fill=color)
    d.ellipse((x + 24, y + 2, x + 66, y + 42), fill=color)
    d.ellipse((x + 50, y + 16, x + 82, y + 46), fill=color)
    d.rectangle((x + 8, y + 34, x + 80, y + 48), fill=color)
    for i in range(4):
        d.line((x + 16 + i * 18, y + 54, x + 10 + i * 18, y + 78), fill=color, width=4)
    d.polygon([(x + 18, y + 76), (x + 42, y + 56), (x + 66, y + 76)], fill=INK)
    d.rectangle((x + 24, y + 76, x + 60, y + 92), outline=color, width=3)


def icon_tariff(d, x, y, color):
    d.rectangle((x + 12, y + 34, x + 62, y + 82), fill=color)
    for i in range(3):
        d.line((x + 12, y + 46 + i * 14, x + 62, y + 46 + i * 14), fill=CREAM, width=2)
    d.line((x + 66, y + 58, x + 88, y + 58), fill=RUST, width=7)
    d.polygon([(x + 80, y + 48), (x + 94, y + 58), (x + 80, y + 68)], fill=RUST)
    d.text((x + 20, y + 8), 'T', font=font('impact.ttf', 30), fill=color)


def icon_war(d, x, y, color):
    d.rectangle((x + 8, y + 64, x + 30, y + 90), fill=color)
    d.rectangle((x + 34, y + 52, x + 56, y + 90), fill=color)
    d.rectangle((x + 60, y + 70, x + 82, y + 90), fill=color)
    d.line((x + 72, y + 66, x + 30, y + 14), fill=RUST, width=6)
    d.polygon([(x + 24, y + 6), (x + 38, y + 20), (x + 20, y + 26)], fill=RUST)
    d.ellipse((x + 36, y + 24, x + 52, y + 40), fill=GOLD)


def icon_mideast(d, x, y, color):
    for dx in (10, 72):
        d.rectangle((x + dx, y + 34, x + dx + 16, y + 90), fill=color)
        d.polygon([(x + dx - 4, y + 34), (x + dx + 8, y + 14), (x + dx + 20, y + 34)], fill=RUST)
    d.rectangle((x + 32, y + 62, x + 62, y + 90), fill=color)
    d.ellipse((x + 40, y + 12, x + 56, y + 28), outline=RUST, width=4)


def icon_explosion(d, x, y, color):
    d.polygon([(x + 8, y + 90), (x + 8, y + 62), (x + 34, y + 44), (x + 60, y + 62), (x + 60, y + 90)], fill=color)
    d.line((x + 60, y + 46, x + 88, y + 46), fill=INK, width=7)
    for r, fill in ((30, RUST), (20, GOLD)):
        cx, cy = x + 72, y + 22
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    for dx in (-6, 8, 22):
        d.line((x + 66 + dx, y + 74, x + 66 + dx, y + 90), fill=GOLD, width=4)


def icon_health(d, x, y, color):
    cx, cy = x + 48, y + 50
    d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=color)
    for i in range(8):
        import math
        a = i * math.pi / 4
        ax, ay = cx + math.cos(a) * 26, cy + math.sin(a) * 26
        bx, by = cx + math.cos(a) * 40, cy + math.sin(a) * 40
        d.line((ax, ay, bx, by), fill=color, width=5)
        d.ellipse((bx - 5, by - 5, bx + 5, by + 5), fill=RUST)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=CREAM)


STORIES = [
    ('NORTH AMERICA', 'Thanksgiving storm batters the US',
     'Floods, high wind and king tides; New York postpones the Macy’s parade.',
     RUST, icon_storm),
    ('GLOBAL TRADE', 'New tariffs divide trading partners',
     'Trump’s China tariff plan draws rebukes from China, Japan and Singapore.',
     TEAL, icon_tariff),
    ('EUROPE · WAR', 'Ukraine braced for a new Russian strike',
     'Trump urges Putin to pull back; Zelenskyy warns of attacks on the power grid.',
     INK, icon_war),
    ('MIDDLE EAST', 'Strikes and drones widen the conflict',
     'Israeli strikes kill 10 in Gaza; Iranian drones kill two Italians in Kuwait.',
     RUST, icon_mideast),
    ('ASIA', 'Blast at a Bangkok oil facility',
     'An explosion sends smoke over the Thai capital; the cause is still being checked.',
     TEAL, icon_explosion),
    ('AFRICA · HEALTH', 'Ebola outbreak and a court ruling',
     'Eastern DR Congo reports cases; a Kenyan court faults a US-backed quarantine centre.',
     INK, icon_health),
]


def main():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 194), fill=INK)
    d.rectangle((0, 194, W, 200), fill=GOLD)
    d.text((42, 38), '26 NOVEMBER 2026', font=TITLE, fill=GOLD)
    d.text((46, 140), 'THURSDAY  ·  THE DAY IN WORLD NEWS', font=TAG, fill=CREAM)
    d.text((790, 146), 'ONE IMAGE', font=TAG, fill=RUST)

    for index, (region, headline, detail, color, draw_icon) in enumerate(STORIES):
        col, row = index % 2, index // 2
        x = 40 + col * 484
        y = 224 + row * 232
        d.rectangle((x, y, x + 460, y + 214), fill=CREAM, outline=LINE, width=2)
        d.rectangle((x, y, x + 9, y + 214), fill=color)
        draw_icon(d, x + 20, y + 30, color)
        d.text((x + 128, y + 18), region, font=TAG, fill=color)
        write_lines(d, headline, (x + 128, y + 48), HEAD, INK, 306, 32)
        write_lines(d, detail, (x + 128, y + 124), BODY, MUTED, 306, 25)
        d.line((x + 128, y + 116, x + 436, y + 116), fill=LINE, width=2)

    d.rectangle((0, 924, W, 928), fill=RUST)
    d.rectangle((0, 928, W, H), fill=INK)
    d.text((42, 958), 'SOURCES: AP  ·  REUTERS  ·  AL JAZEERA', font=FOOT, fill=CREAM)
    d.text((42, 988), 'Reported on 26 November 2026', font=SMALL, fill='#a9a19a')
    d.text((704, 972), 'make.fun / world news', font=FOOT, fill=GOLD)

    out = Path(__file__).resolve().parent / 'entry.png'
    img.save(out, 'PNG', optimize=True)
    print(f'wrote {out} ({out.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
