import asyncio
import os
from fastapi import APIRouter, UploadFile, BackgroundTasks

from db import get_all_books
from processing import file_processing
from schemas import BookInfo

router = APIRouter(tags=['gateway'])

PATH_TO_FILES = '/app/upload/'
os.makedirs(PATH_TO_FILES, exist_ok=True)


@router.post('/upload/')
async def upload_new_book(file: UploadFile, background_tasks: BackgroundTasks):
    print('!new file', PATH_TO_FILES + file.filename)
    with open(PATH_TO_FILES + file.filename, "wb") as upload_file:
        content = await file.read()
        upload_file.write(content)
    # background_tasks.add_task(file_processing, PATH_TO_FILES, file.filename)
    asyncio.create_task(file_processing(PATH_TO_FILES, file.filename))
    return "File {} in progress".format(file.filename)


@router.get('/books', response_model=list[BookInfo])
async def get_book_list():
    books = await get_all_books()
    print("books=", *books)
    return [BookInfo(datetime=b.datetime, title=b.title, x_avg_count_in_line=b.x_avg_count_in_line) for b in books]


