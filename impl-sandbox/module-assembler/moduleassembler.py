import os
import errno
import pytoml

from itertools import islice, chain, repeat


DEFAULT_DEPENDENCIES = [
    {
        'name': 'std-io',
        'version': '1.x',
    },
    {
        'name': 'std-util',
        'version': '1.x',
    },
]


def parse_version(version):
    bits = version.split('.')
    if len(bits) not in (1, 2, 3):
        raise ValueError('invalid version %r' % version)
    return tuple(map(int, islice(chain(bits, repeat(0)), 3)))


def parse_version_spec(version):
    bits = version.split('.')
    if len(bits) not in (1, 2, 3):
        raise ValueError('invalid version %r' % version)

    def convert_part(part):
        if part in ('*', '', 'x', 'X'):
            return None
        return int(part)
    return tuple(map(convert_part, islice(chain(bits, repeat(0)), 3)))


def matches_version_spec(version, spec):
    parsed_version = parse_version(version)
    parsed_spec = parse_version_spec(spec)

    for (val, ref) in zip(parsed_version, parsed_spec):
        if ref is None:
            continue
        if val != ref:
            return False
    return True


def load_book_definition(root):
    metadata_file = os.path.join(root, 'book.toml')
    try:
        with open(metadata_file) as f:
            metadata = pytoml.load(f)
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise LookupError('book metadata not found')

    metadata['dependencies'] = {}
    metadata['root_path'] = os.path.abspath(root)

    dep_folder = os.path.join(root, 'dependencies')
    if os.path.isdir(dep_folder):
        for dep_ref in os.listdir(dep_folder):
            dep_file = os.path.join(root, 'dependencies', dep_ref)

            if dep_file.endswith('.toml') and \
               os.path.isfile(dep_file):
                with open(dep_file) as f:
                    dep_ref_data = pytoml.load(f)
                    dep_ref_data.setdefault('name', dep_ref[:-5])
                    dep = {
                        'dependency_reference': dep_ref_data,
                    }
            elif os.path.isfile(os.path.join(dep_file, 'book.toml')):
                with open(os.path.join(dep_file, 'book.toml')) as f:
                    dep = pytoml.load(f)
                    dep['dependency_reference'] = {
                        'name': dep['book']['name'],
                        'version': dep['book']['name'],
                    }
            else:
                continue

            metadata['dependencies'][dep['dependency_reference']['name']] = dep

    return metadata


class ModuleMatch(object):

    def __init__(self, book_name, book_version, import_path, fs_path):
        self.book_name = book_name
        self.book_version = book_version
        self.import_path = import_path
        self.fs_path = fs_path

    @property
    def fqid(self):
        return '{%s@%s}%s' % (
            self.book_name,
            self.book_version,
            self.import_path,
        )

    def __repr__(self):
        return '<ModuleName fqid=%r path=%r>' % (
            self.fqid,
            self.fs_path,
        )


class Book(object):

    def __init__(self, fs_path, name, version, author=None, license=None,
                 import_path=None, dependencies=None):
        self.fs_path = fs_path
        self.name = name
        self.version = version
        self.author = author
        self.import_path = import_path
        self.license = license
        self.dependencies = dependencies

        self.athenaeum = Athenaeum(self.fs_path)
        if dependencies:
            self.athenaeum.load_dependencies(dependencies)

    def resolve_local_module(self, import_path):
        """Resolves a module within the book."""
        pieces = import_path.strip('.').split('.')
        prefix = (self.import_path or '').strip('.').split('.')

        if not prefix or prefix == ['']:
            local_path = pieces
        elif pieces[:len(prefix)] == prefix:
            local_path = pieces[len(prefix):]
        else:
            raise LookupError('Module not found')

        fs_path = os.path.join(self.fs_path, 'src', *local_path)
        if os.path.isfile(fs_path + '.q'):
            return fs_path + '.q'
        elif os.path.isfile(os.path.join(fs_path, 'index.q')):
            return os.path.join(fs_path, 'index.q')
        raise LookupError('Module not found')

    def resolve_module(self, import_path):
        """Resolve a module with the book or its athenaeum"""
        try:
            fs_path = self.resolve_local_module(import_path)
        except LookupError:
            pass
        else:
            return ModuleMatch(self.name, self.version, import_path, fs_path)
        return self.athenaeum.resolve_module(import_path)

    def open_resource(self, path):
        """Opens a resource stream"""
        try:
            return open(os.path.join(self.fs_path, *path.split('/')))
        except IOError:
            raise LookupError('Resource not found')

    @classmethod
    def from_definition(cls, md):
        book = md['book']
        return cls(
            fs_path=md['root_path'],
            name=book['name'],
            version=book['version'],
            author=book.get('author'),
            license=book.get('license'),
            import_path=book.get('import_path'),
            dependencies=md.get('dependencies') or {},
        )

    @classmethod
    def from_path(cls, path):
        md = load_book_definition(path)
        return cls.from_definition(md)


class DependencyInfo(object):

    def __init__(self, name, dep_data, book):
        self.name = name
        self.dep_data = dep_data
        self.book = book


class Athenaeum(object):

    def __init__(self, root_path):
        self.root_path = root_path
        self.dependencies = {}

    def load_dependency(self, dep_name, dep_data):
        if 'book' in dep_data:
            book = Book.from_definition(dep_data)
        elif 'path' in dep_data['dependency_reference']:
            book = Book.from_path(os.path.join(
                self.root_path, dep_data['dependency_reference']['path']))
        else:
            raise NotImplementedError('no search path for modules yet')
        self.dependencies[dep_name] = DependencyInfo(
            name=dep_name,
            dep_data=dep_data,
            book=book
        )

    def load_dependencies(self, dependencies):
        for dep_name, dep_data in dependencies.iteritems():
            self.load_dependency(dep_name, dep_data)

    def resolve_module(self, import_path):
        for dep_info in self.dependencies.itervalues():
            try:
                return dep_info.book.resolve_module(import_path)
            except LookupError:
                pass
        raise LookupError('Module not found')


def test():
    book = Book.from_path('example')
    print book.resolve_module('org.pocoo.example')
    print book.resolve_module('org.pocoo.other')
    with book.open_resource('README') as f:
        print f.read().strip()
