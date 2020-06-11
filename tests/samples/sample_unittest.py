import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        print("Setup test case")

    def test_passed(self):
        self.assertTrue(True)

    def test_failed(self):
        self.assertTrue(False)

    @unittest.skip("A skipped test case")
    def test_skipped(self):
        pass

    def tearDown(self):
        print("Teardown test case")
