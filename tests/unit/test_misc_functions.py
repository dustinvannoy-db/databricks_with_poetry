import pytest

from databricks_with_poetry import misc_functions

def test_lookup_key_valid():
    assert misc_functions.id_lookup('person1') == 111

def test_lookup_key_invalid():
    assert misc_functions.id_lookup('fake-person') == 0

# if __name__ == "__main__":
#     print(pytest.main(["-p", "no:cacheprovider", "tests/test_misc_functions.py"]))