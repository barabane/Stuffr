from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models.user_model import User
from src.dependencies import get_current_user
from src.schemas.announcement_schemas import (
    AnnouncementStatus,
    CreateAnnouncementScheme,
    GetAnnouncementScheme,
    GetMyAnnouncementScheme,
    SearchParams,
    SearchParamsProfile,
)
from src.services.announcement_service import (
    AnnouncementService,
    get_announcement_service,
)
from src.utils.cache import redis_cache
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
    return announcement_service.schemas.get_scheme(**announcement_model.__dict__)


@announcement_router.patch('/decline', response_model=GetAnnouncementScheme)
@protect(role_id=2)
async def decline_announcement(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    announcement_model = await announcement_service.decline(
        announcement_id, user=user, session=session
    )
    return announcement_service.schemas.get_scheme(**announcement_model.__dict__)


@announcement_router.get('', response_model=List[GetAnnouncementScheme])
async def get_announcement_catalog(
    search_params: SearchParams = Depends(),
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    session: AsyncSession = Depends(get_async_session),
) -> List[GetAnnouncementScheme]:
    filters = search_params.model_dump()
    filters['status'] = AnnouncementStatus.PUBLISHED.value

    cache_key = f'announcements:{search_params.offset}{search_params.limit}'
    cached_values = await redis_cache.get(key=cache_key)

    if cached_values:
        return [
            announcement_service.schemas.get_scheme(**announcement_dict)
            for announcement_dict in cached_values
        ]

    announcements = [
        announcement_service.schemas.get_scheme(**announcement_model.__dict__)
        for announcement_model in await announcement_service.get_all(
            filters=filters, session=session
        )
    ]

    await redis_cache.set(key=cache_key, value=announcements)
    return announcements


@announcement_router.get(
    '/my_announcements', response_model=List[GetMyAnnouncementScheme]
)
async def get_my_announcements(
    search_params: SearchParamsProfile = Depends(),
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> List[GetMyAnnouncementScheme]:
    filters = search_params.model_dump()
    filters['user_id'] = user.id

    cache_key = f'announcements:{search_params.offset}{search_params.limit}{user.id}'
    cached_values = await redis_cache.get(key=cache_key)

    if cached_values:
        return [
            GetMyAnnouncementScheme(**announcement_dict)
            for announcement_dict in cached_values
        ]

    announcements = [
        GetMyAnnouncementScheme(**announcement_model.__dict__)
        for announcement_model in await announcement_service.get_all(
            filters=filters, session=session
        )
    ]

    await redis_cache.set(key=cache_key, value=announcements)
    return announcements
