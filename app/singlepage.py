"""Simple single-page app."""

import plotly.express as px
import streamlit as st
from model import Param, Trial

with st.container(border=True):
    st.subheader("Patients")

    st.slider(
        label="Mean patient inter-arrival time (minutes)",
        min_value=3.0,
        max_value=7.0,
        value=5.0,
        step=0.25,
        key="mean_patient_inter",
    )

    st.subheader("Nurses")

    st.number_input(
        label="Mean nurse consultation length (minutes)",
        min_value=3.0,
        max_value=9.0,
        value=6.0,
        key="mean_nurse_consult_time",
    )

    st.number_input(
        label="Standard deviation of nurse consultation length (minutes)",
        min_value=0.0,
        value=1.0,
        key="sd_nurse_consult_time",
    )

    st.pills(label="Number of nurses", options=range(1, 5), default=1, key="num_nurses")

    st.number_input(
        label="Cost per nurse per hour (£)",
        min_value=0.0,
        value=30.0,
        step=1.0,
        key="nurse_cost_per_hour",
        help="Nurses are costed for the full simulation duration, including time when they are not seeing patients",
    )

    st.space(size="xxsmall")
    st.subheader("Simulation")

    st.slider(
        label="Simulation duration (minutes)",
        min_value=50,
        max_value=200,
        value=120,
        key="sim_duration",
    )

    st.slider(
        label="Number of replications",
        min_value=10,
        max_value=50,
        value=30,
        key="num_replications",
    )

if st.button("Run simulation", type="primary"):
    params = Param(
        mean_patient_inter=st.session_state.mean_patient_inter,
        mean_nurse_consult_time=st.session_state.mean_nurse_consult_time,
        sd_nurse_consult_time=st.session_state.sd_nurse_consult_time,
        num_nurses=st.session_state.num_nurses,
        sim_duration=st.session_state.sim_duration,
        num_replications=st.session_state.num_replications,
        nurse_cost_per_hour=st.session_state.nurse_cost_per_hour,
    )
    trial = Trial(param=params)
    trial.run_trial()
    trial.calculate_trial_results()

    results = {
        "mean": trial.trial_mean_q_time_nurse,
        "sd": trial.trial_sd_q_time_nurse,
        "p90": trial.trial_perc_90_q_time_nurse,
        "se": trial.se_q_time_nurse,
        "ci_lower": trial.ci_lower_q_time_nurse,
        "ci_upper": trial.ci_upper_q_time_nurse,
        "cost": trial.total_nurse_cost,
        "df": trial.replication_df,
    }

    st.space()
    st.subheader("Scenario summary")
    st.write(f"""
    Summary of nurse queue times across **all** replications.

    * Mean: {results["mean"]:.2f} minutes.
    * SD: {results["sd"]:.2f} minutes.
    * 90th Perc: {results["p90"]:.2f} minutes.
    * Standard error: {results["se"]:.2f}
    * 95% CI: ({results["ci_lower"]:.2f}, {results["ci_upper"]:.2f}) minutes
    
    Total nurse staffing cost: £{results["cost"]:,.2f}
    """)

    st.space()
    st.subheader("Results from individual replications")
    st.write(
        "The chart shows how the mean nurse queue time varies between **individual** replications."
    )

    fig = px.histogram(
        data_frame=results["df"],
        x="mean_q_time_nurse",
        labels={"mean_q_time_nurse": "Mean nurse queue time"},
    )
    fig.update_layout(yaxis_title="Number of replications")
    st.plotly_chart(fig)

    with st.expander("View underlying data from each replication"):
        st.dataframe(
            results["df"][
                [
                    "replication_id",
                    "patient_counter",
                    "mean_q_time_nurse",
                    "sd_q_time_nurse",
                    "perc_90_q_time_nurse",
                ]
            ]
        )
