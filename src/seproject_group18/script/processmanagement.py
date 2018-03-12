import subprocess, os, signal, sys

class ProcessManagement:
    def __init__(self, process_name):
        self.__process_name = process_name

    def findProcess(self):
        ps= subprocess.Popen("ps -ef | grep -e "+self.__process_name[0]+"  -e " +self.__process_name[1]+" | grep "+self.__process_name[2], shell=True, stdout=subprocess.PIPE)
        lines = []
        output = ps.stdout.readline().strip()
        while(output):
            lines.append(str(output))
            output = ps.stdout.readline().strip()
        ps.stdout.close()
        ps.wait()
        return lines

    def isProcessRunning(self):
        output = self.findProcess()
        if len(output) > 1:
            return True
        else:
            return False

    def killProcessRunning(self):
        output = self.findProcess()
        pids = []
        for line in output:
            elements = line.split()
            if elements[1] not in pids:
                pids.append(elements[1])
        try:
            for pid_str in pids:
                os.kill(int(pid_str), signal.SIGTERM)
        except:
            pass
        return not self.isProcessRunning()

'''
#print(isProcessRunning('run.py'))
# ProcessManagement([pattern1, pattern2, pattern3])
# pattern1 or pattern2 + pattern3
my_process = ProcessManagement(['run.py', 'dublinbike', 'allstart'])
my_process.killProcessRunning()
'''
