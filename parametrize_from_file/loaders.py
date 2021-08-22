#!/usr/bin/env python3

import json, toml, yaml, nestedtext as nt
import functools

@functools.wraps(json.load)
def _load_json(path):
    with open(path) as f:
        return json.load(f)

@functools.wraps(yaml.safe_load)
def _load_yml(path):
    with open(path) as f:
        return yaml.safe_load(f)

_LOADERS = {
        '.json': _load_json,
        '.yaml': _load_yml,
        '.yml': _load_yml,
        '.toml': toml.load,
        '.nt': nt.load,
}

def add_loader(suffix, loader):
    """
    Read test parameters from a custom file type.

    Arguments:
        suffix (str):
            The file suffix to associate with the given loader.  This should 
            include a leading dot, e.g. ``'.yml'``.  It is possible to 
            overwrite the default suffixes with this function.

        loader (collections.abc.Callable):
            A function that will be used to load parameters from a file.  It 
            should have the following signature::

                def loader(path: pathlib.Path) -> Dict[str, List[Dict[str, Any]]]

            In other words, it should accept a path and return the top-level 
            data structure expected by :deco:`parametrize_from_file`.

    Note:
        Each file is only loaded once per pytest session.
    """
    _LOADERS[suffix] = loader

def drop_loader(suffix):
    """
    Prevent parameters from being read from files with the given suffix.
    """
    del _LOADERS[suffix]

def get_loaders():
    """
    Return the dictionary of known loaders.
    """
    return _LOADERS
