if __name__ == "__main__":
    import json
    from modules.render import KeyboardLayoutRenderer

    with open("keyboard_layouts/ANSI104-BIG-enter/QWERTY.json", encoding="utf-8") as f:
        layout_data = json.load(f)

    renderer = KeyboardLayoutRenderer(layout_data)
    renderer.render_to_image("rendered_keyboard.png")