from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Dict

def _serialize_value(value):
    """Convert non-JSON-serializable types to strings."""
    if isinstance(value, (date, datetime)):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    return value

def convert_to_table(
        session: Session,
        sql: str
    ) -> List[Dict[str, any]]:

    result = session.execute(text(sql))
    column_names = result.keys()

    # Directly create the list of dictionaries from the fetched rows
    return [
        {col: _serialize_value(val) for col, val in zip(column_names, row)}
        for row in result
    ]

