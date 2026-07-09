from fastapi import FastAPI,HTTPException,status,Depends,Path,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import *
from model import *
from schema import *
from user_service import *
from datetime import datetime
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind = engine)

def create_response(
        status_code:int,
        message:str,
        error = None,
        data = None,
        path = ""
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code":status_code,
            "message":message,
            "error":error,
            "data":data,
            "timestamp":datetime.utcnow().isoformat(),
            "path":path
        }
    )

@app.exception_handler(RequestValidationError)

def request_validation_handler(request:Request,exc:RequestValidationError):
    return create_response(
        status_code=422,
        message="Dinh dang du lieu khong hop le",
        error=exc.errors,
        path=request.url.path
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request:Request,exc:HTTPException):
    return create_response(
        status_code=exc.status_code,
        message=exc.detail,
        path=request.url.path
    )

@app.exception_handler(Exception)

def exception_handler(request:Request,exc:Exception):
    print(f"[INTERNAL SERVER ERROR] Path: {request.url.path} | {str(exc)}")
    return create_response(
        status_code=500,
        message="Server bi loi vui long thu lai sau",
        path=request.url.path
    )

@app.get("/menu-items",response_model=Response,status_code=status.HTTP_200_OK)

def show_all_item(request:Request,db:Session = Depends(get_db)):
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Lay thong tin mon an thanh cong",
        data=jsonable_encoder(show_all(db)),
        path=request.url.path
    )


@app.post("/menu-items",response_model=Response,status_code=status.HTTP_201_CREATED)
def add_new_item(request:Request,new_item:Items,db:Session = Depends(get_db)):
    check = add_item(new_item,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ma code mon an da ton tai"
        )
    return create_response(
        status_code=status.HTTP_201_CREATED,
        message="Them moi mon an thanh cong",
        data=jsonable_encoder(check),
        path=request.url.path
    )

@app.get("/menu-items/{item_id}",response_model=Response,status_code=status.HTTP_200_OK)
def show_item_through_id(request:Request,item_id:int = Path(...),db:Session = Depends(get_db)):
    check = show_through_id(item_id,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay id mon an tuong tu"
        )
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Lay thong tin mon an thanh cong",
        data=jsonable_encoder(check),
        path=request.url.path
    )

@app.put("/menu-items/{item_id}",response_model=Response,status_code=status.HTTP_200_OK)
def update_information(request:Request,new_item:Items,item_id:int = Path(...),db:Session = Depends(get_db)):
    check = update_item(item_id,new_item,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay id mon an tuong tu"
        )
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Cap nhat thong tin mon an thanh cong",
        data=jsonable_encoder(check),
        path=request.url.path
    )

@app.delete("/menu-items/{item_id}",response_model=Response,status_code=status.HTTP_200_OK)
def delete_item(request:Request,item_id:int = Path(...),db:Session = Depends(get_db)):
    check = remove_item(item_id,db)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay id mon an tuong tu"
        )
    return create_response(
        status_code=status.HTTP_200_OK,
        message="Xoa thong tin mon an thanh cong",
        data=jsonable_encoder(check),
        path=request.url.path
    )