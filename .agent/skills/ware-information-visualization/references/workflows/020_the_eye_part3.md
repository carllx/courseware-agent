# Visual Resolution, Contrast, and Surface Lightness

## 1. Prerequisites & Context
**Why & When to use this workflow:**
This workflow focuses on the physiological limits of the eye (resolution, acuity) and the brain's mechanism for interpreting lightness and contrast. Use these heuristics when determining display specifications (resolution, size) and designing color palettes, grayscales, and contrast ratios for maximum legibility.

*For deeper theoretical dives, use:*
```bash
bash scripts/query_theory.sh "What defines an optimal display in terms of human visual acuity and resolution?"
bash scripts/query_theory.sh "How do neurons and receptive fields create brightness illusions like lateral inhibition?"
bash scripts/query_theory.sh "Explain the difference between Luminance, Brightness, and Lightness, and the role of Gamma correction."
```

## 2. Comprehensive Guide & Best Practices

### A. Design for the Limits of Visual Acuity
- **Snellen Acuity & Spatial Frequency**: The human eye can resolve details up to a specific spatial frequency. Text and fine lines must exceed this threshold (usually around 30 cycles per degree) to be readable.
- **The Optimal Display**: A "perfect" display only needs to match the maximum acuity of the fovea (roughly 300 pixels per inch at standard viewing distances). Pushing resolution far beyond this yields diminishing returns.
- *Heuristic*: When designing for large screens or varied distances, calculate the subtended visual angle of your critical data elements. Ensure they are large enough to be resolved by the fovea.

### B. Master Luminance, Brightness, and Lightness
- **Luminance**: The physical measure of light.
- **Brightness**: The perceived amount of light.
- **Lightness**: The perceived reflectance of a surface (how "white" or "black" a surface appears relative to its environment).
- **Gamma Correction**: Display monitors have nonlinear responses to voltage (Gamma). Ensure your data mappings (e.g., a grayscale heat map) are perceptually linear, which usually requires gamma correction so that a data value of 50% visually appears exactly halfway between black and white.

### C. Exploit and Mitigate Contrast Effects
- **Receptive Fields & Lateral Inhibition**: The eye's neurons process light via center-surround receptive fields. This enhances edges but causes *simultaneous contrast illusions* (e.g., a gray square looks darker on a white background and lighter on a black background).
- **Designing Grayscales**: Never use a simple grayscale map to encode absolute quantitative data across a complex background, as lateral inhibition will severely distort the perceived values.
- *Heuristic*: Use strong luminance contrast to define edges and shapes. To encode data values robustly, use perceptually uniform color spaces or spatial position rather than relying solely on grayscale shading.

### D. Perception of Surface Lightness
- The brain achieves **lightness constancy** by discounting the illuminant. We perceive a white piece of paper as white whether it's in bright sunlight or a dim room.
- In 3D visualizations, use realistic shading, cast shadows, and specular highlights to help the brain understand the geometry of data objects. The brain is highly adept at calculating surface lightness when environmental lighting cues are present.

## 3. If/Then Troubleshooting Logic
- **IF** data points encoded using a grayscale colormap appear distorted or users misread their values... **THEN** the simultaneous contrast illusion is occurring. Switch to a perceptually uniform sequential colormap (e.g., Viridis or Magma) or add a constant background behind the data points.
- **IF** users struggle to read fine text or thin lines... **THEN** verify the contrast ratio. Ensure you have high luminance contrast (not just color difference) between the text and the background.
- **IF** a visualization looks washed out or overly dark on a specific monitor... **THEN** check the gamma correction. Ensure the software is rendering perceptually linear steps that account for the display's gamma curve.

## 4. Verification Checklists
- [ ] Are critical visual details appropriately sized for the viewing distance and display resolution?
- [ ] Is the data mapping perceptually linear (has gamma correction been considered)?
- [ ] Have you checked for simultaneous contrast illusions if using lightness to encode quantitative data?
- [ ] Is there sufficient luminance contrast at the edges of shapes and text?
- [ ] For 3D representations, are lighting models (shadows, shading) consistent to support lightness constancy?