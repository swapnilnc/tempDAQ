import tempfile
# from threading import Thread
from multiprocessing import Process
import os
import time


def setValue():
    currentDir = os.getcwd()
    inPath = '{}/tempFiles'.format(currentDir)
    outDic = tempfile.TemporaryFile(mode='w+b', dir=inPath, delete=False)
    opList = b'21.265, 21.592, 24.693, 20.673, 25.573, 23.851, 21.262, 25.552, 0., 0.'
    outDic.write(opList)
    outDic.seek(0)
    return str(outDic.name)


def readValue(dir):
    # currentDir = os.getcwd()
    # dir = '{}/tempFiles'.format(currentDir)
    print('in read',dir)
    outDic = open(dir, 'r')
    # outDic.seek(0)

    listDoc = outDic.read()
    print('qwerty', listDoc)



if __name__ == '__main__':
    dir = setValue()
    print(dir)
    # p1 = Thread(target=readValue, args=[dir])
    p1 = Process(target=readValue, args=[dir])
    p1.start()
    p1.join()
