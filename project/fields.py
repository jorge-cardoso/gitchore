# -*- coding: utf-8 -*-
"""
Special fields.
"""
from typing import List, Dict


FIELDS: Dict[str, Dict] = {
    "Date": {
        "name": "date",
        "start_symbol": "[",
        "regex": r'\[.*?\]',
        "desc": 'parse string with brackets'
    },
    "Name": {
        "name": "User name",
        "start_symbol": "",
        "regex": r'(.+\@.+)',
        "desc": 'parse string with brackets'
    }
}

FIELDS_NAMES: List[str] = list(FIELDS.keys())
FIELDS_REGEX: List[str] = list({c['regex'] for c in FIELDS.values()})
