from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Float, Date, Boolean, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from config import DB_USER, DB_PASS, DB_NAME, DB_PORT, DB_HOST

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)


Base = declarative_base()


class Project(Base):
    __tablename__ = "project"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(127))
    name: Mapped[str] = mapped_column(String(127))
    url: Mapped[str | None] = mapped_column(String(255))
    metro: Mapped[str | None] = mapped_column(String(127))
    time_to_metro: Mapped[int | None] = mapped_column(Integer)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    address: Mapped[str | None] = mapped_column(String(255))
    data_created: Mapped[datetime.date] = mapped_column(Date)
    data_closed: Mapped[Optional[datetime.date]] = mapped_column(Date)

    flat: Mapped[list["Flat"]] = relationship(back_populates="project")


class Flat(Base):
    __tablename__ = "flat"

    flat_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.project_id"))
    address: Mapped[str | None] = mapped_column(String(255))
    floor: Mapped[int | None] = mapped_column(Integer)
    rooms: Mapped[int | None] = mapped_column(Integer)
    area: Mapped[float | None] = mapped_column(Integer)
    finishing: Mapped[bool | None] = mapped_column(Boolean)
    bulk: Mapped[str | None] = mapped_column(String(127))
    settlement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    url_suffix: Mapped[str] = mapped_column(String(127))
    data_created: Mapped[datetime.date] = mapped_column(Date)
    data_closed: Mapped[Optional[datetime.date]] = mapped_column(Date)

    project: Mapped["Project"] = relationship(back_populates="flat")
    prices: Mapped[list["Price"]] = relationship(back_populates="flat")


class Price(Base):
    __tablename__ = "price"

    price_id: Mapped[int] = mapped_column(primary_key=True)
    flat_id: Mapped[int] = mapped_column(ForeignKey("flat.flat_id"))
    benefit_name: Mapped[str | None] = mapped_column(String(127))
    benefit_description: Mapped[str | None] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    meter_price: Mapped[int | None] = mapped_column(Integer)
    booking_status: Mapped[str | None] = mapped_column(String(15))
    data_created: Mapped[datetime.date] = mapped_column(Date)

    flat: Mapped["Flat"] = relationship(back_populates="prices")
