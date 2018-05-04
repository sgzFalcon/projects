# Quiz suit

Use `quizCreator.py` to create or modify your quizes, data is stored in `data` folder. The quiz created are of the type *advanced* see below.

Use `quiz.py` to take the quizes. It supports two types *standard* where no progress is saved, questions are displayed randomly and only admits one
kind of questions (i.e. capitals of states). The second type is *advanced*, now correct answers and tries are registered and stored, questions are
displayed following the degree of knowledge and it can have several kinds of questions (i.e. capitals of states, persons, years...). You need **at least 
four** questions of each kind for this mode to work properly.

In the `data`folder you have one file of each type:
* Standard: `test.json`
* Advanced: `test2.json`