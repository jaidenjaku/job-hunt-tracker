# SQLAlchemy models + helpers for persisting scraped job listings.
from sqlalchemy import create_engine, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import date
import os

# Defaults to a local sqlite file; override with DB_URI env var (e.g. in CI) for a different backend.
DB_URI = os.environ.get("DB_URI", "sqlite:///listings.db")
engine = create_engine(DB_URI)

class Base(DeclarativeBase):
    pass

class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    date_posted: Mapped[str] = mapped_column(String(250), nullable=False)
    link: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)  # dedup key, see add_job_if_new
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    date_found: Mapped[str] = mapped_column(String(250), default=lambda: str(date.today()))
    applied: Mapped[bool] = mapped_column(Boolean, default=False)  # manually flipped once you've applied

def init_db():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_job_if_new(session, job: dict) -> bool:
    """Returns True if the job was new and added, False if it already existed."""
    # link is unique, so it's used as the de-dupe key across scraper runs
    existing = session.query(JobListing).filter_by(link=job["link"]).first()
    if existing:
        return False

    new_job = JobListing(
        title=job["title"],
        location=job["location"],
        date_posted=job["date"],
        link=job["link"],
        source=job["source"],
    )
    session.add(new_job)
    session.commit()
    return True