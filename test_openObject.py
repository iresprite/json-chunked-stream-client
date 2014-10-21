from unittest import TestCase
import ByteStreamHandler


class TestOpenObject(TestCase):
    def setUp(self):
        stack = [ByteStreamHandler.State()]
        self.open_object = ByteStreamHandler.OpenObject(stack)

    def test_handle(self):
        self.assertIsInstance(self.open_object.handle("}", []), ByteStreamHandler.EmptyState)
        self.assertIsInstance(self.open_object.handle("\\", []), ByteStreamHandler.EscapedChar)
        self.assertIsInstance(self.open_object.handle("\'", []), ByteStreamHandler.SingleQuoteBlock)
        self.assertIsInstance(self.open_object.handle("\"", []), ByteStreamHandler.DoubleQuoteBlock)
        self.assertIsInstance(self.open_object.handle("[", []), ByteStreamHandler.OpenArrayBlock)
        self.assertIsInstance(self.open_object.handle("{", []), ByteStreamHandler.OpenObject)

    def test_closed_quote_block(self):
        state = ByteStreamHandler.State()
        oo_state = ByteStreamHandler.OpenObject([])
        stack = [state, oo_state]
        self.assertEqual(self.open_object.close_object(stack), state)
        self.assertIsInstance(self.open_object.close_object([]), ByteStreamHandler.EmptyState)