import itertools

class Data:
    def __init__(self):
        self.name = ''
        self.temperatureL = []
        self.humidityL = []
    
    def dataInfo(self, name, temperature, humidity):
        self.name = name
        self.temperatureL.append(temperature)
        self.humidityL.append(humidity)

data1 = Data()
data1.dataInfo('WY', 26, 73)

print('name =', data1.name)
print('temperatureL =', data1.temperatureL)
print('humidityL =', data1.humidityL)
print('\n')

data1.dataInfo('WY', 24, 64)

print('name =', data1.name)
print('temperatureL =', data1.temperatureL)
print('humidityL =', data1.humidityL)


    