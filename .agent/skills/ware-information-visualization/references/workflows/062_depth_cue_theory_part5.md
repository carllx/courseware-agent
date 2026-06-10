# Workflow: Depth Cue Theory (Structure from Motion and Stereopsis)

## Prerequisites & Context
**Why and When:**
When navigating complex 3D environments or visualizing discrete data clouds, static depth cues are often insufficient. Using structure-from-motion (kinetic depth) and stereoscopic depth can drastically improve the perception of 3D layout, object rigidity, and depth relationships.
- *Theory Deep Dive*: For detailed explanations on the neurological mechanisms of the kinetic depth effect or Panum's fusional area, run `bash scripts/query_theory.sh "Explain kinetic depth effect, tau, and Panum's fusional area."`

## Comprehensive Guide & Best Practices

1. **Utilize Kinetic Depth and Structure from Motion:**
   - **Rotate or Oscillate Data Space**: To help users understand complex structures (like 3D node-link structures or discrete point clouds), rotate the scene around a vertical axis. This causes the visual system to perceive a rigid 3D object rather than a 2D projection.
   - **Oscillation over Full Rotation**: To prevent the user from losing a preferred viewpoint during constant rotation, use an oscillatory motion. This preserves the viewpoint while still providing the kinetic depth cue.

2. **Apply Stereoscopic Depth Sparingly but Effectively:**
   - **Near-field Tasks**: Stereoscopic depth is a superacuity (resolving down to 10 seconds of arc) and is optimally useful for objects within arm's reach (less than 30m, practically up to 2m for eye convergence).
   - **Managing Disparity**: Keep the angular disparity small. Exceeding the limits of Panum's fusional area (e.g., 1/10 degree at the fovea) will cause diplopia (double vision).
   - Keep in mind that up to 20% of the population may be stereo-blind, so do not rely solely on stereoscopic cues for critical tasks.

## If/Then Troubleshooting Logic
- **IF** users complain of double vision (diplopia) in stereoscopic displays, **THEN** the angular disparity between the left and right images is too large and exceeds Panum's fusional area. Reduce the disparity.
- **IF** a 3D point cloud looks flat and confusing, **THEN** introduce a slow rotation or oscillation around the center of interest to activate the kinetic depth effect.
- **IF** the viewpoint is constantly lost during rotation, **THEN** switch from full rotation to a gentle oscillatory back-and-forth motion.

## Verification Checklists
- [ ] Is kinetic depth applied (e.g., via oscillation) for detached objects or 3D node-link structures?
- [ ] Are stereoscopic disparities kept within the strict limits of Panum's fusional area (max 1/10 degree at the fovea)?
- [ ] Is there a fallback for users who are stereo-blind (e.g., motion parallax, shadows)?
- [ ] Are images appropriately referenced (e.g., `../../images/f07-24-9780128128756.jpg`, `../../images/f07-25-9780128128756.jpg`, `../../images/f07-26-9780128128756.jpg`)?

![Motion Parallax and Kinetic Depth](../../images/f07-24-9780128128756.jpg)
![Eye Convergence](../../images/f07-25-9780128128756.jpg)
![Stereoscopic Display](../../images/f07-26-9780128128756.jpg)