from schema import *
from model import *
from sqlalchemy.orm import Session


def add_item(new_item:Items,db:Session):
    check = db.query(MenuItem).filter(MenuItem.dish_code==new_item.dish_code).first()
    if check:
        return None
    totally_new = MenuItem(
        dish_code = new_item.dish_code,
        dish_name = new_item.dish_name,
        calorie_count = new_item.calorie_count,
        price = new_item.price,
        status = new_item.status
    )
    db.add(totally_new)
    db.commit()
    db.refresh(totally_new)
    return totally_new

def show_all(db:Session):
    return db.query(MenuItem).all()

def show_through_id(item_id:int,db:Session):
    check = db.query(MenuItem).filter(MenuItem.id==item_id).first()
    if check:
        return check
    return None

def update_item(item_id:int,new_item:Items,db:Session):
    check = db.query(MenuItem).filter(MenuItem.id==item_id).first()
    if check:
        check.dish_code = new_item.dish_code
        check.dish_name = new_item.dish_name
        check.calorie_count= new_item.calorie_count
        check.price = new_item.price
        check.status = new_item.status
        db.commit()
        db.refresh(check)
        return check
    return None


def remove_item(item_id:int,db:Session):
    check = db.query(MenuItem).filter(MenuItem.id==item_id).first()
    if check:
        db.delete(check)
        db.commit()
        return check
    return None