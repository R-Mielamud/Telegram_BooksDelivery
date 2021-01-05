class ClassDictionary:
    def __init__(self, value):
        self.dict_value = value

    def __getattribute__(self, name):
        if name == "dict_value":
            return super().__getattribute__(name)

        result = self.dict_value.get(name)
        return result

    def __setattr__(self, name, value):
        if name == "dict_value":
            return super().__setattr__(name, value)

        self.dict_value[name] = value

    def pop(self, name, default=None):
        return self.dict_value.pop(name, default)
