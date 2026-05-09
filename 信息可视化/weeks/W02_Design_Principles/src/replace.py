import re
with open("M03_视觉偏差的陷阱__心理学精度与视觉弹出.md", "r", encoding="utf-8") as f:
    text = f.read()

target = """> [VISUAL]
> *   **Slide**: `S06_Visual_Popout_Failure`
> *   **Asset**: ![教材配图](../public/slides/S06_Visual_Popout_Failure.jpg)
> *   **Layout**: `Grid`"""

replacement = """> [VISUAL]
> *   **Slide**: `S06_Visual_Popout_Failure`
> *   **Asset**: ![教材配图](../public/slides/S06_Visual_Popout_Failure.jpg)
> *   **Resource**: ![Munzner Fig 5.11](../public/textbook/Fig5.11_Visual_Popout.jpg)
> *   **Source**: Textbook
> *   **Layout**: `Grid`"""

text = text.replace(target, replacement)

with open("M03_视觉偏差的陷阱__心理学精度与视觉弹出.md", "w", encoding="utf-8") as f:
    f.write(text)
