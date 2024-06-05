import uvicorn
import app.user.model as userModel
import app.email_verify.model as emailverifyModel
from database import engine

# userModel.Base.metadata.create_all(bind=engine)
# emailverifyModel.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app.api:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=False)