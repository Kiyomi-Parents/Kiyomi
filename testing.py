import asyncio


class Cog:
    async def someFunction(self):
        print("Called some function")

    async def __aenter__(self):
        print("A ENTER")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("A EXIT")


async def get_cog() -> Cog:
    cog = Cog()

    return cog


async def main():
    async with await get_cog() as cog:
        await cog.someFunction()


if __name__ == '__main__':
    asyncio.run(main())