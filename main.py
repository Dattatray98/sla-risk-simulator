from core.state import system_state
from engine.simulator import run_single_simulation
from core.parameters import get_system_parameters

params = get_system_parameters()


runs = int(input("Enter the simulation runs = "))
breach_count = 0
WORKERS = int(input("Enter number of workers = "))
QUEUE_LENGTH = int(input("Enter the Queue Length = "))
total_breach_rate = 0.0

What_if = True

while What_if:
    for _ in range(runs):
        state = system_state(workers=WORKERS, QueueLength=QUEUE_LENGTH)
        state.worker_list()
        state.QueueList()
        state.SLA_time = params["SLA_time_90th_percentile_minutes"]

        result = run_single_simulation(
            base_state=state,
            forecast_minutes=60,  # 7 days
            params=params,
        )

        total_breach_rate += result["breach_rate"]
        avg_breach_rate = total_breach_rate / runs

    print("SLA breach probability:", avg_breach_rate)

    user_input = input("Do you want to run another scenario? (yes/no) : ")
    if user_input.lower() != "yes":
        What_if = False
    else:
        WORKERS = int(input("Enter number of workers for another scenario = "))
