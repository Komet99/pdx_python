class Idea:
    header = "Placeholder Idea"
    modifiers = {None:1}

    def __init__(self, name=None, modifier=None, value=None):
        if name is not None:
            self.name = name

        if modifier is not None:
            self.modifier = modifier

        if value is not None:
            self.value = value
