# Workflow: Reducing Cognitive Load & Focusing Attention

## Prerequisites & Context
- **Why and When**: Every element added to a visual communication increases the audience's cognitive load (the mental effort required to learn new information). Minimizing extraneous cognitive load is crucial to prevent the audience from abandoning the visualization. Once clutter is removed, you must then strategically focus the audience's attention using memory and visual perception cues.
- **Deep Dive Theory**: For the full theoretical context on cognitive load and the signal-to-noise ratio, run:
  `bash scripts/query_theory.sh "Explain cognitive load and data-ink ratio in visual design"`
  For details on human memory (Iconic, Short-term, Long-term), run:
  `bash scripts/query_theory.sh "How do iconic, short-term, and long-term memory affect visual processing?"`

## Comprehensive Guide & Best Practices

### 1. Identify and Maximize Signal-to-Noise Ratio
- Assess the perceived cognitive load. How hard will your audience believe they have to work to understand the graphic?
- Maximize the data-ink ratio: The larger the share of a graphic's ink devoted to data, the better.
- Remove elements that take up space but do not increase understanding (clutter).

### 2. Apply Gestalt Principles of Visual Perception
Use these principles to identify noise and structure signal:
- **Proximity**: Group related items physically close together (e.g., to create columns or rows naturally, see `../../images/Image00041.jpg`).
- **Similarity**: Use similar color, shape, size, or orientation to relate objects (e.g., using color to draw eyes across rows, see `../../images/Image00043.jpg`).
- **Enclosure**: Use light background shading to group items and visually separate them (e.g., separating forecast from actual data, see `../../images/Image00045.jpg`).
- **Closure**: Remove unnecessary borders and backgrounds. The audience's eyes will fill in the gaps (`../../images/Image00047.jpg`).
- **Continuity**: Align elements and use consistent white space to remove unnecessary lines (e.g., removing the y-axis line entirely, see `../../images/Image00049.jpg`).
- **Connection**: Connect related items with lines (e.g., line graphs, see `../../images/Image00051.jpg`). This often creates a stronger associative value than color, size, or shape.
- **Theory Check**: `bash scripts/query_theory.sh "What are the Gestalt Principles of Visual Perception?"`

### 3. Establish Visual Order
- **Alignment**:
  - Avoid center-aligned text. It creates jagged edges.
  - Left-justify or right-justify text to create clean horizontal and vertical lines.
  - Upper-left-most justify the text (title, axis titles, legend) so the audience hits the instructions before the data.
  - Turn on rulers/gridlines in presentation software to precisely align elements.
- **Avoid Diagonal Components**:
  - Never use diagonal lines or diagonally oriented text (e.g., x-axis labels). They look messy and are hard to read.
- **White Space**:
  - Do not fear white space. Treat it like a dramatic pause in public speaking.
  - Keep margins free of text and visuals. Do not stretch visuals to fill space.
  - Use white space strategically for emphasis.

### 4. Step-by-Step Decluttering Process
Execute these six steps to declutter any graph (refer to the transformation leading to `../../images/Image00063.jpg`):
1. **Remove chart borders**: They are usually unnecessary (Gestalt principle of closure).
2. **Remove gridlines**: If needed, make them thin and light grey. Ideally, get rid of them completely to let data stand out.
3. **Remove data markers**: Do not use them by default. Only add them with a specific purpose.
4. **Clean up axis labels**: Remove trailing zeros (e.g., change `10.0` to `10`). Abbreviate categories (like months) to fit horizontally and avoid diagonal text.
5. **Label data directly**: Leverage proximity to put labels right next to the data they describe, eliminating the need for a separate legend.
6. **Leverage consistent color**: Leverage similarity by matching the data label color to the data line/bar color.

### 5. Direct Attention with Preattentive Attributes
Once clutter is removed, use preattentive attributes (color, size, position, shape) to encode quantitative data and direct focus. These attributes tap into iconic memory, allowing audiences to process information before conscious thought occurs.
- **Use Sparingly**: If everything is highlighted, nothing stands out. Use contrast to highlight the "hawk" in a sky full of "pigeons".
- **Visual Hierarchy**: Use preattentive attributes to create a clear visual hierarchy. Push non-essential items to the background (e.g., by making them grey) and emphasize the primary takeaway with bolder colors or larger size (e.g., `../../images/Image00072.jpg`).
- **Data Labels for Emphasis**: Add data markers and numeric labels *only* to the specific points you want to highlight, rather than cluttering every point (e.g., `../../images/Image00077.jpg`).
- **Theory Check**: `bash scripts/query_theory.sh "How to use preattentive attributes strategically in visual design?"`

## If/Then Troubleshooting Logic
- **If** there are negative values in a scatterplot that complicate reading... **Then** consider changing the chart type to a horizontal bar chart and rescaling to focus on relative differences.
- **If** the x-axis labels are too long and overlap horizontally... **Then** abbreviate the words or rotate the chart 90 degrees (e.g., from vertical columns to horizontal bars) instead of making the labels diagonal.
- **If** the audience needs to trace their finger to an exact axis value... **Then** keep the gridlines, but make them very thin and light grey so they don't compete with the data.
- **If** you have multiple categories to display and the legend is hard to read... **Then** label the data directly at the end of the lines/bars and color-match the text to the data series.
- **If** you have empty space on a slide... **Then** leave it empty! Do not add data just for the sake of adding data.
- **If** you highlight one aspect and it obscures another important point... **Then** consider creating multiple iterations of the same visual, emphasizing different pieces sequentially to tell a complete story without visual conflict.

## Verification Checklists

### Pre-Flight Checklist
- [ ] Are all elements on the page adding informative value?
- [ ] Is the data-ink ratio maximized?
- [ ] Have you evaluated the perceived cognitive load from a fresh perspective?
- [ ] Are redundant details removed (except mandatory ones like $, %, and commas in large numbers)?

### Decluttering Checklist
- [ ] Chart border removed?
- [ ] Gridlines removed or faded to light grey?
- [ ] Unnecessary data markers removed?
- [ ] Axis labels cleaned up (no trailing zeros, no diagonal text)?
- [ ] Data labeled directly (legend removed)?
- [ ] Colors consistent between data and labels?

### Design & Layout Checklist
- [ ] All text is left- or right-justified (no center alignment)?
- [ ] Titles and legends upper-left-most justified?
- [ ] No diagonal components present?
- [ ] Margins are clear, and white space is used effectively for emphasis?
- [ ] Strategic use of preattentive attributes creates a clear visual hierarchy?
- [ ] The most important information is visually distinct from the rest of the elements?
