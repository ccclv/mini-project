from app import check_guess


def test_too_low():
    assert check_guess(10, 50) == "Too LOW"


def test_too_high():
    assert check_guess(90, 50) == "Too HIGH"


def test_correct():
    assert check_guess(50, 50) == "Correct!"