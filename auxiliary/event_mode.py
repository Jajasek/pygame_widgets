_post_events = True


def set_mode_init():
    global _post_events
    _post_events = False


def set_mode_mainloop():
    global _post_events
    _post_events = True


def get_mode():
    return _post_events
