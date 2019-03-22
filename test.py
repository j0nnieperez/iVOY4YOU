import ev3dev.ev3 as ev3
from time import sleep

ColorS      = ev3.ColorSensor()             # Sensor de color
ProximityS  = ev3.UltrasonicSensor()        # Sensor Ultrasonico (proximidad)
GiroS       = ev3.GyroSensor()              # Sensor Giroscopio
MotorL      = ev3.LargeMotor('outA')        # Motor izquierdo
MotorR      = ev3.LargeMotor('outD')        # Motor derecho
MotorSonico = ev3.MediumMotor('outB')       # Motor del sensor de arriba

for i in range(150):
        print(GiroS.value())
        sleep(0.5)