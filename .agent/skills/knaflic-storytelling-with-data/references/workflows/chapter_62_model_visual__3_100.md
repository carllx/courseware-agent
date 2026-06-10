# Workflow: Advanced Stacked Bars & Storytelling Narratives

## Prerequisites & Context

Before applying these techniques, you should have a firm grasp of basic data visualization principles (context, audience, clutter removal, and basic cognitive load). This workflow covers advanced implementation of stacked bar variations (100%, positive/negative, horizontal) as well as the fundamental architecture for crafting a compelling narrative structure around your data.

**When to use this workflow:**
- When deciding between different structural models of stacked bar charts.
- When you have analyzed the data and need to build a compelling, emotion-driven narrative to present findings (especially for live presentations or self-guided reports).
- When standard bulleted facts fail to persuade your audience.

*For deep theoretical rationale on why storytelling outperforms conventional rhetoric, run:*
`bash scripts/query_theory.sh "Why is storytelling more effective than conventional rhetoric for data presentations?"`

## Comprehensive Guide & Best Practices

### 1. Advanced Stacked Bar Variations

#### A. 100% Stacked Bars (Example: Progress Against Goals)
- **Alignment:** Align the graph title, legend, and *y*-axis title in the upper-left-most position so the audience reads how to interpret the graph before hitting the data. Create a clean vertical line on the left side.
- **Focusing Attention:** Use a single attention-grabbing color (e.g., burnt red) for the critical data series. Push the rest to the background using distinct but muted shades of grey.
- **Data Labels:** Add numeric labels (with high contrast, e.g., white text on a colored bar) only on the specific points you want the audience to focus on.
- **Category Ordering:** Leverage a logical scale (e.g., "Miss" to "Exceed") from bottom to top. Place the most critical category closest to the *x*-axis to make change-over-time tracking easy via a consistent baseline.
- **Accessibility:** Use super-categories on axes to reduce redundant labeling and make the graph scannable. Include a footnote for total counts if raw numbers are masked by the 100% scale.

#### B. Positive and Negative Stacked Bars (Example: Unmet Needs vs. Attrition)
- **Eye Path Management:** Design the flow from the title, directly to large, bold numbers indicating the primary gap or unmet need. 
- **Intentional Color Logic:** 
  - Use a standard base color for the existing baseline.
  - Use a less saturated version of the base color for negative/exiting metrics (falling below the axis).
  - Use a positive color (like green) for additions.
  - Depict "unmet needs" or gaps with an outline only to visually represent empty space.
- **Deliberate Ordering:** The existing baseline sits on the horizontal axis. Negative series fall below. Additions stack above. The "gap" sits at the top to be encountered earliest in the vertical scan.
- **Axis Treatment:** Preserve the *y*-axis for magnitude context, but push it to the background using grey text. Label only the specific points requiring attention.

#### C. Horizontal Stacked Bars (Example: Survey Priorities)
- **Orientation:** Use horizontal bars when category names are long, ensuring they remain easily readable from left to right.
- **Descending Order:** Organize categories vertically in descending order of the total percentage to give the audience a clear, predictable construct.
- **Emphasizing Priorities:** Use color strategically for the top priorities. Tie the category name, total %, and the specific stacked bar segment together by using the exact same color.
- **Label Alignment:** If preserving numeric data labels within the bars, de-emphasize them via smaller text, lower-contrast colors (light blue/grey instead of white), and left-align them to create a clean vertical scanning line. You may safely eliminate the *x*-axis entirely.

*To review the exact visual case studies discussed here, see:*
`../../images/Image00096.jpg` (100% stacked bars)
`../../images/Image00097.jpg` (Positive/negative stacked bars)
`../../images/Image00098.jpg` (Horizontal stacked bars)

### 2. Crafting the Data Story

#### Step 1: Establish the Plot (The Beginning)
Set up the story to get everyone on common ground.
- **The Main Character:** Frame the story with the audience as the protagonist.
- **The Imbalance:** Introduce the conflict or problem. Why is action necessary? What has changed? "Subjective expectation meets cruel reality."
- **The Solution:** Outline how you will bring about the changes. Address the question: *"What's in it for me?"*

#### Step 2: Develop "What Could Be" (The Middle)
Retain attention by addressing how the audience can solve the problem.
- Incorporate external context, comparisons, and illustrative examples.
- Include data specifically to demonstrate the severity of the problem or the viability of the solution.
- Clearly articulate what happens if no action is taken.
- Make the information highly specific and relevant to the audience's primary motivations (e.g., saving time, increasing revenue, beating competition).

#### Step 3: End with a Call to Action (The Ending)
- Be explicit about what you want the audience to *do* with this new understanding.
- Tie the conclusion back to the dramatic tension introduced at the beginning to provide closure.

*For deep dives into narrative structure theory across different mediums, run:*
`bash scripts/query_theory.sh "What are Aristotle's and Robert McKee's foundational rules for storytelling?"`
`bash scripts/query_theory.sh "What are Kurt Vonnegut's rules for writing with style?"`

### 3. Executing Narrative Flow

- **Chronological vs. Lead with the Ending:**
  - *Chronological:* Use when you need to establish credibility, or when the audience explicitly cares about the analytical process. Follow the path of problem identification -> data gathering -> analysis -> findings.
  - *Lead with the Ending:* Start with the call to action, then back up into supporting evidence. Use when trust is established and the audience primarily cares about the "so what."
- **Live Presentations:** Utilize the voiceover to make the "so what" clear. Ensure slide text is minimal so the audience listens rather than reads. Clearly state the rules of engagement (e.g., "I will answer questions at the end").
- **Written Reports (or Slideuments):** Without a voiceover, every visual and section must explicitly state its relevance and "so what." Seek feedback from a naive reader to ensure clarity and flow.

## If/Then Troubleshooting Logic

- **If** the audience is prone to interrupting or derailing live presentations:
  - **Then** explicitly state the narrative flow upfront (e.g., "I'm going to start with our request, walk through the analysis, and leave 10 minutes for questions").
- **If** the 100% stacked bar makes it impossible to compare raw volumes between columns:
  - **Then** add a footnote with the raw "N" (total count) for each column or provide an accompanying standard bar chart if raw volume is the critical metric.
- **If** your presentation feels like a dry list of facts:
  - **Then** rewrite your slide titles to read as a cohesive story (write the headlines first on sticky notes), ensuring each slide identifies a clear conflict or proposed resolution.
- **If** you are unsure whether your visual or written report stands alone without a voiceover:
  - **Then** give it to a colleague with no context. If they cannot immediately articulate the "so what," you must add explicit text or annotations to guide them.

## Verification Checklists

### Visual Design Checklist
- [ ] Graph title, legend, and axis titles are aligned to the upper-left to prime the reader.
- [ ] Only the focal data series uses an attention-grabbing color; context data is pushed to grey.
- [ ] Categories are ordered logically (e.g., descending order by volume, or structural scale like "Miss" to "Exceed").
- [ ] Positive/Negative stacks use standard colors for baseline, less saturated colors for attrition, and distinct styling (like outlines) for gaps.
- [ ] Words are used effectively to make the visual accessible (titles, data labels, footnotes).

### Narrative Structure Checklist
- [ ] The story structure follows a clear Beginning (Imbalance/Problem), Middle (Development/Data), and End (Call to Action).
- [ ] The audience is positioned as the main character.
- [ ] The communication appeals to the specific motivations of the audience (e.g., saving money, gaining market share).
- [ ] For live presentations: The expected audience interaction and flow are established immediately.
- [ ] For written reports: The "so what" is explicitly stated on every page/section, leaving zero ambiguity.