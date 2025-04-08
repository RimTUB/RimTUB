__all__ = [
    'RimTUBError',
    'LoadError',
    'ModuleError'
]

class RimTUBError(Exception): ...

class ModuleError(RimTUBError): ...

class LoadError(ModuleError): ...
