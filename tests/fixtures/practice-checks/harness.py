_tally = {"passed": 0, "total": 0}


def check(label, make_actual, expected):
    """Run one check. It never raises, so the notebook always runs from top to bottom."""
    _tally["total"] += 1
    try:
        actual = make_actual()
    except Exception as error:
        print(f"error  {label}: {type(error).__name__}: {error}")
        return
    if actual == expected:
        _tally["passed"] += 1
        print(f"pass   {label}")
    else:
        print(f"todo   {label}: got {actual!r}")


def raises(make_actual, error_type):
    """True when the call raises error_type, False when it raises anything else or nothing."""
    try:
        make_actual()
    except error_type:
        return True
    except Exception:
        return False
    return False


def score():
    print(f"\nScore: {_tally['passed']} of {_tally['total']} checks pass")
