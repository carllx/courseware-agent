# Workflow: Brainstorming for Innovation & Bringing Requirements to Life

## Prerequisites & Context
**When to Use This Workflow:**
Use this workflow when transitioning from raw user research data to actionable design requirements. It covers the ideation phase (Brainstorming) and the translation of requirements into tangible design tools (Personas and Scenarios). This ensures that abstract data is transformed into relatable, human-centered design targets.

**Deep Dive Context:**
To explore the theoretical origins of brainstorming or the formal specification methods (e.g., Z formal notation) for safety-critical systems, use the dynamic query script:
```bash
bash scripts/query_theory.sh "Explain the principles of Osborn's brainstorming rules and the use of formal notations for requirements as outlined in Chapter 11."
```

## Comprehensive Guide & Best Practices

### 1. Brainstorming for Innovation
Brainstorming is a divergent and convergent process used to generate alternative designs and explore the problem space. Follow Osborn’s four core rules:
- **Quantity over Quality:** Focus on generating as many ideas as possible. High volume increases the chance of uncovering novel solutions.
- **Withhold Criticism:** Create a psychologically safe environment. Do not evaluate or shoot down "dumb" ideas during the generation phase.
- **Encourage Out-of-the-Box Thinking:** Welcome unorthodox, impractical ideas—they often serve as catalysts or prompts for other, more feasible innovations.
- **Combine, Refine, and Improve (Crucial Convergent Step):** Do not skip this step. After generating ideas, fuse and modify them to extract concrete, actionable requirements.

*Facilitation Tip:* Keep groups between 5 and 12 participants. Provide specific problem definitions and physical or verbal catalysts to prompt different perspectives.

### 2. Bringing Requirements to Life
Raw requirements (e.g., captured in Volere shells or user stories) often lack empathetic context. Bring them to life using specific representations.
- **For Safety-Critical Systems:** Use formal, mathematically-based specification languages (e.g., Z formal notation or petri nets) to unambiguously define UI behavior (like medical infusion pumps) and avoid fatal bugs.
- **For Everyday Systems:** Use **Personas** and **Scenarios** in parallel to represent who is using the product and how they use it.

### 3. Developing Effective Personas
Personas represent a synthesis of your data gathering, not just a single specific user or a generic job description.
- **Goal-Oriented:** Define the persona by their unique set of goals relating to the product, rather than just demographics.
- **Credible Details:** Include precise, relevant details (e.g., "completed Day Skipper qualification with 100+ hours of experience") rather than vague descriptions ("competent sailor").
- **Visuals Matter:** The photo chosen influences designer perception. For example, using *unhappy* photographs can increase the perceived realism and severity of a persona's pain points, while *happy* photos make the persona seem more agreeable and extroverted.
- **Scope:** Include *only* information pertinent to the product context. Do not document their favorite clothing brand unless developing a fashion or shopping center app.

### 4. Crafting Associated Scenarios
- Ensure the initial narrative does not conflate the persona's background with the scenario itself. 
- **Focus:** Scope the scenario to describe exactly *one* specific use of the product or one instance of achieving a goal.

## If/Then Troubleshooting Logic
- **IF** a brainstorming session stalls or devolves into analyzing a single idea, **THEN** explicitly enforce the "Withhold Criticism" rule and introduce a random physical object or word as a catalyst to force out-of-the-box thinking.
- **IF** the development team views a persona as an unrealistic stereotype, **THEN** replace generic demographic data with precise, credible behavioral details derived directly from ethnographic interviews.
- **IF** designers are underestimating the severity of user pain points, **THEN** update the persona document using an unhappy or stressed photograph to subtly shift the team's empathetic response.
- **IF** you are designing a highly technical or safety-critical interface (e.g., a dosing calculator), **THEN** augment standard user stories with formal specification notations to prevent logic inconsistencies.

## Verification Checklists
- [ ] Brainstorming sessions explicitly include a convergent phase to combine and refine ideas into requirements.
- [ ] Personas are constructed from aggregated research data, not assumptions.
- [ ] Each persona is defined primarily by their goals and relevant behaviors, not just demographics.
- [ ] Scenarios are strictly scoped to a single narrative of product usage.
- [ ] Formal modeling (e.g., petri nets) is employed if the UI requirements are safety-critical.
- [ ] All embedded image references (e.g., `../../images/persona_example.jpg`) strictly use relative paths.