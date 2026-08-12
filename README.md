======================= Installation ===============================

1. Install VS Code
2. Install Python through MS Store
4. For Environment
  --------> python -m venv venv

5. To Activate
  --------> venv\Scripts\activate
cd pages

6. pytest installation
  --------> python -m pip install pytest

7. Version
  --------> python -m pytest --version

8. Playwright Installation
  --------> python -m pip install playwright

9. playwright Browsers Installation
  --------> python -m playwright install

10. Install Pytest Playwright Plugin
  --------> python -m pip install pytest-playwright

11. For Excel readable
  --------> python -m pip install openpyxl

12. Run Command
  -------->
python -m pytest -s test_cv.py
pytest -s test_mc.py
python -m pytest -s test_uat_pc.py
python -m pytest -s test_pa.py

For paralell execution
---> pytest test_pc.py test_mc.py -n 2 -v --capture=no

For one by one
---> pytest -s -v test_pc.py test_mc.py

******Git Commands*******
git status
git add <file name>
git commit -m "Message"
git push
git ls-files
del /s /q *.pyc
rmdir /s /q .pytest_cache
rmdir /s /q __pycache__

git update-index --skip-worktree <filename>   -    command to ignore PUSH file
git update-index --no-skip-worktree <filename>
git ls-files -v | findstr "^S"                -    for Git ignored files










