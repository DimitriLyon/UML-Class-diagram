# UML-Class-diagram
A python script that generates the fields to go into a uml class diagram automatically based on java code.

Just put it in a folder with your .java files and run it.
---
### Known Issues/TODO:
1. It does not detect interfaces.
2. Multi line method headers are not detected.  Both the opening and closing parenthesis must be present on the same line for the code to detect a method header.
3. Script does not detect the "throws" keyword.
4. Script does not detect the "implements" keyword.
