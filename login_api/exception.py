
class ApiException(Exception):

    def __init__(self, message, code):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_json(self):
        return {"message": self.message, "code": self.code}
