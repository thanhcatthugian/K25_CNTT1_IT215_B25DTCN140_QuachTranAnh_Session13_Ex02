from schema import *
from model import *
from sqlalchemy.orm import Session

def add_slot(new_slot:Slots,db:Session):
    check = db.query(BoardingSlot).filter(BoardingSlot.slot_number == new_slot.slot_number).first()
    if check:
        return None
    totally_new = BoardingSlot(
        slot_number = new_slot.slot_number,
        room_size = new_slot.room_size,
        price_per_day = new_slot.price_per_day,
        status = new_slot.status
    )
    db.add(totally_new)
    db.commit()
    db.refresh(totally_new)
    return totally_new

def show_all(db:Session):
    return db.query(BoardingSlot).all()

def show_through_id(slot_id:int,db:Session):
    check = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if check:
        return check
    return None

def update_information(slot_id:int,new_slot:Slots,db:Session):
    check = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if check:
        check.slot_number = new_slot.slot_number
        check.room_size = new_slot.room_size
        check.price_per_day = new_slot.price_per_day
        check.status = new_slot.status
        db.commit()
        db.refresh(check)
        return check
    return None

def remove_information(slot_id:int,db:Session):
    check = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if check:
        db.delete(check)
        db.commit()
        return check
    return None