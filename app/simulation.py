from model import Param, Model
import streamlit as st

st.title("Simulation")

# ----------------------------------------------------------------------------
# Run the model
# ----------------------------------------------------------------------------

my_params = Param()

st.header("Parameters")
st.write(my_params.__dict__)

if st.button("Run simulation"):
    my_model = Model(my_params)
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
