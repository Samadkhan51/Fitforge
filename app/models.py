# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"

class Goal(str, enum.Enum):
    LOSE_FAT = "lose_fat"
    BUILD_MUSCLE = "build_muscle"
    MAINTAIN = "maintain"

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    # ... (rest of the schema is the same)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    age = Column(Integer)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    gender = Column(String)
    activity_level = Column(Enum(ActivityLevel))
    goal = Column(Enum(Goal))
    user = relationship("User", back_populates="profile")

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    target_muscle = Column(String)
    equipment = Column(String)
    instructions = Column(String)
    video_url = Column(String, nullable=True)

class Food(Base):
    __tablename__ = 'foods'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    calories_per_100g = Column(Float)
    protein_g_per_100g = Column(Float)
    carbs_g_per_100g = Column(Float)
    fat_g_per_100g = Column(Float)

class WorkoutLog(Base):
    __tablename__ = 'workout_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    # (Keep all the existing classes like User, Exercise, Food, etc.)

class WeightLog(Base):
    __tablename__ = 'weight_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    weight_kg = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)