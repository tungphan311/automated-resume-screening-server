from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor


class ThreadPool:
   __instance = None
   executor = None

   @staticmethod
   def instance():
        """ Static access method. """
        if ThreadPool.__instance == None:
            ThreadPool()
        return ThreadPool.__instance

   def __init__(self):
        """ Virtually private constructor. """
        if ThreadPool.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.executor = ThreadPoolExecutor(max_workers=4)
            ThreadPool.__instance = self
