import org.pocoo.other.get_name

pub def hello_world() -> Str {
    return 'Hello {}!'.format(get_name())
}
