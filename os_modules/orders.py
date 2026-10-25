"""Illustrative order validation; does not contact payment or delivery providers."""
class OrderProcessor:
    def process(self, orders):
        output=[]
        for i,o in enumerate(orders):
            oid=str(o.get("order_id",f"ORD-{i+1}"))
            try: qty=int(o.get("quantity",1)); price=float(o.get("unit_price",0))
            except (TypeError,ValueError):
                output.append({"order_id":oid,"status":"rejected","reason":"Invalid quantity or unit price"}); continue
            if qty<=0 or price<0:
                output.append({"order_id":oid,"status":"rejected","reason":"Quantity must be positive and price non-negative"}); continue
            total=round(qty*price,2)
            output.append({"order_id":oid,"quantity":qty,"unit_price":price,"total":total,
                           "payment_status":"SIMULATED - not charged","inventory_status":"SIMULATED - not connected",
                           "invoice_id":f"INV-{oid}","delivery_status":"Pending (simulation)","status":"validated"})
        return {"orders":output,"count":len(output),"note":"Demonstration only: no real payment, inventory mutation, or delivery booking occurs."}
