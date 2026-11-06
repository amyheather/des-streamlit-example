"""Run and save simulation scenarios."""

import streamlit as st
from model import Param, Trial

# ----------------------------------------------------------------------------
# Allow user to choose model parameters
# ----------------------------------------------------------------------------

st.title("Run simulation")

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

if st.button("Run and save scenario", type="primary"):
    # ----------------------------------------------------------------------------
    # Run the model
    # ----------------------------------------------------------------------------

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

    # ----------------------------------------------------------------------------
    # Save results to session state to allow comparison between scenarios
    # ----------------------------------------------------------------------------

    scenario_name = f"Scenario {len(st.session_state.scenarios) + 1}"
    st.session_state.scenarios[scenario_name] = {
        "settings": {
            "Scenario": scenario_name,
            "Inter-arrival": st.session_state.mean_patient_inter,
            "Consultation mean": st.session_state.mean_nurse_consult_time,
            "Consultation SD": st.session_state.sd_nurse_consult_time,
            "Nurses": st.session_state.num_nurses,
            "Cost per hour": st.session_state.nurse_cost_per_hour,
            "Duration": st.session_state.sim_duration,
            "Replications": st.session_state.num_replications,
        },
        "mean": trial.trial_mean_q_time_nurse,
        "sd": trial.trial_sd_q_time_nurse,
        "p90": trial.trial_perc_90_q_time_nurse,
        "se": trial.se_q_time_nurse,
        "ci_lower": trial.ci_lower_q_time_nurse,
        "ci_upper": trial.ci_upper_q_time_nurse,
        "cost": trial.total_nurse_cost,
        "df": trial.replication_df,
    }

    # Select the newly saved scenario and show confirmation
    st.session_state.chosen_scenario = scenario_name
    st.success(f"""
    {scenario_name} ran successfully and was saved for this sesssion.
    """)

if st.session_state.scenarios:
    st.divider()
    st.header("Saved scenarios")

    st.dataframe(
        [scenario["settings"] for scenario in st.session_state.scenarios.values()],
        hide_index=True,
    )
    st.caption("Scenarios are saved for the current session only.")

    st.divider()
    st.header("Results")
    if st.button(label="Go to results page", type="primary"):
        st.switch_page("results.py")
