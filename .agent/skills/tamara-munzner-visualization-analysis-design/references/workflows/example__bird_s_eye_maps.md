---
title: "Workflow: Designing Coordinated Multiple Views & Bird’s-Eye Maps"
description: "A comprehensive guide on creating and coordinating multiple views, including overview-detail maps, multiform views, and small multiples for complex data exploration."
---

# Workflow: Designing Coordinated Multiple Views & Bird’s-Eye Maps

## Prerequisites & Context

When dealing with complex, multidimensional, or geographic datasets, a single monolithic view is rarely sufficient to support the varied tasks of discovery, location, and comparison. Coordinated multiple views allow users to seamlessly transition between high-level overviews and granular details without losing context. 

This workflow establishes actionable heuristics for utilizing Bird's-Eye Maps, Multiform Overview-Detail, and Small Multiples, driven by domain analysis and task abstraction.

> **Deep Dive on Theory**  
> To understand the foundational theory of view coordination combinations, run:  
> `bash scripts/query_theory.sh "What are the design choices for coordinating views in terms of sharing encoding and data?"`

## Comprehensive Guide & Best Practices

### 1. Designing Bird's-Eye Maps (Overview-Detail)
For geographic or spatial data where users must navigate large scopes, use a bidirectionally linked bird’s-eye map.

- **Establish the Overview**: Create a smaller secondary view that maintains the same visual encoding as the primary detail view but at a broader zoom level.
- **Implement Linked Navigation**: Place a bounding rectangle within the overview that dynamically updates as the user pans or zooms in the large detail view (unidirectional linkage).
- **Enable Bidirectional Control**: Allow the user to drag or resize the bounding rectangle in the overview to automatically update the region shown in the large detail view.

> *Reference Image*: Overview-detail with geographic maps (differing in viewpoint and size).  
> ![](../../images/7de45697e7959738daa65b41654391fd0a61964cd94b955a3ad13db52adc01ab.jpg)

### 2. Implementing Multiform Overview-Detail (Different Encodings)
When data attributes have distinct characteristics (e.g., time-series vs. functional groups), apply different visual encodings across views.

- **Identify Domain Tasks**: Example from microarray data: finding genes active over a period (trend), matching functional groups (similarity).
- **Select Optimal Encodings**: Use superimposed line charts for time-series overview and a scatterplot for querying derived variables (like value change or fold change). 
- **Add Auxiliary Views**: Incorporate simple supplementary views, like alphabetical text lists, to support direct lookup and browsing without excessive hovering.
- **Coordinate with Linked Highlighting**: Ensure that selecting a region or item in one view (like a time slider) automatically filters or highlights the relevant data in the detail view.

> *Reference Image*: Multiform overview-detail tool.  
> ![](../../images/dc0bc7dd4462d76fc29372eb8e1887ff957ad4b7f41b6400ef18e65491127d1c.jpg)

### 3. Deploying Small Multiples (Different Partitions, Same Encoding)
When comparing multiple slices or partitions of a dataset (e.g., conditions over time), utilize small multiples as a spatially distributed alternative to temporal animation.

- **Partition by Category/Condition**: Divide the dataset and assign each partition to its own view.
- **Maintain Common Reference Frames**: Ensure all small views use the exact same visual encoding so spatial positions and color mappings are directly comparable at a glance.
- **Align for Precision**: Arrange small multiples in a matrix or list layout to optimize side-by-side visual comparisons.
- **Manage Screen Real Estate**: Keep in mind the operational limit of current displays (typically a few dozen views with several hundred elements each).

> **Deep Dive on Theory**  
> To understand why small multiples are often preferred over animation, run:  
> `bash scripts/query_theory.sh "What is the relationship between animation and memory load compared to small multiples?"`

### 4. Combining Complex View Systems
For multifaceted systems (e.g., *Cerebral* or *Improvise*), interweave multiform views, overview-detail navigation, and small multiples.

- **Harmonize Encodings**: Use consistent colormaps (e.g., diverging or bivariate sequential) across multiform views to establish a continuous visual thread.
- **Link Everything**: Synchronize navigation, highlighting, and filtering. For example, a blue selected item in a scatterplot should be highlighted simultaneously in parallel coordinates, map views, and text matrices.

> *Reference Image*: Coordinated design choices matrix.  
> ![](../../images/d449eb118bca70ff2feda7397c4acebf79342b7ca7d4d8e1d7d0028a5e3e0f92.jpg)

> *Reference Image*: *Cerebral* (Small-multiple views).  
> ![](../../images/61670325cf69e869df201a082daf12ce0b285f4ce17f415493697427361fca3e.jpg)

> *Reference Image*: *Improvise* toolkit census visualization.  
> ![](../../images/6321452c0101802169644b6bc9d04e8e597852a773dd775201d79e6aa77d96f3.jpg)

## If/Then Troubleshooting Logic

| Condition | Action | Rationale |
| :--- | :--- | :--- |
| **If** users struggle to maintain spatial context when zooming into a map... | **Then** add a bird's-eye view with a bounding box and linked navigation. | An overview minimizes cognitive load by showing the macro context while allowing detailed micro exploration. |
| **If** animating between data states causes users to lose track of complex changes... | **Then** switch to a small-multiples layout arranged in a matrix. | Animation imposes heavy memory load; small multiples allow eyes to dart between states instantly. |
| **If** screen real estate is exhausted by too many small multiples... | **Then** consolidate using multiform overview-detail views or reduce the cardinality of the partitions. | Visual clutter degrades comparison precision. Operational limits sit around a few dozen views. |
| **If** users cannot easily locate known items in a complex scatterplot... | **Then** introduce a supplemental interactive text-list view linked by highlighting. | Text lists excel at lookup tasks where interacting with hundreds of spatial marks would be tedious. |
| **If** views are identical in both data and encoding... | **Then** remove or alter one of the views. | Fully identical views are redundant and waste valuable screen space. |

## Verification Checklists

### Interaction & Linkage Checklist
- [ ] Bird's-eye bounding box updates when the detail map is panned/zoomed.
- [ ] Dragging the bounding box in the overview correctly updates the detail map.
- [ ] Highlighting an item in one view simultaneously highlights the corresponding item in all multiform views.
- [ ] Navigation (panning/zooming) is synchronized where spatial coordinates are shared.

### Design & Layout Checklist
- [ ] Small multiples share an identical visual encoding and axis scale to allow fair comparison.
- [ ] Small multiples are aligned into structured rows, columns, or matrices.
- [ ] Multiform views use consistent color semantics (e.g., the same bivariate colormap) to represent shared attributes.
- [ ] Supplementary views (like text lists) are included to alleviate the friction of hovering over dense visualizations.
- [ ] Derived attributes (e.g., differences, fold changes) are clearly encoded and distinct from raw base data.