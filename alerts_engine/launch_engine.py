"""
Main script running the alerts engine.
"""

############
# Standard #
############
import logging
import datetime
import configparser

###############
# Third Party #
###############

##########
# Custom #
##########
from engine_tools import scheduler_async
from engine_tools import email_wrapper
from engine_tools import record_scanner
from engine_tools import django_connect

#################
# Configuration #
#################
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(levelname)8s|" \
        + "%(asctime)19s.%(msecs)03d|" \
        + "%(filename)s|" \
        + "%(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)



def main():
    logger.info("START {}".format(str(datetime.datetime.now())))
    # access configuration for alerts engine, treat conf mostly like a dict 
    conf = configparser.ConfigParser()
    conf.read('alert_engine.ini')
    
    rep_t = datetime.timedelta(
        hours = float(conf['scan_period']['hours']),
        minutes = float(conf['scan_period']['minutes']),
        seconds = float(conf['scan_period']['seconds']),
    )


    logger.debug("start test_db")
    z = record_scanner.TriggerScan()
    print(z.dbPvPull())
    logger.debug("end test_db")


    
    # configure Event Manager
    engine = scheduler_async.EventMgr(
        rep_t,
        block=True,
        task=None
    )

    logger.debug('ENGINE START')
    engine.start()
    logger.debug('ENGINE END')



if __name__ == '__main__':
    main()
