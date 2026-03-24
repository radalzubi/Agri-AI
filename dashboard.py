"""Local Streamlit command center for Agri-AI planning outputs."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from dashboard_data import (
    MODULES,
    MODULE_CAPTIONS,
    REQUIRED_OUTPUT_FILES,
    ROLE_CONFIG,
    build_context,
    build_focus_detail,
    choose_default_focus,
    focus_exists,
    load_output_bundle,
)
from dashboard_views import (
    inject_css,
    render_admin,
    render_control_tower,
    render_demand,
    render_footer,
    render_header,
    render_intelligence,
    render_missing_outputs,
    render_operations,
    render_page_header,
    render_planning,
    render_status_badge,
)


def _ensure_sidebar_defaults(role_lens: str) -> None:
    if st.session_state.get("last_role_lens") != role_lens:
        st.session_state["module_nav"] = ROLE_CONFIG[role_lens]["default_module"]
        st.session_state["last_role_lens"] = role_lens


def _sync_focus_state(context: dict[str, object]) -> dict[str, int | str] | None:
    filtered_gap = context["filtered_gap"]
    default_focus = context["default_focus"]
    focus_crop = st.session_state.get("focus_crop")
    focus_year = st.session_state.get("focus_year")
    focus_week = st.session_state.get("focus_week")

    if (
        focus_crop is None
        or focus_year is None
        or focus_week is None
        or not focus_exists(filtered_gap, str(focus_crop), int(focus_year), int(focus_week))
    ):
        if default_focus is None:
            st.session_state.pop("focus_crop", None)
            st.session_state.pop("focus_year", None)
            st.session_state.pop("focus_week", None)
            return None
        st.session_state["focus_crop"] = default_focus[0]
        st.session_state["focus_year"] = default_focus[1]
        st.session_state["focus_week"] = default_focus[2]

    return {
        "crop": str(st.session_state["focus_crop"]),
        "year": int(st.session_state["focus_year"]),
        "week": int(st.session_state["focus_week"]),
    }


def main() -> None:
    st.set_page_config(
        page_title="Agri-AI Command Center",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    st.sidebar.markdown(
        "<h2 style='color:#cfe8d7;font-size:1.05rem;font-weight:800;margin:0 0 0.8rem 0'>"
        "Agri-AI</h2>",
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Supplier-side planning command center")

    output_dir_input = st.sidebar.text_input("Output directory", value="output")
    role_lens = st.sidebar.selectbox(
        "Role lens",
        options=list(ROLE_CONFIG.keys()),
        index=0,
    )
    _ensure_sidebar_defaults(role_lens)

    module = st.sidebar.radio(
        "Workspace",
        options=MODULES,
        key="module_nav",
    )
    st.sidebar.caption(MODULE_CAPTIONS[module])

    bundle, missing_files = load_output_bundle(output_dir_input)
    output_dir = Path(output_dir_input).expanduser()
    if missing_files:
        render_header("Control Tower", role_lens, ROLE_CONFIG[role_lens]["headline"])
        render_missing_outputs(output_dir, missing_files)
        st.stop()

    gap_df = bundle["gap_df"]
    year_options = sorted(gap_df["year"].dropna().unique().tolist()) if not gap_df.empty else []
    crop_options = sorted(gap_df["crop_canonical"].dropna().unique().tolist()) if not gap_df.empty else []
    min_week = int(gap_df["week_iso"].min()) if not gap_df.empty else 1
    max_week = int(gap_df["week_iso"].max()) if not gap_df.empty else 52

    render_header(module, role_lens, ROLE_CONFIG[role_lens]["headline"])

    context_preview = build_context(
        bundle=bundle,
        output_dir=output_dir,
        years=year_options,
        crops=[],
        week_range=(min_week, max_week),
    )
    trust_label = context_preview["confidence"]["state_label"]
    trust_tone = context_preview["confidence"]["state_tone"]
    last_updated = context_preview["output_status"].loc[
        context_preview["output_status"]["file_name"] == REQUIRED_OUTPUT_FILES["gap_analysis"],
        "last_updated",
    ].iloc[0]

    st.markdown("<div class='context-strip'>", unsafe_allow_html=True)
    filter_cols = st.columns([1.05, 1.65, 1.35, 0.95])
    selected_years = filter_cols[0].multiselect(
        "Season",
        options=year_options,
        default=year_options[-1:] if year_options else [],
    )
    selected_years = selected_years or year_options
    selected_crops = filter_cols[1].multiselect(
        "Crop scope",
        options=crop_options,
        default=[],
        format_func=lambda crop: crop.replace("_", " ").title(),
    )
    week_range = filter_cols[2].slider(
        "Week horizon",
        min_value=min_week,
        max_value=max_week,
        value=(min_week, max_week),
    )
    with filter_cols[3]:
        st.markdown(
            f"<div style='margin-top:0.3rem'>{render_status_badge(trust_label, trust_tone)}</div>"
            f"<div style='margin-top:0.6rem' class='micro-label'>Last refresh</div>"
            f"<div style='font-size:0.88rem;color:#12202a;font-weight:700'>{last_updated}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    context = build_context(
        bundle=bundle,
        output_dir=output_dir,
        years=selected_years,
        crops=selected_crops,
        week_range=week_range,
    )

    focus_state = _sync_focus_state(context)
    focus_detail = (
        build_focus_detail(
            context["filtered_gap"],
            focus_state["crop"],
            focus_state["year"],
            focus_state["week"],
        )
        if focus_state is not None
        else None
    )

    st.caption(
        f"Current view: {len(context['available_crops'])} crop(s), "
        f"{int(context['filtered_gap'][['year', 'week_iso']].drop_duplicates().shape[0]) if not context['filtered_gap'].empty else 0} crop-week(s), "
        f"{context['kpis']['risk_weeks']} risk week(s)"
    )

    if module == "Control Tower":
        render_control_tower(context, role_lens, focus_detail)
    elif module == "Planning":
        render_planning(context, focus_detail)
    elif module == "Demand":
        render_demand(context, focus_detail)
    elif module == "Operations":
        render_operations(context)
    elif module == "Intelligence":
        render_intelligence(context, role_lens)
    elif module == "Admin":
        render_admin(context)

    render_footer()


if __name__ == "__main__":
    main()
