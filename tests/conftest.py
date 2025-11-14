'''import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src import config

@pytest.fixture(scope="session", autouse=True)
def _clean_reports():
    shutil.rmtree('reports', ignore_errors=True)

@pytest.fixture(scope="session")
def driver():
    options = FirefoxOptions()
    if config.HEADLESS:
        options.add_argument("-headless")

    drv = webdriver.Firefox(options=options)
    drv.set_page_load_timeout(config.PAGELOAD_TIMEOUT)
    yield drv
    drv.quit()'''

# conftest.py
import os
import shutil
import time
import pytest
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src import config

# --- session cleanup ---
@pytest.fixture(scope="session", autouse=True)
def _clean_reports():
    shutil.rmtree("reports", ignore_errors=True)
    shutil.rmtree("screenshots", ignore_errors=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    print("[conftest] cleaned reports/screenshots")

# --- create driver with retries ---
def _create_driver_with_retries(retries=3, retry_delay=2):
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            opts = FirefoxOptions()
            if getattr(config, "HEADLESS", False):
                try:
                    opts.add_argument("-headless")
                except Exception:
                    opts.headless = True
            drv = webdriver.Firefox(options=opts)
            # timeouts & implicit wait
            try:
                page_timeout = getattr(config, "PAGELOAD_TIMEOUT", None)
                if page_timeout:
                    drv.set_page_load_timeout(page_timeout)
            except Exception:
                pass
            try:
                drv.implicitly_wait(getattr(config, "IMPLICIT_WAIT", 2))
            except Exception:
                drv.implicitly_wait(2)
            # quick sanity check: is driver responding?
            try:
                drv.title  # this triggers a call to the driver; if driver not ready it may raise
            except Exception:
                # not fatal; driver may be starting — we accept the driver if no immediate fatal error
                pass
            return drv
        except Exception as e:
            last_exc = e
            print(f"[conftest] webdriver start attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(retry_delay)
    # all attempts failed
    print("[conftest] All webdriver startup attempts failed")
    raise last_exc

@pytest.fixture(scope="function")
def driver(request):
    """
    Provide a fresh webdriver for each test function and ensure proper teardown.
    After quitting the browser we sleep 10s to give the system a short breathing window
    before the next test starts (this avoids port/process races).
    """
    test_name = request.node.name
    print(f"[conftest] Creating browser for test: {test_name}")
    drv = None
    try:
        drv = _create_driver_with_retries(retries=3, retry_delay=2)
    except Exception as e:
        print(f"[conftest] Failed to create webdriver for {test_name}: {e}")
        raise

    request.node._driver = drv
    yield drv

    # teardown: capture screenshot if test failed
    try:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:
            ts = time.strftime("%Y%m%d_%H%M%S")
            safe_name = request.node.nodeid.replace("/", "_").replace("::", "_")
            png = os.path.join("screenshots", f"{safe_name}_{ts}.png")
            html = os.path.join("screenshots", f"{safe_name}_{ts}.html")
            try:
                drv.save_screenshot(png)
                with open(html, "w", encoding="utf-8") as fh:
                    fh.write(drv.page_source)
                print(f"[conftest] Saved failure screenshot/html: {png}, {html}")
            except Exception as e:
                print("[conftest] Failed to save screenshot/html:", e)
    except Exception as e:
        print("[conftest] error checking rep_call:", e)

    # Always quit the browser
    print(f"[conftest] Quitting browser for test: {test_name}")
    try:
        drv.quit()
    except Exception as e:
        print("[conftest] Error quitting browser:", e, traceback.format_exc())

    # *** Delay AFTER browser quit to avoid driver race conditions ***
    delay_seconds = getattr(config, "POST_TEST_DELAY", 10)
    if delay_seconds and delay_seconds > 0:
        print(f"[conftest] Waiting {delay_seconds}s after test (post-teardown delay).")
        time.sleep(delay_seconds)

# proper hook wrapper so fixtures can inspect outcome
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_call", rep)









