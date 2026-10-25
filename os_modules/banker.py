"""Banker's safety algorithm. Resource vectors are integer lists."""
def safety_check(data):
    try:
        available=[int(x) for x in data["available"]]
        allocation=[[int(x) for x in row] for row in data["allocation"]]
        maximum=[[int(x) for x in row] for row in data["maximum"]]
    except (KeyError,TypeError,ValueError):
        return {"error":"Provide available, allocation and maximum integer vectors/matrices."}
    n=len(allocation)
    if n==0 or len(maximum)!=n: return {"error":"Allocation and maximum must have the same non-zero row count."}
    m=len(available)
    if any(len(r)!=m for r in allocation+maximum): return {"error":"Every resource row must match available-vector length."}
    if any(x<0 for x in available) or any(x<0 for row in allocation+maximum for x in row):
        return {"error":"Resource values cannot be negative."}
    if any(allocation[i][j]>maximum[i][j] for i in range(n) for j in range(m)):
        return {"error":"Allocation cannot exceed maximum claim."}
    need=[[maximum[i][j]-allocation[i][j] for j in range(m)] for i in range(n)]
    work=available[:]; finish=[False]*n; sequence=[]; steps=[]
    while True:
        found=False
        for i in range(n):
            if not finish[i] and all(need[i][j]<=work[j] for j in range(m)):
                before=work[:]; work=[work[j]+allocation[i][j] for j in range(m)]
                finish[i]=True; sequence.append(f"P{i+1}")
                steps.append({"process":f"P{i+1}","need":need[i],"work_before":before,"work_after":work[:]})
                found=True; break
        if not found: break
    return {"safe":all(finish),"state":"SAFE" if all(finish) else "UNSAFE",
            "safe_sequence":sequence if all(finish) else [],
            "need":need,"steps":steps,"available":available,
            "message":"A safe completion order exists." if all(finish) else "No complete safe sequence exists."}
