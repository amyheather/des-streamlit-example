import streamlit as st
from model import Model, Param

# ----------------------------------------------------------------------------
# Allow user to choose model parameters
# ----------------------------------------------------------------------------

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

    st.slider(
        label="Number of nurses", min_value=1, max_value=4, value=1, key="num_nurses"
    )

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
        min_value=1,
        max_value=10,
        value=5,
        key="num_replications",
    )

if st.button("Run simulation", type="primary"):
    # ----------------------------------------------------------------------------
    # Run the model
    # ----------------------------------------------------------------------------

    my_params = Param(
        mean_patient_inter=st.session_state.mean_patient_inter,
        mean_nurse_consult_time=st.session_state.mean_nurse_consult_time,
        sd_nurse_consult_time=st.session_state.sd_nurse_consult_time,
        num_nurses=st.session_state.num_nurses,
        sim_duration=st.session_state.sim_duration,
        num_replications=st.session_state.num_replications,
    )

    my_model = Model(param=my_params, replication_id=0)
    my_model.run_model()

    patient_df = my_model.convert_entity_list_to_dataframe(my_model.list_of_patients)
    run_results = my_model.calculate_run_results(patient_df)

    # ----------------------------------------------------------------------------
    # Show results
    # ----------------------------------------------------------------------------

    st.header("Results")
    st.write(f"""
    Mean queuing time for the nurse was {my_model.mean_q_time_nurse:.2f} minutes.

    SD queuing time for the nurse was {my_model.sd_q_time_nurse:.2f} minutes.

    90th percentile queuing time for the nurse was {my_model.perc_90_q_time_nurse:.2f} minutes.
    """)
