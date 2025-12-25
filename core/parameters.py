import pandas as pd

def get_system_parameters():
    data = pd.read_csv("data/Insurance_claims_event_log.csv")

    pdata = pd.DataFrame(data)

    df = pdata[["case_id", "timestamp"]].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])


    # Arrival rate calculation
    arrival_df = (
        df.groupby("case_id")["timestamp"]
        .min()
        .reset_index()
    )

    arrival_df["arrival_date"] = arrival_df["timestamp"].dt.date

    # chaging the column name for clarity
    arrival_rate_ts = (
        arrival_df.groupby("arrival_date").size().reset_index(name="arrivals")
    )


    # converting the string timestamp into actual timestamp
    arrival_rate_ts["arrival_date"] = pd.to_datetime(arrival_rate_ts["arrival_date"])

    # finding the missing dates and filling with zero
    arrival_rate_ts = (
        arrival_rate_ts.set_index("arrival_date")
        .asfreq("D", fill_value=0)
        .reset_index()
    )

    # calculating avg and variation 
    avg_arrivals = int(arrival_rate_ts["arrivals"].mean())
    arrival_variation = arrival_rate_ts["arrivals"].max() - arrival_rate_ts["arrivals"].min()

    # processing behavior (days)
    proc_df = df.groupby("case_id")['timestamp'].agg(['min', 'max'])
    proc_days = (proc_df['max'] - proc_df['min']).dt.total_seconds() / (60 * 60 * 24)


    processing_cap = proc_days.quantile(0.5)
    proc_days = proc_days.clip(upper=processing_cap)


    SLA_time = proc_days.quantile(0.75)


    print("sla time = ",SLA_time)
    print("avg arrivals = ", avg_arrivals )
    print("processing time = ", proc_days.mean())
    print("arrival variation = ", arrival_variation)

    return {
        "processing_time_minutes": proc_days.tolist(),
        "arrival_variation": arrival_variation,
        "avg_arrivals_per_day": avg_arrivals,
        "SLA_time_90th_percentile_minutes": SLA_time,
    }
