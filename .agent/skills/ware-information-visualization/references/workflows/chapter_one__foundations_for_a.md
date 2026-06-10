# Chapter 1: Foundations for an Applied Science of Data Visualization

## 1. Prerequisites & Context
**Why & When to use this workflow:**
Use this workflow to establish the foundational mappings between raw data and visual representations. It addresses how to convert abstract data into perceptual forms using the science of vision, Gibson’s Affordance Theory, and the distinction between sensory and arbitrary symbols.

*For deeper theoretical dives, use:*
```bash
bash scripts/query_theory.sh "What are the four visualization stages in Ware's model?"
bash scripts/query_theory.sh "Differentiate between sensory symbols and arbitrary symbols in experimental semiotics."
bash scripts/query_theory.sh "How does Gibson's Affordance Theory apply to digital data visualization?"
```

## 2. Comprehensive Guide & Best Practices

### A. Navigate the Visualization Stages
Ensure your system accounts for the four core stages:
1. **Data Collection & Storage**: Organize data into formats suitable for transformation.
2. **Data Transformation**: Filter, compute, and format the data (e.g., calculating moving averages).
3. **Graphics Engine / Visual Mapping**: Map transformed data into visual properties (color, shape, spatial position).
4. **Human Perception & Cognition**: Design the output so the human visual system can preattentively process and cognitively model the information.

### B. Map Data to Sensory vs. Arbitrary Symbols
- **Sensory Symbols**: Use sensory symbols (e.g., contrasting colors, size, position, texture) to represent data that needs immediate, cross-cultural recognition. Sensory symbols rely on hardwired perceptual processing.
- **Arbitrary Symbols**: Use arbitrary symbols (e.g., text, numbers, culturally specific icons) only when the user has time to learn them and context supports their interpretation. 
- *Heuristic*: "If you want to highlight a trend, use sensory codes (a thick red line). If you want to label a specific exact value, use an arbitrary code (the number 42)."

### C. Apply Gibson's Affordance Theory
- Surfaces, textures, and structures in the visualization should *afford* specific actions. 
- Make interactive elements visually suggest their manipulability. For instance, a 3D-looking button affords pushing; a draggable timeline affords sliding.
- Build visual structures that map to the environment the visual system evolved to understand (e.g., continuous surfaces, depth cues).

### D. Optimize for the Model of Perceptual Processing
- **Stage 1: Preattentive Processing** (Bottom-up, parallel, fast): Use color, motion, and spatial layout to draw attention immediately.
- **Stage 2: Pattern Perception** (Sequential, object recognition): Ensure clear boundaries and Gestalt groupings so users can separate foreground from background.
- **Stage 3: Sequential Goal-Directed Processing** (Top-down, slow): Support visual queries (e.g., "Where is the highest value?") by ensuring the target visually pops out.

## 3. If/Then Troubleshooting Logic
- **IF** users fail to notice a critical alert... **THEN** you are likely relying on an arbitrary symbol instead of a sensory symbol. Switch the alert to use a preattentive sensory cue (e.g., flashing motion or high-contrast color).
- **IF** the data structure feels disconnected from user interaction... **THEN** revisit Gibson's affordances. Ensure that actionable data points visually invite the exact interaction you intend (clicking, dragging).
- **IF** users are overwhelmed by data density... **THEN** verify your Data Transformation stage. You might be skipping necessary filtering or aggregation before pushing to the graphics engine.

## 4. Verification Checklists
- [ ] Does the design pipeline clearly delineate Data Transformation from Visual Mapping?
- [ ] Are critical metrics encoded using sensory symbols (color, size, spatial position)?
- [ ] Do arbitrary symbols (text, domain-specific icons) have appropriate context and legends?
- [ ] Does the visual layout afford the interactions the user is expected to perform?
- [ ] Are bottom-up preattentive cues aligned with top-down user goals (visual queries)?