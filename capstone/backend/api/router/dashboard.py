import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from capstone.backend.api.models import SQLModel
from capstone.backend.api.utils import convert_to_table
from capstone.backend.api.utils.dashboard_query import (
    DOCUMENT_TABLE,
    ERROR_PERCENTAGE,
    HISTORY_TABLE,
    OVERALL_CHAT,
    TIME_USAGE,
    TOP_CATEGORY,
    TOP_USER_TIME,
    UPLOAD_PAGE,
)
from capstone.backend.database.connection import get_db

logger = logging.getLogger(__name__)

tags = ["Dashboard"]
router_dashboard = APIRouter(prefix="/dashboard", tags=tags)


# Using Base 64 to query Database.
@router_dashboard.post("/query")
def SQL_query(request: SQLModel, db: Session = Depends(get_db)):
    # Decode Base64 SQL
    sql_query = request.get_decoded_sql()

    # logging Debug
    logger.debug(f"Recieve SQL >> {sql_query}")

    # logging info
    logger.info("Get SQL query")

    # Query data from database
    query_data = db.execute(text(sql_query))

    # Convert data to JSON format
    column_name = list(query_data.keys())
    row_data = query_data.all()
    json_data = [dict(zip(column_name, row)) for row in row_data]

    return JSONResponse(content={"data": json_data})


# Query from Database.
@router_dashboard.get("/query")
async def query(db: Session = Depends(get_db)):
    # Prepare Data for Dashboard
    queries = {
        "total_user": OVERALL_CHAT,
        "avg_time_usage": TIME_USAGE,
        "upload_time": UPLOAD_PAGE,
        "user_time": TOP_USER_TIME,
        "top_category": TOP_CATEGORY,
        "history_table": HISTORY_TABLE,
        "document_table": DOCUMENT_TABLE,
        "error_percentage": ERROR_PERCENTAGE,
    }

    combined_data = {
        key: convert_to_table(session=db, sql=sql) for key, sql in queries.items()
    }

    return JSONResponse(content={"data": combined_data})