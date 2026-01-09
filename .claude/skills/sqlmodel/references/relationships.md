# SQLModel Relationships

## Table of Contents
- [One-to-Many (1:N)](#one-to-many-1n)
- [Many-to-Many (N:N)](#many-to-many-nn)
- [One-to-One (1:1)](#one-to-one-11)
- [Self-Referential](#self-referential)
- [Queries with Relationships](#queries-with-relationships)
- [FastAPI with Relationships](#fastapi-with-relationships)

## One-to-Many (1:N)

### Example: Team has many Heroes

```python
from sqlmodel import Field, Relationship, SQLModel

# Team model (the "one" side)
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # Relationship: One team has many heroes
    heroes: list["Hero"] = Relationship(back_populates="team")

# Hero model (the "many" side)
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

    # Foreign key to Team
    team_id: int | None = Field(default=None, foreign_key="team.id")

    # Relationship back to Team
    team: Team | None = Relationship(back_populates="heroes")
```

### Creating Related Objects

```python
from sqlmodel import Session

# Method 1: Create separately, then link
with Session(engine) as session:
    team = Team(name="Avengers", headquarters="New York")
    session.add(team)
    session.commit()
    session.refresh(team)

    hero = Hero(name="Spider-Boy", secret_name="Pedro", team_id=team.id)
    session.add(hero)
    session.commit()

# Method 2: Create together using relationship
with Session(engine) as session:
    hero1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp")

    team = Team(
        name="Z-Force",
        headquarters="Secret Base",
        heroes=[hero1, hero2]
    )
    session.add(team)
    session.commit()

# Method 3: Add hero to existing team
with Session(engine) as session:
    team = session.get(Team, 1)
    new_hero = Hero(name="Black Lion", secret_name="Trevor", team=team)
    session.add(new_hero)
    session.commit()
```

### Querying Relationships

```python
from sqlmodel import select

# Get team with heroes
with Session(engine) as session:
    team = session.get(Team, 1)
    print(f"Team: {team.name}")
    for hero in team.heroes:
        print(f"  - {hero.name}")

# Get hero with team
with Session(engine) as session:
    hero = session.get(Hero, 1)
    if hero.team:
        print(f"{hero.name} belongs to {hero.team.name}")

# Query heroes by team name
with Session(engine) as session:
    statement = (
        select(Hero)
        .join(Team)
        .where(Team.name == "Avengers")
    )
    heroes = session.exec(statement).all()
```

## Many-to-Many (N:N)

### Example: Heroes belong to many Teams

```python
from sqlmodel import Field, Relationship, SQLModel

# Link table (association table)
class HeroTeamLink(SQLModel, table=True):
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    team_id: int = Field(foreign_key="team.id", primary_key=True)

# Hero model
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str

    teams: list["Team"] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )

# Team model
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list[Hero] = Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )
```

### Link Table with Extra Fields

```python
from datetime import datetime

class HeroTeamLink(SQLModel, table=True):
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    team_id: int = Field(foreign_key="team.id", primary_key=True)

    # Extra fields on the relationship
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(default="member")
    is_active: bool = Field(default=True)
```

### Creating Many-to-Many Relationships

```python
with Session(engine) as session:
    # Create team
    team1 = Team(name="Avengers", headquarters="New York")
    team2 = Team(name="X-Force", headquarters="Mansion")

    # Create hero
    hero = Hero(name="Wolverine", secret_name="Logan")

    # Link hero to multiple teams
    hero.teams = [team1, team2]

    session.add(hero)
    session.commit()

# Add hero to existing team
with Session(engine) as session:
    hero = session.get(Hero, 1)
    team = session.get(Team, 2)

    hero.teams.append(team)
    session.add(hero)
    session.commit()

# Remove hero from team
with Session(engine) as session:
    hero = session.get(Hero, 1)
    team = session.get(Team, 2)

    hero.teams.remove(team)
    session.add(hero)
    session.commit()
```

### Querying Many-to-Many

```python
# Get all teams a hero belongs to
with Session(engine) as session:
    hero = session.get(Hero, 1)
    for team in hero.teams:
        print(f"{hero.name} is in {team.name}")

# Get all heroes in a team
with Session(engine) as session:
    team = session.get(Team, 1)
    for hero in team.heroes:
        print(f"{hero.name} is in {team.name}")

# Query heroes in specific team
with Session(engine) as session:
    statement = (
        select(Hero)
        .join(HeroTeamLink)
        .join(Team)
        .where(Team.name == "Avengers")
    )
    heroes = session.exec(statement).all()

# Query with link table data
with Session(engine) as session:
    statement = (
        select(Hero, HeroTeamLink.role)
        .join(HeroTeamLink)
        .where(HeroTeamLink.team_id == 1)
    )
    results = session.exec(statement).all()
    for hero, role in results:
        print(f"{hero.name}: {role}")
```

## One-to-One (1:1)

### Example: Hero has one Profile

```python
class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bio: str | None = None
    website: str | None = None

    hero_id: int = Field(foreign_key="hero.id", unique=True)
    hero: "Hero" = Relationship(back_populates="profile")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str

    profile: Profile | None = Relationship(
        back_populates="hero",
        sa_relationship_kwargs={"uselist": False}
    )
```

### Usage

```python
with Session(engine) as session:
    hero = Hero(name="Spider-Boy", secret_name="Pedro")
    profile = Profile(bio="Friendly neighborhood hero", hero=hero)

    session.add(profile)
    session.commit()

# Access profile
with Session(engine) as session:
    hero = session.get(Hero, 1)
    if hero.profile:
        print(hero.profile.bio)
```

## Self-Referential

### Example: Hero has a Mentor (another Hero)

```python
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str

    # Foreign key to self
    mentor_id: int | None = Field(default=None, foreign_key="hero.id")

    # Relationship to mentor
    mentor: "Hero | None" = Relationship(
        back_populates="students",
        sa_relationship_kwargs={"remote_side": "Hero.id"}
    )

    # Students of this hero
    students: list["Hero"] = Relationship(back_populates="mentor")
```

### Usage

```python
with Session(engine) as session:
    mentor = Hero(name="Professor X", secret_name="Charles Xavier")
    session.add(mentor)
    session.commit()
    session.refresh(mentor)

    student = Hero(
        name="Cyclops",
        secret_name="Scott Summers",
        mentor_id=mentor.id
    )
    session.add(student)
    session.commit()

# Query
with Session(engine) as session:
    hero = session.get(Hero, 2)  # Cyclops
    if hero.mentor:
        print(f"{hero.name}'s mentor is {hero.mentor.name}")

    mentor = session.get(Hero, 1)  # Professor X
    for student in mentor.students:
        print(f"{mentor.name} mentors {student.name}")
```

## Queries with Relationships

### Eager Loading (avoid N+1)

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload

# Load heroes with their teams in one query
with Session(engine) as session:
    statement = (
        select(Hero)
        .options(selectinload(Hero.teams))
    )
    heroes = session.exec(statement).all()

    for hero in heroes:
        # No additional query needed
        print(f"{hero.name}: {[t.name for t in hero.teams]}")

# Load team with heroes
with Session(engine) as session:
    statement = (
        select(Team)
        .options(selectinload(Team.heroes))
        .where(Team.name == "Avengers")
    )
    team = session.exec(statement).first()

    for hero in team.heroes:
        print(hero.name)
```

### Filtering by Relationship

```python
# Heroes with a team
statement = select(Hero).where(Hero.team_id != None)

# Heroes without a team
statement = select(Hero).where(Hero.team_id == None)

# Heroes in a specific team
statement = (
    select(Hero)
    .join(Team)
    .where(Team.name == "Avengers")
)

# Teams with more than 3 heroes
from sqlmodel import func

statement = (
    select(Team)
    .join(Hero)
    .group_by(Team.id)
    .having(func.count(Hero.id) > 3)
)
```

## FastAPI with Relationships

### Response Models

```python
# Base models
class TeamBase(SQLModel):
    name: str
    headquarters: str

class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

# Database models
class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")

# Read models (with nested data)
class HeroRead(HeroBase):
    id: int
    team_id: int | None = None

class HeroReadWithTeam(HeroRead):
    team: TeamBase | None = None

class TeamRead(TeamBase):
    id: int

class TeamReadWithHeroes(TeamRead):
    heroes: list[HeroBase] = []
```

### Endpoints

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

router = APIRouter()

# Get hero with team
@router.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero_with_team(hero_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Hero)
        .options(selectinload(Hero.team))
        .where(Hero.id == hero_id)
    )
    hero = session.exec(statement).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Get team with heroes
@router.get("/teams/{team_id}", response_model=TeamReadWithHeroes)
def read_team_with_heroes(team_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Team)
        .options(selectinload(Team.heroes))
        .where(Team.id == team_id)
    )
    team = session.exec(statement).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Add hero to team
@router.post("/teams/{team_id}/heroes/{hero_id}")
def add_hero_to_team(
    team_id: int,
    hero_id: int,
    session: Session = Depends(get_session)
):
    team = session.get(Team, team_id)
    hero = session.get(Hero, hero_id)

    if not team or not hero:
        raise HTTPException(status_code=404, detail="Team or Hero not found")

    hero.team_id = team_id
    session.add(hero)
    session.commit()
    return {"message": f"Hero {hero.name} added to team {team.name}"}
```
