import asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

# 1. Налаштування бази даних (SQLite через aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///network.db"
Base = declarative_base()


# 2. Оголошення моделі вузла
class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    status = Column(String, default="unknown")


# Створення асинхронного рушія та сесії
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# 3. Створення таблиць у базі даних
async def create_tables():
    async with engine.begin() as conn:
        # run_sync використовується для виконання синхронних методів метаданих [cite: 64]
        await conn.run_sync(Base.metadata.create_all)
    print("--- Систему ініціалізовано: таблиці створено ---")


# 4. Очищення бази перед початком (для демонстрації)
async def reset_nodes():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM nodes"))
        await session.commit()


# 5. Додавання 12 вузлів (імітація початкових даних)
async def add_nodes():
    async with AsyncSessionLocal() as session:
        nodes = [
            Node(ip_address=f"192.168.1.{i}", status="active")
            for i in range(1, 13)
        ]
        session.add_all(nodes)
        await session.commit()
        print(f"--- До бази додано {len(nodes)} вузлів ---")


# 6. Асинхронний моніторинг (оновлення статусів)
async def monitor_nodes():
    async with AsyncSessionLocal() as session:
        # Виконуємо асинхронний запит до БД [cite: 84]
        result = await session.execute(select(Node))
        nodes = result.scalars().all()

        for node in nodes:
            # Логіка: якщо останній октет IP парний — статус offline [cite: 97]
            last_octet = int(node.ip_address.split('.')[-1])
            node.status = "offline" if last_octet % 2 == 0 else "active"

        await session.commit()
        print("\n--- Моніторинг завершено: статуси оновлено на основі IP ---")


# 7. Виведення результатів у консоль
async def print_nodes(label):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        print(f"\n>>> {label}:")
        for node in nodes:
            print(f"Вузол ID {node.id:2} | IP: {node.ip_address:12} | Статус: {node.status}")


# ГОЛОВНИЙ ЦИКЛ ПРОГРАМИ
async def main():
    # 1. Створюємо таблиці
    await create_tables()

    # 2. Очищуємо та заповнюємо базу
    await reset_nodes()
    await add_nodes()

    # 3. Показуємо стан до змін
    await print_nodes("СТАН ДО МОНІТОРИНГУ")

    # 4. Запускаємо асинхронну імітацію моніторингу
    print("\n[Запуск асинхронного процесу перевірки вузлів...]")
    await asyncio.sleep(1)  # Імітація затримки мережі
    await monitor_nodes()

    # 5. Показуємо результат
    await print_nodes("СТАН ПІСЛЯ МОНІТОРИНГУ")


if __name__ == "__main__":
    try:
        # Запуск подійного циклу asyncio [cite: 11]
        asyncio.run(main())
    except KeyboardInterrupt:
        pass