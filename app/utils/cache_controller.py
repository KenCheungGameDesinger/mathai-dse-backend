import uuid
import os
import time
from flask_apscheduler import APScheduler
from flask import url_for
from werkzeug.utils import secure_filename
from io import BytesIO


# TODO: fix error when run with file_bytes = file.read() at ocr_routes.py
def save_image_to_cache(image, cache_dir='image'):
    """
    Save the uploaded image to the cache directory and return its URL.

    :param image: The image file to be saved.
    :param cache_dir: Directory to save cached images.
    :return: URL of the cached image.
    """
    ROOT = "cache"
    full_dir = os.path.join(ROOT, cache_dir)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    filename = secure_filename(image.filename).split('.')[0] + '_' + str(uuid.uuid4()) + '.' + \
               secure_filename(image.filename).split('.')[-1]
    filepath = os.path.join(full_dir, filename)

    image.seek(0)
    image.save(filepath)
    image.seek(0)
    # Generate a URL for the cached image
    image_url = url_for('static', filename=os.path.join(full_dir, filename), _external=True)
    return image_url


class Config:
    SCHEDULER_API_ENABLED = True


# def init_scheduler(app):
#     app.config.from_object(Config())
#     scheduler = APScheduler()
#     scheduler.init_app(app)
#
#     print("APScheduler initialized")
#
#     @scheduler.task('cron', id='delete_old_images', hour=3)
#     def delete_old_images():
#         ROOT = "cache"
#         CACHE_DIR = os.path.join(ROOT, "image")
#         cutoff_time = time.time() - 14 * 24 * 60 * 60  # 14 天前
#
#         if not os.path.exists(CACHE_DIR):
#             return
#
#         for filename in os.listdir(CACHE_DIR):
#             filepath = os.path.join(CACHE_DIR, filename)
#             try:
#                 if os.path.isfile(filepath):
#                     file_mtime = os.path.getmtime(filepath)
#                     if file_mtime < cutoff_time:
#                         os.remove(filepath)
#                         print(f"[Scheduler] Deleted old image: {filepath}")
#             except Exception as e:
#                 print(f"[Scheduler] Error deleting {filepath}: {e}")
#
#     scheduler.start()
