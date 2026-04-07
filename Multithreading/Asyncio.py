import asyncio


async def main(filenames):
    tasks = [read_file_async(filename) for filename in filenames]
    results = await asyncio.gather(*tasks)
    names_str = ' '.join(results)
    return names_str

#asyncio.run(main(filenames))

