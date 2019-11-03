import unittest
from backend import Backend

class TestBackend(unittest.TestCase):

    backend = Backend()

    def test_is_special_json(self):
        self.assertTrue(self.backend._is_special_json(1))
        self.assertTrue(self.backend._is_special_json(1.0))
        self.assertTrue(self.backend._is_special_json(1.0))
        self.assertTrue(self.backend._is_special_json({"name" : 4}))
        self.assertTrue(self.backend._is_special_json({"name" : "string"}))
        self.assertTrue(self.backend._is_special_json({"name" : {"name" : 4}}))
        self.assertFalse(self.backend._is_special_json({"name" : {"not_name" : 4}}))

    def test_list_valid(self):
        self.assertTrue(self.backend._list_valid([1, 2, 3]))
        self.assertTrue(self.backend._list_valid(["string", "string2", "string3"]))
        self.assertFalse(self.backend._list_valid(["string", "string2", {"string3": "string4"}]))

    def test_cmp(self):
        inputs = [
            [2, 1],
            ["b", "a"],
            [{"name" : 4}, {"name" : 3}],
            [{"name" : "b"}, {"name" : "a"}],
            [{"name" : "b"}, {"name" : 1}],
            [{"name" : "b"}, 1],
            [{"name" : "b"}, "some string"],
            [{"name" : {"name" : 4}}, 1],
            [{"name" : {"name" : 4}}, "some string"]
        ]

        for x, y in inputs:
            self.assertEqual(self.backend._cmp(x,y), 1)
            self.assertEqual(self.backend._cmp(y, x), -1)


if __name__ == '__main__':
    unittest.main()