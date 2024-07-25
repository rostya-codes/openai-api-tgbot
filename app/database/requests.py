from decimal import Decimal

from sqlalchemy import delete, desc, select, update

from app.database.models import AiModel, AiType, User, async_session


def connection(func):
    """async with connection decorator"""
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id, username):
    """Create new user record in database"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, username=username, balance='0.15'))
        await session.commit()


@connection
async def get_user(session, tg_id):
    """Get user from database"""
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def calculate(session, tg_id, summ, model_name, user):
    model = await session.scalar(select(AiModel).where(AiModel.name == model_name))
    new_balance = Decimal(Decimal(user.balance) - Decimal(Decimal(model.price) * Decimal(summ)))
    await session.execute(update(User).where(User.id == user.id).values(balance=str(new_balance)))
    await session.commit()
