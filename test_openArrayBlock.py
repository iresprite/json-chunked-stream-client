from unittest import TestCase
import ByteStreamHandler


class TestOpenArrayBlock(TestCase):
    def setUp(self):
        stack = [ByteStreamHandler.State()]
        self.open_array_block = ByteStreamHandler.OpenArrayBlock(stack)

    def test_handle(self):
        self.assertIsInstance(self.open_array_block.handle("]", []), ByteStreamHandler.EmptyState)
        self.assertIsInstance(self.open_array_block.handle("\\", []), ByteStreamHandler.EscapedChar)
        self.assertIsInstance(self.open_array_block.handle("'", []), ByteStreamHandler.SingleQuoteBlock)
        self.assertIsInstance(self.open_array_block.handle("\"", []), ByteStreamHandler.DoubleQuoteBlock)
        self.assertIsInstance(self.open_array_block.handle("{", []), ByteStreamHandler.OpenObject)

    def test_close_array(self):
        state = ByteStreamHandler.State()
        oa_state = ByteStreamHandler.OpenArrayBlock([])
        stack = [state, oa_state]
        self.assertEqual(self.open_array_block.close_array(stack), state)
        self.assertIsInstance(self.open_array_block.close_array([]),ByteStreamHandler.EmptyState)