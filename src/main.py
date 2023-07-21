from flask import Flask, render_template, request

from services import get_flat_and_prices, get_all_projects, get_project_flats


app = Flask(__name__)


@app.route("/")
def index() -> str:
    paginator, all_flats = get_project_flats(request)
    return render_template('flats/table_cls.html', flats=all_flats, page_obj=paginator)


@app.route('/project/<int:project_id>/')
def project(project_id: int) -> str:
    paginator, project_flats = get_project_flats(request, project_id)
    return render_template('flats/table_cls.html', flats=project_flats, page_obj=paginator)


@app.route('/flat/<int:flat_id>/')
def flats(flat_id: int) -> str:
    flat, prices = get_flat_and_prices(flat_id)
    return render_template('flats/flat_detail.html', flats=flat, prices=prices)


@app.context_processor
def inject_projects() -> dict:
    """ Добавляет список Жилых Комплексов """
    return {"projects": get_all_projects()}


if __name__ == '__main__':
    app.run(debug=True)
