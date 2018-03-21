import os, sys, time, subprocess
import logging, threading
from seproject_group18.app import views
from seproject_group18.script import bikeinfo, weatherinfo, processmanagement 
from multiprocessing import Process

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

class WebServer(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        '''
        app.run(host='0.0.0.0', port=5000)
        '''
        while True:
            # Do something
            print('Doing something imporant in the background')

            time.sleep(self.interval)


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def webserver_func():
    views.app.run(host='0.0.0.0', port=5000, debug=True)

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    stdout = current_path + "/../../log/DublinBike.log"
    logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
       filename=stdout,
       filemode='a'
    )

    if len(sys.argv) == 1:
        print(sys.argv[0] + " {webstart|dbstart|allstart|status|stop}")
        sys.exit(0)
    elif sys.argv[1] == 'status':
        my_process = processmanagement.ProcessManagement(['run.py', 'dublinbike', 'start'])
        if my_process.isProcessRunning():
            print("It is running now!")
        else:
            print("It is stopped!")
    elif sys.argv[1] == 'stop':
        my_process = processmanagement.ProcessManagement(['run.py', 'dublinbike', 'start'])
        if my_process.killProcessRunning():
            print("Stopped!")
    elif 'webstart' != sys.argv[1] and 'dbstart' != sys.argv[1] and 'allstart' != sys.argv[1]:
        print(sys.argv[0] + " {webstart|dbstart|allstart|status|stop}")
        sys.exit(0)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    fpid = os.fork()
    if fpid!=0:
        sys.exit(0)
    if sys.argv[1] == 'webstart':
        webserver_func()
    elif sys.argv[1] == 'dbstart':
        runInParallel(bikeinfo.main, weatherinfo.main)
    elif sys.argv[1] == 'allstart':
        runInParallel(bikeinfo.main, weatherinfo.main, webserver_func)


if __name__ == "__main__": 
    main()
