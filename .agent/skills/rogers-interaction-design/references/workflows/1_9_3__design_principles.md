# Comprehensive Guide: Core Design Principles, Cognition, and Heuristic Evaluation

## Prerequisites & Context

**Why and When to Use This Workflow:**
This workflow bridges foundational interaction design principles (Visibility, Consistency, Affordance) with human cognitive realities (Perception, Memory, Cognitive Load). It guides designers and evaluators through creating conceptual models, leveraging interface metaphors, and rigorously evaluating interfaces using heuristic walk-throughs and qualitative analysis.

Use this workflow when:
- Establishing the baseline design principles for a new interface.
- Analyzing an existing interface for cognitive overload or memory bottlenecks.
- Defining a conceptual model and interface metaphors.
- Conducting a formal heuristic evaluation or inspection of a product.
- Synthesizing qualitative data (e.g., identifying themes from video analysis).

*For deep dives into theoretical background or specific heuristic definitions, run the following command:*
`bash scripts/query_theory.sh "What are the core design principles of visibility, consistency, and affordance, and how do they relate to cognitive load?"`

---

## Comprehensive Guide & Best Practices

### 1. Core Design Principles
- **Visibility**: Ensure that the available actions are highly visible to the user. Do not hide core functionality behind obscure menus. The more visible functions are, the more likely users will be able to know what to do next.
- **Consistency**: Design interfaces to have similar operations and use similar elements for achieving similar tasks. Establish a clear internal consistency (within the app) and external consistency (matching OS or industry standards).
- **Affordance**: Ensure that an attribute of an object allows people to know how to use it (e.g., a button physically looks like it can be pushed). For digital interfaces, use "perceived affordances" (shadows, gradients) to indicate interactivity.

### 2. Managing Human Cognition & Memory
- **Perception & Information Presentation**: Group related items clearly (Gestalt principles). Ensure high contrast and legible typography.
- **Memory & The Magical Number Seven**: Acknowledge that human short-term memory is limited. Avoid making users memorize passcodes or complex sequences. Rely on *recognition* over *recall*.
- **Cognitive Offloading & External Cognition**: Allow the interface to remember for the user. Pre-fill forms, provide clear search histories, and use computational offloading (e.g., providing a calculator instead of forcing mental math).
- **Digital Forgetting**: Build systems that allow for the graceful archiving or deletion of old data, rather than overwhelming the user with a permanent, cluttered digital memory.

### 3. Conceptual Models and Metaphors
- **Conceptual Models**: Before sketching screens, clearly define the system's conceptual model. How should the user think about the system? Is it a "desktop," a "shopping cart," or a "feed"?
- **Interface Metaphors**: Use metaphors to bootstrap learning. If a concept is abstract, map it to a physical world equivalent. **Warning**: Do not constrain the digital functionality strictly to the physical metaphor (e.g., a digital "folder" doesn't have a physical page limit).

### 4. Inspections & Heuristic Evaluation
- **Minimize Unnecessary Complexity**: During heuristic evaluation, explicitly look for cognitive load bottlenecks. Ask, "Does the user need to know this right now?"
- **Provide Context**: Ensure the user always knows where they are, where they came from, and where they can go next.
- **Reliability & Usability Problems**: When conducting inspections, use 3-5 evaluators. Single evaluators will miss issues. Categorize found usability problems by severity.
- **In-the-Wild Studies**: Validate heuristics against actual usage. Combine inspections with ethnographic or in-the-wild studies (e.g., observing a pain-monitoring device used in a patient's home).

### 5. Qualitative Data Analysis
- **Identifying Themes**: When analyzing feedback or video material, transcribe the data and inductively code it to identify recurring themes (e.g., using affinity diagramming).
- **Basic Qualitative Analysis**: Look for patterns in how users misinterpret affordances or where they exhibit signs of high cognitive load (hesitation, backtracking).

---

## If/Then Troubleshooting Logic

- **If** users frequently ask "What do I do next?", **Then** the interface lacks Visibility. Surface the primary call-to-action out of nested menus and place it directly in the user's focal path.
- **If** users are failing to fill out long forms online, **Then** cognitive load is too high. Implement Cognitive Offloading by breaking the form into smaller, chunked steps, pre-filling known data, and providing inline validation.
- **If** the interface metaphor breaks down (e.g., users expect a digital "trash can" to automatically empty like a physical one), **Then** provide clear feedback or adjust the conceptual model to explain the system's actual rules.
- **If** evaluators in a heuristic inspection find widely different usability problems, **Then** synthesize their findings to establish Reliability. It is expected that different evaluators find different issues; merge them into a single severity-ranked backlog.

---

## Verification Checklists

**Design Principles & Cognition Checklist**
- [ ] Are primary actions explicitly visible without requiring a hover or click?
- [ ] Does the UI maintain strict internal and external consistency?
- [ ] Do interactive elements provide clear perceived affordances?
- [ ] Does the system rely on user recognition rather than recall?
- [ ] Are complex tasks supported by cognitive offloading (e.g., saved states, pre-filled data)?

**Metaphor & Evaluation Checklist**
- [ ] Is the conceptual model clearly defined and communicated to the user?
- [ ] If an interface metaphor is used, does it enhance learnability without arbitrarily constraining functionality?
- [ ] Have at least 3 evaluators conducted an independent heuristic evaluation?
- [ ] Are usability problems prioritized by severity and frequency?
- [ ] Have qualitative themes been rigorously extracted from user testing sessions or video analyses?