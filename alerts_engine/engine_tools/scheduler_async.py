"""
scheduler_async.py provides the EventMgr object for scheduling regular tasks
with minimal clock drift. 
"""


import asyncio
import datetime
import logging
import time
import signal
'''
logging.basicConfig(                                                        
    datefmt="%Y-%m-%d %H:%M:%S",                                            
    #format="%(levelname)8s : %(asctime)19s.%(msecs)03d : %(threadName)20s : %(message)s",
    format="%(levelname)8s : %(asctime)19s.%(msecs)03d : %(message)s",
)
'''
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class EndRun(Exception):
    pass

class EventMgr():
    """
    The EventMgr class manages a single repeated task. The frequency and
    duration of the tasks can be limited. The task is any callable object
    either a function or class method.
    """
    def __init__(self,  interval, end = None, task=None, block=True, 
                 *args, **kwargs):
        """
        Initial configuration of EventMgr

        Parameters
        ----------
        interval : datetime.timedelta
            Specify the delay time between successive executions of the task.

        end : datetime.timedelta 
            A limiting time. The run will end after the last exection of the
            task before the end time. 

        task : Any callable function or class method. None also acceptable
            This is the task to be executed. A default task simply logging the
            task calls will be run if no task is provided.

        block : bool
            Determines whether or not the call to start is blocking. A blocking
            call will freeze the program until SIGTERM is sent. A non-blocking
            call will allow the flow of the main program to continue while
            running the EventMgr in the background. A non-blocking run should
            be terminated with the end method.  

            
        ToDo
        ----
            - allow integer end (n runs max)
            - pass *args, **kwargs to task, use a few default variables
            - allow return statuses from task to terminate loop

        """
        self.interval = interval
        if task == None:
            self.task = self.default_task
        else:
            self.task = task
        self.end_time = end
        self.iteration = 0
        self.block = block
        self.loop = asyncio.get_event_loop()
        self.loop.call_soon(self.executor)

    def run(self):
        """
        Starts the blocking event loop and configures signal handlers. Should
        the EvengMgr be set for non-blocking mode, the responsibility of 
        catching the kill signal is given to the no_block_loop.
        
        Note
        ----
            Intended for internal use only.
        
        """
        if not self.block:
            try:
                self.loop.run_forever()
            except KeyboardInterrupt: 
                self.terminate()
        else:
            for sig in (signal.SIGINT, signal.SIGTERM):
                self.loop.add_signal_handler(sig,self.terminate)
        
            self.loop.run_forever()

    def terminate(self):
        """
        Halts the blocking event loop. Also used as the signal handler.
        
        Note
        ----
            Intended for internal use only.
        
        """
        self.loop.stop()
        #self.loop.close()
        
    def no_block_terminate(self):
        """
        Halts the non-blocking event loop. Also used as the signal handler
        
        Note
        ----
            Intended for internal use only.
        
        """
        self.no_block_loop.stop()
        #self.no_block_loop.close()

    def start(self):
        """
        Launch the EventMgr using this method.

        """
        if self.block:
            self.run()
            return None
        else:
            self.no_block_loop = asyncio.get_event_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                self.no_block_loop.add_signal_handler(
                    sig,self.no_block_terminate
                )
            self.future = self.no_block_loop.run_in_executor(None,self.run)
            return self.future 

   

    def end(self):
        """
        Force the EventMgr to end. Block-agnostic. 

        ToDo
        ----
            - is the ability to call the blocking terminate at all useful?

        """
        if self.block:
            self.terminate()
        else:
            self.no_block_terminate()

        self.loop.close()

    '''
    async def waiter(self):
        response = await self.future
        return response
        #await asyncio.wait_for(self.future)


    def collect(self):
        #print(type(self.__async__waiter))
        self.no_block_loop.run_until_complete(self.waiter())
    '''


    def executor(self,target_time=None):
        """
        The executor method manages the execution of the given task and
        schedules the next task at the according time. 

        Parameters
        ----------
        target_time = datetime.datetime
            Specify the time at which the execution should ideally happen. 
        
        Note
        ----
            Intended for internal use only.
        
        """
        args = {'target_time':target_time}
        try:
            self.task(target_time)
        except:
            self.end()
            return
        
        #self.task()
        self.iteration = self.iteration + 1
        if target_time == None:
            target_time = datetime.datetime.now() + self.interval
        else:
            target_time = target_time + self.interval 
    
        now = datetime.datetime.now()
        delay = target_time - datetime.datetime.now()
        #logger.debug("EXTRA TIME: {:4.3}f {}s".format(delay/self.interval,delay))
        logger.info("load: {:7.4f}%".format((1-delay/self.interval)*100))
        if delay < datetime.timedelta():
            logger.warn("task exceeding cycle time")
        delay = max(delay,datetime.timedelta()) 
        if self.end_time != None:
            if (now + delay) < self.end_time:
                self.loop.call_later(
                    delay.total_seconds(),
                    self.executor,target_time
                )
            else:
                self.loop.stop()
        else:
            self.loop.call_later(
                delay.total_seconds(),
                self.executor,target_time
            )
        
    def default_task(self,*args,**kwargs):
        """
        Example task to be used when a 'None' is provided as the task. 

        Note
        ----
            Intended for internal use only.
        
        """
        #print("{:>5}".format(self.iteration),datetime.datetime.now())
        logger.debug("{:>7} DEFAULT TASK".format(self.iteration))


class demo:
    def __init__(self):
        self.x = 0

    def it(self):
        self.x = self.x + 1

if __name__ == "__main__":
    a = demo()
    z = EventMgr(datetime.timedelta(seconds=.01),end=datetime.datetime.now() +
        datetime.timedelta(seconds=.2),block=True,task=None)
    #z.start()
    z.start()
    print(a.x)
    print('s')

    u = []
    end = datetime.datetime.now()+datetime.timedelta(seconds=2)
    for i in range(1,3):
        u.append(EventMgr(datetime.timedelta(seconds=i/10),end=end,block=True))
    print(u)
    print(u[0])
    u[0].start()
    '''
    for i in u:
        i.start()
    '''
    time.sleep(5)

    #time.sleep(2)


