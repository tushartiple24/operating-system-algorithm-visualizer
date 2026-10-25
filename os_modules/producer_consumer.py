"""Thread-safe bounded queue primitives and a deterministic teaching simulator."""
from collections import deque
from threading import Lock

class QueueSimulator:
    def __init__(self, capacity=5):
        if capacity < 1: raise ValueError("Capacity must be positive.")
        self.capacity=capacity; self.items=deque(); self.lock=Lock(); self.produced=0; self.consumed=0
    def produce(self, order):
        with self.lock:
            if len(self.items)>=self.capacity:
                return {"status":"blocked","message":"Queue full: producer must wait.","queue":list(self.items),
                        "produced":self.produced,"consumed":self.consumed,"capacity":self.capacity}
            item=dict(order)
            if not item: item={"order_id":f"ORD-{self.produced+1}","status":"submitted"}
            self.items.append(item); self.produced+=1
            return self.snapshot_unlocked("produced")
    def consume(self):
        with self.lock:
            if not self.items:
                return {"status":"blocked","message":"Queue empty: consumer must wait.","queue":[],
                        "produced":self.produced,"consumed":self.consumed,"capacity":self.capacity}
            item=self.items.popleft(); self.consumed+=1
            result=self.snapshot_unlocked("consumed"); result["item"]=item; return result
    def snapshot_unlocked(self,status="ok"):
        return {"status":status,"queue":list(self.items),"produced":self.produced,"consumed":self.consumed,
                "capacity":self.capacity,"invariant":self.produced-self.consumed==len(self.items)}
    def snapshot(self):
        with self.lock: return self.snapshot_unlocked()
    def reset(self):
        with self.lock: self.items.clear(); self.produced=0; self.consumed=0
