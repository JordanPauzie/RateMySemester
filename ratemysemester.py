import threading
import time

from scraper import UniversityProfessorData
from collections import deque

class RateMySemester:
    def __init__(self, id):
        self.id = id
        self.courses = None
        self.data = None
        self.prof_dict = None

    def run(self):
        self.courses = self.process_inputs()
        prof = {cls[1] for cls in self.courses}
        self.data = UniversityProfessorData(self.id, prof)

        # Start a concurrent thread that allows for loading screen to run on the terminal while the scraping process is ongoing
        loading_thread = threading.Thread(target=self.loading_screen)
        loading_thread.start()

        # Begin scraping
        self.prof_dict = self.data.scrape_professors()
        
        # End the loading screen when all of the professor data has been scraped
        loading_thread.join()
        
        self.semester_rating()

    def process_inputs(self):
        process = True
        # Tuple stores name of the course taken and which professor is teaching
        courses = set()

        while process:
            cls = input("What course will you be taking? ")
            prof = input("And what professor is teaching the course? Please answer using the format [First Name] [Last Name]. ")
            crs = (cls, prof)

            courses.add(crs)

            print("You have inputted the following courses:")

            for course in courses:
                print(course[0], course[1])
            
            correct = True
            valid = {"Y", "N"}

            while correct:
                ans = input("Do you still want to add more courses? Please answer with Y or N. ")

                if ans not in valid:
                    print("Please input a valid answer")
                else:
                    if ans == "N":
                        process = False
                        
                    correct = False   

        print("Thank you, your semester will now be analyzed.")
        
        return courses

    def semester_rating(self):
        # Used a stack to process each course/professor tuple sequentially
        stack = deque(self.courses)
        rating_sum = 0
        difficulty_sum = 0
        num = 0
        highest_rated = (None, 0)
        lowest_rated = (None, float('inf'))
        highest_difficulty = (None, 0)
        lowest_difficulty = (None, float('inf'))

        while stack:
            cls, prof = stack.pop()
            # If-else clause because there is chance that a professor's name was not recognized as part of the university 
            # (for various reasons) and resulted in no data being found
            if prof in self.prof_dict.keys():
                # Extract Professor object from map if professor's name has data linked to it
                professor = self.prof_dict[prof]
                rating = professor.rating
                difficulty = professor.difficulty

                if rating > highest_rated[1]:
                    highest_rated = (prof, rating)

                if rating < lowest_rated[1]:
                    lowest_rated = (prof, rating)

                if difficulty > highest_difficulty[1]:
                    highest_difficulty = (prof, difficulty)

                if difficulty < lowest_difficulty[1]:
                    lowest_difficulty = (prof, difficulty)

                print("Course:", str(cls) + ",", "Professor:", str(prof) + ",", "Rating:", str(rating) + ",", 
                      "Difficulty:", str(difficulty) + ",", "Would take again:", str(round(professor.retake, 2)) + "%")
                # Keep track of total rating/difficulty sums and number of professors with data in order to compute average later
                rating_sum += rating
                difficulty_sum += difficulty
                num += 1
            else:
                print(prof, "not found")

        print("\n")

        avg_rating = round(rating_sum / num, 2)
        avg_difficulty = round(difficulty_sum / num, 2)

        print("Your average professor rating is", avg_rating)
        print("Your average professor difficulty is", avg_difficulty, "\n")

        print("Your highest rated professor is", highest_rated[0], "with a rating of", highest_rated[1])
        print("Your lowest rated professor is", lowest_rated[0], "with a rating of", lowest_rated[1], "\n")

        print("Your hardest professor is", highest_difficulty[0], "with a rating of", highest_difficulty[1])
        print("Your easiest professor is", lowest_difficulty[0], "with a rating of", lowest_difficulty[1])

        return
    
    def loading_screen(self):
        # Continue loading screen until self.prof_dict is no longer None which means that the scraping process has completed
        while self.prof_dict is None:
            # Print • in intervals of 0.5 seconds or 500 milliseconds to create a loading animation
            print("•", end="", flush=True)
            time.sleep(0.5) 
        print("\n")

if __name__ == '__main__':
    tufts = RateMySemester(1040)
    tufts.run()