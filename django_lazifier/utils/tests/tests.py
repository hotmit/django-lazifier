from django.test import SimpleTestCase
from django_lazifier.utils.builtin_types.list import Lst
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str


class LstTest(SimpleTestCase):
    def test_list_functions(self):
        # to int
        self.assertEqual(Lst.convert_to_int(["1", "2.99999", "0.11"]), [1, 3, 0])

        # all test
        self.assertTrue(Lst.any([1, 2, 3], lambda x: x == 1))
        self.assertFalse(Lst.any([1, 2, 3], lambda x: x == 7))

        self.assertTrue(Lst.all([2, 4, 8], lambda x: x % 2 == 0))
        self.assertFalse(Lst.all([2, 5, 8], lambda x: x % 2 == 0))


class StrTest(SimpleTestCase):
    def test_str(self):
        self.assertEqual(Str.casefold('ViỆt Nam'), Str.casefold('việt nam'))

        self.assertTrue(Str.eq('a', 'A'))
        self.assertFalse(Str.eq('a', 'A', case=True))

        self.assertTrue(Str.contains("Hello", "hell"))
        self.assertFalse(Str.contains("Hello", "hell", case=True))

        # base64
        plain_str = 'hello world!'
        b64 = 'aGVsbG8gd29ybGQh'
        self.assertEqual(Str.base64_encode(plain_str), b64)
        self.assertEqual(Str.base64_decode(b64), plain_str)
        plain_str = 'this is a test'
        b64 = 'dGhpcyBpcyBhIHRlc3Q='
        self.assertEqual(Str.base64_encode(plain_str), b64)
        self.assertEqual(Str.base64_decode(b64), plain_str)

        # is_int()
        self.assertTrue(Str.is_int('0'))
        self.assertTrue(Str.is_int('1'))
        self.assertTrue(Str.is_int('-1'))
        self.assertFalse(Str.is_int('1.0'))
        self.assertFalse(Str.is_int('-1.0'))
        self.assertFalse(Str.is_int('-0'))
        self.assertFalse(Str.is_int('- 70'))


class ObjTest(SimpleTestCase):

    def test_get_attr(self):
        not_found = 'Not Found!'

        class Test:
            def __init__(self, a, b, other_test=None):
                self.a = a
                self.b = b
                self.other_test = other_test

        my_obj = {
            'hello': 'hello world',
            'obj': {
                'int': 10, 
                'arr': [7, 0, 3, 2, 5],
                'none': None,
            }
        }
        sub = Test('sub', 'class')
        parent = Test('parent class', 99, sub)

        self.assertEqual(Obj.getattr(my_obj, 'obj.arr', not_found), my_obj['obj']['arr'])
        self.assertEqual(Obj.getattr(my_obj, 'obj.arr.4', not_found), 5)
        self.assertEqual(Obj.getattr(my_obj, 'obj.arr.7', not_found), not_found)
        self.assertEqual(Obj.getattr(my_obj, 'obj.int', not_found), 10)
        self.assertEqual(Obj.getattr(my_obj, 'obj.none', not_found), None)
        self.assertEqual(Obj.getattr(my_obj, 'hello', not_found), my_obj['hello'])

        self.assertEqual(Obj.getattr(sub, 'a', not_found), sub.a)
        self.assertEqual(Obj.getattr(sub, 'b', not_found), sub.b)
        self.assertEqual(Obj.getattr(sub, 'other_test', not_found), sub.other_test)

        self.assertEqual(Obj.getattr(parent, 'a', not_found), parent.a)
        self.assertEqual(Obj.getattr(parent, 'b', not_found), parent.b)
        self.assertEqual(Obj.getattr(parent, 'other_test', not_found), sub)
        self.assertEqual(Obj.getattr(parent, 'other_test.a', not_found), sub.a)
        self.assertEqual(Obj.getattr(parent, 'other_test.b', not_found), sub.b)
        self.assertEqual(Obj.getattr(parent, 'other_test.other_test', not_found), sub.other_test)



