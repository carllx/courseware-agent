# Workflow: Virtual Reality Design and User Research Methodologies

## Prerequisites & Context
**When to Use This Workflow:**
This workflow serves a dual purpose: it guides the design and conceptualization of Virtual Reality (VR) environments, and it outlines best practices for essential data-gathering methodologies (Interviews, Questionnaires, and Observation) necessary for evaluating complex interaction systems like VR.

**Deep Dive Context:**
To explore the deep theoretical principles underlying psychological presence in VR or the detailed nuances of qualitative vs. quantitative data gathering (e.g., Likert vs. Semantic Differential scales), use the dynamic query script:
```bash
bash scripts/query_theory.sh "What are the core concepts of presence in Virtual Reality and the best practices for ethnographic data gathering as detailed in the textbook?"
```

## Comprehensive Guide & Best Practices

### 1. Designing Virtual Reality (VR) Experiences
- **Fidelity and Presence:** Design VR environments with sufficient fidelity to induce a strong sense of *presence* (the psychological feeling of "being there"). Combine stereoscopic displays with auditory and haptic feedback to deepen immersion.
- **Perspective Selection:**
  - *First-Person Perspective:* Best for simulations requiring direct and immediate control (e.g., flying, driving). The user views the world through their own eyes.
  - *Third-Person Perspective:* Best for environments where seeing a representation of self (an avatar) relative to the environment and others is crucial (e.g., collaborative spaces).
- **Empathy and Storytelling:** Leverage VR to create empathetic responses. Utilize expressive avatars (e.g., distinct artistic polygon styles with expressive eyes, as seen in the "We Wait" VR experience) rather than striving solely for photorealism.
  - *Reference:* ![](../../images/80a7db4e5d1dfc7a9e3e01062415096568c1451e3fb8bee50f71341e046cb8f4.jpg)

### 2. Conducting User Interviews
- **Select the Appropriate Format:**
  - *Unstructured:* Exploratory and open-ended. Use for early discovery. Maintain a topic list but allow the interviewee to steer the conversation.
  - *Structured:* Pre-determined, closed questions. Best when goals are specific and time is limited.
  - *Semi-Structured:* Combines closed and open questions with a base script. Probe gently ("Tell me more") without leading the interviewee.
- **The 5-Step Interview Process:**
  1. *Introduction:* Set expectations, verify consent.
  2. *Warm-up:* Ask straightforward demographic questions to build comfort.
  3. *Main Session:* Proceed logically, saving deep probing questions for the end.
  4. *Cooling-off:* Wind down with easy questions ("Anything else you'd like to add?").
  5. *Closing:* Express gratitude, stop recording.
- **Enrichment:** Use props (personas, scenarios, or virtual prototypes) to ground the discussion and maintain ecological validity, particularly in remote interviews.

### 3. Designing Questionnaires
- **Structure and Flow:** Group questions logically. Place relevant demographic questions at the beginning to contextualize responses. Provide clear instructions and consider pacing/dropout points.
- **Response Formats and Scales:**
  - *Ranges:* Ensure numerical ranges do not overlap (e.g., use 15–19, 20–24 instead of 15–20, 20–25).
  - *Likert Scales:* Measure agreement using clear statements. A 5-point or 7-point scale provides adequate discrimination without overwhelming the user.
  - *Semantic Differential:* Use bipolar adjectives (e.g., Confusing <--> Clear). Mix positive and negative poles across the questionnaire to prevent automatic clicking down one side.

### 4. Direct Observation in the Wild
- **Observation Frameworks:** Use structured frameworks to manage complex environments.
  - *Simple Framework:* Track **The Person**, **The Place**, and **The Thing**.
  - *Detailed Framework:* Track Space, Actors, Activities, Objects, Acts, Events, Time, Goals, and Feelings.
- **Degree of Participation:** 
  - *Passive Observer:* Complete detachment (often restricted to lab settings).
  - *Participant Observer:* Immersing oneself as an insider to gain deep contextual understanding, while striving to maintain objective observation notes.

## If/Then Troubleshooting Logic
- **IF** VR users experience disorientation or struggle with the degrees of freedom compared to GUIs, **THEN** reconsider the movement mechanics, provide clearer affordances, and optionally switch the perspective from 1st-person to 3rd-person.
- **IF** an interviewee consistently provides answers they think you want to hear (acquiescence bias), **THEN** neutralize your phrasing, monitor your body language, and triangulate their verbal responses with observed behavior logs.
- **IF** respondents frequently select the middle option of a Likert scale ("sitting on the fence"), **THEN** switch to an even-numbered scale (e.g., 4 or 6 points) to force a directional choice in subsequent iterations.
- **IF** an observation session in the wild becomes overwhelming due to unexpected activities, **THEN** immediately revert to the simple "Person, Place, Thing" framework to regain focus.

## Verification Checklists
- [ ] VR perspective (1st vs 3rd) specifically supports the primary user tasks.
- [ ] The chosen interview format (unstructured vs. structured) aligns with the specific phase of the design process.
- [ ] Questionnaire ranges are mutually exclusive and collectively exhaustive.
- [ ] Likert and Semantic Differential scales are balanced and clearly worded.
- [ ] The observation strategy clearly defines the researcher's level of participation and structural framework.
- [ ] All embedded image paths use the correct relative formatting (e.g., `../../images/img.jpg`).