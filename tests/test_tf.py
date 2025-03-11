def test_load_runners_returns_all_runners_if_all_runners_exist():
    # All supported runners must exist in the test environment!
    from vineyard.tf import load_runners, SUPPORTED_RUNNERS
    assert load_runners() == SUPPORTED_RUNNERS
