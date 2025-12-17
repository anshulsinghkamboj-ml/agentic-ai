import asyncio
import random


async def retry_with_backoff_async(
    fn,
    max_retries: int = 3,
    base_delay: float = 1.0
):
    attempt = 0

    while True:
        try:
            return await fn()
        except Exception as e:
            attempt += 1
            if attempt > max_retries:
                raise

            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay * 0.1)
            await asyncio.sleep(delay + jitter)
