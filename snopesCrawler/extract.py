# -*- coding: UTF-8 -*-
import json
from tkinter import *

listelement=0
datasjon=list()

def processnext():
    global listelement
    global textaera
    if listelement<len(datasjon)-1:
        listelement=listelement+1
        textaera.delete('1.0', END)

        textaera.insert(END,datasjon[listelement]['Claim'])
        print (datasjon[listelement]['Claim'] )

def processlast():
    global listelement
    if listelement>0:
        listelement=listelement-1
        textaera.delete('1.0', END)
        textaera.insert(END,datasjon[listelement]['Claim'])

        print (datasjon[listelement]['Claim'] )


with open( 'jounral.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        datajson2=json.loads(line)
        if datajson2['Label'] =='FACT CHECK':
            datasjon.append(datajson2)
thisjson=datasjon[listelement]

window = Tk()

# 将按钮置在窗口上
frame1 = Frame(window)        # 创建一个框架
frame1.pack()                 # 将框架frame1放置在window中
btOk = Button(frame1,text = "next", fg = "red", command = processnext)
btCancel = Button(frame1,text = "last", bg = "yellow", command = processlast)
btOk.grid(row=1,column=6)
btCancel.grid(row=1,column=0)
textaera=Text(window, height=20, width=90)
textaera.pack()
fearture='Claim'
setofrumors=set()
window.mainloop()



