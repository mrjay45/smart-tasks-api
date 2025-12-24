from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from classification_service import (
    category_classification,
    entity_extraction,
    priority_detection,
    suggested_action,
)
from schemas import TaskCreate, TaskUpdate
from supabase_client import supabase


# create the fastapi object
app = FastAPI()


# Global error handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )


# home route
@app.get("/")
def index():
    return {"Message": "The API is running"}


# task post route
@app.post("/api/tasks")
def post_task(task: TaskCreate):
    try:
        text = f"{task.title} {task.description or ''}"
        category = category_classification(text).lower()
        priority = priority_detection(text).lower()
        entities = entity_extraction(text)
        actions = suggested_action(category)

        response = (
            supabase.table("tasks")
            .insert(
                {
                    "title": task.title,
                    "description": task.description,
                    "category": category,
                    "priority": priority,
                    "status": task.status,
                    "assigned_to": task.assigned_to,
                    "due_date": task.due_date,
                    "extracted_entities": entities,
                    "suggested_actions": actions,
                }
            )
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create task.")
        created_task = response.data[0]
        log_task_history(
            task_id=created_task["id"],
            new_val=created_task,
            old_val=None,
            action="created",
        )
        return created_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


# get task endpoint
@app.get("/api/tasks")
def get_tasks(
    status: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    try:
        query = supabase.table("tasks").select("*")
        if status is not None:
            query = query.eq("status", status)
        if category is not None:
            query = query.eq("category", category)
        if priority is not None:
            query = query.eq("priority", priority)
        response = query.range(offset, offset + limit - 1).execute()
        if response.data is None:
            raise HTTPException(status_code=404, detail="No tasks found.")
        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")


# get the task by id and history
@app.get("/api/tasks/{id}")
def get_task_by_id(id: str):
    try:
        response = supabase.table("tasks").select().eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Task Not Found")
        task = response.data[0]
        task_history = (
            supabase.table("task_history")
            .select("*")
            .eq("task_id", id)
            .order("changed_at", desc=True)
            .execute()
        )
        return {"task": task, "history": task_history.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching task by id: {str(e)}"
        )


# Patch the data (Update the data)
@app.patch("/api/task/{id}")
def update_task(id: str, task: TaskUpdate):
    try:
        existing = supabase.table("tasks").select().eq("id", id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Task Not Found")

        old_value = {"task_id": existing.data[0]["id"]}

        update_data = task.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=400, detail="No fields are provided for update"
            )

        for e_k, e_v in existing.data[0].items():
            if e_k in update_data:
                old_value[e_k] = e_v

        if "due_date" in update_data and update_data["due_date"] is not None:
            update_data["due_date"] = update_data["due_date"].isoformat()

        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        response = supabase.table("tasks").update(update_data).eq("id", id).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to update task.")

        updated_task = {"task_id": response.data[0]["id"]}

        for u_k, u_v in response.data[0].items():
            if u_k in old_value:
                updated_task[u_k] = u_v
                
        if "status" in update_data and update_data["status"] == "completed":
            log_task_history(
                task_id=updated_task["task_id"],
                action="completed",
                new_val=updated_task,
                old_val=old_value,
            )
        elif "status" in update_data and update_data["status"] is not None:
            log_task_history(
                task_id=updated_task["task_id"],
                action="status_changed",
                new_val=updated_task,
                old_val=old_value,
            )
        else:
            log_task_history(
                task_id=updated_task["task_id"],
                action="updated",
                new_val=updated_task,
                old_val=old_value,
            )
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


# delete the task
@app.delete("/api/task/{id}")
def delete_task(id: str):
    try:
        existing = supabase.table("tasks").select("*").eq("id", id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Task Not Found")

        supabase.table("task_history").delete().eq("task_id", id).execute()

        supabase.table("tasks").delete().eq("id", id).execute()

        return {"detail": "Task Deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")


def log_task_history(task_id: str, action: str, old_val: dict, new_val: dict):

    supabase.table("task_history").insert(
        {
            "task_id": task_id,
            "action": action,
            "old_value": old_val,
            "new_value": new_val,
            "changed_by": "system",
        }
    ).execute()
