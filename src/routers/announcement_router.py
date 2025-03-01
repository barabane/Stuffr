from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models.user_model import User
from src.dependencies import get_cache, get_current_user
from src.exceptions import AnnouncementUnderReviewException, NotFoundException
from src.schemas.announcement_schemas import (
    AnnouncementStatus,
    CreateAnnouncementOuterScheme,
    CreateAnnouncementScheme,
    GetAnnouncementScheme,
    GetMyAnnouncementScheme,
    SearchParams,
    SearchParamsProfile,
    UpdateAnnouncementOuterScheme,
)
from src.services.announcement_service import (
    AnnouncementService,
    get_announcement_service,
)
from src.utils.cache import RedisCache
from src.utils.decorators import protect

announcement_router = APIRouter(prefix='/announcement', tags=['Announcement'])


@announcement_router.post('', tags=['AnnouncementUser'])
async def create_announcement(
    announcement_scheme: CreateAnnouncementOuterScheme,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    announcement_scheme = CreateAnnouncementScheme(
        **announcement_scheme.model_dump(), user_id=user.id
    )

    await announcement_service.add(
        announcement_service.schemas.create_scheme(**announcement_scheme.model_dump()),
        session=session,
    )

    return JSONResponse(
        status_code=201,
        content={'details': 'Ваше объявление отправлено на модерацию'},
    )


@announcement_router.patch('/edit/{announcement_id}', tags=['AnnouncementUser'])
async def edit_announcement(
    announcement_id: str,
    announcement_scheme: UpdateAnnouncementOuterScheme,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    announcement_model = await session.get(
        announcement_service.repository.model, announcement_id
    )

    if not announcement_model:
        raise NotFoundException(detail='Такого объявления не существует')

    if announcement_model.status == AnnouncementStatus.UNDER_REVIEW.value:
        raise AnnouncementUnderReviewException

    await announcement_service.update(
        entity=announcement_service.schemas.update_scheme(
            **announcement_scheme.model_dump()
        ),
        entity_id=announcement_id,
        session=session,
    )

    return JSONResponse(
        status_code=201,
        content={'details': 'Ваше объявление отправлено на модерацию'},
    )


@announcement_router.patch(
    '/approve', response_model=GetAnnouncementScheme, tags=['AnnouncementAdmin']
)
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


@announcement_router.patch(
    '/decline', response_model=GetAnnouncementScheme, tags=['AnnouncementAdmin']
)
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


@announcement_router.get(
    '', response_model=List[GetAnnouncementScheme], tags=['AnnouncementUser']
)
async def get_announcement_catalog(
    search_params: SearchParams = Depends(),
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    session: AsyncSession = Depends(get_async_session),
    cache: RedisCache = Depends(get_cache),
) -> List[GetAnnouncementScheme]:
    filters = search_params.model_dump()
    filters['status'] = AnnouncementStatus.PUBLISHED.value

    cache_key = f'announcements:{search_params.offset}{search_params.limit}'
    cached_values = await cache.get(key=cache_key)

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

    await cache.set(key=cache_key, value=announcements)
    return announcements


@announcement_router.get(
    '/my_announcements',
    response_model=List[GetMyAnnouncementScheme],
    tags=['AnnouncementUser'],
)
async def get_my_announcements(
    search_params: SearchParamsProfile = Depends(),
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    cache: RedisCache = Depends(get_cache),
) -> List[GetMyAnnouncementScheme]:
    filters = search_params.model_dump()
    filters['user_id'] = user.id

    cache_key = f'announcements:{search_params.offset}{search_params.limit}{user.id}'
    cached_values = await cache.get(key=cache_key)

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

    await cache.set(key=cache_key, value=announcements)
    return announcements


@announcement_router.patch(
    '/unpublish', tags=['AnnouncementUser'], response_model=GetMyAnnouncementScheme
)
async def unpublish_announcement(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> GetMyAnnouncementScheme:
    announcement_model = await announcement_service.unpublish(
        announcement_id=announcement_id, user=user, session=session
    )
    return GetMyAnnouncementScheme(**announcement_model.__dict__)


@announcement_router.patch(
    '/archive/{announcement_id}',
    tags=['AnnouncementUser'],
)
async def archive_announcement(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await announcement_service.archive_announcement(
        announcement_id=announcement_id, session=session
    )


@announcement_router.delete(
    '/delete/{announcement_id}',
    tags=['AnnouncementUser'],
)
async def delete_announcement(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await announcement_service.delete(entity_id=announcement_id, session=session)


@announcement_router.post('/add_favorite')
async def add_to_favorite(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await announcement_service.add_to_favorite(
        announcement_id=announcement_id, user=user, session=session
    )

    return JSONResponse(
        status_code=200,
        content={'details': 'Добавлено в список избранного'},
    )


@announcement_router.delete('/delete_favorite')
async def delete_from_favorite(
    announcement_id: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await announcement_service.delete_from_favorite(
        announcement_id=announcement_id, user=user, session=session
    )

    return JSONResponse(
        status_code=200,
        content={'details': 'Удалено из списка избранного'},
    )
