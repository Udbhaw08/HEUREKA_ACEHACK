$env:USE_ZYND="1"
$env:PYTHONPATH="backend;."
.venv\Scripts\python.exe test_zynd_fresh.py *> final_results.txt
