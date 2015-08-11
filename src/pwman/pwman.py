import sys

from passlib.context import CryptContext

import os.path

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


class UnicodeMixin(object):
    """
    Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3.

    https://docs.python.org/3.3/howto/pyporting.html
    """

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')


class Entry(UnicodeMixin):
    def __init__(self, username, encrypted_password, comment=None):
        self.username = username
        self.password = encrypted_password
        self.comment = comment

    @classmethod
    def from_plain_pw(cls, username, password, comment=None):
        """
        Create an Entry based on unencrypted password.
        """
        return cls(username, cls._hash(password), comment)

    @classmethod
    def from_line(cls, line):
        """
        Create an Entry based on line containing encrypted password.
        """
        parts = line.split(':')
        # Account for missing comment
        assert (len(parts) in [2, 3])
        if len(parts) == 2:
            parts.append(None)
        return cls(*parts)

    @staticmethod
    def _hash(password):
        return nginx_context.encrypt(password)

    def __unicode__(self):
        parts = [self.username, self.password]
        if self.comment:
            parts.append(self.comment)
        return ':'.join(parts)

    def as_tuple(self):
        return self.username, self.password, self.comment

    def verify(self, password):
        return nginx_context.verify(password, self.password)


class AuthDict(dict, UnicodeMixin):
    """
    List of password file entries. Duh...
    """

    def __init__(self, contents):
        super(AuthDict, self).__init__()
        if contents == '':
            return
        for e in [Entry.from_line(line) for line in contents.strip().split('\n')]:
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


class AuthFile(AuthDict, UnicodeMixin):
    def __init__(self, path, create=False):
        self.path = path
        if not os.path.exists(self.path):
            if create:
                open(self.path, 'w').close()  # touch
            else:
                raise IOError('File does not exist: {0}'.format(path))
        with open(path) as f:
            contents = f.read().strip()
            super(AuthFile, self).__init__(contents)

    def set(self, new_entry):
        self[new_entry.username] = new_entry

    def delete(self, username):
        if username in self:
            del self[username]
        else:
            raise KeyError('Unknown user name {0}'.format(username))

    def save(self):
        self.write(self.path)

    @property
    def users(self):
        return sorted(self.keys())

    @property
    def userlist(self):
        return self.as_sorted_tuples()

    def asdict(self):
        return dict(self)
