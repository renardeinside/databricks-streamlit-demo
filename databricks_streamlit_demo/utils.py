import streamlit as st
import contextlib as _contextlib
import threading as _threading
from streamlit.report_thread import add_report_ctx as _add_report_ctx


def write_aligned_header(text: str, alignment: str = "left", level: int = 3):
    """
    Writes header with given alignment and level, useful for doing left/right switches
    """
    st.markdown(
        f"""
            <div style='text-align: {alignment};'> 
                <h{level}>{text}</h{level}>
            </div>
        """,
        unsafe_allow_html=True,
    )


def empty_date_warning():
    st.warning(
        """
Pickup/dropoff locations are missing in the source data for any day after 2016.06.30, please choose the date before 1st of July 2016 for a density map visualization.
"""
    )


def _spinner_component(text: str) -> str:
    """
    Returns HTML code for custom spinner with spinner component from Bootstrap 4
    """
    component = f"""
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet"/>
        <div class="d-flex flex-column align-items-center justify-content-center">
        <div class="row">
            <div class="spinner-border m-1 text-success" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            </div>
            <div class="row">
            <p>{text}</p>
            </div>
        </div>
        """
    return component


@_contextlib.contextmanager
def custom_spinner(text="In progress..."):
    """
    This function is a fork of st.spinner
    """
    import streamlit.caching as caching

    with caching.suppress_cached_st_function_warning():
        # clean up the message content in the beginning
        message = st.empty()

    try:
        DELAY_SECS = 0.1
        display_message = True
        display_message_lock = _threading.Lock()

        def set_message():
            with display_message_lock:
                if display_message:
                    with caching.suppress_cached_st_function_warning():
                        # keep the spinner component on the screen until context is finished
                        message.markdown(
                            _spinner_component(text), unsafe_allow_html=True
                        )

        _add_report_ctx(_threading.Timer(DELAY_SECS, set_message)).start()

        # Yield control back to the context.
        yield
    finally:
        if display_message_lock:
            with display_message_lock:
                display_message = False
        with caching.suppress_cached_st_function_warning():
            # clean up the spinner as soon as context is finished.
            message.empty()
