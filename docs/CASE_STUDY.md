# Practical 9 — Complex Problem-Solving Case Study
## Online Shopping and Order Processing System

**Name:** Tushar Tiple · **UID:** 24003145 · **Batch:** B2 · **Class:** 5th Sem, Section B  
**Subject:** Operating Systems

## 1. Problem statement and context
An e-commerce platform receives customer orders, processes payments, updates inventory, generates invoices and schedules deliveries. During a sale, many requests arrive together. Each task needs CPU time, memory and shared services such as inventory endpoints, payment workers and database connections. The challenge is to process requests safely, manage concurrency and avoid unsafe resource allocation.

**Scope:** ShopOS simulates the OS mechanisms around an order pipeline. Payment, inventory updates and delivery bookings are represented as statuses only; no external service is contacted.

## 2. Objectives and assumptions
- Compare CPU scheduling strategies using waiting, turnaround, completion and response metrics.
- Demonstrate a bounded producer–consumer queue with synchronized access and explicit full/empty states.
- Evaluate resource allocation using Banker’s safety algorithm and report a safe sequence when one exists.
- Compare First Fit, Best Fit and Worst Fit for contiguous memory allocation.
- Connect the concepts to one illustrative order-processing flow.

Assumptions: processing times, resource counts and memory sizes are educational values; priority 1 is highest; Banker’s Algorithm receives each task’s maximum resource claim in advance; memory is modelled as contiguous free blocks.

## 3. Four OS concepts
### CPU scheduling
Orders become processing tasks such as payment validation, inventory verification, invoice generation and delivery scheduling. FCFS uses arrival order; SJF chooses the shortest ready task; Priority chooses the lowest priority number; Round Robin allocates a time quantum. For each task: `Turnaround = Completion − Arrival`; `Waiting = Turnaround − Burst`; `Response = First Start − Arrival`.

### Process synchronization — Producer–Consumer
Incoming orders are producers and worker threads are consumers. A bounded queue limits pending work. A lock protects shared queue/counter state, preventing simultaneous unsafe updates. When full, the producer operation is reported blocked; when empty, the consumer operation is reported blocked. The invariant is `produced − consumed = items currently in queue`.

### Deadlock avoidance — Banker’s Algorithm
Resources represent payment workers, inventory connections and database connections. `Need = Maximum − Allocation`. Starting with `Work = Available`, the algorithm finds an unfinished process whose Need is no greater than Work, then simulates its completion and returns its allocated resources to Work. If all processes can finish, the state is safe and the order is a safe sequence; otherwise it is unsafe.

### Memory management
Order payloads and processing data request memory blocks. First Fit chooses the first suitable block; Best Fit chooses the smallest suitable block; Worst Fit chooses the largest suitable block. The simulator reports each allocation, remaining block sizes and requests that could not be allocated. It models contiguous allocation, not real RAM.

## 4. Integration flow
1. An order arrives and is submitted to the bounded queue.
2. A worker consumes the order and treats its processing stages as schedulable tasks.
3. Before a shared-resource grant, the resource state is checked with Banker’s Algorithm.
4. A memory block is selected for the task’s data.
5. The scheduler determines execution order; the order simulator displays a validation result, invoice total and simulated payment/inventory/delivery statuses.

## 5. Test cases
- Scheduler: non-zero arrival times, different bursts, algorithm selection and Round Robin quantum.
- Queue: produce into available capacity; detect full queue; detect empty queue; verify produced/consumed invariant.
- Banker: safe sample, unsafe sample and invalid allocation greater than maximum.
- Memory: request that fits, request that does not fit, and differing results across fit strategies.
- Orders: valid quantities, invalid quantity and total calculation.

## 6. Limitations and future work
This is a teaching simulator, not a production commerce platform. It has no authentication, persistent database, real payment integration, stock reservation or courier API. The queue endpoint reports blocking conditions rather than suspending a web request. Banker’s Algorithm demonstrates safety checking but is not a complete concurrent resource manager. Future improvements could add persistent order storage, real worker threads, atomic resource-request handling, authentication and external-service adapters.

## 7. Conclusion
The integrated ShopOS project demonstrates how CPU scheduling, synchronization, deadlock avoidance and memory management address different risks in a high-volume order pipeline. Scheduling helps reason about latency, synchronization protects queue state, Banker’s Algorithm tests safe resource progress, and memory strategies compare allocation and fragmentation.
