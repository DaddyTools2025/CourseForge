---
description: How to add or update new API models for CourseForge
---
# Updating API Models in CourseForge

When new models need to be added to the project, follow these automated steps:

## Step 1: Update the Frontend Dropdown
1. Locate `app.py` in the root directory.
2. Find the `model_name = st.selectbox("模型选择 *", options=[...])` component.
3. Update the `options` array with the new list of models provided by the user. Ensure the names exactly match the API's expected model strings.

// turbo
## Step 2: Validate the Changes
Run a quick test or review the changes to ensure syntax is correct. You can use the `python run_app.py --help` or similar to just verify it parses.

```bash
python -m py_compile app.py
```

// turbo-all
## Step 3: Package the Application
Run PyInstaller to rebuild the executable with the updated model list.
```bash
cd c:\Users\lucien\Desktop\CourseForge
python -m PyInstaller -y --clean CourseForge.spec
```

## Step 4: Notify the User
After the build completes successfully (exit code 0), notify the user that the models have been updated and integrated into `dist/CourseForge.exe`.
