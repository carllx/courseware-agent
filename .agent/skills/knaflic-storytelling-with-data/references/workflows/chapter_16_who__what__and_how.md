# Workflow: Context, Storyboarding, and Effective Visual Selection

## Prerequisites & Context
- **Why & When:** Before visualizing any data or creating content, you must clearly define *who* you are communicating to, *what* you want them to know or do, and *how* you will use data to make your point. This minimizes iterations and ensures the final communication hits its mark.
- **Dynamic Context (Deep Dives):**
  - `bash scripts/query_theory.sh "What are the theoretical impacts of cognitive load on audience perception?"`
  - `bash scripts/query_theory.sh "How does the communication mechanism continuum dictate information density?"`
  - `bash scripts/query_theory.sh "Why do tables and graphs interact differently with our verbal and visual processing systems?"`

## Comprehensive Guide & Best Practices

### 1. Define the "Who"
- **Your Audience:** Avoid general audiences (e.g., "internal and external stakeholders" or "anyone interested"). Narrow down to a specific decision-maker or group. The more specific, the better positioned you are to resonate with their needs. Sometimes this requires creating different communications for different audiences.
- **You (The Communicator):** Analyze your relationship with the audience. Do they know you? Do they trust you as an expert, or do you need to establish credibility? This impacts the order, flow, and usage of data in your story.

### 2. Define the "What"
- **Determine the Action:** Ask yourself, "What do I need my audience to know or do?" You are the subject matter expert and must confidently make specific observations and recommendations. Even an imperfect recommendation drives the conversation forward toward action.
  - *Heuristic:* Use clear action words (e.g., *accept, agree, collaborate, recommend, implement*).
- **Choose the Communication Mechanism:** Understand where your deliverable falls on the communication mechanism continuum:
  ![Communication mechanism continuum](../../images/Image00010.jpg)
  - **Live Presentation (Left):** You have full control. Keep slides sparse. They should reinforce your spoken words, not act as a teleprompter.
  - **Written Document or Email (Right):** You have less control. The document must contain higher detail to address potential questions directly.
  - **The "Slideument":** A single document attempting to serve both needs. Recognize its challenges (detailed in later sections).
- **Set the Tone:** Identify whether the tone should be celebratory, serious, urgent, etc. This will inform future design choices.

### 3. Define the "How"
- **Identify Supporting Data:** Once *Who* and *What* are clear, ask: "What data is available that will help make my point?" Data acts as evidence.
  - *Heuristic:* Do not ignore non-supporting data. Presenting a one-sided story damages credibility. Provide the right amount of context.

### 4. Consult for Context
- If creating a communication at the request of someone else, use these questions to tease out hidden context:
  - What background information is essential?
  - Who is the decision-maker? What are their biases?
  - What data is available? Is it new to the audience?
  - What factors could weaken our case?
  - What does a successful outcome look like?
  - If you had limited time (or a single sentence), what would you say?

### 5. Crafting the Core Message
- **The 3-Minute Story:** Be able to tell your audience what they need to know in exactly three minutes, without relying on slides.
- **The Big Idea:** Boil the "so-what" down to a single sentence that:
  1. Articulates your unique point of view.
  2. Conveys what's at stake.
  3. Is a complete sentence.

### 6. Storyboarding
- **Go Low Tech:** Establish the structure visually using a whiteboard, Post-it notes, or paper. Do not start with presentation software to avoid attachment to early iterations.
  ![Example storyboard](../../images/Image00011.jpg)
- Arrange and re-arrange components to explore narrative flows (e.g., leading with the recommendation vs. building up to it).
- Get early alignment with stakeholders using this rough storyboard.

### 7. Choosing an Effective Visual (Initial Guidelines)
![The visuals I use most](../../images/Image00012.jpg)
![The visuals I use most 2](../../images/Image00013.jpg)

- **Simple Text:** If you have only a number or two, use the numbers directly with a few supporting words. Do not force simple numbers into a graph (which can skew perception) or a complex table.
  *Before:*
  ![Stay-at-home moms original graph](../../images/Image00014.jpg)
  *After (Simple Text):*
  ![Stay-at-home moms simple text makeover](../../images/Image00015.jpg)
- **Tables:** Use tables when communicating to a mixed audience where individuals will look up specific rows of interest, or when dealing with multiple units of measure. Tables interact with our verbal system (we read them).
  - *Heuristic:* Fade the table design into the background. Use light borders or white space so the data stands out. Avoid tables in live presentations.
  ![Table borders](../../images/Image00016.jpg)
- **Heatmaps:** A special table case using color saturation to provide visual cues, reducing mental processing time when identifying high/low values. Always include a legend.
  ![Two views of the same data](../../images/Image00017.jpg)

## If/Then Troubleshooting Logic

- **IF** your audience is too broad, **THEN** identify the primary decision-maker and tailor the communication to them. If multiple key decision-makers have conflicting needs, split the deliverable into separate, tailored communications.
- **IF** you are uncomfortable recommending a specific action, **THEN** suggest possible next steps to prompt a productive discussion rather than leaving a blank slate.
- **IF** you are preparing for a live presentation, **THEN** practice out loud and write out speaking notes instead of placing all text on the slides. Do not read from the slides.
- **IF** you uncover data that opposes your recommendation, **THEN** address it proactively. Omitting conflicting data can destroy trust if the audience discovers it.
- **IF** you find yourself using a complex table in a live presentation, **THEN** ask what specific point you want to make, visualize that specific point, and move the full table to an appendix.
- **IF** you only have one or two key numbers to show, **THEN** avoid creating a graph and instead make the numbers prominent using Simple Text.

## Verification Checklists

- [ ] Has the specific target audience (the "Who") been identified and narrowed down?
- [ ] Have I evaluated my relationship with the audience to establish the necessary credibility?
- [ ] Is there a clear, verb-driven action I want the audience to take (the "What")?
- [ ] Has the communication mechanism (live presentation vs. written document) been decided, and is the level of detail adjusted accordingly?
- [ ] Is the intended tone clearly defined?
- [ ] Have I formulated a clear 3-minute story?
- [ ] Does the "Big Idea" articulate a unique point of view, convey what's at stake, and form a single complete sentence?
- [ ] Was the initial structure built using a low-tech storyboard (e.g., Post-it notes) before opening presentation software?
- [ ] If using simple text or tables, does the design push structural elements (like heavy borders) to the background so the data stands out?
- [ ] Are all image paths accurately referencing the relative `../../images/` directory?