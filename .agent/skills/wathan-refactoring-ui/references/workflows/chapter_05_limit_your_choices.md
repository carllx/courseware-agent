# Workflow: Structuring UI through Constraints and Hierarchy

## Prerequisites & Context

Before applying visual styling to an interface, it is crucial to establish foundational systems and understand the principles of visual hierarchy. Designing without constraints—where every color value or pixel dimension is chosen arbitrarily—leads to decision fatigue, inconsistent interfaces, and ultimately poor user experiences. This workflow focuses on limiting design choices up front and deliberately managing visual importance (hierarchy) through size, weight, color, and context.

**When to use this workflow:**
- You are starting a new design and need to define initial styling rules (color palettes, typography scales).
- You are refining an existing interface that feels chaotic, noisy, or lacking in structural organization.
- You are struggling with low-level design decisions (e.g., specific pixel values or shades of color) and need a reliable heuristic to break the paralysis.

**Deep Dive Context (Runtime Agent Instructions):**
If you need the underlying theoretical rationale for these principles, invoke the query script:
```bash
bash scripts/query_theory.sh "Why is establishing a constrained system critical for UI design and reducing decision fatigue?"
bash scripts/query_theory.sh "How does visual hierarchy affect user perception, and why is relying solely on size insufficient?"
```

---

## Comprehensive Guide & Best Practices

### 1. Limit Your Choices & Define Systems
Instead of picking arbitrary values on the fly, build a constrained set of options in advance to streamline decision-making.

- **Pre-define a scale:** Create systems for font sizes, font weights, line heights, colors, margins, padding, widths, heights, box shadows, border radii, border widths, and opacity.
- **Design by process of elimination:** When choosing a size or spacing, test an option and the values immediately above and below it in your defined scale. 
  - *Heuristic:* If the outer options look obviously wrong, your middle choice is correct.
- **Avoid pixel-tweaking:** Never guess between similar values (e.g., 120px vs. 125px). Stick strictly to your predefined scale.

*Visual Example: Comparing Arbitrary vs. Constrained Selections*
![](../../images/index-29_1.png)
![](../../images/index-29_2.png)

*Deep Dive Context:*
```bash
bash scripts/query_theory.sh "What are the recommended values and intervals for building a baseline spacing and sizing system?"
```

### 2. Establish Visual Hierarchy
Not all elements are equal. When everything competes for attention, the UI becomes chaotic and overwhelming. 

- **De-emphasize secondary info:** Deliberately push secondary and tertiary information into the background to allow primary elements to stand out.
  ![](../../images/index-37_1.png) (Chaotic UI)
  ![](../../images/index-38_1.png) (Hierarchical UI)
- **Don't rely solely on size:** Font size is not the only tool for hierarchy. Use **font weight** or **color** to communicate importance.
  - *Example:* A heavier font weight (600 or 700) emphasizes text better than simply making it larger.
  - *Example:* A softer color (grey) de-emphasizes supporting text without sacrificing readability by making the font tiny.
  ![](../../images/index-39_1.png)
  ![](../../images/index-40_1.png)
- **Emphasize by de-emphasizing:** If an active element isn't standing out, don't make it bolder or larger. Instead, de-emphasize the elements competing with it (e.g., soften the colors of inactive elements or remove background colors from competing sidebars).
  ![](../../images/index-47_1.png)
  ![](../../images/index-48_1.png)

### 3. Handle Color and Contrast Carefully
Using the right color contrast is essential for maintaining hierarchy without washing out the design.

- **Three-tier color approach:** 
  1. A dark color for primary content (e.g., article titles).
  2. A grey for secondary content (e.g., publishing dates).
  3. A lighter grey for tertiary content (e.g., footer copyrights).
