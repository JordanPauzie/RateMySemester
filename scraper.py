import re
import requests
import json
import math

from professor import Professor

class UniversityProfessorData:
    def __init__(self, id, prof):
        self.id = id 
        self.prof = prof

    def scrape_professors(self):
        # Python dictionary will store the professors' scraped Rate My Professor data
        prof_dict = dict()
        # Eliminate case-sensitivity by converting all names into lowercase
        prof_set = set([name.strip().lower().replace(" ", "") for name in self.prof])
        seg = [
            "http://www.ratemyprofessors.com/filter/professor/?&page=", 
            "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
        ]
        num_prof = self.num_professors(self.id)
        num_pages = math.ceil(num_prof / 20) + 1
        
        for i in range(1, num_pages):
            # If anything fails, throw an exception
            try:
                # Get request for page
                page = requests.get(seg[0] + str(i) + seg[1] + str(self.id), timeout=5)
                page.raise_for_status()
                # Parse JSON string into Python dictionary
                json_page = json.loads(page.content)

                for prof in json_page["professors"]:
                    first = prof["tFname"]
                    last = prof["tLname"]
                    # Eliminate case-sensitivity by converting all names into lowercase
                    name = (first + " " + last).strip().lower().replace(" ", "")
                    
                    # While searching through every possible professor, check if the current one is in the inputted set of professors
                    if name in prof_set:
                        id = prof["tid"]
                        difficulty, retake = self.difficulty_and_retake(id)
                        # Dict's key is the professor's name and maps to a Professor object containing that professor's data
                        prof_dict[first + " " + last] = Professor(
                            id, first, last, 
                            prof["tNumRatings"], 
                            prof["overall_rating"], 
                            difficulty, retake
                        )
                        # Professor data has been acquired already so that professor can be removed from the set
                        prof_set.remove(name)
                    
                    # End the loop once all the professors in the set have had their data found to prevent useless looping
                    if not prof_set:
                        break
            except requests.RequestException as e:
                print(f"Failed to fetch page {i}: {e}")
            
                break

        return prof_dict

    # Helper function that returns the number of professors at a given university
    def num_professors(self, id):
        link = (
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&"
            "query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
        )
        # If anything fails, throw an exception
        try:
            # Get request for page
            page = requests.get(link + str(id), timeout=5)
            page.raise_for_status()
            # Parse JSON string into Python dictionary
            json_page = json.loads(page.content)

            return json_page["remaining"] + 20
        except requests.RequestException as e:
            print(f"Failed to fetch number of professors: {e}")

            return 0
    
    # Helper function that returns the level of difficulty and percent of students that would retake a professor's class
    def difficulty_and_retake(self, id):
        # This data can only be obtained at this page unlike the other professor statistics
        url = "https://www.ratemyprofessors.com/professor/"
        # If anything fails, throw an exception
        try:
            # Get request for page
            page = requests.get(url + str(id), timeout=10)
            page.raise_for_status()

            # HTML instead of JSON so we can simply call .text
            data = page.text

            difficulty_match = re.search(r'"avgDifficulty":([\d.]+)', data)
            retake_match = re.search(r'"wouldTakeAgainPercent":([\d.]+)', data)

            difficulty = float(difficulty_match.group(1)) if difficulty_match else 0.0
            retake = float(retake_match.group(1)) if retake_match else 0.0

            return difficulty, retake
        except requests.RequestException as e:
            print(f"Failed to fetch difficulty and retake for professor {id}: {e}")

            return 0.0, 0.0

