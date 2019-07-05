class Handler:
    def __init__(self, func, args=None, kwargs=None, self_arg=True, event_arg=True):
        self.func = func
        self.args = list() if args is None else args
        self.kwargs = dict() if kwargs is None else kwargs
        self.self_arg = self_arg
        self.event_arg = event_arg

    def __call__(self, widget, event):
        args = list()
        if self.self_arg:
            args.append(widget)
        if self.event_arg:
            args.append(event)
        args += self.args
        self.func(*args, **self.kwargs)
