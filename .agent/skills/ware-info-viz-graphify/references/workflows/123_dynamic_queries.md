# Dynamic Queries: Multidimensional Data Filtering

## Prerequisites & Context

Dynamic queries solve the problem of exploring multidimensional discrete datasets by allowing users to rapidly filter entities based on multiple attributes simultaneously. By translating complex database queries into intuitive epistemic actions (e.g., adjusting double-ended sliders), users can isolate a small, relevant subset of data for detailed analysis.

**When to use this workflow:**
- When analyzing datasets with multiple continuous or ordinal attributes (e.g., a movie database with ratings, runtime, and release year; or a medical database with heart rate, lipid levels, and blood pressure).
- When the goal is to rapidly reduce a large dataset (up to $10^d$ entities, where $d$ is the number of query dimensions) into a manageable handful of entities that can be explored via a "drill down" operation.

> **Deep Dive Theory:**
> To explore the cognitive psychology of epistemic actions and information scent in visual search, run:
> ```bash
> bash scripts/query_theory.sh "What are epistemic actions in the context of dynamic queries and visual thinking?"
> ```

## Comprehensive Guide & Best Practices

To build cognitively efficient dynamic queries, implement the following heuristics:

### 1. Implement Multi-Dimensional Sliders
Each attribute of the database should be assigned its own interface control.
- **Action:** Use double-ended sliders that allow the user to define both the minimum and maximum threshold for a given attribute.

### 2. Calculate Scalability Constraints
Ensure your dataset size aligns with the interaction paradigm's capabilities.
- **Action:** Use the heuristic that each slider can roughly reduce the range to 10% of the original.
- **Heuristic:** The maximum dataset size suitable for dynamic queries is approximately $10^d$, where $d$ is the number of attributes selectable by sliders (e.g., 5 sliders can efficiently filter 100,000 objects). 
  *(Note: Table summaries occasionally cite $2^d$ depending on the strictness of the distribution, but $10^d$ is the functional benchmark for slider-based elimination).*

### 3. Ensure Immediate Visual Feedback
The cognitive loop breaks if the user has to wait for the visual result of a slider movement.
- **Action:** Optimize the database query and rendering engine to update the visualization synchronously with the slider movement.
- **Interaction Guideline:** The display update following a slider manipulation must be extraordinarily rapid (latency < 100 milliseconds).

### 4. Provide Information Scent
Once the dataset is reduced, the user must be able to visually search the remaining objects.
- **Action:** Do not merely render identical dots. Use glyphs (shapes, colors, sizes) to encode additional attributes.
- **Information Scent Guideline:** Additional attributes should be encoded in the data glyphs to facilitate visual search for task-relevant information before the user commits to a click/drill-down.

### 5. Combine with Appropriate Visual Types
Dynamic queries are agnostic to the primary visualization but work best with specific forms.
- **Action:** Pair dynamic queries with scatter plots, time-series plots, geographic maps, or node-link diagrams (where restrictions mask out nodes/links).

## If/Then Troubleshooting Logic

- **If** the visualization stutters or lags when moving a slider:
  - **Then** the >100ms latency is breaking the cognitive loop. You must implement data indexing, spatial data structures, or client-side caching to ensure real-time rendering. Do not rely on round-trip network requests for every slider tick.
- **If** users successfully filter the data but still don't know which of the remaining objects to select:
  - **Then** your visualization lacks "information scent". Enhance the data glyphs (e.g., use color coding or size) to represent secondary variables so users can visually differentiate the remaining targets.
- **If** the dataset is too massive (e.g., millions of rows) and 5 sliders aren't enough to filter it down:
  - **Then** dynamic queries alone are insufficient. Implement a keyword search or categorical filter *before* loading the dynamic query interface (as discussed in the Big Data two-stage process).

> **Theoretical Constraints Inquiry:**
> ```bash
> bash scripts/query_theory.sh "What are the limitations of dynamic queries on highly dense data representations?"
> ```

## Verification Checklists

- [ ] Are double-ended sliders provided for all relevant continuous/ordinal variables?
- [ ] Is the dataset size constrained to $\sim 10^d$ entities relative to the number of sliders ($d$)?
- [ ] Does the visual canvas update in under 100 milliseconds during continuous slider manipulation?
- [ ] Are the remaining data objects rendered with rich glyphs (information scent) rather than uniform dots?
- [ ] Does the interaction naturally lead into a "drill down" operation for individual entities?