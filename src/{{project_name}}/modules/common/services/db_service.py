from typing import Sequence, Tuple, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.orm import class_mapper

from ....config.db import Session


T = TypeVar('T')
Parent_T = TypeVar('Parent_T')
Child_T = TypeVar('Child_T')


async def find_one_or_fail(
        *,
        query: Select[Tuple[T]],
        session: Session, 
        error_message: str
) -> T:
    result = await session.scalar(query)

    if not result:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )

    return result


async def update_model(
    *,
    instance: T,
    schema: BaseModel,
    session: Session
) -> T:
    for key, value in schema.model_dump(exclude_unset=True).items():
        setattr(instance, key, value)
    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance



def _get_relationship_name(child_cls: type[Child_T], parent_cls: type[Parent_T]) -> str | None:
    for rel in class_mapper(child_cls).relationships:
        if rel.mapper.class_ == parent_cls:
            return rel.key
    return None


def _validate_children_relationship(children: Sequence[Child_T], parent_cls: type[Parent_T]) -> str:
    rel_names = {_get_relationship_name(type(child), parent_cls) for child in children}
    if len(rel_names) != 1 or None in rel_names:
        raise ValueError("Nem todos os filhos possuem o mesmo relacionamento com o parent.")
    return rel_names.pop()


async def attach(parent_model: Parent_T, children_models: Sequence[Child_T], session: Session) -> None:
    if not children_models:
        return
    parent_cls = type(parent_model)
    rel_name = _validate_children_relationship(children_models, parent_cls)
    for child in children_models:
        setattr(child, rel_name, parent_model)
        session.add(child)