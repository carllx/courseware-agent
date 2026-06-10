# Data Typology, Environmental Optics, and the Eye

## 1. Prerequisites & Context
**Why & When to use this workflow:**
Use this workflow when categorizing data types to determine the most appropriate visual encodings, assessing the costs vs. benefits of interactive visualization, and aligning your display with the physical realities of the human eye and environmental optics.

*For deeper theoretical dives, use:*
```bash
bash scripts/query_theory.sh "What are the cognitive costs and benefits of using visualizations over raw data?"
bash scripts/query_theory.sh "How does Ware classify Types of Data and Metadata?"
bash scripts/query_theory.sh "Explain the physics of environmental optics and how the eye forms an image."
```

## 2. Comprehensive Guide & Best Practices

### A. Assess Costs and Benefits of Visualization
- **Benefits**: High bandwidth information transfer, support for pattern recognition, visual grouping, and reducing the working memory load by offloading it to the display.
- **Costs**: The time and cognitive effort to learn the visualization mapping, the computational cost of rendering, and the space cost on the screen.
- *Heuristic*: Only use a complex visualization if the pattern discovery benefits outweigh the cost of learning the visual grammar. Simple tables are better for pure lookups.

### B. Categorize Data and Metadata Correctly
- **Data Entities**: Objects you wish to visualize (e.g., people, servers, financial transactions).
- **Relationships**: The structures connecting entities (e.g., hierarchy, network, sequence).
- **Attributes/Variables**: The properties of entities. Map these according to their type:
  - *Category (Nominal)*: Use hue, shape, or texture.
  - *Ordinal*: Use ordered sequences like size, lightness, or position.
  - *Quantitative (Ratio/Interval)*: Use spatial position along an axis, or length.
- **Metadata**: Always visualize the "data about the data" (e.g., missing values, confidence intervals, or data provenance). Do not hide uncertainty.

### C. Design for Environmental Optics
- **Light and Surfaces**: Humans perceive the environment through light interacting with surfaces (Lambertian reflectance, specular highlights, cast shadows).
- Use these natural optical properties to create distinct 3D visual objects when spatial depth is required.
- **Ambient Illumination**: Ensure the visualization remains legible under various ambient lighting conditions by relying on luminance contrast rather than pure chrominance.

### D. Accommodate the Optics of the Eye
- **Acuity and the Fovea**: The eye only has high resolution at the fovea (the center of vision). The periphery is poor at detail but highly sensitive to motion.
- *Heuristic*: Place critical detailed information (text, intricate charts) centrally or ensure user gaze is directed to it. Use peripheral changes (like blinking or animation) to grab attention.
- **Chromatic Aberration**: The eye cannot focus on deep blue and bright red simultaneously. Avoid putting red text on a blue background (or vice versa), as it causes visual fatigue and a 3D "floating" illusion.

## 3. If/Then Troubleshooting Logic
- **IF** users cannot distinguish between two quantities... **THEN** check the data type mapping. Ensure you are using a quantitative encoding (like position) rather than a nominal encoding (like hue).
- **IF** the text or detailed lines appear blurry or cause eye strain... **THEN** eliminate chromatically contrasting boundaries (especially red/blue and red/green) and rely on strong luminance contrast.
- **IF** users are missing important updates on a dashboard... **THEN** leverage peripheral vision by adding subtle motion or luminance flashes to the update area to guide the fovea.

## 4. Verification Checklists
- [ ] Is the choice between a table and a visual chart justified by the need for pattern discovery?
- [ ] Are ordinal and quantitative data mapped to appropriate visual channels (position, size, lightness)?
- [ ] Is metadata (especially data uncertainty or missing records) clearly represented?
- [ ] Are high-detail elements placed where the fovea is expected to rest?
- [ ] Has chromatic aberration (e.g., red on blue) been avoided in detailed visual elements?