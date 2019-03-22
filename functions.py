from time import sleep

MotorL = None
MotorR = None
MotorS = None
MotorG = None

CurrentAngle = 0
Advance = False

ColorSensor     = None
ProximitySensor = None
ProximityTopSensor = None
GyroSensor      = None

def LoadMotors(ML, MR, MS, MG):
    global MotorL
    global MotorR
    global MotorS
    global MotorG
    MotorL = ML
    MotorR = MR
    MotorS = MS
    MotorG = MG

def LoadSensors(CS, PS, PTS, GS):
    global ColorSensor     
    global ProximitySensor 
    global GyroSensor      
    ColorSensor         = CS
    ProximitySensor     = PS
    ProximityTopSensor  = PTS
    GyroSensor          = GS
    ColorSensor.color
    GyroSensor.mode     = 'GYRO-CAL'
    GyroSensor.value()
    GyroSensor.mode     = 'GYRO-ANG'

def Advance():
    #global GyroSensor
    MotorR.run_forever(speed_sp=300)
    MotorL.run_forever(speed_sp=300)
    #while True:
    #    print("Angulo: "+str(GyroSensor.value()))

def Fix():
    CA = GyroSensor.value()
    TA = CurrentAngle
    print(" "+str(CA) + " - " + str(TA))
    if(TA > CA):
        MotorR.run_forever(speed_sp=-100)
        MotorL.run_forever(speed_sp=100)
        while TA > CA:
            CA = GyroSensor.value()
    elif(TA < CA):
        MotorR.run_forever(speed_sp=100)
        MotorL.run_forever(speed_sp=-100)
    else: 
        pass
    Advance()

def ToReturn():
    MotorR.run_forever(speed_sp=-500)
    MotorL.run_forever(speed_sp=-500)

def TurnR():
    global CurrentAngle
    CA = GyroSensor.value()
    TA = CurrentAngle+90
    MotorR.run_forever(speed_sp=-100)
    MotorL.run_forever(speed_sp=100)
    #print("Current Angle: "+str(CA))
    #print("Target Angle: "+str(TA))
    while CA < TA:
        CA = GyroSensor.value()
        if((TA-CA) <= 15):
            MotorR.run_forever(speed_sp=-30)
            MotorL.run_forever(speed_sp=30)
    MotorL.stop(), MotorR.stop()
    CurrentAngle = TA
    #print(GyroSensor.value())

def TurnL():
    global CurrentAngle
    CA = GyroSensor.value()
    TA = CurrentAngle-90
    MotorR.run_forever(speed_sp=100)
    MotorL.run_forever(speed_sp=-100)
    #print("Current Angle: "+str(CA))
    #print("Target Angle: "+str(TA))
    while CA > TA:
        CA = GyroSensor.value()
        if((CA-TA) <= 15):
            MotorR.run_forever(speed_sp=30)
            MotorL.run_forever(speed_sp=-30)
        #print("Angle: "+str(Angle))
    MotorL.stop(), MotorR.stop()
    CurrentAngle = TA
    #print(GyroSensor.value())

def Turn(Deg):
    global CurrentAngle
    CA = GyroSensor.value()
    TA = Deg
    if(TA > CA):
        MotorR.run_forever(speed_sp=-100)
        MotorL.run_forever(speed_sp=100)
        while CA < TA:
            CA = GyroSensor.value()
            if((TA-CA) <= 15):
                MotorR.run_forever(speed_sp=-30)
                MotorL.run_forever(speed_sp=30)
    else:
        MotorR.run_forever(speed_sp=100)
        MotorL.run_forever(speed_sp=-100)
        while CA > TA:
            CA = GyroSensor.value()
            if((CA-TA) <= 15):
                MotorR.run_forever(speed_sp=30)
                MotorL.run_forever(speed_sp=-30)
    
        #print("Angle: "+str(Angle))
    MotorL.stop(), MotorR.stop()
    CurrentAngle = TA

def Stop():
    MotorR.run_timed(time_sp=220, speed_sp=-500)
    MotorL.run_timed(time_sp=220, speed_sp=500)

def MoveLTopProxiS():
    MotorS.run_timed(time_sp=220, speed_sp=500)

def MoveRTopProxiS():
    MotorS.run_timed(time_sp=220, speed_sp=-500)

def GetColor(ColorValue):
    colors = {
        "0":"NoneColor",
        "1":"Black",
        "2":"Blue",
        "3":"Green",
        "4":"Yellow",
        "5":"Red",
        "6":"White",
        "7":"Brown",
    }
    return colors[str(ColorValue)]

def Take():
    MotorG.run_forever(speed_sp=-50), sleep(3), MotorG.stop() ## Abrir
    Advance = True
    Prox = 0
    MotorR.run_forever(speed_sp=50), MotorL.run_forever(speed_sp=50) ## Avanzar
    FistConfirm = False
    SecondConfirm = False
    ThirdConfirm = False
    while Advance:
        Prox = ProximitySensor.value()
        print(Prox)
        if(Prox <= 90):
            FistConfirm = True
        if(Prox <= 70):
            SecondConfirm = True
        if(Prox <= 60):
            ThirdConfirm = True
        Advance = not (FistConfirm and SecondConfirm and ThirdConfirm)
    sleep(1)
    MotorR.stop()
    MotorL.stop()
    MotorG.run_forever(speed_sp=50), sleep(3.5), MotorG.stop() ## Cerrar
    MotorR.run_forever(speed_sp=100)
    MotorL.run_forever(speed_sp=100)
    sleep(3)
    MotorR.stop()
    MotorL.stop()

def Let():
    MotorG.run_forever(speed_sp=-50), sleep(3), MotorG.stop() ## Abrir
    MotorR.run_forever(speed_sp=-100)
    MotorL.run_forever(speed_sp=-100)
    sleep(3)
    MotorR.stop()
    MotorL.stop()
    MotorG.run_forever(speed_sp=50), sleep(3.5), MotorG.stop() ## Cerrar
