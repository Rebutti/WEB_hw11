from src import db
from src import models
from src.libs.file_service import move_user_pic, delete_user_pic
from src.repository.users import find_by_id
from sqlalchemy import and_

def get_pictures_user(user_id):
    return db.session.query(models.Picture).where(models.Picture.user_id == user_id).all()

def get_picture_user(pic_id, user_id):
    return db.session.query(models.Picture).filter(
        and_(models.Picture.user_id == user_id, models.Picture.id == pic_id)).one()

def upload_file_for_user(user_id, file_path, description):
    file_name, size = move_user_pic(user_id, file_path)
    picture = models.Picture(description=description, user_id=user_id, path=file_name, size=size)
    db.session.add(picture)
    db.session.commit()

def update_picture(pic_id, user_id, description):
    picture = get_picture_user(pic_id, user_id)
    picture.description = description
    db.session.commit()

def delete(pic_id, user_id):
    picture = get_picture_user(pic_id, user_id)
    db.session.query(models.Picture).filter(
        and_(models.Picture.user_id == user_id, models.Picture.id == pic_id)).delete()
    delete_user_pic(picture.path)
    db.session.commit()