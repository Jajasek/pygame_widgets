class Attributes:
    def __get__(self, instance, owner):
        return self.__dict__

    def __set__(self, instance, value):
        if isinstance(value, dict):
            self.__dict__ = value
            return
        try:
            new = dict()
            for index, item in enumerate(value):
                new[f'attr{index}'] = item
        except TypeError:
            self.__dict__ = {'attr0': value}
        else:
            self.__dict__ = new

    def __delete__(self, instance):
        self.__dict__ = dict()

    def __getitem__(self, item):
        if isinstance(item, int):
            item = f'attr{item}'
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __add__(self, other):
        if not isinstance(other, dict):
            raise TypeError
        self.__dict__.update(other)

    def __sub__(self, other):
        if isinstance(other, dict):
            other = other.keys()
        try:
            for key in other:
                if isinstance(key, int):
                    key = f'attr{key}'
                del self.__dict__[key]
        except KeyError:
            pass
        except TypeError:
            try:
                del self.__dict__[other]
            except KeyError:
                pass
