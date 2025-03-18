from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), nullable = False)
    email = Column(String(100),unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    last_login = Column(DateTime, nullable = True)
    status = Column(Boolean, nullable = False, default = False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates = 'users')
    hives = relationship('Hive', back_populates = 'owner')
    analyses = relationship('HiveAnalysis', back_populates = 'user')
    backups = relationship('AnalysisBackup', back_populates = 'user')
    beetypes = relationship('BeeType', back_populates = 'user')
