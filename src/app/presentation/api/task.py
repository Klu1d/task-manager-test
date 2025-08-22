from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Query
from app.domain.entities import Status

from app.application.interactors import (
    GetAllTaskInteractor,
    GetTaskInteractor,
    NewTaskInteractor,
    RemoveTaskInteractor,
    UpdateTaskInteractor,
)
from app.presentation.api.schemas import (
    TaskRequest,
    TaskResponse,
)

router = APIRouter(prefix="/task", tags=["Tasks"], route_class=DishkaRoute)


@router.get("/")
async def get_list(interactor: FromDishka[GetAllTaskInteractor]) -> list[TaskResponse]:
    return await interactor()


@router.post("/")
async def create_task(
    body: TaskRequest,
    interactor: FromDishka[NewTaskInteractor],
) -> TaskResponse:
    domain_task = await interactor(body)
    return TaskResponse(
        uuid=str(domain_task.uuid),
        title=domain_task.title,
        description=domain_task.description,
        status=domain_task.status,
        created_at=domain_task.created_at,
        updated_at=domain_task.updated_at,
    )


@router.get("/{id}")
async def get_task(
    uuid: UUID,
    interactor: FromDishka[GetTaskInteractor],
) -> TaskResponse:
    domain_task = await interactor(str(uuid))
    if domain_task is None:
        raise HTTPException(status_code=404, detail=f"Task with '{uuid}' not found")
    return TaskResponse(
        uuid=str(domain_task.uuid),
        title=domain_task.title,
        description=domain_task.description,
        status=domain_task.status,
        created_at=domain_task.created_at,
        updated_at=domain_task.updated_at,
    )


@router.patch("/{id}")
async def update_task(
    uuid: UUID,
    body: TaskRequest,
    interactor: FromDishka[UpdateTaskInteractor],
    status: Status = Query(None),
) -> TaskResponse:
    domain_task = await interactor(uuid, status, body)
    if domain_task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with '{uuid}' not found"
        )
    return TaskResponse(
        uuid=str(uuid),
        title=domain_task.title,
        description=domain_task.description,
        status=domain_task.status,
        created_at=domain_task.created_at,
        updated_at=domain_task.updated_at,
    )


@router.delete("/{id}")
async def delete_task(uuid: UUID, interactor: FromDishka[RemoveTaskInteractor]):
    result = await interactor(str(uuid))
    if result is None:
        raise HTTPException(status_code=404, detail=f"Task with '{uuid}' not found")
    return {"message": "success"}
