from asciimatics.screen import Screen

from log_message import LogMessage


class LogBuffer:
    messages: [LogMessage]
    frozen_messages: [LogMessage]
    is_frozen = False
    max_messages: int

    def __init__(self, max_messages: int = 1024):
        self.messages = []
        self.frozen_messages = []
        self.max_messages = max_messages

    def add_message(self, message: str | LogMessage):
        if type(message) is LogMessage:
            self.messages.append(message)
        else:
            self.messages.append(LogMessage(message))

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def generate_screen_text(self, width: int, height: int) -> [(str, int)]:
        lines: [(str, int)] = []
        use_messages = self.messages
        if self.is_frozen:
            use_messages = self.frozen_messages
        for log_message in use_messages[::-1]:
            message: str = log_message.message
            timestamp: str = log_message.get_formatted_timestamp()
            line_start = ''
            color: int = 0

            line_start += f'[{timestamp}]'
            if log_message.is_system:
                line_start += '[SYS]'
                color = Screen.COLOUR_CYAN
            else:
                line_start += '[DEV]'
                color += Screen.COLOUR_WHITE
            line_start += ': '

            remaining_width = width - len(line_start)
            message_lines: [str] = []
            split_message=  message.split('\n')
            for i in range(len(split_message)):
                message_line = split_message[i]
                message_lines += [message_line[j:j + remaining_width] for j in range(0, len(message_line), remaining_width)]

            for i in range(len(message_lines)):
                if i == 0:
                    message_lines[0] = line_start + message_lines[0]
                else:
                    message_lines[i] = ' ' * len(line_start) + message_lines[i]

            message_lines = [(line, color) for line in message_lines]
            lines = message_lines + lines

            if len(lines) >= height:
                lines = lines[len(lines) - height:]
                break

        return lines

    def freeze(self):
        self.frozen_messages = self.messages.copy()
        self.is_frozen = True

    def unfreeze(self):
        self.is_frozen = False
