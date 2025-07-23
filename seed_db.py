 
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.models import Base, Exercise, Food

DATABASE_URL = "postgresql://fitforge:fitforgepassword@postgres-db:5432/fitforgedb"

def seed_database():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Dropping and recreating tables...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tables created.")

    print("Seeding database with expanded knowledge base...")

    
    exercises = [
        
        Exercise(name="Barbell Bench Press", target_muscle="Chest", equipment="Barbell, Bench"),
        Exercise(name="Dumbbell Bench Press", target_muscle="Chest", equipment="Dumbbells, Bench"),
        Exercise(name="Incline Dumbbell Press", target_muscle="Chest", equipment="Dumbbells, Bench"),
        Exercise(name="Push-up", target_muscle="Chest", equipment="Bodyweight"),
        Exercise(name="Cable Crossover", target_muscle="Chest", equipment="Cable Machine"),
        
        
        Exercise(name="Pull-up", target_muscle="Back", equipment="Pull-up Bar"),
        Exercise(name="Chin-up", target_muscle="Back", equipment="Pull-up Bar"),
        Exercise(name="Barbell Row", target_muscle="Back", equipment="Barbell"),
        Exercise(name="Dumbbell Row", target_muscle="Back", equipment="Dumbbell, Bench"),
        Exercise(name="Lat Pulldown", target_muscle="Back", equipment="Cable Machine"),
        Exercise(name="Deadlift", target_muscle="Back", equipment="Barbell"),

        
        Exercise(name="Barbell Squat", target_muscle="Legs", equipment="Barbell, Squat Rack"),
        Exercise(name="Dumbbell Lunge", target_muscle="Legs", equipment="Dumbbells"),
        Exercise(name="Leg Press", target_muscle="Legs", equipment="Leg Press Machine"),
        Exercise(name="Romanian Deadlift", target_muscle="Legs", equipment="Barbell"),
        Exercise(name="Goblet Squat", target_muscle="Legs", equipment="Dumbbell"),
        Exercise(name="Calf Raise", target_muscle="Legs", equipment="Bodyweight"),

        
        Exercise(name="Overhead Press", target_muscle="Shoulders", equipment="Barbell"),
        Exercise(name="Dumbbell Shoulder Press", target_muscle="Shoulders", equipment="Dumbbells"),
        Exercise(name="Dumbbell Lateral Raise", target_muscle="Shoulders", equipment="Dumbbells"),
        Exercise(name="Face Pull", target_muscle="Shoulders", equipment="Cable Machine"),

        
        Exercise(name="Barbell Curl", target_muscle="Biceps", equipment="Barbell"),
        Exercise(name="Dumbbell Hammer Curl", target_muscle="Biceps", equipment="Dumbbells"),
        Exercise(name="Preacher Curl", target_muscle="Biceps", equipment="Dumbbell, Bench"),
        Exercise(name="Tricep Pushdown", target_muscle="Triceps", equipment="Cable Machine"),
        Exercise(name="Skull Crusher", target_muscle="Triceps", equipment="Barbell, Bench"),
        Exercise(name="Diamond Push-up", target_muscle="Triceps", equipment="Bodyweight"),

        
        Exercise(name="Plank", target_muscle="Core", equipment="Bodyweight"),
        Exercise(name="Hanging Leg Raise", target_muscle="Core", equipment="Pull-up Bar"),
        Exercise(name="Cable Crunch", target_muscle="Core", equipment="Cable Machine"),

        
        Exercise(name="Treadmill Running", target_muscle="Cardio", equipment="Treadmill"),
        Exercise(name="Cycling", target_muscle="Cardio", equipment="Stationary Bike"),
        Exercise(name="Rowing", target_muscle="Cardio", equipment="Rowing Machine"),
    ]

    
    foods = [
        
        Food(name="Chicken Breast (Cooked)", calories_per_100g=165, protein_g_per_100g=31, carbs_g_per_100g=0, fat_g_per_100g=3.6),
        Food(name="Salmon (Cooked)", calories_per_100g=206, protein_g_per_100g=22, carbs_g_per_100g=0, fat_g_per_100g=13),
        Food(name="Ground Beef 90/10 (Cooked)", calories_per_100g=217, protein_g_per_100g=26, carbs_g_per_100g=0, fat_g_per_100g=12),
        Food(name="Tuna (Canned in water)", calories_per_100g=116, protein_g_per_100g=26, carbs_g_per_100g=0, fat_g_per_100g=1),
        Food(name="Egg (Large)", calories_per_100g=155, protein_g_per_100g=13, carbs_g_per_100g=1.1, fat_g_per_100g=11),
        Food(name="Greek Yogurt (Plain, Non-fat)", calories_per_100g=59, protein_g_per_100g=10, carbs_g_per_100g=3.6, fat_g_per_100g=0.4),
        Food(name="Tofu (Firm)", calories_per_100g=76, protein_g_per_100g=8, carbs_g_per_100g=1.9, fat_g_per_100g=4.8),
        Food(name="Lentils (Cooked)", calories_per_100g=116, protein_g_per_100g=9, carbs_g_per_100g=20, fat_g_per_100g=0.4),
        
        
        Food(name="White Rice (Cooked)", calories_per_100g=130, protein_g_per_100g=2.7, carbs_g_per_100g=28, fat_g_per_100g=0.3),
        Food(name="Brown Rice (Cooked)", calories_per_100g=123, protein_g_per_100g=2.6, carbs_g_per_100g=26, fat_g_per_100g=0.9),
        Food(name="Quinoa (Cooked)", calories_per_100g=120, protein_g_per_100g=4.4, carbs_g_per_100g=21, fat_g_per_100g=1.9),
        Food(name="Oats (Dry)", calories_per_100g=389, protein_g_per_100g=16.9, carbs_g_per_100g=66.3, fat_g_per_100g=6.9),
        Food(name="Sweet Potato (Cooked)", calories_per_100g=86, protein_g_per_100g=1.6, carbs_g_per_100g=20, fat_g_per_100g=0.1),
        Food(name="Potato (Cooked)", calories_per_100g=87, protein_g_per_100g=1.9, carbs_g_per_100g=20, fat_g_per_100g=0.1),
        Food(name="Whole Wheat Bread", calories_per_100g=247, protein_g_per_100g=13, carbs_g_per_100g=41, fat_g_per_100g=3.4),

        
        Food(name="Olive Oil", calories_per_100g=884, protein_g_per_100g=0, carbs_g_per_100g=0, fat_g_per_100g=100),
        Food(name="Avocado", calories_per_100g=160, protein_g_per_100g=2, carbs_g_per_100g=9, fat_g_per_100g=15),
        Food(name="Almonds", calories_per_100g=579, protein_g_per_100g=21, carbs_g_per_100g=22, fat_g_per_100g=49),
        Food(name="Peanut Butter", calories_per_100g=588, protein_g_per_100g=25, carbs_g_per_100g=20, fat_g_per_100g=50),

        
        Food(name="Broccoli (Raw)", calories_per_100g=34, protein_g_per_100g=2.8, carbs_g_per_100g=7, fat_g_per_100g=0.4),
        Food(name="Spinach (Raw)", calories_per_100g=23, protein_g_per_100g=2.9, carbs_g_per_100g=3.6, fat_g_per_100g=0.4),
        Food(name="Apple", calories_per_100g=52, protein_g_per_100g=0.3, carbs_g_per_100g=14, fat_g_per_100g=0.2),
        Food(name="Banana", calories_per_100g=89, protein_g_per_100g=1.1, carbs_g_per_100g=23, fat_g_per_100g=0.3),
    ]

    session.add_all(exercises)
    session.add_all(foods)
    session.commit()
    session.close()

    print("✅ Database seeding complete!")

if __name__ == "__main__":
    seed_database()