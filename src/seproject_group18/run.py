import os 
from seproject_group18.app import app
from seproject_group18.script import bikeinfo, weatherinfo 
from multiprocessing import Process

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def webserver():
    app.run(host='0.0.0.0', port=5000)

def main():
    runInParallel(bikeinfo.main, weatherinfo.main, webserver)
    #app.run(host='0.0.0.0', port=5000)
    print("import module successfull")

if __name__ == "__main__": 
    main()
