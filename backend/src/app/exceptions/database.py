
class UserNotFoundException(Exception):
    ...


class AccountNotFoundException(Exception):
    ...


class AccountNameExistsException(Exception):
    ...


class CategoryNotFoundException(Exception):
    ...


class CategoryCreateException(Exception):
    ...


class CategoryUpdateException(Exception):
    ...


class CategoryNameExistsException(Exception):
    ...


class CategoryParentNotFoundException(Exception):
    ...


class NestedCategoryException(Exception):
    ...


class CategoryInUseException(Exception):
    ...
