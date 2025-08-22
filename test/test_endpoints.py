from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException

from app.domain.entities import Status
from app.presentation.api.schemas import TaskRequest
from app.presentation.api.task import (
    create_task,
    delete_task,
    get_list,
    get_task,
    update_task,
)


def make_domain_task(**overrides):
    base = SimpleNamespace(
        uuid=uuid4(),
        title="Test task",
        description="Description",
        status=getattr(Status, "TODO", "todo"),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    for k, v in overrides.items():
        setattr(base, k, v)
    return base


@pytest.mark.asyncio
async def test_list_tasks():
    domain = make_domain_task()

    async def fake_interactor():
        return [domain]

    res = await get_list(fake_interactor)
    assert isinstance(res, list)
    assert len(res) == 1

    item = res[0]
    assert hasattr(item, "uuid") and (
        item.uuid == domain.uuid or str(item.uuid) == str(domain.uuid)
    )
    assert item.title == domain.title
    assert item.description == domain.description
    assert item.status == domain.status
    assert item.created_at == domain.created_at
    assert item.updated_at == domain.updated_at


@pytest.mark.asyncio
async def test_create_task():
    domain = make_domain_task()

    called = {"args": None}

    async def fake_interactor(body):
        called["args"] = body
        return domain

    if TaskRequest is not None:
        body = TaskRequest(title="t", description="d")
    else:
        body = SimpleNamespace(title="t", description="d")

    res = await create_task(body, fake_interactor)

    assert called["args"] is body

    assert hasattr(res, "uuid")
    assert res.uuid == domain.uuid or str(res.uuid) == str(domain.uuid)
    assert res.title == domain.title
    assert res.description == domain.description
    assert res.status == domain.status
    assert res.created_at == domain.created_at
    assert res.updated_at == domain.updated_at


@pytest.mark.asyncio
async def test_get_task():
    domain = make_domain_task()

    async def fake_interactor(id_str: str):
        assert isinstance(id_str, str)
        return domain

    uid = uuid4()
    res = await get_task(uid, fake_interactor)

    assert hasattr(res, "uuid")
    assert str(res.uuid) == str(domain.uuid)
    assert res.title == domain.title


@pytest.mark.asyncio
async def test_get_task_404():
    async def fake_interactor(id_str: str):
        return None

    with pytest.raises(HTTPException) as exc:
        await get_task(uuid4(), fake_interactor)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_update_task():
    domain = make_domain_task()

    async def fake_interactor(uuid_arg, status_arg, body_arg):
        assert isinstance(uuid_arg, (UUID, str))
        assert body_arg is not None
        return domain

    if TaskRequest is not None:
        body = TaskRequest(title="upd", description="desc")
    else:
        body = SimpleNamespace(title="upd", description="desc")

    new_status = getattr(Status, "DONE", None)
    uid = uuid4()
    res = await update_task(uid, body, fake_interactor, new_status)

    assert str(res.uuid) == str(uid)
    assert res.title == domain.title
    assert res.description == domain.description
    assert res.status == domain.status


@pytest.mark.asyncio
async def test_update_task_404():
    async def fake_interactor(uuid_arg, status_arg, body_arg):
        return None

    body = SimpleNamespace(title="doesn't matter", description="")
    with pytest.raises(HTTPException) as exc:
        await update_task(uuid4(), body, fake_interactor, None)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_task():
    async def fake_interactor_ok(id_str: str):
        return True

    async def fake_interactor_none(id_str: str):
        return None

    res = await delete_task(uuid4(), fake_interactor_ok)
    assert isinstance(res, dict)
    assert res.get("message") == "success"

    with pytest.raises(HTTPException) as exc:
        await delete_task(uuid4(), fake_interactor_none)
    assert exc.value.status_code == 404
