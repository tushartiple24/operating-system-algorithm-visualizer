"""Contiguous variable-sized memory allocation: First/Best/Worst Fit."""
def allocate_memory(blocks, processes, algorithm="First Fit"):
    try:
        free=[int(x) for x in blocks]
        req=[{"pid":str(p.get("pid",f"P{i+1}")),"size":int(p["size"])} for i,p in enumerate(processes)]
    except (TypeError,ValueError,KeyError):
        return {"error":"Blocks and process sizes must be integers."}
    if not free or any(x<0 for x in free): return {"error":"Provide non-negative memory blocks."}
    if any(p["size"]<=0 for p in req): return {"error":"Process sizes must be positive."}
    alg=algorithm.lower()
    if alg not in {"first fit","best fit","worst fit"}: return {"error":"Use First Fit, Best Fit or Worst Fit."}
    initial=free[:]; rows=[]
    for p in req:
        choices=[i for i,b in enumerate(free) if b>=p["size"]]
        idx=None
        if choices:
            if alg=="first fit": idx=choices[0]
            elif alg=="best fit": idx=min(choices,key=lambda i:free[i])
            else: idx=max(choices,key=lambda i:free[i])
        if idx is None: rows.append({"pid":p["pid"],"size":p["size"],"block":None,"status":"Not allocated"})
        else:
            before=free[idx]; free[idx]-=p["size"]
            rows.append({"pid":p["pid"],"size":p["size"],"block":idx+1,"block_before":before,
                         "remaining_in_block":free[idx],"status":"Allocated"})
    return {"algorithm":algorithm,"initial_blocks":initial,"results":rows,"remaining_blocks":free,
            "total_free":sum(free),"allocated_count":sum(r["status"]=="Allocated" for r in rows)}
