import pdx
from idea import Idea


class IdeaSet:
    def __init__(self, tag="NON", start=None, bonus=None, trigger=None, ideas=None, free=True):
        self.tag = tag
        self.start = start
        self.bonus = bonus
        self.trigger = trigger
        self.ideas = ideas

        if free is not None:
            self.free = free

    def dict_to_idea_set(dict):
        return IdeaSet()
