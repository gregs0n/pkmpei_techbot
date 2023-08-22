class BotException(Exception):
    pass

class TicketLimitException(BotException):
    pass

class TicketNotFoundException(BotException):
    pass

class TicketClosedException(BotException):
    pass

class InvalidTicketTextException(BotException):
    pass