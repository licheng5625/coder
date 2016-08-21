dd=[]
for i in range(32421):
    dd.append(i)

print(int(len(dd)/10))
for i in range(0,len(dd),3242):

    selectindex=dd[i:i+3242]
    print(selectindex)