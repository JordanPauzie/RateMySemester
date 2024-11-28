# RateMySemester
Python class that assesses your semester's difficulty in respect to the professors teaching your courses. This is done by scraping through Rate My Professor data and returning important statistics about your professors.
### Initialization
In order to use RateMySemester for a specific university, you need to initialize it with its corresponding Rate My Professor university ID.
```python
tufts = RateMySemester(1040)
```
This ID number can be found by visiting the Rate My Professor page for your university and checking the URL
```html
https://www.ratemyprofessors.com/school/1040
```
### Running the program
To run the program, use the following function
```python
tufts.run()
```
This subsequently prompts you to begin inputting the course you'll be taking for the semester. Each course is read in individually and you will be given the option to input more if desired.
```
What course will you be taking? HIST 53 
And what professor is teaching the course? Please answer using the format [First Name] [Last Name]. David Proctor
You have inputted the following courses:
HIST 53 David Proctor
Do you still want to add more courses? Please answer with Y or N.
```
After inputting all of your professors and their respective courses, your semester statistics will be outputted.
```
Course: MATH 65, Professor: Kim Ruane, Rating: 4.8, Difficulty: 2.8, Would take again: 89.47%
Course: MATH 165, Professor: Loring Tu, Rating: 4.6, Difficulty: 2.8, Would take again: 100.0%
Course: CS 40, Professor: Mark Sheldon, Rating: 3.4, Difficulty: 3.7, Would take again: 59.55%
Course: HIST 53, Professor: David Proctor, Rating: 4.9, Difficulty: 2.4, Would take again: 94.57%


Your average professor rating is 4.42
Your average professor difficulty is 2.93 

Your highest rated professor is David Proctor with a rating of 4.9
Your lowest rated professor is Mark Sheldon with a rating of 3.4 

Your hardest professor is Mark Sheldon with a rating of 3.7
Your easiest professor is David Proctor with a rating of 2.4
```
