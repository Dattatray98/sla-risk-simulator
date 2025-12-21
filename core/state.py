class systemData:
    def __init__(self):
        self.workers = 8
        self.queue_size = 1000
        self.SLA_time = 24 * 60
        self.time = 0 
        self.list = []
    

class worker:
    def __init__(self):
        self.is_busy = False
        self.remaining_time = 0
        self.current_claim = None


class claim :
    def __init__(self):
        self.arrival_time = 0
        self.start_time = None
        self.complition_time = None
        self.SLA_Breached = False


class Queue :
    def __init__(self):
        self.arr = []


class system_state(systemData):
    def __init__(self):
        super().__init__()
        self.current_time = 0
        self.worker_object = []
        self.Queue = Queue()
        self.complited_claims = []

    def worker_list(self):
        for i in range(8):
            self.worker_object.append(worker())
        print("workers  = ",len(self.worker_object))
    
    def queue_list(self):
        for i in range(self.queue_size):
            self.Queue.arr.append(claim())
        print("Queue list = ",len(self.Queue.arr))
