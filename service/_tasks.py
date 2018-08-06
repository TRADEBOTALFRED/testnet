from background_task import background
from logging import getLogger

logger = getLogger(__name__)


@background(schedule=600)
def demo_task(message):
    print('demo_task. message={0}'.format(message))
    logger.debug('demo_task. message={0}'.format(message))

print('tasks!')
#demo_task(0, repeat=30, repeat_until=None)
