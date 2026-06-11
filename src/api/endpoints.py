from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from models.user import User
from models.feedback import FeedBack, FeedbackStatus
from db import engine, get_db, Base
from schemas.request_models import RegisterRequest, LoginRequest, FeedBackCreate, FeedBackUpdate
from schemas.response_models import RegisterResponse, FeedBackResponse
from .helpers import create_access_token
from .dependencies import verify_jwt


# Create tables on startup
Base.metadata.create_all(bind=engine)

router = APIRouter()

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


# ==================== AUTH PAGES & ENDPOINTS ====================

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
      """
      Render login page
      """
      return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
      """
      Render register page
      """
      return templates.TemplateResponse("register.html", {"request": request})


@router.post("/api/register", 
            response_model=RegisterResponse,
            status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterRequest,
             db: Session = Depends(get_db)):
      """
      Register a new user
      """
      existing_user = db.query(User).filter(User.username == user_data.username).first()
      if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
      new_user = User(username=user_data.username)
      new_user.set_password(user_data.password)
    
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
    
      return new_user


@router.post("/api/login")
def login(user_data: LoginRequest,
          db: Session = Depends(get_db)):
      """
      Login user and return JWT token
      """
      user = db.query(User).filter(User.username == user_data.username).first()
    
      if not user or not user.check_password(user_data.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

      access_token = create_access_token(data={"sub": user.id})
    
      return {"access_token": access_token}


# ==================== PUBLIC PAGES & FEEDBACK ENDPOINTS ====================

@router.get("/", response_class=HTMLResponse)
def user_page(request: Request):
      """
      Render main feedback submission page
      """
      return templates.TemplateResponse("index.html", {"request": request})


@router.post("/api/feedback",
             response_model=FeedBackResponse,
             status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: FeedBackCreate,
                    db: Session = Depends(get_db)):
      """
      Submit new feedback
      """
      new_feedback = FeedBack(
            title=feedback.title,
            content=feedback.content
      )
      db.add(new_feedback)
      db.commit()
      db.refresh(new_feedback)
    
      return new_feedback


@router.get("/api/feedback",
            response_model=List[FeedBackResponse])
def get_all_feedback(skip: int = 0, 
                  limit: int = 10,
                  db: Session = Depends(get_db)):
      """
      Get feedbacks with pagination
      """
      return db.query(FeedBack).order_by(FeedBack.created_at.desc()).offset(skip).limit(limit).all()

  
# ==================== ADMIN ROUTES ====================

@router.get("/admin",
            response_class=HTMLResponse)
def admin_page(request: Request,
               db: Session = Depends(get_db)):
      """
      Render admin dashboard
      """
      feedbacks = db.query(FeedBack).order_by(FeedBack.created_at.desc()).all()
      return templates.TemplateResponse("admin.html", {
            "request": request,
            "feedbacks": feedbacks
      })


@router.put("/api/feedback/{feedback_id}",
            response_model=dict)
def update_feedback_status(
      feedback_id: int, 
      update_data: FeedBackUpdate, 
      db: Session = Depends(get_db),
      user = Depends(verify_jwt)
):
      """
      Update feedback status
      """
      feedback = db.query(FeedBack).filter(FeedBack.id == feedback_id).first()
      if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
    
      feedback.status = update_data.status.value
      db.commit()
    
      return {"message": "Status updated successfully"}


@router.delete("/api/feedback/{feedback_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(
      feedback_id: int, 
      db: Session = Depends(get_db),
      user = Depends(verify_jwt)
):
      """
      Delete feedback
      """
      feedback = db.query(FeedBack).filter(FeedBack.id == feedback_id).first()
      if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
    
      db.delete(feedback)
      db.commit()
      # No content returned (204)