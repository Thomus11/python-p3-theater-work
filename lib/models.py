
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    
    auditions = relationship('Audition', back_populates='role')

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions.all()]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions.all()]

    def lead(self):
        hired = self.auditions.filter(Audition.hired == True).first()
        return hired or 'no actor has been hired for this role'

    def understudy(self):
        hired = self.auditions.filter(Audition.hired == True).limit(2).all()
        return hired[1] if len(hired) >= 2 else 'no actor has been hired for understudy for this role'


engine = create_engine('sqlite:///theater.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
    
    
role = Role(character_name='Hamlet')

audition1 = Audition(actor='Joy Jane', location='New York', phone=1723466238, role=role)
audition2 = Audition(actor='Jane Smith', location='Los Angeles', phone=9876543210, role=role) 
audition3 = Audition(actor='Alice Johnson', location='Chicago', phone=5555555555, role=role)

session.add(role)
session.add_all([audition1, audition2, audition3])
session.commit()

    ## Hire an actor (Joy Jane)
audition1.call_back()
session.commit()

print("Actors who auditioned for Hamlet:", role.actors)
print("Locations where auditions took place:", role.locations)

    # Get the lead actor
lead = role.lead()
print("Lead actor for Hamlet:", lead.actor if isinstance(lead, Audition) else lead)

    #get the understudy
understudy = role.understudy()
print("Understudy for Hamlet:", understudy.actor if isinstance(understudy, Audition) else understudy)