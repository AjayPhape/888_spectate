class ErrorCodes:

    @classmethod
    def get_error_message(cls, arg):
        assert arg in cls.CONSTANT, f"Error Code {arg} not configured."
        return cls.CONSTANT.get(arg)

    @classmethod
    def get_error_response(cls, error_code):
        return {
            "responseCode": error_code,
            "responseMessage": cls.get_error_message(error_code)
        }

    CONSTANT = {
        200: 'Success',
        201: 'Partial Success',
        300: "Parent id doesn't exists",
        301: "Record doesn't exists",
        302: "Invalid Timezone",
        500: 'Server Error'
    }