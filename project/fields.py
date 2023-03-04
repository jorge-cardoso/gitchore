# -*- coding: utf-8 -*-
"""
Special fields.
"""
from typing import List, Dict


FIELDS: Dict[str, Dict] = {
    "Date": {
        "name": "date",
        "start_symbol": "[",
        "regex": r'(\d{1,2})\.(\d{2})\.(\d{4})',
        "example": '28.02.2023'
    },
    "User_name": {
        "name": "User name",
        "start_symbol": "",
        "regex": r'\s*([a-zA-Z\s]*\w)\s*(@[\w]+)\s*',
        "example": ' Jorge Cardoso @j00760260 '
    },
    "Results": {
        "name": "Results",
        "start_symbol": "",
        "regex": r'(__[\w\s]+__)',
        "example": ' (__System Design__) '
    },
    "Status": {
        "name": "Task status",
        "start_symbol": "",
        "regex": r'\(\s*(__[a-zA-Z_]+__)\s*,\s*([a-zA-Z\s]*\w*)\s*(@[\w]+)\s*,\s*(\d+%)\s*\)',
        "example": '(__Design__, Jorge Cardoso @j00760260, 75% )'
    },
    "Task_description": {
        "name": "Task description",
        "start_symbol": "",
        "regex": r'\(\s*(_[\w\s]+_)\)\s*([a-zA-Z\s]*\w)',
        "example": '(_Research_) Review literature of log management systems'
    },
    "Sprints": {
        "name": "Sprint",
        "start_symbol": "",
        "regex": r'(__[\w\s]+__)',
        "example": ' (__System Design__) '
    },
    "Tasks": {
        "name": "Task name",
        "start_symbol": "",
        "regex": r'(__[\w\s]+__)',
        "example": ' (__System Design__) '
    },
    "Milestones": {
        "name": "Milestone",
        "start_symbol": "",
        "regex": r'\s*(\d{1,2}\.\d{2}\.\d{4})\W*(.*\w)',
        "example": '    M1: 01.01.2023, EDCP, mid-review    '
    }
}

FIELDS_NAMES: List[str] = list(FIELDS.keys())
FIELDS_REGEX: List[str] = list({c['regex'] for c in FIELDS.values()})
