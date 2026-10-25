from flask import Flask, render_template, request, jsonify
from os_modules.scheduler import schedule_processes
from os_modules.banker import safety_check
from os_modules.memory import allocate_memory
from os_modules.producer_consumer import QueueSimulator
from os_modules.orders import OrderProcessor

app = Flask(__name__)
queue_sim = QueueSimulator(capacity=5)
order_processor = OrderProcessor()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/schedule")
def api_schedule():
    data = request.get_json(force=True)
    return jsonify(schedule_processes(data.get("processes", []), data.get("algorithm", "FCFS"),
                                     int(data.get("quantum", 2))))

@app.post("/api/banker")
def api_banker():
    return jsonify(safety_check(request.get_json(force=True)))

@app.post("/api/memory")
def api_memory():
    data = request.get_json(force=True)
    return jsonify(allocate_memory(data.get("blocks", []), data.get("processes", []),
                                   data.get("algorithm", "First Fit")))

@app.post("/api/queue")
def api_queue():
    data = request.get_json(force=True)
    action = data.get("action", "snapshot")
    if action == "produce":
        return jsonify(queue_sim.produce(data.get("order", {})))
    if action == "consume":
        return jsonify(queue_sim.consume())
    if action == "reset":
        queue_sim.reset()
    return jsonify(queue_sim.snapshot())

@app.post("/api/orders")
def api_orders():
    data = request.get_json(force=True)
    return jsonify(order_processor.process(data.get("orders", [])))

if __name__ == "__main__":
    app.run(debug=True)
