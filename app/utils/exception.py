"""Implementing error exceptions."""

from fastapi import HTTPException

def http_exception(message: str, status: int, headers:dict = None) -> HTTPException:
    """Generate an HTTPException with the specified error message and status.

    This function creates and returns an instance of `HTTPException`, which is used to
    handle HTTP errors. It takes a string for the error message, a status code to
    indicate the type of error, and optional headers for the response.

    Arguments:
        message (str): A string containing the error message details.
        status (int): The HTTP status code representing the error.
        headers (dict, optional): Optional headers to include in the HTTP response.

    Returns:
        HTTPException: An instance of `HTTPException` with the provided status,
        message, and headers.

    """
    return HTTPException(
        status_code=status,
        detail=message,
        headers=headers
    )
