Usage
=====

After installing the library, you can easily integrate it into your project. Below is a basic usage example:

.. code-block:: python

    import asyncio

    from judobase import JudoBase, Competition, Contest


    async def main():
        async with JudoBase() as api:
            contests: list[Contest] = await api.all_contests()
            print(len(contests)) # Output: 195161

        api = JudoBase()
        olympic_games_2024: Competition = await api.competition_by_id(2653)
        print(olympic_games_2024.city) # Output: Paris
        await api.close_session()

    asyncio.run(main())


Also it is available to retrieve data about contest events like score, osaekomi, shido, etc.:

.. image:: /_static/events_example.png

.. code-block:: python

    import asyncio

    from judobase import JudoBase, Contest


    async def main():
        async with JudoBase() as api:
            contests: list[Contest] = await api.contests_by_competition_id(
                competition_id=2869,
                weight="-60",
                include_events=True
            )

            print(contests[-1].events[-1].tags[0].name) # Output: Seoi-nage

    asyncio.run(main())



.. note::
    The library uses the ``aiohttp`` library to make asynchronous requests. Therefore, you need to run the code in an asynchronous context.


**Key classes:**

- ``JudoBase``: Main class that provides access to user-friendly methods.
- ``JudokaAPI``: Base methods for fetching data about athletes.
- ``CompetitionAPI``: Base methods for fetching data about competitions.
- ``ContestAPI``: Base methods for fetching data about contests.
- ``CountryAPI``: Base methods for fetching data about countries.


More examples can be found in the `examples <https://github.com/anotherjudorating/judobase/tree/master/examples>`_ directory of the project.
