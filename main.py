import costEval
import orkGen
import matplotlib.pyplot as plt
import time

print(costEval.cost("test.ork"))

fin = orkGen.orkGet("sample.ork")
print(fin)

for i in range(1,3):
    fin[i][0]=fin[i][0]+0.005
    fin[i][1]=fin[i][1]+0.005

orkGen.orkGen("test.ork", fin)
orkGen.orkGet("test.ork")
