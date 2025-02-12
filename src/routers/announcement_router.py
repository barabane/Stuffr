from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models.user_model import User
from src.dependencies import get_current_user
from src.schemas.announcement_schemas import (
    CreateAnnouncementScheme,
    GetAnnouncementScheme,
)
from src.services.announcement_service import (
    AnnouncementService,
    get_announcement_service,
)
from src.utils.decorators import protect

announcement_router = APIRouter(prefix='/announcement', tags=['Announcement'])


@announcement_router.post('')
async def create_announcement(
    announcement_scheme: CreateAnnouncementScheme,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    announcement_scheme.user_id = user.id
    await announcement_service.add(announcement_scheme, session=session)

    return JSONResponse(
        status_code=201,
        content={'details': 'Ваше объявление отправлено на модерацию'},
    )


@announcement_router.patch('/approve', response_model=GetAnnouncementScheme)
@protect(role_id=2)
async def approve_announcement(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> GetAnnouncementScheme:
    announcement_model = await announcement_service.approve(
        announcement_id, user=user, session=session
    )
    return GetAnnouncementScheme(**announcement_model.__dict__)
