# Workflow: Superimpose Layers & Multi-Level Network Layout

## Prerequisites & Context

- **When to Use**: This workflow is applicable when visualizing dense, multi-level networks (such as paths, subgraphs, and thousands of nodes) where extensive reading of node labels is a primary requirement, and edge crossings are unavoidable due to connectivity density. 
- **Core Philosophy**: Instead of relying on algorithmic edge-crossing minimization (which often sacrifices consistent spatial predictability), this approach leverages **dynamic superimposed layers** to filter noise perceptually. The underlying layout optimizes spatial position to encode ordinal or quantitative attributes (e.g., plausibility) rather than minimizing crossings.
- **Task Abstraction**: Consume-discover scenarios involving browsing highly ranked paths, identifying and comparing low-believability paths, and reading node definitions at scale.

> **Theory Deep Dive**
> To fully understand the perceptual rationale behind choosing attribute-driven spatial positioning over algorithmic edge-crossing minimization, prompt the Runtime Agent:
> ```bash
> bash scripts/query_theory.sh "Why use dynamic superimposed layers instead of algorithmic edge crossing minimization in dense networks?"
> ```

---

## Comprehensive Guide & Best Practices

### Step 1: Design the High-Level Spatial Grid
Establish a macro-layout that structures the network's overarching flows using a curvilinear grid.

1. **Attribute-Based Horizontal Ordering**: Order the primary macro-structures (e.g., paths) horizontally based on a key attribute. For example, place the most plausible or important paths on the left, and less important ones on the right.
2. **Vertical Flow**: Allow structures to flow sequentially top-to-bottom within vertical columns.
3. **Proportional Space Allocation**: Grant more horizontal space to columns with higher plausibility, as they tend to require closer inspection.
4. **Information Density Maximization**:
   - Eliminate empty vertical columns.
   - Eliminate empty cell rows within columns.
   - Expand full cells horizontally and vertically to fill all available screen real estate.

![Base Curvilinear Grid](../../images/0e36bef33c9650463735fc648c351cb110182854b77a46b8130787be2ff1d7fc.jpg)
*(a) Base curvilinear grid.*

![Grid Empty Column Elimination](../../images/8323d0719e495991bcabd48b1784a330ae87dd9472ea232b541f460eba0328de.jpg)
*(b) Eliminating empty columns.*

![Grid Vertical Expansion](../../images/fd939de8a401d8e8f89c899f65e7f10a3af216a9eb4e90b3a81b5da59eb5ce07.jpg)
*(c) Eliminating empty cell rows to increase information density.*

### Step 2: Implement Dynamic Superimposed Layers
Manage visual clutter (the "hairball" effect) by partitioning edge visibility across perceptually distinct layers.

1. **Background Layer**: Render the global topology unobtrusively. Use low luminance, low saturation, and thin line marks so it doesn't overwhelm the viewer.
2. **Foreground Layer**: Dynamically highlight interactively selected subsets. Use increased size (thickness), high luminance, and strong saturation to make the subset pop against the background.
3. **Highlight Targeting**: Allow users to highlight specific structural motifs:
   - Complete paths
   - Subgraphs (e.g., definition graphs)
   - All direct connections to a specific node
   - All links matching a specific categorical type

![Background Layer](../../images/c24166f00d09f8d1c8206a5897f122ab07eb20bedfc13942a7bc08d980b7feff.jpg)
*(a) Background version of a definition graph with unobtrusive edges.*

![Foreground Layer](../../images/457c45c1647d184a2eb458ef7623558663acc4ff3856ac4d008406092317d290.jpg)
*(b) Foreground version highlighted using size, luminance, and saturation channels.*

![Link Type Highlight](../../images/203a53de36baf6225a2e5438f12670f58c7a34fddbdc44226cf3734f46198b6d.jpg)
*Highlighting a specific structural motif (e.g., all links of type 'Part').*

> **Theory Deep Dive**
> To explore heuristics for tuning the luminance and saturation channels to clearly separate foreground from background layers, execute:
> ```bash
> bash scripts/query_theory.sh "How to optimize size, luminance, and saturation channels for dynamic superimposed layers?"
> ```

### Step 3: Structure Mid-Level Segments with Containment
Group intermediate structures hierarchically using spatial containment rather than connection marks alone.

1. **Segment Containers**: Allocate a bounding box with a specific background color (e.g., tan) for a complete path segment.
2. **Nested Structures**: If a node contains sub-definitions or internal structures, enclose those within secondary, differently colored boxes (e.g., green) nested inside the primary segment box.

![Containment Level 1](../../images/821d03c8bf76e5cf140716b62c65e05393d112b730f0d81c39424e94a1a6b299.jpg)
*(a) Primary definition nesting.*

