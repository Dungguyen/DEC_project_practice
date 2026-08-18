# src/utils/exceptions.py

class ETLException(Exception):
    """Base exception for ETL pipeline"""
    pass

class ExtractionError(ETLException):
    """Raised when extraction fails"""
    pass

class TransformationError(ETLException):
    """Raised when transformation fails"""
    pass

class LoadError(ETLException):
    """Raised when loading fails"""
    pass

class ValidationError(ETLException):
    """Raised when data validation fails"""
    pass

class DatabaseConnectionError(ETLException):
    """Raised when database connection fails"""
    pass