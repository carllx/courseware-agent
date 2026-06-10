# Lean UX: Collaborative Design & The Lean UX Canvas (Box 1-5)

## Prerequisites & Context
- **Why**: Lean UX relies on cross-functional collaboration, psychological safety, and shared understanding rather than siloed hand-offs. The Lean UX Canvas (specifically Boxes 1-5) serves to align the team on the business problem, desired outcomes, and target users before anyone proposes solutions.
- **When**: Use this workflow when kicking off a new product initiative, framing a complex problem, or when a cross-functional team needs to ideate together (e.g., via an informal whiteboard session, a structured Design Studio, or a Design Sprint).
- **Deep Dive Reference**:
  - `bash scripts/query_theory.sh "What are the core principles of Lean UX collaboration and psychological safety?"`
  - `bash scripts/query_theory.sh "How does the Lean UX Canvas differ from traditional requirements documents?"`
  - `bash scripts/query_theory.sh "What are the common differences between Lean UX Canvas and a Design Sprint?"`

## Comprehensive Guide & Best Practices

### Phase 1: Framing the Work using the Lean UX Canvas
The Lean UX Canvas aligns the team on the problem, the audience, and the desired outcomes. This phase must be completed collaboratively before jumping into solutioning.

**1. Box 1: Business Problem Statement**
- **Action**: Define the current state, the problem, and the high-level business goals (e.g., KPIs, impact metrics).
- **Heuristics**:
  - *Don’t specify the solution*: Keep it at a level the team can actually influence. Do not use phrases like "How might we implement a mobile app that...".
  - *Be specific*: Include explicit metrics or evidence to set clear business-level success criteria.
- **Deep Dive**: `bash scripts/query_theory.sh "What are common antipatterns when writing business problem statements?"`

**2. Box 2: Business Outcomes**
- **Action**: Identify the *leading indicators* (user behaviors) that predict business impact. What will people be doing differently if our solutions work?
- **Heuristics**:
  - Start every option in the brainstorm with an actionable verb.
  - Use frameworks like Pirate Metrics (AARRR), Metrics Mountain, or Service Journeys to map out the current vs. desired customer behaviors.

**3. Box 3: Users (Proto-Personas)**
- **Action**: Sketch out proto-personas representing the target audience.
- **Heuristics**: Focus on behaviors, needs, and obstacles rather than demographics. Use the team's existing assumptions to build these proto-personas, and plan to validate them with real users early.

**4. Box 4: User Outcomes and Benefits**
- **Action**: Determine what the user gets out of the product. Why would they use it? What problem does it solve for them?

**5. Box 5: Solutions**
- **Action**: Brainstorm potential features, products, or enhancements that could deliver the user outcomes and drive the business outcomes.
- **Heuristics**:
  - Emphasize quantity over quality initially.
  - Use affinity mapping to group similar ideas and spot recurring themes.
- **Deep Dive**: `bash scripts/query_theory.sh "How to effectively facilitate the affinity mapping exercise for Lean UX solutions?"`

### Phase 2: Collaborative Design & Ideation
Translate the business problem and desired outcomes into potential solutions through structured, cross-functional collaboration.

**1. Informal Collaborative Design**
- **Action**: Bring the designer, PM, and engineer to a whiteboard to outline flows together.
- **Heuristics**:
  - *Conversation is your most powerful tool*: The discussion around the drawing is more important than the drawing itself.
  - *Don't skip the fat markers*: Using thick markers forces the team to focus on structure, layout, and flow rather than aesthetic details.

**2. Structured Approach: Running a Design Studio**
- **Action**: A time-boxed, cross-functional workshop to generate, critique, and iterate on solutions.
- **Process Steps**:
  - *Problem Definition & Constraints (15 mins)*: Review the Canvas and establish boundaries.
  - *Individual Idea Generation (10 mins)*: Create "six-up" sketches rapidly.
  - *Presentation & Critique (3 mins per person)*: Focus on constructive, outcome-focused feedback.
  - *Pair Up to Iterate (10 mins)*: Consolidate and refine ideas with a partner.
  - *Team Idea Generation (45 mins)*: Converge on the strongest concepts to carry forward.
- **Deep Dive**: `bash scripts/query_theory.sh "How to effectively facilitate a Design Studio presentation and critique?"`

**3. Utilizing Design Systems**
- **Action**: Leverage a design system to speed up collaborative design and maintain consistency.
- **Heuristics**:
  - Treat the design system as a living product, and the design systems team as a product team.
  - Use design systems to bridge the gap between design and engineering, allowing for rapid prototyping in code.

## If/Then Troubleshooting Logic

- **If** the problem statement in Box 1 implies a specific feature or solution (e.g., "build an intuitive UI"):
  - **Then** pause and repeatedly ask "Why?" to uncover the underlying business or user need. Reframe the statement to focus on the problem (e.g., "decrease cart abandonment rate"), not the output.
- **If** the team struggles to generate solutions without getting stuck on high-fidelity visual details:
  - **Then** enforce the use of "fat markers" (sharpies) and low-fidelity mediums (paper/whiteboards). Remove digital design tools from the early ideation phase.
- **If** the team is geographically distributed and cannot do an in-person Design Studio:
  - **Then** leverage digital whiteboarding tools, but maintain strict timeboxing and clear facilitation rules. Focus heavily on establishing *psychological safety* before starting.
  - **Deep Dive**: `bash scripts/query_theory.sh "Best practices and tools for collaborating with geographically distributed teams in Lean UX?"`
- **If** stakeholders push for exhaustive requirements documentation instead of collaborative design:
  - **Then** explain the Lean UX principle of "shared understanding." Invite them to a Design Studio to show that cross-functional workshops produce actionable consensus faster and with less waste than writing and reading a 50-page spec.

## Verification Checklists

### Lean UX Canvas (Phase 1) Verification
- [ ] Is the business problem statement strictly focused on the problem and devoid of predefined solutions?
- [ ] Are the business outcomes framed as observable user behaviors (leading indicators)?
- [ ] Are proto-personas based on actionable user behaviors, obstacles, and needs?
- [ ] Has the team explicitly mapped the user outcomes directly back to the business outcomes?
- [ ] Has the team completed an affinity mapping exercise to group and prioritize the generated solutions?

### Collaborative Design (Phase 2) Verification
- [ ] Is the problem definition and constraint box clearly stated and understood by all workshop participants?
- [ ] Did you enforce low-fidelity constraints (e.g., 6-up templates, thick markers)?
- [ ] Did the critique session stay focused on solving the problem statement rather than personal design preferences?
- [ ] Did the cross-functional team successfully converge on a set of solutions to validate?
- [ ] Is psychological safety actively maintained to ensure all disciplines (engineering, product, design) contribute to the ideation?