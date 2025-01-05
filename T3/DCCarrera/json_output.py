import json

class JSON_output:
    def __init__(self):
        self.problems = []

    def add_problem(self, start, path, vel, goal):
        d = {}
        d['start'] = start
        d['path'] = path
        d['velocity'] = vel
        d['goal'] = goal
        self.problems.append(d)

    def write(self, filename):
        json.dump(self.problems, open(filename, "w"))
