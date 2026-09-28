# Day 3 — Building AI Applications with Foundation Models

**FDE learning journey | Reading notes**

## Main takeaway

A powerful model makes a demo possible. A Forward Deployed Engineer (FDE) makes the application useful, reliable, and safe in the customer's real workflow. Start with the customer's problem, measure a baseline, build a focused pilot, and evaluate the complete system.

## Key concepts

| Concept | Plain-English meaning | Why an FDE cares |
| --- | --- | --- |
| Foundation model | A general-purpose model that can perform many tasks. | Start with an available model and adapt it to the customer's problem. |
| Tokens | Pieces of text that a model processes and generates. | Input and output length affect cost, response time, and available context. |
| Probabilistic output | The model's response is generated from learned patterns; accuracy is not guaranteed. | Plan for incorrect answers and uncertainty. |
| Self-supervision | Training where examples supply their own prediction targets, such as the next token in text. | Explains how language models could learn from large amounts of data without manually labeling every example. |
| Prompting and context | Instructions and relevant information supplied in a request, without changing model weights. | Often the simplest place to improve an application. |
| RAG | Retrieve relevant information and provide it to the model as context. | Helps an assistant use the customer's approved documents. |
| Fine-tuning | Further training that changes model weights. | Consider when simpler adaptation methods do not meet a measured requirement. |
| Evaluation | Testing the application against representative tasks and failure cases. | Determine whether the system is ready for real users and whether changes help. |

**Vocabulary check:** Supplying documents in a prompt or through RAG is not training the model. Fine-tuning changes model weights.

## How this becomes FDE work

1. **Discover the problem.** Identify the users, their current workflow, time-consuming steps, data sources, and consequences of mistakes.
2. **Check whether AI fits.** Compare an AI feature with simpler search, rules, forms, or existing products. Consider building versus buying.
3. **Define a baseline.** Measure the current process so that improvement means something.
4. **Build a small pilot.** Use a model, instructions, necessary context, and an interface that fits the workflow.
5. **Evaluate the whole application.** Track answer quality, latency, cost, user satisfaction, and important failure cases.
6. **Plan for operation.** Decide how people review errors, give feedback, update source material, and handle changes to models or requirements.

The chapter's **last-mile challenge** is especially relevant: a first demo can work quickly, while handling unusual requests, permissions, incorrect outputs, and day-to-day operations takes much longer.

## Example: A school district policy assistant

**Customer request:** “We want an AI assistant to answer questions about our policies.”

### Discovery questions

- Which questions take staff the most time to answer today?
- Where do approved policies live, and who keeps them current?
- Is the assistant for staff, students, families, or some combination?
- Which questions require a person to make a decision?
- What information may the assistant access, and who may see each document?
- What outcome matters most: fewer repetitive tickets, faster answers, or better staff satisfaction?

### Possible first pilot

Answer a narrow set of staff questions using approved documents. Show the source document for each answer. When the answer is missing or sensitive, direct the user to the right person instead of guessing.

### Example evaluation measures

| Measure | What to check |
| --- | --- |
| Answer quality | Is the answer supported by the cited policy and useful to the staff member? |
| Appropriate escalation | Does the assistant hand off questions that need human judgment or lack a reliable source? |
| Speed | How long does an answer take compared with the current workflow? |
| Cost | What does each answered question cost to process? |
| Staff experience | Do staff trust the answer and know what to do next? |

## Three layers of the AI application stack

1. **Application:** interface, instructions, retrieved context, workflow, and evaluation.
2. **Model:** the model's capabilities, adaptation, and inference behavior.
3. **Infrastructure:** deployment, data access, serving, monitoring, and reliability.

As an FDE, you may work across all three, even when you do not train a model. Your web development experience is useful for turning a model capability into a usable product and iterating with customer feedback.

## Study priorities

**Learn deeply now:** customer discovery, Python APIs, prompting and RAG, evaluation sets, data permissions, deployment, logging, and explaining tradeoffs.

**Understand at a working level:** self-supervised learning, tokenization, architecture, fine-tuning, and inference optimization. Know when these affect a design decision; training a foundation model is not a prerequisite for this project.

## Day 3 practice assignment

Write a one-page proposal for the school policy assistant under these headings:

1. Customer problem
2. Current baseline
3. Proposed pilot
4. Success measures: quality, speed, cost, and staff experience
5. Failure handling and human handoff

**Checkpoint:** Be able to explain why you chose this narrow pilot, how you would test it with real staff questions, and what evidence would make you expand or stop it.

## Reflection questions

1. Why doesn't a convincing demo prove that an AI application is ready to deploy?
2. When would you retrieve district documents instead of fine-tuning a model?
3. What would you measure before and after introducing the assistant?
4. Which answers should always go to a human?
5. Which parts of this project draw on your existing full-stack skills?

---

*Source: the Chapter 1 text you shared, “Introduction to Building AI Applications with Foundation Models.” These are study notes and an FDE application exercise, not a verbatim copy of the chapter.*
