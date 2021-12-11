import ConcretePy as rc
 
shape = rc.Shape(width =50, depth =80)
material = rc.Material(fc=280,fy=4200)
force = rc.Force(moment=106.8*1000*100)
rebar = rc.ReinforcementData(cover_top =5,cover_bot=5)
inp =  rc.InputData(shape,force,material,rebar)

out = rc.rectangleRCdesign(inp)
print(out)