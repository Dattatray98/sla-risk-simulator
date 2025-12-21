from core.state import system_state, claim, worker, Queue
import random


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


def future_arrivals(state, expected=10, variation=4):
    if state.current_time % 60 != 0:
        return
    low = max(0, expected - variation)
    high = expected + variation

    arrivals = random.randint(low, high)

    for _ in range(arrivals):
        claim_obj = claim()
        claim_obj.arrival_time = state.current_time
        state.Queue.arr.append(claim_obj)


def run_single_simulation(
    base_state,
    forecast_window,
    processing_time,
    expected_arrivals,
    arrival_variation,
):
    state = cloned_system_state(base_state)

    while state.current_time < forecast_window:

        future_arrivals(state, expected_arrivals, arrival_variation)

        assign_workers(state, processing_time)
        process_work(state)
        complete_claims(state)
        SLA_check(state)
        advance_time(state)

    total_completed = len(state.complited_claims)
    sla_breaches = sum(1 for c in state.complited_claims if c.SLA_Breached)
    final_queue_size = len(state.Queue.arr)
  
    return {
        "completed": total_completed,
        "sla_breaches": sla_breaches,
        "final_queue_size": final_queue_size,
    }


def run_forecast(
    base_state,
    forecast_window,
    processing_time,
    num_simulations,
    expected_arrivals,
    arrival_variations,
):

    total_runs = num_simulations
    sla_breach_runs = 0
    total_completed = 0
    total_final_queue = 0

    for _ in range(num_simulations):
        result = run_single_simulation(
            base_state=base_state,
            forecast_window=forecast_window,
            processing_time=processing_time,
            expected_arrivals=expected_arrivals,
            arrival_variation=arrival_variations,
        )

        total_completed += result["completed"]
        total_final_queue += result["final_queue_size"]

        if result["sla_breaches"] > 0:
            sla_breach_runs += 1
        
    sla_breach_probabiltiy = sla_breach_runs / total_runs

    print(
        f"sla_breach_probability: {sla_breach_probabiltiy}, \navg_completed_claims: {total_completed / total_runs}\navg_final_queue_size: {total_final_queue / total_runs},\nsimulations_run: {total_runs}"
    )

    return {
        "sla_breach_probability": sla_breach_probabiltiy,
        "avg_completed_claims": total_completed / total_runs,
        "avg_final_queue_size": total_final_queue / total_runs,
        "simulations_run": total_runs,
    }


ss = system_state()
ss.worker_list()
ss.queue_list()


run_forecast(
    base_state=ss,
    forecast_window=240,
    processing_time=5,
    num_simulations=50,
    expected_arrivals=5,
    arrival_variations=4,
)
