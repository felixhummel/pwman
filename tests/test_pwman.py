import json

import pytest
from pwman import pwman


@pytest.fixture()
def tmp_path(tmpdir):
    return str(tmpdir.join('users'))


def test_hash():
    h = pwman.hash('felix', 'secret', 'master of the universe')
    parts = h.split(':')
    assert (len(parts) == 3)
    username, hashed_password, comment = parts
    assert (username == 'felix')
    assert (len(hashed_password) == 38)  # 32 + 6 for {SSHA} prefix
    assert (comment == 'master of the universe')
    # empty comment
    h = pwman.hash('felix', 'secret')
    parts = h.split(':')
    assert (len(parts) == 2)
    username, hashed_password = parts
    assert (username == 'felix')
    assert (len(hashed_password) == 38)  # 32 + 6 for {SSHA} prefix


def test_Entry():
    e0 = pwman.Entry('felix', '{ssha}hmwnbeoogcitbolbmlpelopp1uv5zxkd')
    assert e0.username == 'felix'
    assert e0.password == '{ssha}hmwnbeoogcitbolbmlpelopp1uv5zxkd'
    e1 = pwman.Entry.from_plain_pw('felix', 'secret')
    assert e1.username == 'felix'
    assert e1.password.startswith('{SSHA}')
    assert e1.comment is None
    assert e1.verify('secret')
    s = json.dumps(e1.__dict__)
    assert len(s) > 2  # more than '{}'
    # with comment
    e2 = pwman.Entry.from_plain_pw('felix', 'secret2', 'some comment')
    assert e2.username == 'felix'
    assert e2.password.startswith('{SSHA}')
    assert e2.comment is 'some comment'
    assert e2.verify('secret2')
    s = json.dumps(e2.__dict__)
    assert len(s) > 2  # more than '{}'
    # make sure hashes differ
    a = pwman.Entry.from_plain_pw('felix', 'secret')
    b = pwman.Entry.from_plain_pw('felix', 'secret')
    assert a.password != b.password
    # parse line
    line = 'felix:{SSHA}hmwNBEOOGCitBOlbMLpELoPP1UV5zxkD'
    e = pwman.Entry.from_line(line)
    assert e.username == 'felix'
    assert e.password == '{SSHA}hmwNBEOOGCitBOlbMLpELoPP1UV5zxkD'
    assert e.comment is None


def test_AuthDict():
    contents = open('tests/fixtures/example_file.txt').read()

    ad = pwman.AuthDict(contents)
    alice = ad['alice']
    assert alice.username == 'alice'
    assert alice.password == '{SSHA}xsQYxwTOV7tIbzRn00RBIvECxKT1vjcm'
    assert alice.comment == 'wonderland'
    s = str(ad)
    assert s.strip() == contents.strip()


def test_AuthFile(tmp_path):
    # create, save
    af = pwman.AuthFile(tmp_path, create=True)
    felix = pwman.Entry.from_plain_pw('felix', 'secret', 'hello world')
    af.set(felix)
    af.save()
    # load, add user, forget to save
    af2 = pwman.AuthFile(tmp_path)
    assert len(af2) == 1
    alice = pwman.Entry.from_plain_pw('alice', 'alice')
    af2.set(alice)
    assert len(af2) == 2
    # load, add user, save
    af3 = pwman.AuthFile(tmp_path)
    assert len(af3) == 1
    bob = pwman.Entry.from_plain_pw('bob', 'bob')
    af3.set(bob)
    assert len(af3) == 2
    af3.save()
    assert len(af3.userlist) == 2
    felix_tup = af3.userlist[1]
    assert felix_tup[0] == 'felix'
    assert felix_tup[1].startswith('{SSHA}')
    assert felix_tup[2] == 'hello world'
    di = af3.asdict()
    # load
    af4 = pwman.AuthFile(tmp_path)
    assert af4.users == ['bob', 'felix']
    # delete
    af4.delete('felix')
    assert af4.users == ['bob']


def test_AuthFileRaisesIOError(tmp_path):
    with pytest.raises(IOError):
        pwman.AuthFile(tmp_path, create=False)


def test_AuthFileRaisesKeyError(tmp_path):
    with pytest.raises(KeyError):
        af = pwman.AuthFile(tmp_path, create=True)
        af.delete('thisuserdoesnotexist')


def test_tool(tmp_path, capsys, monkeypatch):
    from pwman import tool
    import sys
    # error for non-existing files
    try:
        sys.argv = ['pwman', '-b', tmp_path, 'alice', 'secret']
        tool.main()
    except SystemExit as e:
        out, err = capsys.readouterr()
        assert 'does not exist' in err
    # create
    sys.argv = ['pwman', '-bc', tmp_path, 'alice', 'secret']
    tool.main()
    # read pw from stdin
    import getpass
    monkeypatch.setattr(getpass, 'getpass', lambda: 'secret2')
    sys.argv = ['pwman', tmp_path, 'alice']
    tool.main()
    # print
    try:
        sys.argv = ['pwman', '-p', tmp_path, 'alice']
        tool.main()
    except SystemExit as e:
        assert e.code == 0
        out, err = capsys.readouterr()
        assert '{SSHA}' in out
    # delete
    sys.argv = ['pwman', '-D', tmp_path, 'alice']
    tool.main()
