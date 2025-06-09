import json
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any


class KeyboardLayoutRenderer:
    def __init__(self, layout_json: List[List[Any]], key_unit: int = 60, padding: int = 10, font_path: str = None):
        self.layout_json = layout_json
        self.key_unit = key_unit
        self.padding = padding
        self.font = ImageFont.truetype(font_path, 14) if font_path else ImageFont.load_default()
        self.keys = self._parse_layout()

    def _parse_layout(self) -> List[Dict[str, Any]]:
        keys = []
        y_cursor = 0

        for row in self.layout_json:
            x_cursor = 0
            state = {"x": 0, "y": 0, "w": 1, "h": 1}

            for item in row:
                if isinstance(item, dict):
                    state.update(item)
                    continue

                # Apply x and y offsets
                x_cursor += state.get("x", 0)
                y_offset = state.get("y", 0)

                key = {
                    "label": item,
                    "x": x_cursor,
                    "y": y_cursor + y_offset,
                    "w": state.get("w", 1),
                    "h": state.get("h", 1),
                }
                keys.append(key)

                # Move cursor to next position
                x_cursor += state.get("w", 1)

                # Reset x/y/w/h for next key (KLE behavior)
                state = {"x": 0, "y": 0, "w": 1, "h": 1}

            y_cursor += 1

        return keys


    def render_to_image(self, output_path: str = "rendered_keyboard.png"):
        max_x = max((k["x"] + k["w"]) for k in self.keys)
        max_y = max((k["y"] + k["h"]) for k in self.keys)
        width = int((max_x + 1) * self.key_unit + 2 * self.padding)
        height = int((max_y + 1) * self.key_unit + 2 * self.padding)

        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        for key in self.keys:
            x = int(self.padding + key["x"] * self.key_unit)
            y = int(self.padding + key["y"] * self.key_unit)
            w = int(key["w"] * self.key_unit)
            h = int(key["h"] * self.key_unit)
            draw.rectangle([x, y, x + w, y + h], outline="black", width=2, fill="#e0e0e0")
            label = key["label"]
            if label:
                lines = label.split("\n")
                text = "\n".join(lines)
                tw, th = draw.multiline_textbbox((0, 0), text, font=self.font)[2:]
                tx = x + (w - tw) / 2
                ty = y + (h - th) / 2
                draw.multiline_text((tx, ty), text, font=self.font, fill="black", align="center")

        img.save(output_path)
        print(f"Keyboard image saved to '{output_path}'")
