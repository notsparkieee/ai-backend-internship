from app.database import engine, Base
from app.models import user, document  # IMPORTANT: import both models

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
