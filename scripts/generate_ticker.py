import json
import math
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

USERNAME = "DuskForged-Coder"
WIDTH = 1100
HEIGHT = 64
FRAME_COUNT = 60

# Fetch your newest public repositories from GitHub
url = (
    f"https://api.github.com/users/{USERNAME}/repos"
    "?type=owner&sort=created&direction=desc&per_page=100"
)

request = urllib.request.Request(
    url,
    headers={"User-Agent": "GitHub-Project-Ticker"}
)

with urllib.request.urlopen(request) as response:
    repositories = json.loads(response.read())

# Exclude forks, archived repositories and the profile README repository
projects = [
    repo["name"]
    for repo in repositories
    if not repo["fork"]
    and not repo["archived"]
    and repo["name"] != USERNAME
]

if not projects:
    projects = ["More projects coming soon"]

label = "LATEST PROJECTS  ◆  "
ticker = label + "  ◆  ".join(projects) + "  ◆  "

# Font
try:
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 21
    )
except OSError:
    font = ImageFont.load_default()

# Calculate scrolling width
temp = Image.new("RGB", (10, 10))
draw = ImageDraw.Draw(temp)
text_width = draw.textbbox((0, 0), ticker, font=font)[2]

repeat_count = max(3, math.ceil(WIDTH / max(text_width, 1)) + 2)
full_text = ticker * repeat_count

frames = []

for frame_number in range(FRAME_COUNT):
    image = Image.new("RGB", (WIDTH, HEIGHT), "#08131F")
    draw = ImageDraw.Draw(image)

    offset = int((text_width * frame_number) / FRAME_COUNT)
    x = -(offset)

    draw.rectangle((0, 0, WIDTH, 3), fill="#00BFFF")
    draw.rectangle((0, HEIGHT - 3, WIDTH, HEIGHT), fill="#00BFFF")

    draw.text(
        (x, 19),
        full_text,
        font=font,
        fill="#00BFFF"
    )

    frames.append(image)

os.makedirs("dist", exist_ok=True)

frames[0].save(
    "dist/project-train.gif",
    save_all=True,
    append_images=frames[1:],
    duration=75,
    loop=0,
    optimize=True
)

print(f"Generated ticker containing {len(projects)} repositories.")
print("Projects:", ", ".join(projects))
