# Workflow: Transitioning from Showing Data to Storytelling with Data

## Prerequisites & Context

**Why this workflow is necessary:**
Bad graphs are ubiquitous because traditional education focuses on language (sentences) and math (numbers) independently, but rarely teaches us how to pair them to tell stories. As technology has made data and graphing tools globally accessible, there is a dangerous reliance on tool defaults. Being merely "proficient in Microsoft Office" is no longer enough; the true differentiator is the ability to extract the signal from the noise and tell a compelling story. 

**When to use this workflow:**
Trigger this workflow when you have completed your data analysis and are preparing to present it to an audience (e.g., stakeholders, leadership, or clients). It is the critical bridge between analyzing data and communicating findings.

> **Deep Dive for Runtime Agents:**
> To understand the foundational theories driving this approach, execute:
> - `bash scripts/query_theory.sh "Why aren't we naturally good at storytelling with data?"`
> - `bash scripts/query_theory.sh "What is the distinction between exploratory and explanatory analysis?"`

---

## Comprehensive Guide & Best Practices

### 1. Shift from Exploratory to Explanatory Analysis
The most common mistake in data visualization is presenting **exploratory** analysis (the process of understanding the data) instead of **explanatory** analysis (the process of communicating the findings). 
- **The Oyster and Pearl Metaphor:** Exploratory analysis is opening 100 oysters to find two pearls. Explanatory analysis is presenting *only those two pearls* to your audience. Do not force your audience to reopen all 100 oysters. Resist the urge to show all your work just to prove its robustness.
- **Actionable Heuristic:** Before building any slide or chart, ask: "Am I showing the oysters or the pearl?"

### 2. Transcend Tool Defaults
Pretty much anyone can put data into Excel and generate a chart. But tools do not know your story.
- **Actionable Heuristic:** Never accept a tool's default settings at face value. Actively strip away bad defaults (e.g., 3D effects, meaningless colors, pie charts). You—the analyst—must bring the story visually and contextually to life.
- *For deeper rationale, run:* `bash scripts/query_theory.sh "Why are tool defaults dangerous for data visualization?"`

### 3. Master the 6 Core Lessons of Storytelling
To effectively shift from simply showing data to storytelling with data, apply these six sequential lessons:
1. **Understand the context:** Know who your audience is, what you need them to do, and how you will communicate it.
2. **Choose an appropriate visual display:** Select the right chart for the right data.
3. **Eliminate clutter:** Reduce cognitive load by removing extraneous elements.
4. **Focus attention where you want it:** Use preattentive attributes (like size and color) strategically.
5. **Think like a designer:** Ensure form follows function (affordances, accessibility, aesthetics).
6. **Tell a story:** Construct a narrative with a clear beginning, middle, and end.
- *For deep dives into these pillars, run:* `bash scripts/query_theory.sh "What are the 6 key lessons of storytelling with data?"`

### 4. Generalize Across Domains and Tools
The principles of effective data visualization are fundamental and agnostic. Whether you work in finance, HR (e.g., Google's Project Oxygen), education, or technology, the same rules apply. Focus on the core principles rather than the specific software being used.

### Visual Evolution: From Showing to Storytelling
Examine these before-and-after transformations to understand the visual shift:

![A sampling of ineffective graphs](../../images/Image00003.jpg)
*Figure 0.1: A sampling of ineffective graphs.*

**Example 1 Transformation:**
![Example 1 (before): showing data](../../images/Image00004.jpg)
![Example 1 (after): storytelling with data](../../images/Image00005.jpg)

**Example 2 Transformation:**
![Example 2 (before): showing data](../../images/Image00006.jpg)
![Example 2 (after): storytelling with data](../../images/Image00007.jpg)

**Example 3 Transformation:**
![Example 3 (before): showing data](../../images/Image00008.jpg)
![Example 3 (after): storytelling with data](../../images/Image00009.jpg)

---

## If/Then Troubleshooting Logic

- **IF** your audience asks to "show the data" and you feel overwhelmed by the pressure to show everything, **THEN** remember the oyster and pearl metaphor. Explicitly pivot to explanatory analysis. Extract the actionable insights (the pearls) and place the exhaustive exploratory data (the oysters) in an appendix.
- **IF** you are relying solely on tool defaults (e.g., standard Excel charts), **THEN** actively intercept the process. Explicitly review and strip away unnecessary clutter to ensure the visual serves your specific narrative, not the software's generic template.
- **IF** you are facing mixed audiences where technical stakeholders (like engineers) demand exhaustive details while executives need high-level summaries, **THEN** structure the communication to appease detailed reviewers without muddying the clean, explanatory narrative for leaders.
  - *To see how this was handled at Google, run:* `bash scripts/query_theory.sh "How did Project Oxygen balance detailed methodology with big-picture findings?"`

---

## Verification Checklists

- [ ] Have I completed the exploratory phase and firmly transitioned to the explanatory phase?
- [ ] Am I showing only the "pearls" (insights) rather than all the "oysters" (the raw analysis process)?
- [ ] Have I explicitly defined the story I want to tell before opening my graphing tool?
- [ ] Did I actively override the default settings in my graphing software to eliminate bad practices (e.g., 3D, pie charts, unnecessary borders)?
- [ ] Is my data visualization tailored to my specific audience's needs rather than acting as a generic data dump?
- [ ] Have I applied the 6 core lessons (context, visual display, clutter removal, attention focus, design thinking, storytelling)?