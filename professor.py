class Professor:
    def __init__(self, id, first, last, num_ratings, rating, difficulty, retake):
        self.id = id
        self.name = f"{first} {last}"
        self.first = first
        self.last = last
        self.num_ratings = num_ratings
        self.difficulty = difficulty
        self.retake = retake

        if self.num_ratings < 1:
            self.rating = 0
        else:
            self.rating = float(rating)