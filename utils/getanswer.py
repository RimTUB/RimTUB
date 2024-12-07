from logging import getLogger

logger = getLogger('RimTUB')


async def get_answer(*_, **__) -> None:
    """
    # Устарело!
    Используйте `client.listen` или `client.ask` из модуля pyromod.
    """
    logger.warning("get_answer and make_request functions are deprecated. Use client.listen or client.ask from the pyromod module.")
    return
    

async def make_request(*_, **__) -> None:
    """
    # Устарело!
    Используйте `client.listen` или `client.ask` из модуля pyromod.
    """
    logger.warning("get_answer and make_request functions are deprecated. Use client.listen or client.ask from the pyromod module.")
    return
