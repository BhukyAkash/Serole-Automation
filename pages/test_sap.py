import SAP.test_motor as motor

def test_motor(page):
    # ------- MotorCycle - MC ------
    try:
        motor.test_mc(page)
    except Exception as e:
        print("Test Failed: ", e)

    # ----- Private Motor Car - PMC --------
    try:
        motor.test_pc(page)
    except Exception as e:
            print("Test Failed: ", e)