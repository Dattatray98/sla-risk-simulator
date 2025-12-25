import random
from core.state import claim
from core.parameters import get_system_parameters


def assign_workers(state):
    for w in state.worker_object:
        if w.is_busy or not state.Queue.arr:
            continue

        c = state.Queue.arr.pop(0)

        w.current_claim = c
        w.is_busy = True
        w.remaining_time = c.processing_time

        c.start_time = state.current_time


def process_work(state):
    for w in state.worker_object:
        if w.is_busy:
            w.remaining_time -= 1


def complete_claims(state):
    for w in state.worker_object:

        if w.is_busy and w.remaining_time <= 0:
            c = w.current_claim

            # mark completion
            c.complition_time = state.current_time

            if (c.complition_time - c.arrival_time) > state.SLA_time:
                c.SLA_Breached = True

            # move claim to completed list
            state.complited_claims.append(c)

            # free the worker
            w.current_claim = None
            w.is_busy = False
            w.remaining_time = 0


def check_active_sla_breaches(state):
    # waiting claims
    for c in state.Queue.arr:
        if not c.SLA_Breached:
            if (state.current_time - c.arrival_time) > state.SLA_time:
                c.SLA_Breached = True

    # in-progress claims
    for w in state.worker_object:
        if w.is_busy:
            c = w.current_claim
            if not c.SLA_Breached:
                if (state.current_time - c.arrival_time) > state.SLA_time:
                    c.SLA_Breached = True


def future_arrivals(state, params):
    low = max(0, params["avg_arrivals_per_day"] - params["arrival_variation"])
    high = params["avg_arrivals_per_day"] + params["arrival_variation"]

    arrivals = random.randint(low, high)

    for _ in range(arrivals):
        proc_time = random.choice(params["processing_time_minutes"])
        state.Queue.arr.append(claim(state.current_time, int(proc_time)))


def run_single_simulation(base_state, forecast_minutes, params):
    state = base_state

    while state.current_time < forecast_minutes:
        future_arrivals(state, params)
        assign_workers(state)
        process_work(state)
        complete_claims(state)
        check_active_sla_breaches(state)
        state.current_time += 1

    # collect all claims
    all_claims = []
    all_claims.extend(state.Queue.arr)
    all_claims.extend(state.complited_claims)

    for w in state.worker_object:
        if w.is_busy and w.current_claim:
            all_claims.append(w.current_claim)

    total_claims = len(all_claims)
    sla_breached = sum(1 for c in all_claims if c.SLA_Breached)

    breach_rate = sla_breached / total_claims if total_claims > 0 else 0.0

    return {
        "total_claims": total_claims,
        "sla_breached": sla_breached,
        "breach_rate": breach_rate,
        "final_queue": len(state.Queue.arr),
    }
