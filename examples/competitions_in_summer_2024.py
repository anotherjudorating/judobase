import asyncio
from datetime import date

from judobase import Competition, JudoBase


async def main():
    async with JudoBase() as api:
        competitions: list[Competition] = await api.competitions_in_range(
            date(2024, 6, 1),
            date(2024, 8, 31),
        )
        print(len(competitions))  # Output: 14


asyncio.run(main())
