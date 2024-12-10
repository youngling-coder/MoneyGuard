from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path

from .. import models, schemas
from ..database import get_db
from ..oauth2 import oauth2

router = APIRouter(prefix="/transactions", tags=["Transactions"])