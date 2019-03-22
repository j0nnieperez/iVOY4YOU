import ev3dev.ev3 as ev3
from time import sleep
import functions as FN
from random import randint

ColorS      = ev3.ColorSensor()             # Sensor de color
ProxS       = ev3.UltrasonicSensor()        # Sensor Ultrasonico (proximidad)
ProxTS      = ev3.UltrasonicSensor()       # Sensor Ultrasonico de arriba(proximidad)
GyroS       = ev3.GyroSensor()              # Sensor Giroscopio

MotorL      = ev3.LargeMotor('outA')        # Motor izquierdo
MotorR      = ev3.LargeMotor('outD')        # Motor derecho
MotorS      = ev3.MediumMotor('outB')       # Motor del sensor de arriba
MotorG      = ev3.MediumMotor('outC')       # Motor del sensor de arriba
Finish      = False

MadeM = []
MadeCM = []
MadeCMR = []
AllPosibleM = [90,-90,0, 180]
CurrentPosibleM = [90,-90,0]

BaseColors  = ['NoneColor', 'White', 'Brown']
StopColor   = 'Black' ## Deberia ser Black
CurrentAngle = 0

def Stop():
    return MotorL.stop(), MotorR.stop()

FN.LoadMotors(MotorL, MotorR, MotorS, MotorG)
FN.LoadSensors(ColorS, ProxS, ProxTS, GyroS)

MadeM.append(0)
LastMovement = 0
IsReturn = False
LastBackPosition = None
IsFinal = False
LastColor = ''

while not Finish:
    FN.Fix()
    Color = FN.GetColor(ColorS.value())
    print(Color)
    if(not Color in BaseColors): ## Si el color no es invalido
        if(Color == StopColor): ## Si el color es de parada
            Stop()
            FN.ToReturn(), sleep(0.3), Stop()
            LastBackPosition = CurrentAngle
            if(CurrentAngle > 0):
                CurrentAngle -= 180
            else:
                CurrentAngle += 180
            print(CurrentAngle)
            FN.Turn(CurrentAngle)
            FN.Fix()
            IsReturn = True
            sleep(0.3)
        else: ## Si el color es Valido
            LastColor = Color
            sleep(0.4)
            Color = FN.GetColor(ColorS.value())
            print(Color)
            if(Color != LastColor):
                LastColor = Color
                sleep(0.4)
                Color = FN.GetColor(ColorS.value())
                if(Color != LastColor):
                    IsFinal = True
            if(IsReturn): ## Si esta regresando
                IsReturn = False
                CurrentPosibleM = list(filter(lambda x: x != LastBackPosition, CurrentPosibleM))
            else: ## Si llego a una base correcta (no esta regresando) 
                MadeCM.append(LastMovement)
                if(LastMovement == 0): MadeCMR.append( 180 )
                elif(LastMovement == 90): MadeCMR.append( -90 )
                elif(LastMovement == -90): MadeCMR.append( 90 )
                elif(LastMovement == 180): MadeCMR.append( 0 )
                print("Movimientos correctos: "+str(MadeCM))
                print("Movimientos correctos (reversa): "+str(MadeCMR))
                CurrentPosibleM = AllPosibleM
                if(CurrentAngle == 90): CurrentPosibleM = [90,0,180]
                elif(CurrentAngle == -90): CurrentPosibleM = [-90,180,0]
                elif(CurrentAngle == 180): CurrentPosibleM = [180,-90,90]
                elif(CurrentAngle == 0): CurrentPosibleM = [0,-90,90]
            print("Movimientos posibles: "+str(CurrentPosibleM))
            sleep(0.4)
            Movement = CurrentPosibleM[randint(0, (len(CurrentPosibleM)-1) )]
            LastMovement = Movement 
            print(Movement) 
            CurrentAngle = Movement
            FN.Turn(CurrentAngle)
            FN.Fix()
            sleep(1.2)
    sleep(0.4)
    