# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
class Tesuto:
    baseatk = 600
    basedef = 500
    dr = 30

    maxatk = 2101
    maxdef = 1401
    maxdr= 51

    damages = []
    reductions = []
    defenses = []

    @staticmethod
    def fight(a, d, r, enchant):
        db = 0
        a = a + 477
        atkbonus = 1 + .08 + .15 + .2
        if enchant == "rs":
            atkbonus = atkbonus + .1
        else:
            db = .1
        a = a * atkbonus + 60
        d = d*0.8
        r = r*0.01
        r = db + .55 - r
        diff = (a - d)
        return (diff + (diff*r)) * 10

    def calculate(*args):
        bdef = Tesuto.basedef
        bdr = Tesuto.dr
        outperform = False
        for bdef in range(bdef, Tesuto.maxdef, 100):

            rsdamage = Tesuto.fight(Tesuto.baseatk, bdef, bdr, "rs")
            bdamage = Tesuto.fight(Tesuto.baseatk, bdef, bdr, "b")
                #if (bdamage > rsdamage) & (bdr != 100):
                 #   outperform = True
            Tesuto.damages.append("RS Damage: " + str(rsdamage) + " Breeze Damage: " + str(bdamage))
            Tesuto.defenses.append(bdef)
            Tesuto.reductions.append(bdr)

                #print("Def: ", str(bdef), "DR: ", str(bdr), "%")
                #print("Breeze: ", str(bdamage), " Rough Sea: ", str(rsdamage))
            if bdr == Tesuto.maxdr-1:
                bdr = Tesuto.dr




#root=Tk()
#root.title=("Chess")

'''
framey = ttk.Frame(root,padding="3 3 12 12")
defense = ttk.Entry(framey,width)
framey.grid()
root.mainloop()
'''

#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
 #   print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

. 
# Press the green button in the gutter to run the script.
Tesuto.calculate()
while Tesuto.defenses:
    print(str(Tesuto.damages.pop()), " Defense: ", str(Tesuto.defenses.pop()), " DR: ",
          str(Tesuto.reductions.pop()))
    print()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
