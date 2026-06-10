# Lean UX Workflow: Creating and Testing MVPs & Prototypes

## Prerequisites & Context
* **When to use:** Use this workflow when you need to test hypotheses, evaluate business ideas, or gauge customer demand before investing in heavy engineering efforts.
* **Why it matters:** Building full products is risky and expensive. MVPs and prototypes help you quickly navigate uncertainty, search for value propositions that resonate with customers, and collaborate cross-functionally to achieve continuous innovation.
* **Core Philosophy:** We are not in the business of deliverables; we are in the business of delighting customers. Stop wasting time arguing over specifications and start experimenting.
* **For deep theoretical background, run:**
  `bash scripts/query_theory.sh "What is the core philosophy and rationale behind Lean UX MVPs according to the authors?"`
  `bash scripts/query_theory.sh "How do silos and linear organizations hinder continuous innovation and how does Lean UX solve this?"`

## Comprehensive Guide & Best Practices

### 1. Selecting the Right MVP Approach
Before prototyping the entire product experience, focus on the core workflows that let you test the biggest risks in your hypothesis. Select an MVP approach based on what you need to learn.

**A. Landing Page Test**
*   **Goal:** Measure demand and validate if you should invest in building the idea.
*   **Execution:** Create a marketing page with a clear value proposition, a call to action, and a conversion tracking metric.
*   **Traffic:** Drive relevant traffic via existing workflows or online advertising to gather a large enough sample size.
*   **Deep Dive:** `bash scripts/query_theory.sh "What are the key elements and success criteria of a Landing Page MVP?"`

**B. Feature Fake (The Button to Nowhere)**
*   **Goal:** Measure interest in a feature where the cost of implementation is very high.
*   **Execution:** Provide an HTML button or call to action that gives the illusion the feature exists. When clicked, alert the user that the feature is "coming soon."
*   **Caveat:** Use sparingly. Take down as soon as the success threshold is met to avoid damaging customer relationships (offer compensation if needed).
*   **Deep Dive:** `bash scripts/query_theory.sh "How to ethically implement a Feature Fake MVP without alienating users?"`

**C. Wizard of Oz MVP**
*   **Goal:** Figure out the mechanics and business processes of your product after proving demand.
*   **Execution:** Present a fully functioning digital service to the user, but handle the data processing and communication manually behind the scenes (e.g., using a Trello board as a "database" and manually emailing users).
*   **Deep Dive:** `bash scripts/query_theory.sh "What are real-world examples (like Taproot Plus or Amazon Echo) of Wizard of Oz MVPs in practice?"`

### 2. Prototyping Techniques
Choose your prototyping technique based on who will interact with it, what you hope to learn, what you already know, and the time available. Only prototype the necessary parts.

*   **Paper Prototypes:**
    *   *Best for:* Quick, crafty simulation of high-level structure and flow.
    *   *Guidelines:* Use paper, pens, and tape. Great for internal touch interface ideation.
*   **Low-Fidelity On-Screen Mock-Ups:**
    *   *Best for:* Clickable wireframes to assess the findability of core elements and major workflow obstacles.
    *   *Guidelines:* Use digital input mechanisms to provide a realistic feel of the workflow without getting bogged down in visual details.
*   **Middle- and High-Fidelity On-Screen Prototypes:**
    *   *Best for:* Demonstrating and testing visual design, brand elements, and realistic interactions.
    *   *Guidelines:* Build pixel-perfect simulations. Note that interactivity is still somewhat limited since users can't interact with real data.
*   **No-Code MVP:**
    *   *Best for:* Rapidly testing functionality without custom software development.
    *   *Guidelines:* Wire together tools (e.g., Airtable, Zapier, Webflow) to deliver functionality and value, focusing on differentiating features over infrastructure.
*   **Coded and Live-Data Prototypes:**
    *   *Best for:* High realism, A/B testing, and testing with real customers using live data.
    *   *Guidelines:* Build in the native environment. Avoid the temptation to perfect the code before releasing it to customers.

### 3. Demos and Previews
*   **Internal Sharing:** Test with colleagues, teammates, and stakeholders. Take it to the lunch area or a demo day to gather insights and validate investment.
*   **External Validation:** Take the prototype to potential customers. Let them click through the experience and collect their raw feedback.

## If/Then Troubleshooting Logic

*   **If a Landing Page Test yields negative results (no conversions)...**
    *   **Then:** Do not immediately assume the idea has no value. Reevaluate your storytelling and value proposition messaging. Iterate the page and run another quick test.
*   **If you fear user backlash from a Feature Fake MVP...**
    *   **Then:** Monitor click-through rates closely. Once the statistical threshold is reached, remove the fake immediately. Offer a small gift card or apology to users who interacted with it to preserve trust.
*   **If stakeholders demand high fidelity but the core workflow is still unresolved...**
    *   **Then:** Resist jumping to Coded or High-Fidelity prototypes. Use Paper or Low-Fidelity prototypes internally first to align on flow, and explain to stakeholders that early fidelity focuses purely on structure, not presentation.
    *   *Reference:* `bash scripts/query_theory.sh "How to manage stakeholder expectations regarding prototype fidelity in Lean UX?"`
*   **If the team gets bogged down debating the code of a Live-Data Prototype...**
    *   **Then:** Remind the team that it is a simulation meant for learning, not a production release. Time-box the development and push it to users even if the code isn't "perfect."

## Verification Checklists

**MVP Selection Checklist:**
- [ ] Is the primary risk related to demand, functionality, or business process?
- [ ] Have you chosen the MVP type (Landing Page, Feature Fake, Wizard of Oz) that directly tests your riskiest assumption with the least effort?
- [ ] Is there a clear metric defined for success or failure before launching the MVP?

**Prototyping Checklist:**
- [ ] Is the intended audience for the prototype clearly defined (e.g., engineers, stakeholders, customers)?
- [ ] Does the prototype focus only on the core workflows needed to test the hypothesis, omitting unchanged areas (like global navigation if testing a sub-feature)?
- [ ] Are you using the lowest fidelity necessary to learn what you need to know?
- [ ] Have you planned internal demos (teammates, demo days) before external customer testing?