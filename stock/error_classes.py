class AddRecordError(Exception):
    pass


class RecordValueError(AddRecordError):
    pass


class RecordDescriptionError(AddRecordError):
    pass


class RecordValueLittleError(AddRecordError):
    pass
