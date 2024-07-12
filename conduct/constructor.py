import os


def listdir(directory):
    """"""
    for item in os.listdir(directory):
        item_full = os.path.join(directory, item)
        yield item_full


async def crawl(directory):
    """"""
    for item in listdir(directory):
        if os.path.isdir(item):
            yield item
            async for sub_item in crawl(item):
                yield sub_item
        elif os.path.isfile(item):
            yield item
