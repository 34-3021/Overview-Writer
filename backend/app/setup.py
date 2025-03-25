from database import engine
from models.user import User
from models.file import File
from models.document import Document

File.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
Document.metadata.create_all(bind=engine)