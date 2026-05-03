"""Caching utilities for VoteDost."""
from typing import Dict, Tuple

def dict_to_tuple(d: Dict) -> Tuple:
    """Converts a dictionary to a sorted tuple of items to make it hashable.
    
    Args:
        d: The dictionary to convert.
        
    Returns:
        A hashable tuple representation of the dictionary.
    """
    return tuple(sorted(d.items()))
