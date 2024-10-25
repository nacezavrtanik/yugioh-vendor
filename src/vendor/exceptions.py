
class VendorError(Exception):
    """Base exception for the vendor library"""


class CSVProcessingError(VendorError):
    pass


class ArticlePageNotFoundError(VendorError):
    pass
