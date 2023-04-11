from flask import Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from paginator import Paginator
from models import engine, Price, Flat, Project


def get_project_flats(request: Request,
                      project_id: int = None,
                      limit: int = 50) -> tuple[Paginator, list[dict]]:
    """
    Возвращает информацию по квартирам,
    если указан id жилого комплекса - вернет информацию по квартирам только этого ЖК.
    :param request: Объект запроса.
    :param project_id: id жилого комплекса.
    :param limit: Число квартир на странице (пагинация).
    :return: Кортеж (Объект пагинатора, список с информацией по квартирам).
    """
    with Session(engine) as session:

        current_page = int(request.args.get('page', 1))
        stmt = select(Flat.flat_id)
        if project_id:
            stmt = stmt.where(Flat.project_id == project_id)
        total_items = session.execute(stmt).all()

        page_obj = Paginator(total_items, limit).page(current_page)

        stmt = select(Flat.flat_id, Flat.address, Flat.floor, Flat.rooms, Flat.area, Flat.finishing,
                      Flat.settlement_date, Flat.url_suffix,
                      Project.project_id, Project.name, Project.city, Project.url,
                      Price.price, Price.booking_status).join(Project).join(Price)
        if project_id:
            stmt = stmt.where(Project.project_id == project_id).order_by(Price.price)
        stmt = stmt.limit(limit).offset((page_obj.number - 1) * limit)

        project_flats = [row._asdict() for row in session.execute(stmt)]

        return page_obj, project_flats


def get_flat(session: Session, flat_id: int) -> dict:
    """
    Возвращает информацию по квартире.
    :param session: Сессия (sqlalchemy.orm.Session).
    :param flat_id: id квартиры.
    :return: {'flat_id': ..., 'address': ..., 'floor': ...,
        'rooms': ..., 'area': ..., 'finishing': ..., 'settlement_date': ...,
        'url_suffix': ..., 'name': ..., 'url': ...}
    """
    stmt = select(Flat.flat_id, Flat.address, Flat.floor, Flat.rooms, Flat.area, Flat.finishing,
                  Flat.settlement_date, Flat.url_suffix,
                  Project.name, Project.url).join(Project) \
        .where(Flat.flat_id == flat_id)
    return session.execute(stmt).one()._asdict()


def get_flat_prices(session: Session, flat_id: int) -> list[dict]:
    """
    Возвращает информацию о всех изменениях цены и брони по квартире.
    :param session: Сессия (sqlalchemy.orm.Session).
    :param flat_id: id квартиры.
    :return: [{'data_created': ..., 'price': ...,
        'booking_status': ..., 'benefit_name': ..., 'benefit_description': ...}]
    """
    stmt = select(Price.data_created, Price.price, Price.booking_status,
                  Price.benefit_name, Price.benefit_description) \
        .where(Price.flat_id == flat_id).order_by(Price.data_created)
    return [row._asdict() for row in session.execute(stmt)]


def get_flat_and_prices(flat_id: int) -> tuple[dict, list[dict]]:
    """
    Возвращает информацию по квартире и о всех изменениях цены и брони.
    :param flat_id: id квартиры.
    :return: ({'flat_id': ..., 'address': ..., 'floor': ...,
        'rooms': ..., 'area': ..., 'finishing': ..., 'settlement_date': ...,
        'url_suffix': ..., 'name': ..., 'url': ...},
        [{'data_created': ..., 'price': ...,
        'booking_status': ..., 'benefit_name': ..., 'benefit_description': ...}, ])
    """
    with Session(engine) as session:
        return get_flat(session, flat_id), get_flat_prices(session, flat_id)


def get_all_projects() -> list[dict]:
    """
    Возвращает список всех жилых комплексов.
    :return: [{'project_id': ..., 'name': ...}, ]
    """
    with Session(engine) as session:
        return [row._asdict() for row in session.execute(select(Project.project_id, Project.name))]
