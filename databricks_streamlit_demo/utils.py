import streamlit as st
import contextlib as _contextlib
import threading as _threading
from streamlit.report_thread import add_report_ctx as _add_report_ctx

def write_aligned_header(text: str, alignment: str = "left", level: int = 3):
    st.markdown(
        f"""
            <div style='text-align: {alignment};'> 
                <h{level}>{text}</h{level}>
            </div>
        """,
        unsafe_allow_html=True,
    )


def empty_date_warning():
    st.warning("""
Pickup/dropoff locations are missing in the source data for any day after 2016.06.30, please choose the date before 1st of July 2016 for a density map visualization.
"""
)

def _spinner_component(text: str) -> str:
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
    """Temporarily displays a message while executing a block of code.

    Parameters
    ----------
    text : str
        A message to display while executing that block

    Example
    -------

    >>> with st.spinner('Wait for it...'):
    >>>     time.sleep(5)
    >>> st.success('Done!')

    """
    import streamlit.caching as caching

    # @st.cache optionally uses spinner for long-running computations.
    # Normally, streamlit warns the user when they call st functions
    # from within an @st.cache'd function. But we do *not* want to show
    # these warnings for spinner's message, so we create and mutate this
    # message delta within the "suppress_cached_st_function_warning"
    # context.
    with caching.suppress_cached_st_function_warning():
        message = st.empty()

    try:
        # Set the message 0.1 seconds in the future to avoid annoying
        # flickering if this spinner runs too quickly.
        DELAY_SECS = 0.1
        display_message = True
        display_message_lock = _threading.Lock()

        def set_message():
            with display_message_lock:
                if display_message:
                    with caching.suppress_cached_st_function_warning():
                        message.markdown(_spinner_component(text),unsafe_allow_html=True)

        _add_report_ctx(_threading.Timer(DELAY_SECS, set_message)).start()

        # Yield control back to the context.
        yield
    finally:
        if display_message_lock:
            with display_message_lock:
                display_message = False
        with caching.suppress_cached_st_function_warning():
            message.empty()
