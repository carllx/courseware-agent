# Workflow: Self-Movement, Object Positioning, and Simulator Sickness

## Prerequisites & Context
**Why and When:**
When designing immersive virtual environments (VE), aircraft simulators, or 3D interactive manipulation spaces, designers must manage the illusion of self-motion (vection) and accurate 3D hand-eye coordination. Failure to manage these cues can result in severe simulator sickness or frustrating manipulation tasks.
- *Theory Deep Dive*: To explore the sensory conflict theory of simulator sickness or prism adaptation in eye-hand coordination, use `bash scripts/query_theory.sh "What causes simulator sickness and how does proprioceptive adaptation work?"`

## Comprehensive Guide & Best Practices

1. **Managing Vection (Illusion of Self-Motion):**
   - **Maximize Vection**: Use large visual fields. Vection is stronger if the moving part of the visual field is perceived as a distant background. Placing a static foreground frame between the observer and the moving background significantly increases vection.
   - **Mitigate Simulator Sickness**: Avoid designing rides or VR experiences where the participant is expected to look repeatedly from side-to-side while moving. Provide short exposure periods initially, gradually lengthening them to build tolerance.

2. **Selecting and Positioning Objects in 3D:**
   - **Stereo over Head Tracking**: For visually guided reaching and fine positioning, stereoscopic viewing is more important than motion parallax from head tracking.
   - **Visual Feedback and Registration**: Perfect registration between the physical hand and virtual object is difficult. Instead, display a virtual proxy (e.g., a probe or virtual hand) in the same space as the virtual objects to establish clear relative positioning.
   - **Minimize Rotational Mismatch**: Keep rotational mismatch between the virtual space and actual physical space below 30 degrees. Users can adapt to translational mismatches quickly, but rotational mismatches severely degrade eye-hand coordination.

## If/Then Troubleshooting Logic
- **IF** users experience rapid onset of simulator sickness (nausea), **THEN** limit their exposure times, reduce required side-to-side head movements, or minimize the vestibular-visual mismatch.
- **IF** users struggle to accurately grasp or select virtual objects, **THEN** prioritize stereoscopic depth cues and ensure a visible graphical proxy for the user's hand is present to provide continuous relative visual feedback.
- **IF** a user's virtual hand movements feel completely uncoordinated, **THEN** check for rotational mismatch between the physical hand space and virtual space; ensure it does not exceed 30 degrees.

## Verification Checklists
- [ ] Is a static foreground frame used to enhance the feeling of background motion (vection) without requiring excessive physical movement?
- [ ] Are interactions designed to minimize rapid side-to-side head turning in immersive environments?
- [ ] Is a stereoscopic display used for tasks requiring fine 3D manipulation?
- [ ] Is there a clearly visible virtual hand proxy to aid in relative positioning?
- [ ] Is rotational mismatch kept below 30 degrees?
- [ ] Are references updated? (e.g., `../../images/f07-49-9780128128756.jpg`)

![Registration of Hand and Virtual Object](../../images/f07-49-9780128128756.jpg)