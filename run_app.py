import streamlit.web.cli as stcli
import os, sys
import traceback
import ctypes

def resolve_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

def show_error(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)  # 0x10 = MB_ICONERROR

if __name__ == "__main__":
    try:
        app_path = resolve_path("app.py")
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"App file not found: {app_path}")

        # Simulate the "streamlit run app.py" command line arguments
        # We add --global.developmentMode=false to suppress dev warnings
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--global.developmentMode=false",
            "--browser.gatherUsageStats=false",
            "--server.headless=false",
            "--server.address=127.0.0.1",
            "--server.port=8501",
        ]
        sys.exit(stcli.main())
    except Exception as e:
        error_msg = f"An error occurred launching the app:\n\n{str(e)}\n\n{traceback.format_exc()}"
        show_error("CourseForge Error", error_msg)
        sys.exit(1)
