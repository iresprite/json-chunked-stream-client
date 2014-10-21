from unittest import TestCase
import ByteStreamHandler


class TestEmptyState(TestCase):
    def setUp(self):
        self.empty_state = ByteStreamHandler.EmptyState()
        self.symbol_dict = {"'": ByteStreamHandler.SingleQuoteBlock,
                            "\"": ByteStreamHandler.DoubleQuoteBlock,
                            "\\": ByteStreamHandler.EscapedChar,
                            "[": ByteStreamHandler.OpenArrayBlock,
                            "{": ByteStreamHandler.OpenObject}

    def test_handle(self):
        {self.assertIsInstance(self.empty_state.handle(v, []), self.symbol_dict[v]) for k, v in enumerate(self.symbol_dict)}
        for c in range(256):
            if c not in self.symbol_dict:
                self.assertIsInstance(self.empty_state.handle(c, []), ByteStreamHandler.EmptyState)