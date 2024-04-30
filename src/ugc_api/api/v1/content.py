from http import HTTPStatus
from http.client import HTTPException

from aiokafka.errors import KafkaError
from fastapi import APIRouter, Depends
from models.content_model import BaseContent
from services.content_loader import ContentService, get_content_loader_service

router = APIRouter()


@router.post(
    '/set_content',
    response_model=None,
)
async def set_content(
    content: BaseContent,
    content_service: ContentService = Depends(get_content_loader_service),
) -> HTTPStatus | HTTPException:
    try:
        await content_service.produce(content)
    except KafkaError:
        return HTTPStatus.INTERNAL_SERVER_ERROR

    return HTTPStatus.OK

