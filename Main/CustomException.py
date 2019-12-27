#utilisation futures des exceptions
class BAIIOTException(Exception):
    """docstring for BAIIOTException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)


class InvalideSignatureException(BAIIOTException):
    """docstring for InvalideSignatureException."""
    def __init__(self, *arg,**kwargs):
        BAIIOTException.__init__(self, *arg,**kwargs)

class ContractNotInMangementContractException(BAIIOTException):
    """docstring for BAIIOTException."""
    def __init__(self, *arg,**kwargs):
        BAIIOTException.__init__(self, *arg,**kwargs)



class RequestException(Exception):
    """docstring for RequestException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)

class RequestAuthException(RequestException):
    """docstring for RequestAuthException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)

class RequestEndException(RequestException):
    """docstring for RequestEndException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)

class RequestNotEndException(RequestException):
    """docstring for RequestEndException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)


class RequestAccessException(RequestException):
    """docstring for RequestAccessException."""
    def __init__(self, *arg,**kwargs):
        Exception.__init__(self, *arg,**kwargs)
