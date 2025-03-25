from database import engine
from models.user import User
from models.file import File
File.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)