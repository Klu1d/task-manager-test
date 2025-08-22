from unittest.mock import ANY, MagicMock, create_autospec
from uuid import uuid4

import pytest
from faker import Faker

from app.application import interfaces
from app.application.dto import TaskDTO
from app.application.interactors import GetTaskInteractor, NewTaskInteractor
from app.domain import entities

pytestmark = pytest.mark.asyncio


@pytest.fixture
def get_task_interactor() -> GetTaskInteractor:
    task_gateway = create_autospec(interfaces.TaskReader)
    return GetTaskInteractor(task_gateway)


@pytest.mark.parametrize("uuid", [str(uuid4()), str(uuid4())])
async def test_get_task(get_task_interactor: GetTaskInteractor, uuid: str) -> None:
    result = await get_task_interactor(uuid=uuid)
    get_task_interactor._gateway.read_by_uuid.assert_awaited_once_with(uuid=uuid)
    assert result == get_task_interactor._gateway.read_by_uuid.return_value


@pytest.fixture
def new_task_interactor(faker: Faker) -> NewTaskInteractor:
    session = create_autospec(interfaces.DBSession)
    gateway = create_autospec(interfaces.TaskSaver)
    uuid_generator = MagicMock(return_value=faker.uuid4())
    return NewTaskInteractor(gateway, uuid_generator, session)


async def test_new_task_interactor(
    new_task_interactor: NewTaskInteractor, faker: Faker
) -> None:
    dto = TaskDTO(
        title=faker.pystr(),
        description=faker.pyint(),
    )
    result = await new_task_interactor(dto=dto)
    uuid = str(new_task_interactor._uuid_generator())
    new_task_interactor._gateway.save.assert_awaited_with(
        entities.Task(
            uuid=uuid,
            title=dto.title,
            description=dto.description,
            status=entities.Status.CREATED,
            created_at=ANY,
            updated_at=None,
        )
    )
    new_task_interactor._session.commit.assert_awaited_once()
    assert result.uuid == uuid
