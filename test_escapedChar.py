from unittest import TestCase
import ByteStreamHandler


class TestEscapedChar(TestCase):
    def setUp(self):
        stack = [ByteStreamHandler.State()]
        self.escaped_char = ByteStreamHandler.EscapedChar(stack)

    def test_handle(self):
        state = ByteStreamHandler.State()
        ec_state = ByteStreamHandler.EscapedChar([])
        for c in range(256):
            stack = [state, ec_state]
            self.assertEqual(self.escaped_char.handle(c, stack), state)
            self.assertIsInstance(self.escaped_char.handle(c, []), ByteStreamHandler.EmptyState)