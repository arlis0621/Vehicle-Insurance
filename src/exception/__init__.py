import sys
import logging
from typing import Any

# Configure basic logging so errors actually print to the console
logging.basicConfig(level=logging.INFO)

def error_message_detail(error: Exception, error_detail: Any) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.
    """
    # Extract traceback details (exception information)
    _, _, exc_tb = error_detail.exc_info()

    # Safeguard if exc_tb is None (e.g., if called outside an except block)
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown"
        line_number = "Unknown"

    # Create a formatted error message string
    error_message = f"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}"

    # Log the error for better tracking
    logging.error(error_message)

    return error_message


class MyException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """
    def __init__(self, error_message: Exception, error_detail: Any):
        """
        Initializes the MyException with a detailed error message.
        
        :param error_message: The original Exception object caught in the try-except block.
        :param error_detail: The sys module to access traceback details.
        """
        # Pass the string representation of the error to the base Exception class
        super().__init__(str(error_message))

        # FIX: Pass the actual Exception object (not a raw string) to the detail formatter
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.error_message
