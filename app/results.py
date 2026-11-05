"""View results from saved scenarios."""

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------------
# Helper function
# ------------------------------------------------------------------------


# Function for highlighting the row/s with the chosen scenario/s
def style_settings(settings, chosen_scenarios):
    def highlight(row):
        style = (
            "background-color: #dbeafe; color: #111827"
            if row["Scenario"] in chosen_scenarios
            else ""
        )
        return [style] * len(row)

    return settings.style.apply(highlight, axis=1).format(precision=2)


# ------------------------------------------------------------------------
# Page
# ------------------------------------------------------------------------

st.title("View results")

if not st.session_state.scenarios:
    st.info("Run and save scenarios to view results here.", icon="ℹ️")

else:
    st.write(
        "You can either view results from a **single scenario**, or **compare across scenarios**."
    )

    tab_single, tab_compare = st.tabs(["View single scenario", "Compare scenarios"])

    # ------------------------------------------------------------------------
    # View results from a single scenario
    # ------------------------------------------------------------------------

    with tab_single:
        st.space()
        with st.container(border=True):
            st.selectbox(
                label="**Choose a scenario to view:**",
                options=list(st.session_state.scenarios),
                key="chosen_scenario",
            )

            # Convert the settings dictionary into a dataframe
            settings = pd.DataFrame(
                [
                    scenario["settings"]
                    for scenario in st.session_state.scenarios.values()
                ]
            )

            # Show dataframe of saved scenarios, with chosen scenario highlighted
            st.caption("The selected scenario is highlighted below.")
            st.dataframe(
                style_settings(
                    settings=settings,
                    chosen_scenarios=[st.session_state.chosen_scenario],
                ),
                hide_index=True,
            )

        # Get results of chosen scenario
        results = st.session_state.scenarios[st.session_state.chosen_scenario]

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

    # ------------------------------------------------------------------------
    # Compare results from multiple scenarios
    # ------------------------------------------------------------------------

    with tab_compare:
        if len(st.session_state.scenarios) < 2:
            st.info("Run at least two scenarios to enable comparison", icon="ℹ️")

        else:
            st.space()
            with st.container(border=True):
                chosen_compare = st.multiselect(
                    label="**Choose scenarios to compare**",
                    options=list(st.session_state.scenarios),
                )

                st.caption("The selected scenarios are highlighted below.")

                st.dataframe(
                    style_settings(settings=settings, chosen_scenarios=chosen_compare),
                    hide_index=True,
                )

            if len(chosen_compare) < 2:
                st.info("Choose at least two scenario to compare", icon="ℹ️")

            else:
                st.space()
                st.subheader("Mean nurse queue time")
                st.write(
                    "Compare the mean nurse queue times across replications. "
                    "Each point represents one replication."
                )

                # Combine replication results, adding a scenario label.
                replications = pd.concat(
                    [
                        st.session_state.scenarios[name]["df"].assign(Scenario=name)
                        for name in chosen_compare
                    ],
                    ignore_index=True,
                )

                fig = px.box(
                    replications,
                    x="Scenario",
                    y="mean_q_time_nurse",
                    color="Scenario",
                    points="all",
                    category_orders={"Scenario": list(st.session_state.scenarios)},
                    hover_data=["replication_id"],
                    labels={
                        "mean_q_time_nurse": "Mean nurse queue time (minutes)",
                    },
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig)

                st.space()
                st.subheader("Summary statistics")

                summary = pd.DataFrame(
                    [
                        {
                            "Scenario": name,
                            "Mean": st.session_state.scenarios[name]["mean"],
                            "SD": st.session_state.scenarios[name]["sd"],
                            "90th percentile": st.session_state.scenarios[name]["p90"],
                            "Standard error": st.session_state.scenarios[name]["se"],
                            "95% CI lower": st.session_state.scenarios[name][
                                "ci_lower"
                            ],
                            "95% CI upper": st.session_state.scenarios[name][
                                "ci_upper"
                            ],
                        }
                        for name in chosen_compare
                    ]
                )

                st.caption("Nurse queue time summary statistics, in minutes:")

                st.dataframe(
                    summary.style.format(precision=2),
                    hide_index=True,
                )

                st.caption("Total nurse staffing costs:")
                costs = pd.DataFrame(
                    [
                        {
                            "Scenario": name,
                            "Total cost (£)": st.session_state.scenarios[name]["cost"],
                        }
                        for name in chosen_compare
                    ]
                )
                st.dataframe(costs, hide_index=True)
