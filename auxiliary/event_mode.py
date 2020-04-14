_post_events = True


def set_mode_init():
    """Stop widgets posting large number of events when initializating, thus setting lots of attributes."""

    global _post_events
    _post_events = False


def set_mode_mainloop():
    """Continue posting events when setting widgets' attributes."""

    global _post_events
    _post_events = True


def get_mode():
    """Returns True, if are widgets allowed to post events, otherwise False."""

    return _post_events
