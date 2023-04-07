from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Integer, String, Float, Date, Boolean

metadata = MetaData()

projects = Table(
    "Projects",
    metadata,
    Column('project_id', Integer, primary_key=True),
    Column('city', String(127), nullable=False),
    Column('name', String(127), nullable=False),
    Column('url', String(255)),
    Column('metro', String(127)),
    Column('time_to_metro', Integer),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('address', String(255)),
    Column('data_created', Date),
    Column('data_closed', Date),
)

flats = Table(
    "Flats",
    metadata,
    Column('flat_id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('Projects.project_id')),
    Column('address', String(127), nullable=False),
    Column('floor', Integer),
    Column('rooms', Integer),
    Column('area', Float),
    Column('finishing', Boolean),
    Column('bulk', String(127)),
    Column('settlement_date', Date),
    Column('url_suffix', String(127)),
    Column('data_created', Date),
    Column('data_closed', Date),
)


prices = Table(
    "Prices",
    metadata,
    Column('flat_id', Integer, ForeignKey('Flats.flat_id')),
    Column('benefit_name', String(127)),
    Column('benefit_description', String(255)),
    Column('price', Integer),
    Column('meter_price', Integer),
    Column('booking_status', String(15)),
    Column('data_created', Date),
)
