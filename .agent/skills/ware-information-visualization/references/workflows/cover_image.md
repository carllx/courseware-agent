# Cover Image & Preface Workflow: Foundation of Information Visualization

## 1. Prerequisites & Context
**Why & When to use this workflow:**
This workflow serves as the gateway to applying Colin Ware's *Information Visualization: Perception for Design*. Use it when you are initializing a new visualization project or defining the cognitive architecture of an interface. The core paradigm shift here is treating the **brain as a prediction engine** and the user as a **cognitive cyborg** (where cognition is distributed across the brain and the interactive visualization tool).

*For deeper theoretical dives, use:*
```bash
bash scripts/query_theory.sh "How does predictive cognition unify memory and future prediction in visual thinking?"
bash scripts/query_theory.sh "What are the core concepts behind nonmetaphoric spatial navigation and generalized fisheye views?"
```

## 2. Comprehensive Guide & Best Practices

### A. Establish the Cognitive Framework
- **Design for the "Cognitive Cyborg"**: Assume the user relies on the interface as an external working memory. Build tools that reduce the cognitive load of remembering states.
- **Support the Prediction Engine**: Ensure that the visual flow naturally feeds the user's predictive modeling. Visualizations should answer "what might happen" based on "what is currently shown."

### B. Implement Nonmetaphoric Spatial Navigation
- **Focus-Context Balance**: Solve the problem of finding specific objects (focus) within a larger data landscape (context) across three scales:
  - **Spatial Scale**: e.g., mapping individual fish in an ocean.
  - **Structural Scale**: e.g., hierarchical software code (from a single line to an entire system).
  - **Temporal Scale**: e.g., microsecond packet drops vs. daily traffic patterns.
- **Design Adaptive Node-Link Diagrams**:
  - Implement *Intelligent Zoom / Generalized Fisheye Views*: When a user touches a node, expand its immediate cluster while shrinking or hiding less relevant components.
  - *Heuristic*: "Entities most likely to be relevant are brought into visual prominence."
- **Use Near-Neighbor Highlighting in Dense Networks**:
  - For graphs exceeding 30 nodes (where static layouts fail), implement interactive *degree-of-relevance highlighting*. Hovering or clicking a node should instantly highlight its semantic neighbors.
  - Abandon strict edge-crossing minimization in favor of interactive clarity.

### C. Utilize Multidimensional Interactive Tables & Plots
- **Table Lens / Interactive Tables**: Map numerical values to bar lengths within table cells and allow row/column sorting to reveal correlations (e.g., sorting by blood pressure to reveal correlated metrics).
- **Scatterplot Matrices & Parallel Coordinates**: Enable interactive range queries (brushing). Selecting a subset in one plot must instantaneously highlight the equivalent data in all parallel representations.

## 3. If/Then Troubleshooting Logic
- **IF** the network diagram looks like a "hairball" and is incomprehensible... **THEN** switch from static layout optimization to an interactive *hover-query* system with degree-of-relevance highlighting.
- **IF** users struggle to maintain context when zooming into a dataset... **THEN** implement a generalized fisheye view or intelligent zoom, ensuring unselected areas shrink proportionally instead of disappearing abruptly.
- **IF** comparing different parts of a zoomed network overwhelms working memory... **THEN** either simplify the components or provide side-by-side display panels to leverage eye-movement comparisons instead of memory recall.

## 4. Verification Checklists
- [ ] Is the interface designed to act as an external working memory?
- [ ] Have you identified the primary scale (spatial, structural, or temporal) that requires a focus-context solution?
- [ ] Are generalized fisheye views or intelligent zooms applied to dense hierarchical data?
- [ ] Can users hover over network nodes to trigger near-neighbor highlighting?
- [ ] Do multidimensional charts (scatterplots, parallel coordinates) support synchronized brushing and linking?