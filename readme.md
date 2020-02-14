# q-a-bot
Created by Dr. Qiang Hao and Nathan Tresham of Western Washington University

## Configuring virtual environment 
This project uses the python package `virtualenv` and Python 3. To configure the virtual environment, run `python3 -m venv <virtual environment name>`. Then, run `source <virtual environment name>/bin/activate` to start the virtual environment, and `deactivate` to stop it.

## Installing dependencies
use `pip install -r requirements.txt` to install dependencies.

You will have to download NLTK stopwords using the NLTK downloader. To do this, begin the Python shell with `python3`. Then, run `import nltk; nltk.download('stopwords')`.

## Running tests
use `python -m unittest tests.py` to run unit tests.

## Overview (as of 12/16)

`main.py` is the entry point of the program. It can be ran from the command line with `python main.py`. The program then iterates through every file in the `bots/` directory, updating each bot (represented as a JSON file) by calling the function `update_term_data` in `bot.py`, which is where all bot functions are located.

Each bot is represented as JSON file, of which the layout is as follows:
```
{
	"name": "CSCI 145 Helper",
	"login": {
		"email": "treshan@wwu.edu",
		"password": "aKWY34#CKH#X"
	},
	"terms": ["jmccf6d1kva4x4"],
	"data": {
        "folders": {
            "lab1": 1,
            "midterm1": 1
        },
		"questions": [
			{
				"id": 2,
				"term": "term...",
				"folders": ["lab1", "midterm1"],
				"title": "How do you...",
				"content": "make the thing happen?",
				"author": "Nathan Tresham",
				"created": "date & time",
				"responses": [
					{
						"author": "Nathan Tresham",
						"content": "just make it happen!",
                        "instructor_answer": false,
                        "instructor_endorsed": false
					},
					{
						"author": "Nathan Tresham",
						"content": "I agree with the person above me",
                        "instructor_answer": false,
                        "instructor_endorsed": false
					}
				]
			}
		]
	}
}
```

Each bot can only be used for one course (e.g. CS 101, CS 200, etc.) and has a list of 'terms', or the different sections of a course offered (e.g. the Piazza 'course' IDs for Fall 2018, Spring 2020, etc.). Currently, a bot only appends Piazza posts to the `questions` object, so the program must be ran with the `--clean` flag. Ideally, the bot will...
1. organize question data better, such that we don't have to perform a brute-force search every time we want to find a post with a given tag,
2. not have to delete all previous data every time the program is ran, and 
3. only poll the Piazza website for posts and terms that we know need to be updated; i.e., if the total number of posts and replies in the CSCI 145 Fall 2019 is the same as the last time we ran the program, we know that there are no updated needed.

`matcher.py` is where all matcher-related functions are located. Currently, the only defined function is `clean`, which (badly) strips text of all HTML fragments left from the unofficial Piazza API query results, unprintable characters, and general nonsense that isn't needed to process the question. Obviously, this file is where the most interesting parts of the project will be located. The file should contain a function called `questions_match`, which returns whether or not two questions are the same by metrics to be created in the future.

Given all specifications above, the bot will operate by first updating its post data. For each new question, the bot will iterate through all of the questions in the same folder(s) marked as answered, and if it finds a question that has been answered, it will post the response marked as either an instructor answer or a student response endorsed by one.