import os
from grid import Grid
g = Grid(3)

# Folder containing test files
import os
import pytest # type: ignore

test_folder = "test"

# Create a list of (file_path, expected_result) tuples
test_files = [
    (os.path.join(test_folder, "test1.txt"), True),
    (os.path.join(test_folder, "test2.txt"), True),
    (os.path.join(test_folder, "test3.txt"), False),
    (os.path.join(test_folder, "test4.txt"), True),
    (os.path.join(test_folder, "test5.txt"), True),
    (os.path.join(test_folder, "test6.txt"), True),
    (os.path.join(test_folder, "test7.txt"), False),
]

@pytest.mark.parametrize("file_path, expected", test_files)
def test_file_cases(file_path, expected):
    g.populate(file_path)
    result = g.terminal()
    assert result == expected, f"Failed for {file_path}: got {result}, expected {expected}"
