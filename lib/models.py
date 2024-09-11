from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base



convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    freebies = relationship('Freebie', backref=backref('company'))
    devs = relationship('Dev', secondary='freebies', back_populates='companies')


    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, company,dev, item_name, value):
        adding_freebie = Freebie(
            item_name=item_name,
            values=value,
            dev_id = dev.id,
            company_id =  company.id           
        )
        
        session.add(adding_freebie)
        session.commit()
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()
    

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    
    freebies = relationship('Freebie', backref=backref('dev'))
    companies= relationship('Company', secondary='freebies', back_populates='devs')

    def __repr__(self):
        return f'<Dev {self.name}>'
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, dev, freebie):
        if freebie.dev_id == self.id:
            freebie.dev_id = dev.id
            session.commit()

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer, primary_key=True)
    item_name = Column(String())
    values = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    dev = relationship('Dev', backref=backref('freebies'))
    company = relationship('Company', backref=backref('freebies'))
    
    def __repr__(self):
        return f'Freebie(id={self.id}, ' + \
            f'item name={self.item_name}, ' + \
                f'values={self.values}, ' + \
                    f'dev_id={self.dev_id}, ' + \
                        f'company_id={self.company_id})'
                        
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'