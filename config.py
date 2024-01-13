class Config:
    instance = None

    def __init__(self):
        self.config = {}

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'instance') or cls.instance is None:
            cls.instance = Config()
        return cls.instance

    def length(self):
        return len(self.config)

    def set(self, config):
        self.config = config

    def set_config(self, key, value):
        self.config[key] = value

    def get_config(self, key, default_value=None):
        return self.config.get(key, default_value)


class AppState:
    instance = None

    def __init__(self):
        self.state = {}

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'instance') or cls.instance is None:
            cls.instance = AppState()
        return cls.instance

    def length(self):
        return len(self.state)

    def set(self, config):
        self.state = config

    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key, default_value=None):
        return self.state.get(key, default_value)

    def append(self, key, value):
        if key not in self.state:
            self.state[key] = []

        if isinstance(self.state[key], list):
            self.state[key].append(value)
        else:
            raise Exception("key is not a list")

    def prepend(self, key, value):
        if key not in self.state:
            self.state[key] = []

        if isinstance(self.state[key], list):
            self.state[key].insert(0, value)
        else:
            raise Exception("key is not a list")
