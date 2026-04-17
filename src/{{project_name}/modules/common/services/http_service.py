from fastapi import Response


def set_location_service(response: Response, location: str):
    response.headers["Location"] = location