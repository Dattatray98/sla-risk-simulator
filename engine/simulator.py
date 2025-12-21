from core.state import system_state, claim, worker, Queue

def assign_workers(state, processing_time):
    for worker in state.worker_object:
        if worker.is_busy:
            continue

        if not state.Queue.arr:
            break

        claim_obj = state.Queue.arr.pop(0)

        worker.current_claim = claim_obj
        worker.is_busy = True
        worker.remaining_time = processing_time

        claim_obj.start_time = state.current_time


def process_work(state):
    for worker in state.worker_object:
        if worker.is_busy:
            worker.remaining_time -= 1


def complete_claims(state):
    for worker in state.worker_object:

        if worker.is_busy and worker.remaining_time == 0:

            claim_obj = worker.current_claim

            # mark completion
            claim_obj.complition_time = state.current_time

            # move claim to completed list
            state.complited_claims.append(claim_obj)

            # free the worker
            worker.current_claim = None
            worker.is_busy = False
            worker.remaining_time = 0


def SLA_check(state):
    for claim_obj in state.complited_claims:
        if claim_obj.complition_time is None:
            continue

        total_time = claim_obj.complition_time - claim_obj.arrival_time

        if total_time > state.SLA_time:
            claim_obj.SLA_Breached = True


def advance_time(state):
    state.current_time += 1

def cloned_system_state(state):
    cloned = system_state()

    cloned.current_time = state.current_time
    cloned.SLA_time = state.SLA_time
    cloned.workers = state.workers


    claim_map = {}


    for c in state.Queue.arr:
        new_c = claim()
        new_c.arrival_time = c.arrival_time
        new_c.start_time = c.start_time
        new_c.complition_time = c.complition_time
        new_c.SLA_Breached = c.SLA_Breached
        claim_map[c] = new_c
        cloned.Queue.arr.append(new_c)

    
    for c in state.complited_claims:
        new_c = claim()
        new_c.arrival_time = c.arrival_time
        new_c.start_time = c.start_time
        new_c.complition_time = c.complition_time
        new_c.SLA_Breached = c.SLA_Breached
        claim_map[c] = new_c
        cloned.complited_claims.append(new_c)
    

    for w in state.worker_object:
        new_w = worker()
        new_w.current_claim = w.current_claim
        new_w.is_busy = w.is_busy
        new_w.remaining_time = w.remaining_time

        if w.current_claim is not None:
            new_w.current_claim = claim_map[w.current_claim]

        
        cloned.worker_object.append(new_w)
    

    return cloned
