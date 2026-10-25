# ShopOS — Integrated OS Concepts for Online Shopping & Order Processing

**Case study:** Problem 2 — Online Shopping and Order Processing System  
**Student:** Tushar Tiple · **UID:** 24003145 · **Batch:** B2 · **Class:** 5th Sem, Section B

ShopOS is a small Flask application that brings four OS concepts into one demonstrable e-commerce workflow.

## Features
1. **CPU Scheduling:** FCFS, non-preemptive SJF, non-preemptive Priority, Round Robin; completion, turnaround, waiting and response times.
2. **Process Synchronization:** bounded order queue protected by a Python lock; queue-full/empty states and produced-consumed invariant.
3. **Deadlock Avoidance:** Banker’s safety check with allocation, maximum, need, available, safe sequence and work trace.
4. **Memory Management:** contiguous First Fit, Best Fit and Worst Fit with per-process allocation and remaining free blocks.
5. **Order processing scenario:** validates sample orders and calculates invoice totals while clearly marking payment/inventory/delivery as simulated.

## Run locally
Requires Python 3.10+.
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## API routes
- `POST /api/schedule`
- `POST /api/queue` with action `produce`, `consume`, `reset`, or `snapshot`
- `POST /api/banker`
- `POST /api/memory`
- `POST /api/orders`

## Important modelling notes
- The bounded queue API demonstrates synchronized state and reports when an operation would block; it does not hold an HTTP request waiting indefinitely.
- Banker’s Algorithm is a safety-state simulator. A real resource manager would also validate and apply incremental requests atomically.
- Memory management is a contiguous variable-sized block simulation, not actual OS memory allocation.
- The order-processing layer does not connect to payment gateways, inventory databases or delivery services. It never charges a card or books a courier.
- This repository is a cohesive implementation of the concepts; it does not copy external repositories. The supplied CPU scheduler, Banker’s Algorithm and Producer–Consumer repositories are listed as conceptual references for the student's own modules.

## Project layout
```text
ShopOS/
├── app.py
├── os_modules/
│   ├── scheduler.py
│   ├── producer_consumer.py
│   ├── banker.py
│   ├── memory.py
│   └── orders.py
├── templates/index.html
├── static/style.css
├── static/app.js
├── tests/test_modules.py
├── requirements.txt
└── docs/CASE_STUDY.md
```


## Student's existing modules / references
- CPU Scheduling Simulator: https://github.com/tushartiple24/Cpu-Scheduling-Simulator
- Banker's Algorithm: https://github.com/tushartiple24/Banker-s-algorithm
- Producer–Consumer Algorithm: https://github.com/tushartiple24/Producer-Consumer-Algorithm

The integrated modules in this ZIP are self-contained implementations aligned to the requested concepts. Compare them with your existing repositories before replacing or merging any code; repository contents were not imported automatically.


## Screenshots
Generated interface preview and algorithm output screenshots are in `docs/screenshots/`. The case-study PDF in `docs/` includes a screenshot appendix. The interface image is a designed preview; algorithm output panels are generated from the included module functions.


The compact case-study PDF places screenshots beside the relevant theory sections rather than in a separate appendix. It is available at `docs/Tushar_Tiple_Practical_9_Case_Study.pdf`.
