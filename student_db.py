
import sqlite3
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import json

class StudentDB:
    """Manages all the database operations for student data."""
    
    def __init__(self, db_path: str = 'student.db'):
        """Set up the database connection and create tables if needed."""
        self.db_path = db_path
        self._create_tables()  # Make sure our table exists
    
    def _get_connection(self):
        """Get a connection to our SQLite database."""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Set up our database tables if they don't exist yet."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Create the main students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,  -- Unique ID for each student
                    student_name TEXT NOT NULL,   -- Student's full name
                    zpd_score REAL DEFAULT 5.0,   -- Current difficulty level
                    zp_history TEXT DEFAULT '[]', -- Past ZPD scores as JSON array
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()  # Save the changes
    
    def add_student(self, student_id: str, student_name: str, initial_zpd: float = 5.0) -> bool:
        """Add a new student to our system.
        
        Returns True if added successfully, False if the student ID is already taken.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Add the new student with their starting ZPD score
                cursor.execute('''
                    INSERT INTO students (student_id, student_name, zpd_score, zp_history)
                    VALUES (?, ?, ?, ?)
                ''', (student_id, student_name, initial_zpd, '[5.0]'))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Oops, this student ID is already in use
            return False
    
    def update_zpd_score(self, student_id: str, new_zpd: float) -> bool:
        """Update a student's ZPD score and keep track of their history.
        
        Returns True if we found and updated the student, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Grab their current history
            cursor.execute('SELECT zp_history FROM students WHERE student_id = ?', (student_id,))
            result = cursor.fetchone()
            
            # No student found with this ID
            if not result:
                return False
            
            # Update their score history (keep last 10 scores)
            score_history = json.loads(result[0])
            score_history.append(new_zpd)
            score_history = score_history[-10:]
            
            # Save everything back to the database
            cursor.execute('''
                UPDATE students 
                SET zpd_score = ?, 
                    zp_history = ?,
                    last_updated = CURRENT_TIMESTAMP
                WHERE student_id = ?
            ''', (new_zpd, json.dumps(score_history), student_id))
            
            conn.commit()
            return cursor.rowcount > 0  # True if we updated a record
    
    def get_student(self, student_id: str) -> Optional[Dict]:
        """Look up a student by their ID.
        
        Returns their info as a dictionary, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT student_id, student_name, zpd_score, zp_history, created_at, last_updated
                FROM students
                WHERE student_id = ?
            ''', (student_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'student_id': row[0],
                    'student_name': row[1],
                    'zpd_score': row[2],
                    'zp_history': json.loads(row[3]),
                    'created_at': row[4],
                    'last_updated': row[5]
                }
            return None
    
    def get_all_students(self) -> List[Dict]:
        """Get a list of all students in the system, sorted by name."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT student_id, student_name, zpd_score, zp_history, created_at, last_updated
                FROM students
                ORDER BY student_name
            ''')
            
            return [{
                'student_id': row[0],
                'student_name': row[1],
                'zpd_score': row[2],
                'zp_history': json.loads(row[3]),
                'created_at': row[4],
                'last_updated': row[5]
            } for row in cursor.fetchall()]
    
    def get_zpd_history(self, student_id: str) -> list[float]:
        """Get a list of a student's past ZPD scores, with the most recent last.
        
        Returns an empty list if the student isn't found or has no history.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT zp_history FROM students WHERE student_id = ?', (student_id,))
            result = cursor.fetchone()
            
            if not result or not result[0]:
                return []
                
            return json.loads(result[0])

# Quick test if we run this file directly
if __name__ == "__main__":
    # Try out the database
    db = StudentDB()
    
    # Add a test student
    db.add_student("S001", "John Doe", 5.0)
    
    # Bump up their ZPD score
    db.update_zpd_score("S001", 5.5)
    
    # Check their info
    student = db.get_student("S001")
    print(f"Student: {student}")
    
    # List everyone
    all_students = db.get_all_students()
    print(f"All students: {all_students}")
    
    # Look at their progress
    zpd_history = db.get_zpd_history("S001")
    print(f"ZPD history: {zpd_history}")
