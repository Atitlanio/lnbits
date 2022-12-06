from http import HTTPStatus
from typing import Optional

from fastapi import Body, Query
from fastapi.params import Depends
from starlette.exceptions import HTTPException

from lnbits.core.crud import get_wallet
from lnbits.decorators import check_admin
from lnbits.extensions.admin import admin_ext
from lnbits.extensions.admin.models import AdminSettings, UpdateSettings
from lnbits.server import server_restart

from .crud import (
    delete_admin_settings,
    get_admin_settings,
    update_admin_settings,
    update_wallet_balance,
)


@admin_ext.get(
    "/api/v1/restart/", status_code=HTTPStatus.OK, dependencies=[Depends(check_admin)]
)
async def api_restart_server() -> dict[str, str]:
    server_restart.set()
    return {"status": "Success"}


@admin_ext.get("/api/v1/settings/", dependencies=[Depends(check_admin)])
async def api_get_settings() -> Optional[AdminSettings]:
    return await get_admin_settings()


@admin_ext.put(
    "/api/v1/topup/", status_code=HTTPStatus.OK, dependencies=[Depends(check_admin)]
)
async def api_update_balance(
    id: str = Body(...), amount: int = Body(...)
) -> dict[str, str]:
    try:
        await get_wallet(id)
    except:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="wallet does not exist."
        )

    await update_wallet_balance(wallet_id=id, amount=int(amount))

    return {"status": "Success"}


@admin_ext.put(
    "/api/v1/settings/", status_code=HTTPStatus.OK, dependencies=[Depends(check_admin)]
)
async def api_update_settings(data: UpdateSettings):
    await update_admin_settings(data)
    return {"status": "Success"}


@admin_ext.delete(
    "/api/v1/settings/", status_code=HTTPStatus.OK, dependencies=[Depends(check_admin)]
)
async def api_delete_settings() -> dict[str, str]:
    await delete_admin_settings()
    return {"status": "Success"}
