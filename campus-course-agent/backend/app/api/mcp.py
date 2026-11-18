from typing import Annotated
from app.common.response import Response
from fastapi import APIRouter, Depends, Query, Request
from app.dependencies.auth import get_current_user
from app.services import mcp_client_service
from app.models.user import User

router = APIRouter(prefix="/mcp", tags=["MCP服务调试"])


@router.get("/my-schedules")
async def get_my_schedules_by_mcp(
    _user: Annotated[User, Depends(get_current_user)],
    request: Request,
    date: Annotated[str | None, Query(description="YYYY-MM-DD,不传返回全部")] = None,
):
    authorization = request.headers.get("Authorization") or ""
    data = mcp_client_service.call_get_my_schedules(authorization, date)
    return Response.success(data=data)
