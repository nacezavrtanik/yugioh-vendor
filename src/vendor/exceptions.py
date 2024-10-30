
class VendorError(Exception):
    """Base exception for the vendor library"""


class BinderError(VendorError):
    pass


class FormatError(BinderError):
    pass


class CSVFormatError(FormatError):
    pass


class DictFormatError(FormatError):
    pass


class ProcessingError(BinderError):
    pass


class CSVProcessingError(ProcessingError):
    pass


class DictProcessingError(ProcessingError):
    pass
