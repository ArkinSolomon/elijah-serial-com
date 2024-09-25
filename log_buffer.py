from log_message import LogMessage


class LogBuffer:
    messages: [LogMessage]
    max_messages: int

    def __init__(self, max_messages: int = 1024):
        self.messages = []
        self.max_messages = max_messages

    def add_message(self, message: str | LogMessage):
        if type(message) is LogMessage:
            self.messages.append(message)
        else:
            self.messages.append(LogMessage(message))

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
