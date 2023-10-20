from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    selected_date = Column(String)
    workouts = relationship('Workout')


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    workout_type = Column(String)
    approaches_num = Column(Integer)
    repetitions_num = Column(Integer)
    weight = Column(Integer)
    comment = Column(String)
    date = Column(String)
    cardio = relationship('Cardio')


class Cardio(Base):
    __tablename__ = 'cardio'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    cardio_type = Column(String)
    cardio_duration = Column(String)
    cardio_level = Column(String)
    cardio_pulce = Column(String)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
