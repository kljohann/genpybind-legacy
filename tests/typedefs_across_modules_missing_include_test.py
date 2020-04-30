import os

import pytest


def test_warning_emitted_during_import_of_module():
    text = "Reference to unknown type 'definition::Definition'"
    with pytest.warns(Warning, match=text) as recorder:
        # pylint: disable=import-outside-toplevel
        import pytypedefs_across_modules_missing_include as m

    # Alias is broken due to missing import:
    assert m.alias is None

    # The correct line in this file is reported as the location of the warning.
    assert len(recorder) == 1
    warning = recorder[0]
    assert os.path.samefile(warning.filename, __file__)
    with open(__file__) as f:
        line = f.readlines()[warning.lineno - 1].strip()
    assert line == "import pytypedefs_across_modules_missing_include as m"
