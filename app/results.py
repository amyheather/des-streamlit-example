"""View results from saved scenarios."""

import pandas as pd
import plotly.express as px
import streamlit as st

st.title("View results")

if not st.session_state.scenarios:
    st.info("Run and save scenarios to view results here.", icon="ℹ️")

else:
    # ------------------------------------------------------------------------
    # Choose scenario (default is the last saved scenario)
    # ------------------------------------------------------------------------

    with st.container(border=True):
        st.selectbox(
            label="**Choose a scenario to view:**",
            options=list(st.session_state.scenarios),
            key="chosen_scenario",
        )

        # Convert the settings dictionary into a dataframe
        settings = pd.DataFrame(
            [scenario["settings"] for scenario in st.session_state.scenarios.values()]
        )

        # Function for highlighting the row with the chosen scenario
        def highlight_chosen(row, chosen_scenario):
            style = (
                "background-color: #dbeafe; color: #111827"
                if row["Scenario"] == chosen_scenario
                else ""
            )
            return [style] * len(row)

        # Show dataframe of saved scenarios, with chosen scenario highlighted
        st.caption("The selected scenario is highlighted below.")
        st.dataframe(
            settings.style.apply(
                highlight_chosen,
                axis=1,
                chosen_scenario=st.session_state.chosen_scenario,
            ).format(precision=2),
            hide_index=True,
        )

    # Get results of chosen scenario
    results = st.session_state.scenarios[st.session_state.chosen_scenario]

    # ------------------------------------------------------------------------
    # Show scenario results
    # ------------------------------------------------------------------------

    st.space()
    st.subheader("Scenario summary")
    st.write(f"""
    Summary of nurse queue times across **all** replications.

    * Mean: {results["mean"]:.2f} minutes.
    * SD: {results["sd"]:.2f} minutes.
    * 90th Perc: {results["p90"]:.2f} minutes.
    * Standard error: {results["se"]:.2f}
    * 95% CI: ({results["ci_lower"]:.2f}, {results["ci_upper"]:.2f}) minutes
    """)

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
