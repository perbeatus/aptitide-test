class NoPassException(Exception):
    """When no DB passowrd in ENV var"""
    pass


class NoDataException(Exception):
    """When DB returns no data but it should return something"""
    pass