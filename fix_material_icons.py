#!/usr/bin/env python3

from pathlib import Path
import re

docs = Path("docs")

mapping = {
    "🌳": "material/tree",
    "🎸": "material/guitar-acoustic",
    "🍳": "material/chef-hat",
    "📚": "material/book-open-page-variant",
    "📖": "material/book-open",
    "📈": "material/chart-line",
    "🎤": "material/microphone",
    "🎼": "material/music",
    "🎨": "material/palette",
    "🌈": "material/palette",
    "🌍": "material/earth",
    "🚀": "material/rocket-launch",
    "✈️": "material/airplane",
}

count = 0

for md in docs.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    original = text

    for old, new in mapping.items():
        text = re.sub(
            rf"^icon:\s*{re.escape(old)}\s*$",
            f"icon: {new}",
            text,
            flags=re.MULTILINE,
        )

    if text != original:
        md.write_text(text, encoding="utf-8")
        count += 1
        print(f"✔ {md}")

print(f"\nGewijzigde bestanden: {count}")
