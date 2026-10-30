Day 6 Reflection — B2D Cloud AI Knowledge Assistant
Day 6 Objective
The main goal for Day 6 was to connect a simple document retrieval system to a FastAPI application and reinforce the Python concepts used inside that retrieval logic.
By the end of the day, I was able to:
- Load multiple knowledge documents.
- Ask questions through a FastAPI endpoint.
- Return the most relevant source, context, and score.
- Handle questions that do not match any document.
- Understand how dictionaries, loops, functions, return, and score comparisons work together.
- Connect local application behavior to cloud engineering concepts like ports, processes, environment variables, and API boundaries.
What I Built
The B2D Cloud AI Knowledge Assistant currently has a small knowledge base with documents such as:
- attendance-policy.txt
- student-handbook.txt
- career-guide.txt
The application can receive a question and search through those documents for a basic keyword match.
Example request:
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Can students use phones during class?"}'
Example response:
{
  "question": "Can students use phones during class?",
  "source": "student-handbook.txt",
  "context": "Relevant content from the student handbook",
  "score": 2
}
The system can also recognize when no useful document exists.
Example:
{
  "question": "What is for lunch tomorrow?",
  "source": null,
  "context": null,
  "score": 0
}
This is important because the system should not invent an answer when the knowledge base does not contain the information.
FDE Lesson Learned
A Forward Deployed Engineer should not immediately assume that an incorrect or missing AI answer means the model is broken.
A problem can exist at several layers:
1. The request may not be reaching the server.
2. The API route may be incorrect.
3. The retrieval logic may fail.
4. The correct document may not exist in the knowledge base.
5. The AI model may receive weak or missing context.
6. The final response may still be incorrect even when retrieval works.
Day 6 helped me see the importance of checking each layer separately.
For example, if a school employee asks:
What is being served for lunch tomorrow?

and the knowledge base does not contain a lunch menu, then the correct system behavior is to return no match instead of making something up.
That is both a technical decision and an AI governance decision.
Cloud Engineering Connection
Day 6 also connected the application to several cloud concepts.
Process
Uvicorn runs the FastAPI application as a process.
Example:
python3 -m uvicorn app:app --reload
Port
The FastAPI application listens on a network port.
Example:
127.0.0.1:8000
Port 8000 is the network entry point for the local application.
Checking the Listening Process
I can verify which process is using port 8000 with:
lsof -nP -iTCP:8000 -sTCP:LISTEN
This is useful when troubleshooting whether an application is actually running and listening.
Environment Variables
An environment variable can be used to configure where the application looks for knowledge files.
Conceptually:
Local machine
        |
B2D_KNOWLEDGE_DIR
        |
FastAPI application
        |
Knowledge directory
This matters because the file path on my Mac may be different from the file path inside Docker or a cloud server.
The application should be configurable without rewriting its main logic.
Python Refresher Reflection
Dictionaries
I practiced creating a dictionary:
document = {
    "source": "attendance-policy.txt",
    "score": 2
}
I accessed individual values using their keys:
print(document["source"])
print(document["score"])
Output:
attendance-policy.txt
2
A dictionary lets me group related information together using keys and values.
For the B2D assistant, a retrieval result can contain information such as:
{
    "source": "student-handbook.txt",
    "score": 4
}
Functions and Return Values
I practiced creating a function:
def build_result(source, score):
    result = {
        "source": source,
        "score": score
    }

    return result
Then I called it:
answer = build_result("student-handbook.txt", 3)

print(answer)
Output:
{'source': 'student-handbook.txt', 'score': 3}
The main difference I learned is:
print()
= display something on the screen

return
= send a value back to the code that called the function
This is important because FastAPI needs retrieval functions to return information that the API can use.
Lists of Dictionaries
I practiced using a list containing multiple dictionaries:
results = [
    {"source": "attendance-policy.txt", "score": 2},
    {"source": "student-handbook.txt", "score": 4},
    {"source": "career-guide.txt", "score": 1}
]
Each item in the list represents one retrieval result.
Loops
I practiced going through the list one item at a time:
for result in results:
    print(result)
