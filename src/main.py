from flask import Flask, render_template, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import engine, Price, Flat, Project
from paginator import Pagination

PAGINATION_ON_PAGE_LIMIT = 50


app = Flask(__name__)


@app.route("/")
def index():
    with Session(engine) as session:

        current_page = int(request.args.get('page', 1))
        total_items = session.execute(select(Flat.flat_id)).all()
        page_obj = Pagination(total_items, current_page, PAGINATION_ON_PAGE_LIMIT)

        stmt = select(Flat.flat_id, Flat.address, Flat.floor, Flat.rooms, Flat.area, Flat.finishing,
                      Flat.settlement_date, Flat.url_suffix,
                      Project.project_id, Project.name, Project.city, Project.url,
                      Price.price, Price.booking_status).join(Project).join(Price).order_by(Price.price)\
            .limit(PAGINATION_ON_PAGE_LIMIT).offset((page_obj.number - 1) * PAGINATION_ON_PAGE_LIMIT)
        all_flats = [row._asdict() for row in session.execute(stmt)]

    return render_template('flats/table_cls.html', flats=all_flats, page_obj=page_obj)


@app.route('/project/<int:project_id>/')
def project(project_id: int):
    with Session(engine) as session:

        current_page = int(request.args.get('page', 1))
        total_items = session.execute(select(Flat.flat_id).where(Flat.project_id == project_id)).all()
        page_obj = Pagination(total_items, current_page, PAGINATION_ON_PAGE_LIMIT)

        stmt = select(Flat.flat_id, Flat.address, Flat.floor, Flat.rooms, Flat.area, Flat.finishing,
                      Flat.settlement_date, Flat.url_suffix,
                      Project.project_id, Project.name, Project.city, Project.url,
                      Price.price, Price.booking_status).join(Project).join(Price)\
            .where(Project.project_id == project_id).order_by(Price.price)\
            .limit(PAGINATION_ON_PAGE_LIMIT).offset((page_obj.number - 1) * PAGINATION_ON_PAGE_LIMIT)
        project_flats = [row._asdict() for row in session.execute(stmt)]
    return render_template('flats/table_cls.html', flats=project_flats, page_obj=page_obj)


@app.route('/flat/<int:flat_id>/')
def flats(flat_id: int):
    with Session(engine) as session:

        stmt = select(Flat.flat_id, Flat.address, Flat.floor, Flat.rooms, Flat.area, Flat.finishing,
                      Flat.settlement_date, Flat.url_suffix,
                      Project.name, Project.url).join(Project) \
            .where(Flat.flat_id == flat_id)
        flat = session.execute(stmt).one()._asdict()

        stmt = select(Price.data_created, Price.price, Price.booking_status,
                      Price.benefit_name, Price.benefit_description)\
            .where(Price.flat_id == flat_id).order_by(Price.data_created)
        prices = [row._asdict() for row in session.execute(stmt)]

    return render_template('flats/flat_detail.html', flats=flat, prices=prices)


@app.context_processor
def inject_projects():
    """ Добавляет список Жилых Комплексов """
    with Session(engine) as session:
        projects = [row._asdict() for row in session.execute(select(Project.project_id, Project.name))]
    return {"projects": projects}


if __name__ == '__main__':
    app.run(debug=True)
