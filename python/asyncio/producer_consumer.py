#!/usr/bin/env python3

import click
import random
import asyncio

async def producer_coroutine(queue: asyncio.Queue) -> None:
    """ Producer coroutine that adds random integers to a queue
    """
    while True:
        data = random.randint(1, 100)
        await queue.put(data)
        print(f"Producer sent {data}")
        await asyncio.sleep(2)

async def consumer_coroutine(queue: asyncio.Queue) -> None:
    """ Consumer coroutine that reads integers from a queue
    """
    while True:
        data = await queue.get()
        print(f"Consumer received {data}")

async def run_single_producer_consumer() -> None:
    """ Runs an example of single producer consumer interaction
    """
    queue: asyncio.Queue = asyncio.Queue(50)
    producer = producer_coroutine(queue)
    consumer = consumer_coroutine(queue)
    await asyncio.gather(producer, consumer)

async def run_multiple_producer_consumer(num_producer: int, num_consumer: int) -> None:
    """ Runs an example of multiple producer consumer interactions
    """
    queue: asyncio.Queue = asyncio.Queue(50)
    producers = [ producer_coroutine(queue) for i in range(num_producer) ]
    consumers = [ consumer_coroutine(queue) for i in range(num_consumer) ]
    await asyncio.gather(*producers, *consumers)


@click.group(help="Example of Producer Consumer pattern using python-asyncio")
def main(): ...

@main.command(help="Run single producer-consumer instance")
def run_single():
    asyncio.run(run_single_producer_consumer())

@main.command(help="Run multiple producer-consumer instances")
@click.argument("producers", type=int)
@click.argument("consumers", type=int)
def run_multi(producers: int, consumers: int):
    asyncio.run(run_multiple_producer_consumer(producers, consumers))



if __name__ == "__main__":
    main()

