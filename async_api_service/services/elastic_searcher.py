from abc import ABC, abstractmethod

from core.constants import MODELS_BY_INDEX
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.elasticsearch_queries import get_interception_query, titles_by_uuid_query


class AsyncDataStorage(ABC):
    @abstractmethod
    async def search(self, index: str, body: str):
        pass

    @abstractmethod
    async def get_by_id(self, index: str, doc_id: str):
        pass


class ElasticSearcher(AsyncDataStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index: str, doc_id: str) -> dict | None:
        try:
            doc = await self.elastic.get(index=index, id=doc_id)
        except NotFoundError:
            return None

        return MODELS_BY_INDEX[index](**doc['_source'])

    async def search(self, index: str, body: str):
        return await self.elastic.search(
            index=index,
            body=body,
        )

    async def get_interception(self, index: str, movies: list[str]):
        return await self.elastic.search(
            index=index,
            body=get_interception_query(movies),
        )

    async def get_movies_by_uuids(self, index: str, movies: list[str]):
        return await self.elastic.search(
            index=index,
            body=titles_by_uuid_query(movies),
        )


async def get_es_searcher(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticSearcher:
    return ElasticSearcher(elastic)
