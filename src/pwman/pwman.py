import os.path

from passlib.context import CryptContext

nginx_context = CryptContext(
        schemes=['ldap_salted_sha1'],
        default='ldap_salted_sha1'
        )

def hash(username, password, comment=None):
    """Generates salted SHA-1 hash"""
    parts = [username, nginx_context.encrypt(password)]
    if comment:
        parts.append(comment)
    return ':'.join(parts)

class Entry(object):
    def _hash(self, password):
        return nginx_context.encrypt(password)

    def __unicode__(self):
        parts = [self.username, self.password]
        if self.comment:
            parts.append(self.comment)
        return ':'.join(parts)

    def __str__(self):
        return self.__unicode__()

    def as_tuple(self):
        return (self.username, self.password, self.comment)


class NewEntry(Entry):
    """
    Entries with username, unencrypted password and optional comment

    They know their hashed_password and immediately forget the plaintext one.
    """
    def __init__(self, username, password, comment=None):
        self.username = username
        self.password = self._hash(password)
        self.comment = comment


class OldEntry(Entry):
    """
    Entries with username, password and optional comment, as parsed from a line.
    """
    def __init__(self, line):
        # Account for missing comment
        parts = line.split(':')
        assert(len(parts) in [2,3])
        if len(parts) == 2:
            parts.append(None)
        self.username, self.password, self.comment = parts


class AuthDict(dict):
    """
    List of password file entries. Duh...
    """
    def __init__(self, contents):
        if contents == '':
            return
        for e in [OldEntry(line) for line in contents.strip().split('\n')]:
            self[e.username] = e

    @classmethod
    def read(cls, path):
        return cls(open(path).read().strip())

    def write(self, path):
        open(path, 'w').write(str(self))

    def as_list(self):
        return [self[k] for k in sorted(self.keys())]

    def as_sorted_tuples(self):
        return [e.as_tuple() for e in self.as_list()]

    def __unicode__(self):
        return '\n'.join(map(str, self.as_list()))

    def __str__(self):
        return self.__unicode__()

class AuthFile(object):
    def __init__(self, path, create=False):
        self.path = path
        if not os.path.exists(self.path):
            if create:
                open(self.path, 'w').close()  # touch
            else:
                raise IOError('File does not exist: {0}'.format(path))
        self.auth_dict = AuthDict.read(path)

    def update(self, new_entry):
        self.auth_dict[new_entry.username] = new_entry

    def delete(self, username):
        if username in self.auth_dict.keys():
            del self.auth_dict[username]
        else:
            raise KeyError('Unknown user name {0}'.format(username))

    def save(self):
        self.auth_dict.write(self.path)

    @property
    def users(self):
        return sorted(self.auth_dict.keys())

    @property
    def userlist(self):
        return self.auth_dict.as_sorted_tuples()

    def asdict(self):
        return dict(self.auth_dict)

