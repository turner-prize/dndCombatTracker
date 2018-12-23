import models


x=models.getNextTurn() #returns models.Combat row
print (x.enemyid)
current = models.referenceEnemyInstance(x)

print (current.name)
print(current.initiative)