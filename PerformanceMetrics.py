from datetime import datetime, timedelta

# Calculate OEE
def calculateOEE(runTime, plannedProductionTime, idealCycleTime, totalOutput, goodProducts):


    availability = runTime / plannedProductionTime
    performance = (idealCycleTime * totalOutput) / runTime
    quality = goodProducts / totalOutput

    # OEE Calculation
    oee = availability * performance * quality
    return oee

# Calculate Downtime
def calculateDowntime(downtimeEvents):
  
    totalDowntime = sum(event["duration"] for event in downtimeEvents)
    averageDowntime = totalDowntime / len(downtimeEvents)

    return totalDowntime, averageDowntime