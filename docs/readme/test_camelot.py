import parametrize_from_file

@parametrize_from_file
def test_str_find(str, sub, loc):
    assert str.find(sub) == loc
