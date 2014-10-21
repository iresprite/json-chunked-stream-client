from unittest import TestCase
import ByteStreamHandler


class TestSingleQuoteBlock(TestCase):
    def setUp(self):
        stack = [ByteStreamHandler.State()]
        self.single_quote_block = ByteStreamHandler.SingleQuoteBlock(stack)

    def test_handle(self):
        self.assertIsInstance(self.single_quote_block.handle("\'", []), ByteStreamHandler.EmptyState)
        self.assertIsInstance(self.single_quote_block.handle("\\", []), ByteStreamHandler.EscapedChar)

    def test_closed_quote_block(self):
        state = ByteStreamHandler.State()
        dq_state = ByteStreamHandler.SingleQuoteBlock([])
        stack = [state, dq_state]
        self.assertEqual(self.single_quote_block.closed_quote_block(stack), state)
        self.assertIsInstance(self.single_quote_block.closed_quote_block([]), ByteStreamHandler.EmptyState)