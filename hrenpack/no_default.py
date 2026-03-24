class NoDefaultType:
    """A type for representing the undefined value"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "no_default"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, NoDefaultType)


no_default = NoDefaultType()
