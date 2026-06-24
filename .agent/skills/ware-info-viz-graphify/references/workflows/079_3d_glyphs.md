# Workflow: 3D Glyphs, Faces, and Coding Variables

## Prerequisites & Context
**Why and When:**
In scientific and information visualization, complex multidimensional data (such as tensor fields with twist and shear, or highly dimensional attributes) requires advanced glyphs. While 3D glyphs and facial representations (Chernoff faces) offer ways to encode multiple variables, they come with significant perceptual pitfalls and emergent biases.
- *Theory Deep Dive*: For deeper insights into facial action coding systems (FACS), dual coding theory, or tensor field visualization, run `bash scripts/query_theory.sh "Explain FACS, dual coding theory, and the evaluation of 3D glyphs."`

## Comprehensive Guide & Best Practices

1. **Designing 3D Glyphs:**
   - 3D glyphs (e.g., superellipsoids) can encode attributes like orientation, twist, and shear in tensor fields.
   - *Constraint*: Human pattern analysis is optimized for the 2D image plane. 3D glyphs are highly viewpoint-dependent, meaning variations in the camera angle can result in misinterpretation. Use them strictly when 3D spatial context is mandatory, and allow the user to easily adjust their viewpoint.

2. **Using Faces for Data (Chernoff Faces vs. Emotion):**
   - **Avoid Chernoff Faces for Arbitrary Data**: Mapping arbitrary data variables to facial features (nose length, mouth curvature) is strongly discouraged. The perceptual space of faces is highly nonlinear, and arbitrary mappings often create emergent, unintended stereotypical expressions that distort data interpretation.
   - **Use Faces for Emotion**: Faces are powerful, universally recognized communication signals. Use simple face glyphs or avatars explicitly to convey emotion (e.g., anger, disgust, fear, happiness, sadness, surprise) rather than multidimensional abstract data.

3. **Applying Dual Coding Theory:**
   - Visual imagery (imagens) and language information (logogens) are processed in distinct memory systems. Leverage this by combining simple visual representations (like faces for emotion) with structural or textual data to efficiently maximize cognitive bandwidth.

## If/Then Troubleshooting Logic
- **IF** users misinterpret the values encoded in a 3D glyph, **THEN** it is likely due to viewpoint dependency. Provide tools to snap to orthogonal 2D views or use 2D planar representations if possible.
- **IF** using Chernoff faces results in confusing or clustered interpretations of data, **THEN** abandon the facial mapping. Users are responding to emergent facial expressions rather than the underlying data variables. Switch to more objective multivariant charts.

## Verification Checklists
- [ ] Are 3D glyphs restricted only to data where 3D spatial layout is required (e.g., tensor fields)?
- [ ] Has the use of Chernoff faces for mapping arbitrary data variables been eliminated or heavily justified?
- [ ] Are facial glyphs used effectively and exclusively to convey recognizable emotional states?
- [ ] Are images correctly referenced (e.g., `../../images/f08-13-9780128128756.jpg`, `../../images/f08-14-9780128128756.jpg`, `../../images/f08-15-9780128128756.jpg`)?

![3D Glyphs](../../images/f08-13-9780128128756.jpg)
![Facial Expressions](../../images/f08-14-9780128128756.jpg)
![Chernoff Faces](../../images/f08-15-9780128128756.jpg)