
class VendorError(Exception):
    """Base exception for the vendor library"""


class BinderError(VendorError):
    pass


class FormatError(BinderError):
    pass


class CSVFormatError(FormatError):
    TIP = "Tip: Create a valid CSV with vendor.Binder.create_csv_template."

    @classmethod
    def for_duplicate_fields(cls, fields, duplicate_fields):
        instance = cls(f"duplicate fields: {str(duplicate_fields).strip('[]')}")
        instance.add_note(f"Got fields: {str(fields).strip('[]')}")
        instance.add_note(cls.TIP)
        return instance

    @classmethod
    def for_missing_required_fields(cls, fields, missing_required_fields):
        missing_fields_string = str(
            [str(field) for field in missing_required_fields]
        ).strip("[]")
        instance = cls(f"missing required fields: {missing_fields_string}")
        instance.add_note(f"Got fields: {str(fields).strip('[]')}")
        instance.add_note(cls.TIP)
        return instance


class DictFormatError(FormatError):
    pass


class ProcessingError(BinderError):
    NOTES_ON_EXPECTED_TYPES = {
        str: "Expected type: str",
        int: (
            "Expected type:\n"
            "  int (example: 2)\n"
            "  float, must represent an integer (example: 2.0)\n"
            "  str, must represent an integer (example: '2')"
        ),
        bool: (
            "Expected type:\n"
            "  bool (example: True)\n"
            "  str, case-insensitive, must be one of:\n"
            "    'true', 'false', 'yes', 'no' (example: 'Yes')"
        ),
    }

    @classmethod
    def for_field_type(cls, field_type, field, value):
        assert field_type in cls.NOTES_ON_EXPECTED_TYPES
        instance = cls(f"failed to process value for field '{field}'")
        instance.add_note(f"Got type: {type(value).__name__}")
        instance.add_note(f"Got value: {value!r}")
        instance.add_note(cls.NOTES_ON_EXPECTED_TYPES.get(field_type))
        return instance

    @classmethod
    def from_processing_error(cls, processing_error):
        assert isinstance(processing_error, ProcessingError)
        instance = cls(*processing_error.args)
        if hasattr(processing_error, "__notes__"):
            instance.__notes__ = processing_error.__notes__
        return instance


class CSVProcessingError(ProcessingError):
    pass


class DictProcessingError(ProcessingError):
    pass
