from sqlalchemy import create_engine, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import csv
from datetime import datetime

host = "localhost" 
port = "5432"       
name = "safecare_database"   
user = "postgres"  
password = "root"  
url = f"postgresql://{user}:{password}@{host}:{port}/{name}"

csv_file_historico = 'raw_data/historico_corrigido.csv'
csv_file_geografico = 'raw_data/plano_geografico_corrigido.csv'

engine = create_engine(url)

Base = declarative_base()

class GeographicalPlan(Base):
    __tablename__ = 'Geographical Plan'

    id = Column(Integer, primary_key=True)
    ID_PLANO = Column(Integer)
    CD_PLANO = Column(Integer)
    CD_OPERADORA = Column(Integer)
    CD_NOTA = Column(Integer)
    DT_NTRP = Column(DateTime)
    SG_UF = Column(String(2))
    NM_REGIAO = Column(String(100))
    DT_ATUALIZACAO = Column(DateTime)
    CD_MUNICIPIO = Column(Text)
    NM_MUNICIPIO_X = Column(Text)

class History(Base):
    __tablename__ = 'Historico_corrigido'

    id = Column(Integer, primary_key=True)
    ID_PLANO = Column(Integer)
    CD_PLANO = Column(String(225))
    CD_OPERADORA = Column(Integer)
    DT_INICIO_STATUS = Column(DateTime)
    DT_FIM_STATUS = Column(DateTime)
    ID_SITUACAO_PRINCIPAL = Column(Integer)
    DE_SITUACAO_PRINCIAPL = Column(String(100))

Base.metadata.create_all(engine)

try:
    with open(csv_file_historico, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)

        Session = sessionmaker(bind=engine)
        session = Session()

        for row in reader:
            history = History(
                ID_PLANO = int(row[0]),
                CD_PLANO = str(row[1]),
                CD_OPERADORA = int(row[2]),
                DT_INICIO_STATUS = datetime.strptime(row[3], '%d/%m/%Y'),
                DT_FIM_STATUS = datetime.strptime(row[4], '%d/%m/%Y'),
                ID_SITUACAO_PRINCIPAL = int(row[5]),
                DE_SITUACAO_PRINCIAPL = row[6]
            )
            session.add(history)
    
    session.commit()
    session.close()

    with open(csv_file_geografico, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  

        Session = sessionmaker(bind=engine)
        session = Session()

        for row in reader:
            geographical = GeographicalPlan(
                ID_PLANO = int(row[0]),
                CD_PLANO = int(row[1]),
                CD_OPERADORA = int(row[2]),
                CD_NOTA = int(row[3]),
                DT_NTRP = datetime.strptime(row[4], '%m/%d/%Y %H:%M:%S'),
                SG_UF = row[5],
                NM_REGIAO = row[6],
                DT_ATUALIZACAO = datetime.strptime(row[7], '%m/%d/%Y %H:%M:%S'),
                CD_MUNICIPIO = row[8],
                NM_MUNICIPIO_X = row[9]
            )
            session.add(geographical)
    
    session.commit()
    session.close()

    print("CSV data has been transferred to the PostgreSQL table using SQLAlchemy ORM.")

except Exception as e:
    print(f"Error: {e}")