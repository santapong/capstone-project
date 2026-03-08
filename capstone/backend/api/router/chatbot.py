import os
import time
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from capstone.backend.llms import get_agent
from capstone.backend.api.models import (
    ChatModel,
    ResponseModel,
)
from capstone.backend.database.connection import get_db
from capstone.backend.database.models import LogsTable
from capstone.backend.llms.prompts import rag_prompt

logger = logging.getLogger(__name__)

tags = ["Chatbot"]
router_chatbot = APIRouter(prefix='/chatbot', tags=tags)

@router_chatbot.post("/infer", response_model=ResponseModel)
async def inference_Model(
    request: ChatModel, 
    agent = Depends(get_agent),
    db: Session = Depends(get_db),
):
    start_time = time.time()
    
    try:
        answer = await agent.ainvoke({"question": request.question})
        time_usage = time.time() - start_time
        logger.info(f"Time usage: {time_usage}s")

        # Insert successful response into database
        new_log = LogsTable(
            llm_model=os.getenv("LLM_MODEL"),
            prompt=rag_prompt.__name__, 
            question=request.question, 
            answer=answer['refine'], 
            time_usage=time_usage
        )
        db.add(new_log)
        db.commit()

        return JSONResponse(content={
            "time usage": time_usage,
            "question": request.question,
            "answer": answer['refine']
        })
    
    except Exception as e:
        time_usage = time.time() - start_time
        error_message = str(e)
        logger.error(f"Error occurred: {error_message}", exc_info=True)

        # Insert error details into database
        error_log = LogsTable(
            llm_model=os.getenv("LLM_MODEL"),
            prompt=rag_prompt.__name__,
            question=request.question,
            answer="ERROR", 
            time_usage=time_usage
        )
        db.add(error_log)
        db.commit()

        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