![Containment Level 2](../../images/1938ad2b97c96655ed8b30038751bd5ba012051b6caed0d7569b5ebfe208310f.jpg)
*(b) Secondary definition nesting indicating a hierarchical relationship via containment.*

### Step 4: Design Low-Level Layouts
Detail the micro-structure of individual components.

1. **Rectilinear Ladder Layout**: Structure low-level dependencies using horizontal and vertical straight lines to maintain order.
2. **Label Enclosure**: Place leaf nodes (text labels) inside distinct label boxes.
3. **Orthogonal Encoding**:
   - Use vertical lines to represent hierarchical traversal.
   - Use color-coded horizontal lines to represent specific link types between nodes.

![Low-Level Base Layout](../../images/4bb176ba8611037a73d01cc706f7dfaa009738d0371b078e0c2dafff4911a40d.jpg)
*(a) Low-level base layout with rectilinear links and color-coding for link types.*

### Step 5: Handle Shared Nodes with the Master/Proxy Pattern
When words or nodes appear in multiple definitions, avoid long chaotic edge routes.

1. **Master Node**: Draw the primary instance (usually on the most prominent path) in high contrast (e.g., black text).
2. **Proxy Nodes**: Duplicate the node in all other necessary locations. Render these proxies in low contrast (e.g., gray text).
3. **Long-Distance Links**: Connect proxies back to the master using a distinct, slanted line mark.

![Proxy Layout](../../images/df6f3d708ac7d7e90e21da880804b32579368cdfa008a07419b56402b4604975.jpg)
*(b) Long-distance links connecting master nodes to their duplicated proxies.*

### Step 6: Semantic Zooming
Adapt the spatial allocation of nodes dynamically based on the current camera/zoom scale to ensure labels are readable when needed.

1. **Global View**: Emphasize inter-path relationships and overall structure; allocate maximal space to primary header nodes.
2. **Intermediate View**: Balance space between path segments and subgraphs.
3. **Local View**: Equalize space allocation across all nodes to support extensive reading of leaf-level labels.

![Semantic Zoom 1](../../images/f2802466dfb3d8d9c560458a1c6461d72556a26abd7ecbef7d14eabf2a07f02d.jpg)
![Semantic Zoom 2](../../images/f1551d3efbc5a3f67d7a7745317f12fc873ceb5cdac892adea342b4324b02c9a.jpg)
![Semantic Zoom 3](../../images/7ea8df7475bb2d33475d9b41fd672e2ddc153d533eccbb44c9458e90db6cce4f.jpg)
*Subtle semantic zooming sequence: the space allocated for primary nodes versus sub-nodes changes based on the zoom level.*

> **Theory Deep Dive**
> To explore the specific implementation patterns of semantic zooming versus geometric zooming for text legibility, prompt:
> ```bash
> bash scripts/query_theory.sh "What are the trade-offs between semantic zooming and geometric zooming for reading labels in dense networks?"
> ```

---

## If/Then Troubleshooting Logic

- **IF** the primary view degrades into an unreadable "hairball" with massive edge crossings, **THEN** verify that the background layer is sufficiently desaturated/transparent and heavily promote the interactive superimposed foreground layer. Do *not* fallback to algorithmic crossing minimization, as it will break the attribute-driven spatial layout.
- **IF** the layout feels sparse due to varying path lengths and missing definitions, **THEN** enforce curvilinear grid compaction. Actively collapse empty cell rows and columns, stretching full cells to fill the void.
- **IF** routing links between shared nodes creates severe visual interference, **THEN** apply the Master/Proxy pattern. Duplicate the shared nodes locally to eliminate complex routing, and bind proxies to the master with long, straight, slanted link marks.
- **IF** user testing reveals that leaf nodes are unreadable or occupy too much space at a global scale, **THEN** implement semantic zooming to redistribute cell space disproportionately in favor of top-level nodes when zoomed out.

---

## Verification Checklists

### Structure & Layout Checklist
- [ ] The base spatial grid uses positional mapping to encode a primary quantitative/ordinal attribute (e.g., plausibility).
- [ ] The grid algorithm dynamically eliminates empty space and scales populated cells (maximizing information density).
- [ ] Mid-level hierarchies are encoded using nested box containment rather than just node-link connection.
- [ ] Low-level components use rectilinear (orthogonal) link routing.

### Visual Encoding & Interaction Checklist
- [ ] Background network edges are sufficiently suppressed (low luminance, low saturation).
- [ ] Interactive selection elevates elements to a superimposed foreground layer (high thickness, high luminance, high saturation).
- [ ] The system supports highlighting multiple distinct constellations (e.g., path subsets, link-type subsets).
- [ ] Shared dependencies utilize a Master/Proxy duplication model to avoid edge tangling.
- [ ] Semantic zooming seamlessly adjusts text label space allocation based on viewing altitude.
