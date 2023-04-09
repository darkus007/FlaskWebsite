from flask import Flask
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import engine, Price, Flat, Project

app = Flask(__name__)


@app.route("/")
def hello_world():
    with Session(engine) as session:
        stmt = select(Flat, Price).join(Price).limit(10)
        for res in session.execute(stmt):
            print(f"{res.Price.price=}")

    return f"<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
