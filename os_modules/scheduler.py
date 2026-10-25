"""CPU scheduling algorithms for illustrative order-processing tasks."""
def schedule_processes(processes, algorithm="FCFS", quantum=2):
    ps=[]
    for i,p in enumerate(processes):
        try:
            pid=str(p.get("pid", f"P{i+1}"))
            at=int(p.get("arrival",0)); bt=int(p.get("burst",1)); pr=int(p.get("priority",1))
        except (TypeError, ValueError):
            return {"error":"Arrival, burst and priority must be integers."}
        if at < 0 or bt <= 0:
            return {"error":"Arrival must be >= 0 and burst must be > 0."}
        ps.append({"pid":pid,"arrival":at,"burst":bt,"priority":pr,"remaining":bt})
    if not ps: return {"error":"Provide at least one process."}
    alg=algorithm.upper()
    if alg not in {"FCFS","SJF","PRIORITY","ROUND ROBIN"}:
        return {"error":"Algorithm must be FCFS, SJF, Priority or Round Robin."}
    if alg=="ROUND ROBIN" and quantum<=0: return {"error":"Quantum must be > 0."}
    time=0; done=set(); gantt=[]; first_start={}; completion={}
    if alg=="ROUND ROBIN":
        pending=sorted(ps,key=lambda x:(x["arrival"],x["pid"])); ready=[]; idx=0
        while len(done)<len(ps):
            if not ready and idx<len(pending) and time<pending[idx]["arrival"]: time=pending[idx]["arrival"]
            while idx<len(pending) and pending[idx]["arrival"]<=time:
                ready.append(pending[idx]); idx+=1
            if not ready: continue
            p=ready.pop(0); first_start.setdefault(p["pid"],time)
            run=min(quantum,p["remaining"]); start=time; time+=run; p["remaining"]-=run
            gantt.append({"pid":p["pid"],"start":start,"end":time})
            while idx<len(pending) and pending[idx]["arrival"]<=time:
                ready.append(pending[idx]); idx+=1
            if p["remaining"]>0: ready.append(p)
            else: done.add(p["pid"]); completion[p["pid"]]=time
    else:
        while len(done)<len(ps):
            ready=[p for p in ps if p["pid"] not in done and p["arrival"]<=time]
            if not ready:
                time=min(p["arrival"] for p in ps if p["pid"] not in done)
                ready=[p for p in ps if p["pid"] not in done and p["arrival"]<=time]
            if alg=="FCFS": p=min(ready,key=lambda x:(x["arrival"],x["pid"]))
            elif alg=="SJF": p=min(ready,key=lambda x:(x["burst"],x["arrival"],x["pid"]))
            else: p=min(ready,key=lambda x:(x["priority"],x["arrival"],x["pid"]))
            first_start[p["pid"]]=time; start=time; time+=p["burst"]
            gantt.append({"pid":p["pid"],"start":start,"end":time}); completion[p["pid"]]=time; done.add(p["pid"])
    rows=[]
    for p in ps:
        ct=completion[p["pid"]]; tat=ct-p["arrival"]; wt=tat-p["burst"]
        rows.append({"pid":p["pid"],"arrival":p["arrival"],"burst":p["burst"],"priority":p["priority"],
                     "completion":ct,"turnaround":tat,"waiting":wt,"response":first_start[p["pid"]]-p["arrival"]})
    return {"algorithm":algorithm,"gantt":gantt,"results":rows,
            "average_waiting":round(sum(x["waiting"] for x in rows)/len(rows),2),
            "average_turnaround":round(sum(x["turnaround"] for x in rows)/len(rows),2)}
