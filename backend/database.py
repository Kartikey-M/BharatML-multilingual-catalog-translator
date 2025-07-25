"""
Database manager for storing translations and corrections
Uses SQLite for simplicity
"""

import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
import os

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database for translation storage"""
    
    def __init__(self, db_path: str = "../data/translations.db"):
        self.db_path = db_path
        self.ensure_db_directory()
    
    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def initialize_database(self):
        """Initialize database tables"""
        try:
            with self.get_connection() as conn:
                # Create translations table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS translations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_text TEXT NOT NULL,
                        translated_text TEXT NOT NULL,
                        source_language TEXT NOT NULL,
                        target_language TEXT NOT NULL,
                        model_confidence REAL DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create corrections table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS corrections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        translation_id INTEGER NOT NULL,
                        corrected_text TEXT NOT NULL,
                        feedback TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (translation_id) REFERENCES translations (id)
                    )
                """)
                
                # Create indexes for better performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_translations_languages 
                    ON translations (source_language, target_language)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_translations_created 
                    ON translations (created_at)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_corrections_translation 
                    ON corrections (translation_id)
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def store_translation(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        model_confidence: float = 0.0
    ) -> int:
        """
        Store a translation in the database
        
        Args:
            original_text: Original text
            translated_text: Translated text
            source_language: Source language code
            target_language: Target language code
            model_confidence: Model confidence score
            
        Returns:
            Translation ID
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO translations 
                    (original_text, translated_text, source_language, target_language, model_confidence)
                    VALUES (?, ?, ?, ?, ?)
                """, (original_text, translated_text, source_language, target_language, model_confidence))
                
                translation_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Translation stored with ID: {translation_id}")
                return translation_id
                
        except Exception as e:
            logger.error(f"Error storing translation: {str(e)}")
            raise
    
    def store_correction(
        self,
        translation_id: int,
        corrected_text: str,
        feedback: Optional[str] = None
    ) -> int:
        """
        Store a correction for a translation
        
        Args:
            translation_id: ID of the original translation
            corrected_text: Corrected text
            feedback: Optional feedback about the correction
            
        Returns:
            Correction ID
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO corrections (translation_id, corrected_text, feedback)
                    VALUES (?, ?, ?)
                """, (translation_id, corrected_text, feedback))
                
                correction_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Correction stored with ID: {correction_id}")
                return correction_id
                
        except Exception as e:
            logger.error(f"Error storing correction: {str(e)}")
            raise
    
    def get_translation_history(
        self,
        limit: int = 50,
        offset: int = 0,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get translation history
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            source_language: Filter by source language
            target_language: Filter by target language
            
        Returns:
            List of translation history records
        """
        try:
            with self.get_connection() as conn:
                # Build query with optional filters
                where_conditions = []
                params = []
                
                if source_language:
                    where_conditions.append("t.source_language = ?")
                    params.append(source_language)
                
                if target_language:
                    where_conditions.append("t.target_language = ?")
                    params.append(target_language)
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                query = f"""
                    SELECT 
                        t.id,
                        t.original_text,
                        t.translated_text,
                        t.source_language,
                        t.target_language,
                        t.model_confidence,
                        t.created_at,
                        c.corrected_text,
                        c.feedback as correction_feedback
                    FROM translations t
                    LEFT JOIN corrections c ON t.id = c.translation_id
                    {where_clause}
                    ORDER BY t.created_at DESC
                    LIMIT ? OFFSET ?
                """
                
                params.extend([limit, offset])
                
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to dictionaries
                results = []
                for row in rows:
                    results.append({
                        "id": row["id"],
                        "original_text": row["original_text"],
                        "translated_text": row["translated_text"],
                        "source_language": row["source_language"],
                        "target_language": row["target_language"],
                        "model_confidence": row["model_confidence"],
                        "created_at": row["created_at"],
                        "corrected_text": row["corrected_text"],
                        "correction_feedback": row["correction_feedback"]
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error retrieving translation history: {str(e)}")
            raise
    
    def get_translation_by_id(self, translation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific translation by ID
        
        Args:
            translation_id: Translation ID
            
        Returns:
            Translation record or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT 
                        t.id,
                        t.original_text,
                        t.translated_text,
                        t.source_language,
                        t.target_language,
                        t.model_confidence,
                        t.created_at,
                        c.corrected_text,
                        c.feedback as correction_feedback
                    FROM translations t
                    LEFT JOIN corrections c ON t.id = c.translation_id
                    WHERE t.id = ?
                """, (translation_id,))
                
                row = cursor.fetchone()
                
                if row:
                    return {
                        "id": row["id"],
                        "original_text": row["original_text"],
                        "translated_text": row["translated_text"],
                        "source_language": row["source_language"],
                        "target_language": row["target_language"],
                        "model_confidence": row["model_confidence"],
                        "created_at": row["created_at"],
                        "corrected_text": row["corrected_text"],
                        "correction_feedback": row["correction_feedback"]
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving translation {translation_id}: {str(e)}")
            raise
    
    def get_corrections_for_training(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Get corrections that can be used for model fine-tuning
        
        Args:
            limit: Maximum number of corrections to return
            
        Returns:
            List of correction records suitable for training
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT 
                        t.original_text,
                        t.source_language,
                        t.target_language,
                        c.corrected_text,
                        c.feedback,
                        c.created_at
                    FROM corrections c
                    JOIN translations t ON c.translation_id = t.id
                    ORDER BY c.created_at DESC
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    results.append({
                        "original_text": row["original_text"],
                        "source_language": row["source_language"],
                        "target_language": row["target_language"],
                        "corrected_text": row["corrected_text"],
                        "feedback": row["feedback"],
                        "created_at": row["created_at"]
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error retrieving corrections for training: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary with various statistics
        """
        try:
            with self.get_connection() as conn:
                # Total translations
                cursor = conn.execute("SELECT COUNT(*) FROM translations")
                total_translations = cursor.fetchone()[0]
                
                # Total corrections
                cursor = conn.execute("SELECT COUNT(*) FROM corrections")
                total_corrections = cursor.fetchone()[0]
                
                # Translations by language pair
                cursor = conn.execute("""
                    SELECT source_language, target_language, COUNT(*) as count
                    FROM translations
                    GROUP BY source_language, target_language
                    ORDER BY count DESC
                """)
                language_pairs = cursor.fetchall()
                
                # Recent activity (last 7 days)
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM translations
                    WHERE created_at >= datetime('now', '-7 days')
                """)
                recent_translations = cursor.fetchone()[0]
                
                return {
                    "total_translations": total_translations,
                    "total_corrections": total_corrections,
                    "recent_translations": recent_translations,
                    "language_pairs": [
                        {
                            "source": row["source_language"],
                            "target": row["target_language"],
                            "count": row["count"]
                        }
                        for row in language_pairs
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error retrieving statistics: {str(e)}")
            raise
    
    def cleanup_old_records(self, days: int = 30):
        """
        Clean up old translation records
        
        Args:
            days: Number of days to keep records
        """
        try:
            with self.get_connection() as conn:
                # Delete old corrections first (due to foreign key constraint)
                cursor = conn.execute("""
                    DELETE FROM corrections
                    WHERE translation_id IN (
                        SELECT id FROM translations
                        WHERE created_at < datetime('now', '-' || ? || ' days')
                    )
                """, (days,))
                
                deleted_corrections = cursor.rowcount
                
                # Delete old translations
                cursor = conn.execute("""
                    DELETE FROM translations
                    WHERE created_at < datetime('now', '-' || ? || ' days')
                """, (days,))
                
                deleted_translations = cursor.rowcount
                
                conn.commit()
                
                logger.info(f"Cleaned up {deleted_translations} translations and {deleted_corrections} corrections older than {days} days")
                
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise
