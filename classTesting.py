from enemies import Enemy

#name,size,type,alignment,AC,hp,speed,STR,DEX,CON,INT,WIS,CHA
#self,name,type,attackBonus,reach,targetMax,damage,damageType):


weapons =   [{'name':'Scimitar','type':'Melee','attackBonus':'+4','range':'5 ft.','targetMax':1,'damage':'1d6+2','damageType':'slashing'},
             {'name':'Shortbow','type':'Ranged','attackBonus':'+4','range':'80/320 ft.','targetMax':1,'damage':'1d6+2','damageType':'peircing'}]

Goblin1=Enemy('goblin1','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=weapons)
Goblin2=Enemy('goblin2','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=weapons)


Goblin1.Attack(Goblin1.weapons[0],Goblin2)