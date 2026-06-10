# Workflow: Six Key Issues in Data Gathering

## Prerequisites & Context
**When to Use This Workflow:**
This workflow serves as a mandatory foundational checklist when planning any data gathering activity (such as interviews, direct observations, or questionnaires) within user research or interaction design. It ensures that the study is methodologically sound, ethically compliant, and practically feasible.

**Deep Dive Context:**
To explore the theoretical principles underpinning data triangulation, sampling methodologies, or the legal frameworks (such as GDPR) guiding ethical data storage, use the dynamic query script:
```bash
bash scripts/query_theory.sh "What are the six key issues of data gathering and their theoretical grounding in Chapter 8.2?"
```

## Comprehensive Guide & Best Practices

### 1. Setting Goals
- Determine the explicit reason for gathering data (e.g., evaluating a new interface design, understanding family technology use).
- **Formal vs. Exploratory:** 
  - For formal experiments (like A/B testing), define strict mathematical metrics. 
  - For exploratory studies, establish a clear objective so it is obvious when the data gathering goal has been met.

### 2. Identifying Participants & Sampling
- **Defining the Population:** Clearly outline the profile of your target users.
- **Sampling Methods:**
  - *Probability Sampling:* Use simple random or stratified sampling when you need to apply statistical tests and generalize findings to the whole population.
  - *Non-Probability Sampling:* Use convenience sampling, snowball sampling, or crowdsourced volunteer panels (e.g., Mechanical Turk, Prolific) for rapid, flexible feedback where statistical generalization is not the primary goal.
- **Sample Size:** Rely on cost constraints, accepted field guidelines, or *saturation* (continuing to gather data until no new relevant information emerges).

### 3. Relationship with Participants
- **Informed Consent:** Always provide a project information sheet. Capture written or oral consent ensuring participants know the purpose of the study, how their data will be used, and their right to withdraw without penalty at any time.
- **Building Rapport:** Foster a relaxed, professional environment. When working with unique communities or remote groups, invest time upfront to understand sociocultural communication norms to build trust.
- **Incentives:** Tailor compensation to match the specific motivations and contexts of the target demographic.

### 4. Ethical Considerations & Data Storage
- **Data Capture:** Be cautious when using recording equipment (smartphones, webcams) in public spaces to avoid incidental privacy breaches.
- **Data Security:** Ensure data storage complies with relevant jurisdictions (e.g., GDPR in the EU/UK).
  - *Best Practices:* Anonymize personal details, store participant names separately from their data, use locked physical storage, and strictly encrypt digital records and laptops.

### 5. Triangulation
- Enhance the validity of your findings by investigating from multiple perspectives.
- **Methodological Triangulation:** Use more than one data gathering technique (e.g., combining ethnographic observation with structured questionnaires).
- **Other Dimensions:** Employ *Data* triangulation (different sources/times), *Investigator* triangulation (multiple researchers), or *Theoretical* triangulation.
- **Ground Truth Verification:** Be skeptical of treating self-reported data as absolute ground truth. Validate subjective perceptions against objective behavioral or physiological data.

### 6. Pilot Studies
- Always conduct a pilot study (a small-scale trial run) of your methodology and technology. This crucial step uncovers confusing questionnaire wording, technical glitches, or overlooked ethical issues before launching the main study.

## If/Then Troubleshooting Logic
- **IF** you cannot easily access the entire target population, **THEN** determine if the goal requires strict statistical significance. If yes, implement stratified sampling; if no, crowdsourcing or convenience sampling is acceptable.
- **IF** remote participants seem hesitant or withdrawn, **THEN** pause formal data collection. Dedicate time to informal socialization (or preliminary non-recorded meetings) to build rapport and trust.
- **IF** self-reported survey data contradicts observed behavioral logs, **THEN** rely on methodological triangulation to investigate the discrepancy—do not automatically assume the self-report is accurate.
- **IF** collecting data in a busy public or shared environment, **THEN** implement strict anonymization protocols during capture to prevent the unauthorized recording of non-participants.

## Verification Checklists
- [ ] Clear, testable, and actionable goals have been defined for the study.
- [ ] The sampling method directly matches the desired level of statistical rigor.
- [ ] Informed consent protocols (written or oral) are prepared, clear, and legally compliant.
- [ ] A Data Management Plan is in place ensuring storage is secure, encrypted, and anonymized.
- [ ] A triangulation strategy is planned to cross-verify findings from multiple angles.
- [ ] A pilot study has been scheduled prior to main data collection.
- [ ] All required reference images (e.g., `../../images/figure8_2_consent.jpg`) correctly use relative paths.