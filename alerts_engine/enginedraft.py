import logging
import threading
import time
import numpy as np
#import Queue.queue as queue
import queue
from datetime import timedelta
#logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s",level=logging.DEBUG)
#logging.debug('Debugging information')
#logging.info('Informational message')
#logging.warning('Warning:config file %s not found', 'server.conf')
#logging.error('Error occurred')
#logging.critical('Critical error -- shutting down')



class Processor(threading.Thread):
    def __init__(self,cv,event,execute):
        threading.Thread.__init__(self)
        self.cv = cv
        self.go = True
        self.event = event
        self.execute = execute

    def run(self):
        logging.debug('consumer initiating')
        #print(threading.current_thread().name)
        #print(self.name)
        #print(self.ident)
        while self.go:
            with self.cv:
                self.cv.wait()
                if self.event.is_set():
                    self.go = False
                    logging.debug('END RECEIVED')
                    return

                logging.debug('RELEASE RECEIVED')
                self.execute()



class Timer(threading.Thread):
    def __init__(self,delay,cv,event,sweep=1):
        threading.Thread.__init__(self)
        self.cv = cv
        self.go = True
        self.delay = delay
        self.event = event
        self.sweep = sweep

    def run(self):
        logging.debug('producer initiating')
        previous_time = time.time()
        while self.go:
            while time.time() < (previous_time + self.delay):
                time.sleep(self.sweep)
                if self.event.is_set():
                    self.go = False
                    with self.cv:
                        self.cv.notifyAll()
                        logging.debug('ENDING')
                    return

            previous_time = previous_time + self.delay

            with self.cv:
                self.cv.notifyAll()
                logging.debug('RELEASING')


class Launcher():
    def __init__(self,delay,name=None,sweep=timedelta(seconds=.1)):
        if name == None:
            self.name = str(__class__.__name__)+":"+str(delay.total_seconds())
        else:
            self.name = name
        self.messageq = queue.Queue()
        self.endevent = threading.Event()
        self.cv = threading.Condition()
        self.delay = delay.total_seconds()
        self.sweep = sweep.total_seconds()
        self.timer = Timer(
            self.delay,
            self.cv,
            self.endevent,
            self.sweep,
        )
        self.timer.name = self.name + ":timer"
        self.proc = Processor(
            self.cv,
            self.endevent,
            self.execute,
        )
        self.proc.name = self.name + ":proc"

    def start(self):
        self.timer.start()
        self.proc.start()

    def terminate(self):
        self.endevent.set()
        self.timer.join()
        self.proc.join()

    def blocking_hold(self):
        self.timer.join()
        self.proc.join()

    def execute(self):
        logging.debug('EXECUTING')


if __name__ == '__main__':

    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(levelname)8s : %(asctime)19s.%(msecs)03d : %(threadName)20s : %(message)s",
        level=logging.DEBUG
    )





    s = Launcher(timedelta(seconds=2),sweep = timedelta(seconds=.1))
    s.start()
    try:
        s.blocking_hold()
    except KeyboardInterrupt:
        print("")
        s.terminate()

    logging.debug('MAIN ENDING')