I also practiced printing only one value from each dictionary:
for result in results:
    print(result["source"])
Output:
attendance-policy.txt
student-handbook.txt
career-guide.txt
The variable result represents one dictionary from the list during each loop.
Finding the Best Result
I practiced comparing scores:
best_score = 0
best_result = None

for result in results:
    if result["score"] > best_score:
        best_score = result["score"]
        best_result = result
With these results:
[
    {"source": "attendance-policy.txt", "score": 2},
    {"source": "student-handbook.txt", "score": 4},
    {"source": "career-guide.txt", "score": 1}
]
the final best result is:
{'source': 'student-handbook.txt', 'score': 4}
The logic works like this:
Start with best_score = 0

See score 2
2 > 0
Remember score 2

See score 4
4 > 2
Remember score 4

See score 1
1 > 4 is false
Keep score 4
This is the same basic idea the retrieval system uses to select the best matching document.
Handling No Match
I also tested this case:
results = [
    {"source": "attendance-policy.txt", "score": 0},
    {"source": "student-handbook.txt", "score": 0},
    {"source": "career-guide.txt", "score": 0}
]
Because the comparison is:
if result["score"] > best_score:
and best_score starts at 0, every comparison becomes:
0 > 0
which is false.
So:
best_result
remains:
None
This is useful because None can represent:
No useful match was found.

For the B2D assistant, this is safer than returning an unrelated document.
Customer Scenario Reflection
A school staff member asks:
What is for lunch tomorrow?

The system searches the current knowledge base but finds no relevant document.
A good FDE explanation to the customer would be:
The application is working correctly, but the requested information is not currently available in the approved knowledge base. Instead of inventing an answer, the system returns no result. To support this question, an approved lunch or meal schedule would need to be added to the knowledge source.

This shows that the problem is not always the AI model.
Sometimes the missing piece is simply the data.
What I Understand Better After Day 6
I now understand that:
- A dictionary stores related values using keys.
- A list can contain multiple dictionaries.
- A loop checks one list item at a time.
- A function can return structured data.
- return and print have different purposes.
- A score can be used to compare multiple search results.
- best_score remembers the strongest score seen so far.
- best_result remembers which document produced that score.
- None can represent that no useful result was found.
- FastAPI can expose retrieval logic through an API.
- A port is where the application listens for network requests.
- A running server process can be inspected with tools like lsof.
- Environment variables help separate configuration from application logic.
- A reliable AI system should be able to say that it does not have enough information.
Day 6 FDE Takeaway
The biggest lesson from Day 6 is:
Before blaming the AI model, trace the request through the system and verify the data, retrieval logic, API, server process, and network behavior.

As a Forward Deployed AI Engineer, I need to understand both the AI layer and the infrastructure around it.
The goal is not only to make the assistant answer questions.
The goal is to build a system that is:
- understandable,
- testable,
- reliable,
- configurable,
- safe when information is missing,
- and eventually deployable to the cloud.
Current B2D Cloud AI Knowledge Assistant Progress
Current flow:
User question
      |
      v
FastAPI POST /ask
      |
      v
search_documents()
      |
      v
Load knowledge documents
      |
      v
Tokenize question + documents
      |
      v
Compare matching words
      |
      v
Calculate scores
      |
      v
Choose best result
      |
      v
Return source + context + score
No LLM is required yet.
This is intentional because it allows me to understand and test retrieval before adding model complexity.
Next Step
The next logical step is to improve retrieval without making the system too complicated.
Possible Day 7 direction:
1. Break larger documents into smaller passages or chunks.
2. Create a small set of test questions with expected sources.
3. Measure whether retrieval selects the correct source.
4. Introduce the idea of evaluation before introducing more advanced RAG or an LLM.
5. Continue building toward Docker and cloud deployment after the local application behavior is reliable.