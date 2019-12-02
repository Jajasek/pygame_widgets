class Handler:
    def __init__(self, func, args=None, kwargs=None, self_arg=True, event_arg=True, delay=0):
        self.func = func
        self.args = list(args) if args is not None else list()
        self.kwargs = dict() if kwargs is None else kwargs
        self.self_arg = self_arg
        self.event_arg = event_arg
        self.delay = delay

    def __call__(self, widget, event):
        args = list()
        if self.self_arg:
            args.append(widget)
        if self.event_arg:
            args.append(event)
        args += self.args
        self.func(*args, **self.kwargs)

    def copy(self):
        return Handler(self.func, self.args, self.kwargs, self.self_arg, self.event_arg, self.delay)
