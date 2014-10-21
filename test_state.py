from unittest import TestCase
from ByteStreamHandler import State


class TestState(TestCase):
    def setUp(self):
        self.state = State()

    def test_handle(self):
        for c in range(256):
            try:
                self.assertEqual(self.state,self.state.handle(c, []))
            except:
                self.fail('Hit an exception.')