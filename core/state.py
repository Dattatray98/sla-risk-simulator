class systemData:
    def __init__(self, workers, QueueLength = 0):
        self.workers = workers
        self.QueueLength = QueueLength
        self.SLA_time = None


class worker:
    def __init__(self):
        self.is_busy = False
        self.remaining_time = 0
        self.current_claim = None


class claim:
    def __init__(self, arrival_time, processing_time):
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.start_time = None
        self.complition_time = None
        self.SLA_Breached = False


class Queue:
    def __init__(self):
        self.arr = []


class system_state(systemData):
    def __init__(self, workers, QueueLength):
        super().__init__(workers, QueueLength)
        self.current_time = 0
        self.worker_object = []
        self.Queue = Queue()
        self.complited_claims = []

    def worker_list(self):
        for i in range(self.workers):
            self.worker_object.append(worker())

    def QueueList(self):
        if self.QueueLength == None:
            return
        else:
            for i in range(self.QueueLength):
                self.Queue.arr.append(claim(arrival_time=0, processing_time=0))
