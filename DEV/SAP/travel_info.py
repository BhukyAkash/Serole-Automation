OTG = "On-Time Guarantee"
CFAR = "Cancellation for any Reason (CFAR)"

# pytest -s sap\test_travel.py

air_aisa = {

    "BP"    : "1000025327",
    "CC"    : "2210000540",       # 2210001238
    "travel" : {
        "masterPolicy"  : "4010000196",   
        "policy_title"  : "Flight Delay Insurance",
        "pm_id"         : "TRPLAA000000",
        "coverage"      : [OTG, CFAR],
        "si"            : "45000"
    }
}