from app.db.init_db import init_db
from app.db.session import SessionLocal

def main():
    db = SessionLocal()
    init_db(db)

if __name__ == '__main__':
    main()