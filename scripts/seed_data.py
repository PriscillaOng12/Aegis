"""Seed the local development environment with synthetic data.

This script populates the Postgres database with demo users, symptom logs and
wearable snapshots. It also trains the baseline XGBoost model and stores it
in `ml/training/models/` ready for serving.
"""

import asyncio
import os
import uuid
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from api.app.models import Base, User, SymptomLog, WearableSnapshot
from ml.training.train import generate_synthetic_data, train_model


async def seed_db(database_url: str) -> None:
    engine = create_async_engine(database_url, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        # create demo user
        user_id = "demo-user"
        user = User(id=user_id, tenant_id="demo")
        session.add(user)
        # generate logs for past 7 days
        now = datetime.utcnow()
        for i in range(7):
            ts = now - timedelta(days=6 - i)
            log = SymptomLog(
                id=str(uuid.uuid4()),
                user_id=user_id,
                pain=random.randint(0, 10),
                fatigue=random.randint(0, 10),
                nausea=random.randint(0, 5),
                notes="synthetic seed log",
                timestamp=ts,
            )
            session.add(log)
        # wearable snapshots (6 per day)
        for i in range(7 * 6):
            ts = now - timedelta(minutes=60 * i)
            snap = WearableSnapshot(
                id=str(uuid.uuid4()),
                user_id=user_id,
                source="mock",
                timestamp=ts,
                hr=random.uniform(50, 90),
                hrv=random.uniform(20, 80),
                steps=random.randint(0, 200),
                sleep=0.0,
            )
            session.add(snap)
        await session.commit()


def train_baseline_model() -> None:
    df = generate_synthetic_data(5000)
    metrics = train_model(df)
    print("Baseline model trained. Metrics:", metrics)


async def main():
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./seed.db")
    await seed_db(database_url)
    train_baseline_model()


if __name__ == "__main__":
    asyncio.run(main())