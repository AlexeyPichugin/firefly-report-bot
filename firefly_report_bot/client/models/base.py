from pydantic import BaseModel, AnyHttpUrl, types
from abc import ABC


class BaseAttributes(BaseModel, ABC):
    """
    Base class for model attributes
    """

    pass


class BaseData(BaseModel, ABC):
    """
    Base class for response data
    """

    type: str
    id: int
    attributes: BaseAttributes | list[BaseAttributes]
    links: dict | types.Json | None = None


class MetadataPagination(BaseModel):
    """
    Pagination metadata

    Attributes:
        total (int): Total number of items
        count (int): Number of items returned
        per_page (int): Number of items per page
        current_page (int): Current page number
        total_pages (int): Total number of pages
    """

    total: int = 0
    count: int = 0
    per_page: int = 0
    current_page: int = 0
    total_pages: int = 0


class Metadata(BaseModel):
    """
    Metadata for response data

    Attributes:
        pagination (MetadataPagination | None): Pagination metadata
    """

    pagination: MetadataPagination = MetadataPagination()


class Links(BaseModel):
    """
    Links to related resources

    Attributes:
        self (AnyHttpUrl | None): URL to the current resource
        first (AnyHttpUrl | None): URL to the first page of related resources
        prev (AnyHttpUrl | None): URL to the previous page of related resources
        next (AnyHttpUrl | None): URL to the next page of related resources
        last (AnyHttpUrl | None): URL to the last page of related resources
    """

    self: AnyHttpUrl | None = None
    first: AnyHttpUrl | None = None
    prev: AnyHttpUrl | None = None
    next: AnyHttpUrl | None = None
    last: AnyHttpUrl | None = None


class BaseFireflyModel(BaseModel, ABC):
    """
    Base class for all Firefly models

    Attributes:
        meta (Metadata | None): Metadata for the response
        links (Links | None): Links to related resources
    """

    meta: Metadata = Metadata()
    links: Links = Links()
