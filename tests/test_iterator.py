from support import BaseTest


class TestIterator(BaseTest):
    def test_list_iterator(self):
        self.interpret_expr('''
            for i in [1, 2, 3] {
                log(i)
            }
        ''')
