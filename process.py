import json as js 

filename = "./subwaySH.json"
file1 = "node.txt"
file2 = "edge.txt"

with open(filename,"r",encoding="utf-8") as f:
    with open(file1,"w") as file1:
        d = js.load(f)
        data = d["l"]
        i = 1
        for lineData in data:
            stationData = lineData["st"]
            for station in stationData:
                name = station["n"]
                temp = station["sl"]
                x = temp.split(",")[0]
                y = temp.split(",")[1]
                file1.write(f"{name} {x} {y} {i}\n")
            i+=1
with open(filename,"r",encoding="utf-8") as f:
    with open(file2,"w") as file2:
        d = js.load(f)
        data = d["l"]
        i = 1 
        for i in range(len(data)):
            lineData = data[i]
            stationData = lineData["st"]
            prev = stationData[0]["n"]
            cur = ""
            for station in stationData:
                if station["n"]== stationData[0]["n"]:
                    continue
                cur = station["n"]
                file2.write(f"{prev} {cur}\n")
                prev = cur 