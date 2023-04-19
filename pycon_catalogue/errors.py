class PyConCatalogueError(Exception):
    """The base exception class."""


class TalkValidationError(PyConCatalogueError):
    pass


class TalkNotFound(PyConCatalogueError):
    pass


class TalkAlreadyExists(PyConCatalogueError):
    pass
