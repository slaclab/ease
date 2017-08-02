#from engine_tools import scheduler
from engine_tools import scheduler_async
from engine_tools import record_scanner
import logging
import  datetime

if __name__ == '__main__':

    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(levelname)8s : %(asctime)19s.%(msecs)03d : %(threadName)20s : %(message)s",
        level=logging.DEBUG
    )
    rep_t = datetime.timedelta(seconds=1)

    
    #configure task class


    engine = scheduler_async.EventMgr(
        rep_t,
        block=True,
        task=None
    )
    engine.start()
    logging.debug('MAIN ENDING')
