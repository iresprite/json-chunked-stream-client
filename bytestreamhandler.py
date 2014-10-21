class ByteStreamHandler(object):
    """
    ByteStreamHandler is based on the State Machine design pattern, and switches state based on incoming bytechars. It
     indicates a JSON object has been completed when its stack is empty and no states remind.
    """

    def __init__(self, state=None):
        """
        Constructor
        :param state: Initial state of the ByteStreamHandler
        :type state: State
        """
        self.stack = []
        if state:
            self.state = state
        else:
            self.state = EmptyState()
        self.buffer = ''

    def next_byte(self, input_byte):
        """
        Consumes a byte character and changes state depending on content.
        :param input_byte: Byte char to analyze via the current state
        :type input_byte: str
        """
        self.state = self.state.handle(chr(input_byte), self.stack)

    def complete_object(self):
        """
        :return: Boolean indicating whether a complete JSON object has been consumed
        """
        if not self.stack:
            return True
        else:
            return False


class State(object):
    """
    This is the base State class. It defines the default handle method.

    Attributes:
        transition_map: This dictionary has single character strings for keys and maps them to the action they invoke.
    """
    transition_map = {}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte]()
        else:
            return self


class OpenArrayBlock(State):
    """
    State corresponding to a section of bytes entered with the "[" character.
    """
    def __init__(self, stack):
        stack.append(self)
        self.transition_map = {"]": self.close_array, "\\": EscapedChar,
                               "'": SingleQuoteBlock, "\"": DoubleQuoteBlock,
                               "{": OpenObject}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte](stack)
        else:
            return self

    def close_array(self, stack):
        """
        Removes the OpenArrayBlock state from the stack.
        :return: The previous state on the stack (or EmptyState if stack is empty).
        """
        if stack:
            stack.pop()
            if stack:
                return stack[-1]
            else:
                return EmptyState()
        else:
            return EmptyState()


class EscapedChar(State):
    """
    State entered with the "\" character. Used to ignore the next incoming byte char.
    """
    def __init__(self, stack):
        stack.append(self)

    def handle(self, input_byte, stack):
        if stack:
            stack.pop()
            if stack:
                return stack[-1]
            else:
                return EmptyState()
        else:
            return EmptyState()


class DoubleQuoteBlock(State):
    """
    State entered with the '"' character.
    """
    def __init__(self, stack):
        stack.append(self)
        self.transition_map = {"\"": self.closed_quote_block, "\\": EscapedChar}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte](stack)
        else:
            return self

    def closed_quote_block(self, stack):
        """
        Removes the DoubleQuoteBlock state from the stack.
        :return: The previous state on the stack (or EmptyState if stack is empty).
        """
        if stack:
            stack.pop()
            if stack:
                return stack[-1]
            else:
                return EmptyState()
        else:
            return EmptyState()


class SingleQuoteBlock(State):
    """
    State entered with the "'" character.
    """
    def __init__(self, stack):
        stack.append(self)
        self.transition_map = {"\'": self.closed_quote_block, "\\": EscapedChar}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte](stack)
        else:
            return self

    def closed_quote_block(self, stack):
        """
        Removes the SingleQuoteBlock state from the stack.
        :return: The previous state on the stack (or EmptyState if stack is empty).
        """
        if stack:
            stack.pop()
            if stack:
                return stack[-1]
            else:
                return EmptyState()
        else:
            return EmptyState()


class OpenObject(State):
    """
    State entered with the "{" character.
    """
    def __init__(self, stack):
        stack.append(self)
        self.transition_map = {"'": SingleQuoteBlock, "\"": DoubleQuoteBlock,
                               "\\": EscapedChar, "[": OpenArrayBlock,
                               "{": OpenObject, "}": self.close_object}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte](stack)
        else:
            return self

    def close_object(self, stack):
        """
        Removes the OpenObjectBlock state from the stack.
        :return: The previous state on the stack (or EmptyState if stack is empty).
        """
        if stack:
            stack.pop()
            if stack:
                return stack[-1]
            else:
                return EmptyState()
        else:
            return EmptyState()


class EmptyState(State):
    """
    State entered when there are no further states on the stack.
    """
    transition_map = {"'": SingleQuoteBlock, "\"": DoubleQuoteBlock,
                      "\\": EscapedChar, "[": OpenArrayBlock,
                      "{": OpenObject}

    def handle(self, input_byte, stack):
        """

        :param input_byte: Byte char to handle based on state
        :type input_byte: str
        :param stack: Stack of states that indicate enclosing strings, arrays, and objects.
        :return: State or action based on input_byte
        """
        if input_byte in self.transition_map:
            return self.transition_map[input_byte](stack)
        else:
            return self
