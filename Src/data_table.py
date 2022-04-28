from typing import List

from Src.const import TEST_FILE


class DataRow:
    name:str
    correct:int
    incorrect:int
    incorrect_guesses:list

    def __init__(self, name):
        self.name = name
        self.correct = 0
        self.incorrect = 0
        self.incorrect_guesses = []

    def __str__(self) -> str:
        ms = self.most_frequent()
        if(self.correct+self.incorrect>0):
            return f"{self.name};{self.correct};{self.incorrect};{round(self.correct/(self.correct+self.incorrect),3)};{ms};{self.incorrect_guesses.count(ms)}"
        else:
            return f"{self.name};{self.correct};{self.incorrect};{0};{ms};{self.incorrect_guesses.count(ms)}"

    def most_frequent(self):
        if(len(self.incorrect_guesses)>0):
            return max(set(self.incorrect_guesses), key = self.incorrect_guesses.count)
        else:
            return "None"

    def correct_guess(self):
        self.correct += 1

    def incorrect_guess(self, name):
        self.incorrect += 1
        self.incorrect_guesses.append(name)

class DataTable:
    data_table = []

    def __init__(self, names):
        self.data_table = [0]*len(names)
        for i in range(len(names)):
            self.data_table[i] = DataRow(names[i])
        print(len(self.data_table))

    def save(self):
        file = open(TEST_FILE, "w")
        file.write("Doggo;Correct guesses;Incorrect guesses;Accuracy;Most commonly mistaken as;Count of mistakes for this breed")
        for dt in self.data_table:
            file.write(f"{dt}\n")
        file.close()

    def at(self,idx):
        return self.data_table[idx]