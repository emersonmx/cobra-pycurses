import json
import logging
logger = logging.getLogger(__name__)


class ScoreBoard(object):

    def __init__(self):
        self.scores = self.load()
        self.changed = False

    @property
    def difficulties(self):
        return self.scores.keys()

    @property
    def easy(self):
        return self.scores["easy"]

    @property
    def normal(self):
        return self.scores["normal"]

    @property
    def hard(self):
        return self.scores["hard"]

    @property
    def very_hard(self):
        return self.scores["very_hard"]

    def load(self):
        json_object = {}
        with open("data/scores.json") as score_file:
            json_object = json.load(score_file)

        return json_object

    def save(self):
        if self.changed:
            with open("data/scores.json", "w") as score_file:
                json.dump(self.scores, score_file)
        else:
            logger.info("No changes to save!")

    def add(self, difficulty, name, score):
        limit = 10
        scores = self.scores[difficulty]
        scores.append((name, score))
        scores.sort(key=lambda score: score[1])
        self.scores[difficulty] = scores[-limit:]
        self.changed = True
