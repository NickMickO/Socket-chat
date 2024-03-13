class DatabaseException(Exception):
    """ Database Exceptions """
    pass



class DatabaseNotInitialized(DatabaseException):
    """ Error if the init() method was not run """
    pass


class DatabaseSystemUserNotFound(DatabaseException):
    """ Error if system user not found """
    pass