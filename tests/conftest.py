import pytest

EXAMPLE_CONFIG_CONTENTS = """\
[AuthFiles]
example: {0}

[HTTP]
host: localhost
port: 5000
"""
EXAMPLE_AUTH_FILE_CONTENTS = """\
alice:{SSHA}xsQYxwTOV7tIbzRn00RBIvECxKT1vjcm:wonderland
bob:{SSHA}VnT6YAQ8+e4BkDCsERqH9HWa4A40BuB8
charlie:{SSHA}15YW4y+Z/1MsP3OsEOaY1+kYtRt1znkv
felix:{SSHA}hmwNBEOOGCitBOlbMLpELoPP1UV5zxkD
"""

@pytest.fixture
def config_and_example_file(tmpdir, monkeypatch):
    """\
    Creates two files:

    1. example.conf containing path to example auth file
    2. example_users, the auth file pwman operates on
    """
    # gen tmp paths
    cfg_file = tmpdir.join('example.conf')
    auth_file = tmpdir.join('example_users')
    # set auth_file path in example config
    cfg_contents = EXAMPLE_CONFIG_CONTENTS.format(auth_file)
    # write files
    cfg_file.write(cfg_contents)
    auth_file.write(EXAMPLE_AUTH_FILE_CONTENTS)
    # set PWMAN_CONFIG
    monkeypatch.setenv('PWMAN_CONFIG', str(cfg_file))
    return (cfg_file, auth_file)

