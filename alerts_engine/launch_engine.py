from engine_tools import scheduler

import logging
from datetime import timedelta

if __name__ == '__main__':

    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(levelname)8s : %(asctime)19s.%(msecs)03d : %(threadName)20s : %(message)s",
        level=logging.DEBUG
    )





    s = scheduler.EventMgr(timedelta(seconds=.1),sweep = timedelta(seconds=.01), 
                           limit = 300)
    s.start()
    try:
        s.blocking_hold()
    except KeyboardInterrupt:
        print("")
        s.terminate()

    logging.debug('MAIN ENDING')
