import os
import errno
import pytoml

from itertools import islice, chain, repeat


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


def load_book_definition(root, resolve_dependency_references=True):
    metadata_file = os.path.join(root, 'book.toml')
    try:
        with open(metadata_file) as f:
            metadata = pytoml.load(f)
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise LookupError('book metadata not found')

    metadata['dependencies'] = {}

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

    if resolve_dependency_references:
        for dep_name, dep in metadata['dependencies'].iteritems():
            if 'book' in dep:
                continue
            dep_ref_data = dep['dependency_reference']
            target_path = os.path.join(root, dep_ref_data['path'], 'book.toml')
            with open(target_path) as f:
                dep_meta = pytoml.load(f)
                if dep_meta['book']['name'] != dep_ref_data['name']:
                    raise LookupError('Found invalid dependency')
                if not matches_version_spec(dep_meta['book']['version'],
                                            dep_ref_data['version']):
                    raise ValueError('%r does not match %r' % (
                        dep_meta['book']['version'],
                        dep_ref_data['version']))
                dep_meta.pop('dependency_reference', None)
                dep.update(dep_meta)

    return metadata
