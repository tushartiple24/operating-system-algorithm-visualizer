import unittest
from os_modules.scheduler import schedule_processes
from os_modules.banker import safety_check
from os_modules.memory import allocate_memory
from os_modules.producer_consumer import QueueSimulator
from os_modules.orders import OrderProcessor

class ModuleTests(unittest.TestCase):
    def test_scheduler(self):
        r=schedule_processes([{"pid":"A","arrival":0,"burst":5},{"pid":"B","arrival":1,"burst":2}],"FCFS")
        self.assertEqual(r["results"][0]["completion"],5)
        self.assertEqual(r["average_waiting"],2.0)
    def test_banker_safe(self):
        r=safety_check({"available":[3,3,2],"allocation":[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]],
                        "maximum":[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]})
        self.assertTrue(r["safe"])
        self.assertEqual(len(r["safe_sequence"]),5)
    def test_memory_best_fit(self):
        r=allocate_memory([100,500,200],[{"pid":"A","size":180}],"Best Fit")
        self.assertEqual(r["results"][0]["block"],3)
    def test_queue_invariant_and_full(self):
        q=QueueSimulator(1)
        self.assertEqual(q.produce({"id":"a"})["status"],"produced")
        self.assertEqual(q.produce({"id":"b"})["status"],"blocked")
        self.assertTrue(q.consume()["invariant"])
    def test_order_invoice(self):
        r=OrderProcessor().process([{"order_id":"X","quantity":2,"unit_price":10}])
        self.assertEqual(r["orders"][0]["total"],20)
if __name__=="__main__": unittest.main()