- **Colored Backgrounds:** **Never use grey text on colored backgrounds.** Grey text works on white by reducing contrast. On colored backgrounds, reducing opacity or using grey looks dull, washed out, or even disabled. 
  - *Actionable Fix:* Hand-pick a new color with the same hue as the background, adjusting saturation and lightness to reduce contrast naturally. 

*Visual Example: Adjusting Contrast on Colored Backgrounds*
![](../../images/index-43_1.png) (Incorrect)
![](../../images/index-46_1.png) (Correct)

### 4. Re-evaluating Labels
Traditional *label: value* formatting flattens hierarchy and gives every piece of data equal emphasis. Treat labels as a last resort.

- **Remove labels when possible:** Use formatting (e.g., `janedoe@example.com` or `$19.99`) or context (e.g., "Customer Support" under a person's name) to implicitly explain data.
  ![](../../images/index-49_1.png)
- **Combine labels and values:** Instead of displaying `In stock: 12`, use `12 left in stock`. This allows for meaningful styling as a single unit.
  ![](../../images/index-50_1.png)
- **De-emphasize necessary labels:** When labels are absolutely required (like on dense dashboards to ensure scannability), treat them as supporting content. Make them smaller, lighter, or lower contrast than the actual data.
  ![](../../images/index-51_1.png)
- *Exception:* If the user is specifically *searching* for the label (e.g., finding the "depth" in a technical spec sheet), emphasize the label and slightly de-emphasize the value.

### 5. Separate Visual Hierarchy from Document Hierarchy
Do not let semantic HTML elements dictate your visual styling.

- **Semantic tags are secondary for styling:** An `<h1>` tag does not have to be massive. Section titles often act as structural labels and should be styled as supporting content.
- **Prioritize the content:** The content within a section should be the primary visual focus, not the title. 
- **Accessibility vs. Visuals:** In extreme cases, you might include a section title in the markup for screen readers but completely hide it visually because the content naturally speaks for itself.
  ![](../../images/index-55_1.png)

---

## If/Then Troubleshooting Logic

- **IF** you are paralyzed by choosing a color or padding value, **THEN** you are not using a constrained system. Stop, define a small set of predefined options (e.g., 8-10 shades of blue, a specific type scale), and choose strictly from that list.
- **IF** an important active element isn't standing out enough, **THEN** do not add more visual weight to it. Find the adjacent elements competing with it and de-emphasize them by softening their color or reducing their contrast.
- **IF** text on a colored background looks disabled or washed out, **THEN** you are likely using grey text or reducing opacity. Switch to a hand-picked, low-contrast color within the same hue family as the background.
- **IF** a data-heavy page looks cluttered and lacks hierarchy, **THEN** you are over-relying on naive label:value formats. Remove unnecessary labels, combine labels with values, or significantly de-emphasize the labels so the actual data draws the eye.
- **IF** your headers look overwhelmingly large but you must use `h1`/`h2` for SEO/Accessibility, **THEN** decouple your CSS styling from the semantic tag. Size the header based on its actual visual role (e.g., as a subtle section label), not browser defaults.

---

## Verification Checklists

### Pre-Design System Check
- [ ] Have you defined a constrained system for colors (e.g., 8-10 specific shades per primary color)?
- [ ] Is there a defined type scale for font sizes and line heights?
- [ ] Have you established a spacing scale (for margins, padding, and element sizing)?

### Visual Hierarchy Check
- [ ] Is the primary action/content the most obvious element on the screen?
- [ ] Are secondary and tertiary elements clearly de-emphasized using softer colors or lighter weights?
- [ ] Have you avoided relying entirely on font size to establish hierarchy?
- [ ] Are competing elements actively softened to allow primary elements to shine?

### Contrast & Data Styling Check
- [ ] Is text on colored backgrounds derived from the background hue rather than using raw grey/opacity?
- [ ] Are semantic tags (like `<h1>`) styled appropriately for their visual context, rather than relying on default browser sizing?
- [ ] Are data labels removed, combined with their values, or visually de-emphasized where possible?
