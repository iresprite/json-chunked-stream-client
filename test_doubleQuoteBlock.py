from unittest import TestCase
import ByteStreamHandler


class TestDoubleQuoteBlock(TestCase):
    def setUp(self):
        stack = [ByteStreamHandler.State()]
        self.double_quote_block = ByteStreamHandler.DoubleQuoteBlock(stack)

    def test_handle(self):
        self.assertIsInstance(self.double_quote_block.handle("\"", []), ByteStreamHandler.EmptyState)
        self.assertIsInstance(self.double_quote_block.handle("\\", []), ByteStreamHandler.EscapedChar)

    def test_closed_quote_block(self):
        state = ByteStreamHandler.State()
        dq_state = ByteStreamHandler.DoubleQuoteBlock([])
        stack = [state, dq_state]
        self.assertEqual(self.double_quote_block.closed_quote_block(stack), state)
        self.assertIsInstance(self.double_quote_block.closed_quote_block([]), ByteStreamHandler.EmptyState)