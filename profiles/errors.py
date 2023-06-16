class MailServiceError(Exception):
    def __init__(self, message="There was an error with the mail service."):
        self.message = message
        super().__init__(self.message)
