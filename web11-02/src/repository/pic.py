from datetime import datetime
from pathlib import Path

from sqlalchemy import and_

from src import db
from src import models
from .users import find_by_id
from src import config


def upload_file_to_user(_id, path, description):
    user = find_by_id(_id)
    target_folder = config.BASE_DIR / "src" / "static" / str(user.id)
    target_folder = Path(target_folder)
    target_folder.mkdir(exist_ok=True)
    file = path.rename(target_folder / Path(str(datetime.now().strftime("%I_%M_%S")) + path.name))
    size = file.stat().st_size
    filename_to_db = f"/static/{user.id}/{file.name}"
    picture = models.Picture(description=description, user_id=user.id, path=filename_to_db, size=size)
    db.session.add(picture)
    db.session.commit()


def get_pictures_user(user_id):
    return db.session.query(models.Picture).where(models.Picture.user_id == user_id).all()


def get_picture_user(picture_id, user_id):
    return db.session.query(models.Picture).where(
        and_(models.Picture.id == picture_id, models.Picture.user_id == user_id)).one()


def update_picture(picture_id, user_id, description):
    picture = get_picture_user(picture_id, user_id)
    picture.description = description
    db.session.commit()


def delete_picture(picture_id, user_id):
    picture = get_picture_user(picture_id, user_id)
    file_on_disc = Path(f"{config.BASE_DIR }/src{picture.path}")
    try:
        file_on_disc.unlink()
    except FileNotFoundError:
        print(f"Не удалось удалить файл {file_on_disc}")
    db.session.query(models.Picture).where(
        and_(models.Picture.id == picture_id, models.Picture.user_id == user_id)).delete()
    db.session.commit()
