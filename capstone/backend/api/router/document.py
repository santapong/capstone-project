import io
import json
import logging
import os
import time

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pypdf import PdfReader
from sqlalchemy.orm import Session

from capstone.backend.api.models import DocumentModel, FileLength
from capstone.backend.database.connection import get_db
from capstone.backend.database.models import DocumentTable
from capstone.backend.llms import RAGModel, get_RAG

logger = logging.getLogger(__name__)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", default="bge-m3")

tags = ["Document"]
router_document = APIRouter(prefix="/document", tags=tags)


@router_document.post("/document")
async def upload_Docs(
    data: str = Form(default='{"first_page":0,"final_page":0}'),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    RAG: RAGModel = Depends(get_RAG),
):
    try:
        start_time = time.time()
        # Parse the JSON string into the Pydantic model
        interval = FileLength.model_validate_json(data)

        # Read PDF Files.
        content = await file.read()
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)

        # IF start page = final page and zero must extract all.
        if (interval.start_page == interval.final_page) and (
            interval.start_page == 0 and interval.final_page == 0
        ):
            # Make to extract all data.
            interval.start_page = 1  # first_page = 1 in PDF
            interval.final_page = len(reader.pages)
            logger.info("Receive start_page = 0 and final_page = 0 >> Set inteval to extract all")

        # IF start_page != 0 and final_page > max_page or == 0
        elif (interval.start_page != 0) and (
            (interval.final_page > len(reader.pages)) or (interval.final_page == 0)
        ):
            # Set final page to Extract all page.
            interval.final_page = len(reader.pages)
            logger.info(f"Set final_page = {len(reader.pages)} >> Set to extract all from start_page")

        # IF start_page == 0 and final_page != 0
        elif interval.start_page == 0 and interval.final_page != 0:
            # Set start_page = 1
            interval.start_page = 1
            logger.info("Set start_page = 1")

        # start_page must less than final_page
        elif interval.start_page > interval.final_page:
            raise HTTPException(422, f"The interval that given {interval} is not good.")

        # Specific target page to extract
        target_interval = [
            target for target in range(interval.start_page - 1, interval.final_page)
        ]
        logger.info(f"Extract {target_interval}")

        # Prepare Temp Varr.
        contents = ""

        # Extract contents from each page
        for page in reader.pages:
            if page.page_number in target_interval:
                contents += page.extract_text()

        metadatas = [{"source": file.filename}]

        # Upload PDF to Vector Database
        ids = await RAG.aload_from_API(contents=contents, metadatas=metadatas)
        time_usage = time.time() - start_time

        # Insert to Document Table.
        new_doc = DocumentTable(
            ids=ids,
            embedding_model=EMBEDDING_MODEL,
            document_name=file.filename,
            time_usage=time_usage,
            pages=len(target_interval),
        )
        db.add(new_doc)
        db.commit()

        return JSONResponse(
            content={
                "Filename": file.filename,
                "Metadata": metadatas,
                "time_usage": time_usage,
                "ids": ids,
            }
        )

    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON format")
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(400, f"Data validation error: {str(e)}")


@router_document.delete("/document")
async def remove_docs(
    request: DocumentModel, db: Session = Depends(get_db), RAG: RAGModel = Depends(get_RAG)
):
    document_name = request.document_name
    document_id = request.id
    # Find the document in the SQL database
    documents = (
        db.query(DocumentTable)
        .filter(DocumentTable.document_name == document_name, DocumentTable.id == document_id)
        .all()
    )

    # Error Handling when document does not exist.
    if not documents:
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove from vector database
    vector_store = RAG.get_vector_store()
    vector_store.delete(documents[0].ids)

    # Remove from SQL database
    db.delete(documents[0])
    db.commit()

    return JSONResponse(
        content={"message": f"Document {document_name} deleted successfully"}
    )


# Get Document from database.
@router_document.get("/documents")
async def get_Docs(db: Session = Depends(get_db)):
    # Get data from Document Table.
    results = db.query(DocumentTable).all()

    # Wrapping up data for Dashboard Management.
    documents = [
        {
            "document": result.document_name,
            "id": result.id,
            "pages": result.pages,
            "upload_time": result.datetime,
        }
        for result in results
    ]

    return JSONResponse(content={"data": documents})