
import json
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

USERNAME = "DuskForged-Coder"
OUTPUT = "dist/project-train.gif"

WIDTH, HEIGHT = 1100, 64
BACKGROUND = "#08131F"
CYAN = "#00BFFF"
TEXT_COLOR = "#C8CDD5"

os.makedirs("dist", exist_ok=True)

url = (
    f"https://api.github.com/users/{USERNAME}/repos"
    "?type=owner&sort=created&direction=desc&per_page=100"
)

request = urllib.request.Request(
    url,
    headers={"Accept": "application/vnd.github+json",
             "User-Agent": "GitHub-Project-Ticker"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    repos = json.loads(response.read().decode("utf-8"))

projects = [
    repo["name"]
    for repo in repos
    if not repo.get("fork")
    and not repo.get("archived")
    and repo["name"].lower() != USERNAME.lower()
]

if not projects:
    projects = ["NO PUBLIC PROJECTS FOUND"]

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20
)

ticker = "   ◆   ".join(projects)
ticker = f"  LATEST PROJECTS   ◆   {ticker}   ◆   "

probe = Image.new("RGB", (1, 1))
draw = ImageDraw.Draw(probe)
text_width = int(draw.textlength(ticker, font=font))

# Repeat the ticker enough to fill the scrolling canvas.
full_text = ticker * (WIDTH // max(text_width, 1) + 3)
full_width = int(draw.textlength(full_text, font=font))

frames = []
for offset in range(0, max(text_width, 1), 5):
    frame = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    frame_draw = ImageDraw.Draw(frame)

    frame_draw.rectangle((0, 0, WIDTH, 2), fill=CYAN)
    frame_draw.rectangle((0, HEIGHT - 2, WIDTH, HEIGHT), fill=CYAN)
    frame_draw.text(
        (-offset, 19), full_text, font=font, fill=TEXT_COLOR
    )

    frames.append(frame)

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=45,
    loop=0,
    optimize=True
)

print(f"Ticker generated: {OUTPUT}")
print(f"Projects included: {len(projects)}")
print(", ".join(projects))
