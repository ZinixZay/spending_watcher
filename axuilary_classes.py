from database_commands import *


class SpendRecord:
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self):
        add_record_to_a_database(value=self.value, description=self.description)


# Error Classes


class AddRecordError(Exception):
    pass


class RecordValueError(AddRecordError):
    pass


class RecordDescriptionError(AddRecordError):
    pass
