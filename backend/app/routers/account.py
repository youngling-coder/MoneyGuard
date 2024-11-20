from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/accounts", tags=["Accounts"])