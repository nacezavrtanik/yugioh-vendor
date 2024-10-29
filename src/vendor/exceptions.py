
class VendorError(Exception):
    """Base exception for the vendor library"""


class ArticlePageNotFoundError(VendorError):
    pass
