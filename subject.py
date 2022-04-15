class Subject:
    """Class for getting to know the subject's background info"""

    def __init__(self, dry_run=False, evaluation=False):
        if dry_run or evaluation:
            self.name = "Chris"
            self.origin = "Orem"
            self.age = "30"
            self.residence = "New York"
            self.occupation = "Software Engineer"
            print("\nDoing a dry run or evaluation. Auto-populating background info.")
        else:
            print("What is your name?")
            self.name = input()
            print("Where are you from originally?")
            self.origin = input()
            print("How old are you?")
            self.age = input()
            print("Where do you live now?")
            self.residence = input()
            print("What do you do for work?")
            self.occupation = input()

        print(
            "\nGreat, that's all really helpful to know. Let's get started on the interview!\n"
        )

    def print_backstory(self):
        """Convert the subject's info to a descriptive natural language paragraph"""
        return (
            f"This is an interview with {self.name}. "
            f"{self.name} is {self.age} years old and is from {self.origin} originally. "
            f"{self.name} lives in {self.residence}, and their occupation is {self.occupation}."
        )
