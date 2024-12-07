__all__ = [
    'RimTUBError',
    'LoadError',
    'FunctionNotFound'
]

class RimTUBError(Exception): ...

class LoadError(RimTUBError): ...

class FunctionNotFound(RimTUBError): ...