#  define the class or schema that validates the post request

from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List, Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = 'pending'
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] =None
    priority: Optional[str] = None