# Day 7 Customer Scenario

## Customer Report

A teacher asks:

"Are cellphones allowed?"

The school handbook contains the phone policy, but the retrieval system does not return the handbook.

## Expected Result

student-handbook.txt

## Actual Result

None

## Evaluation Result

FAIL

## Why It Failed

The current retrieval system relies on matching words.

The question uses the word "cellphones", while the handbook uses the word "phones".

A human understands that these words are related, but the current retrieval system does not understand that relationship.

## Customer Impact

The correct information exists in the knowledge base, but a user may not receive it if they phrase their question differently.

## Current Safe Behavior

The system returns no result instead of inventing an answer.

## Future Improvement

Improve retrieval so that it can handle similar words and different ways of asking the same question.