"""
Role Router Module to define the FastAPI endpoint for creating, getting, and listing
roles.

Raises:
    HTTPException: The role could not be found.
    HTTPException: The role could not be created.
"""

from typing import List
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from db.db_manager import DatabaseManager

role_router = APIRouter(prefix="/roles", tags=["roles"])
crud = DatabaseManager()


# Pydantic models for request/response
class RoleCreate(BaseModel):
    """
    Pydantic model for creating a new role.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    role_name: str
    level: int


class RoleResponse(BaseModel):
    """
    Pydantic model for role response.

    Args:
        BaseModel (): The base Pydantic model class.
    """

    id: int
    role_name: str
    level: int

    class Config:
        orm_mode = True


@role_router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate):
    """
    Create a new role.

    Args:
        role (RoleCreate): The role to create.

    Raises:
        HTTPException: The role could not be created.

    Returns:
        RoleHierarchy: The created role.
    """
    try:
        return crud.create_role(role_name=role.role_name, level=role.level)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@role_router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int):
    """
    Get a role by ID.

    Args:
        role_id (int): The role ID to get.

    Raises:
        HTTPException: The role could not be found.

    Returns:
        RoleHierarchy: The role.
    """
    role = crud.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@role_router.get("/name/{role_name}", response_model=RoleResponse)
def get_role_by_name(role_name: str):
    """
    Get a role by name.

    Args:
        role_name (str): The role name to get.

    Raises:
        HTTPException: The role could not be found.

    Returns:
        RoleHierarchy: The role.
    """
    role = crud.get_role_by_name(role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@role_router.get("/", response_model=List[RoleResponse])
def get_all_roles():
    """
    Get all roles.

    Returns:
        List[RoleHierarchy]: The list of all roles.
    """
    return crud.get_all_roles()