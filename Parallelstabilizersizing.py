from tkinter import *
from tkinter import messagebox
import webbrowser
from PIL import ImageTk, Image
from tkhtmlview import HTMLLabel


#Variabili
E12= [0.10,0.12,0.15,0.18,0.22,0.27,0.33,0.39,0.47,0.56,0.68,0.82,
      1.0,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2,
      10,12,15,18,22,27,33,39,47,56,68,82,100,120,150,
     180,220,270,330,390,470,560,680,820,1000,1200,1500,
     1800,2200,2700,3300,3900,4700,5600,6800,8200]

diodizener={3.3: '1N5333B', 3.6: '1N5334B',3.9: '1N5335B', 4.3: '1N5336B',4.7: '1N5337B', 5.1: '1N5338B',5.6: '1N5339B', 6.0: '1N5340B',6.2: '1N5341B',
            6.8: '1N5342B',7.5: '1N5343B', 8.2: '1N5344B',8.7: '1N5345B', 9.1: '1N5346B',10: '1N5347B', 11:'1N5348B', 12:'1N5349B', 13:'1N5350B', 
            14:'1N5351B', 15:'1N5352B', 16:'1N5353B', 17:'1N5354B', 18:'1N5355B', 19:'1N5356B', 20:'1N5357B', 22:'1N5358B', 24:'1N5359B', 25:'1N5360B',
            27:'1N5361B', 28:'1N5362B', 30:'1N5363B', 33:'1N5364B', 36:'1N5365B', 39:'1N5366B', 43:'1N5367B', 47:'1N5368B', 51:'1N5369B', 56:'1N5370B',
            60:'1N5371B', 62:'1N5372B', 68:'1N5373B', 75:'1N5374B', 82:'1N5375B', 91:'1N5377B', 100:'1N5378B', 120:'1N5380B', 130:'1N5381B', 150:'1N5383B',
            160:'1N5384B', 180:'1N5386B', 190:'1N5387B', 200:'1N5388B' }
Seriepot=[0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5,10, 15, 25, 30, 50,75,100, 150, 300, 250, 500, 1000]

#Funzioni
def callback(url):
    webbrowser.open_new(url)

def arrotondamento(x):
        x=round(x,1)
        if x<0.1:
                x=float(0.1)
                return x
        else:
                var1=E12.count(x)
                while var1 !=1:
                    x=round((x+0.1),1)
                    var1=E12.count(x)
                return float(x)

def arr_diff(x):
    if x<0.1:
        x=0.1
        return x
    else:
        x=round(x,1)
        var2=E12.count(x)
        while var2 !=1:
            x=round((x-0.1),1)
            var2=E12.count(x)
        return float(x)

def arrvz(x):
    x=round(x,1)
    f=False
    while f == False:
        f= x in diodizener
        x=round((x+0.1),1)
    x=round(x-0.1,1)
    return x
        
def roundpot(x):
        if x>1000:
                errorpotenze()
                return
        else:
            P=float(x*1.3)
            P=round(P,2)
            var3=Seriepot.count(P)
            while var3 !=1:
                P=round((P+0.01),2)
                var3=Seriepot.count(P)
            return float(P)

#Errori
def errorinputs():
       messagebox.showerror('Error', 'Error: You have to fill the inputs with numerc inputs!')
def errorpotenze():
       messagebox.showerror('Error', 'Error: Powers too high!')       
def errorV():
       messagebox.showerror('Error', 'Error: Input voltage must be greater than the output voltage!')
def errorD():
       messagebox.showerror('Error', 'Error: There are no diodes for this voltage!')


#Programma
def output():
    try:
               
                Vin=float(wtensioneiniziale.get())
                Vz=float(wtensioneuscita.get())
                if Vin<=Vz:
                    errorV()
                elif Vz>200:
                    errorD()    
                Tolleranza=float(wtolleranza.get())
                Tambiente=float(wtambiente.get())
                Iz=float(wcorrenteuscita.get())
                Vmin=float(Vin*(1-Tolleranza/100))
                Vmax=float(Vin*(1+Tolleranza/100))
                Vz=arrvz(Vz)
                Iz1=float(Iz*0.001)
                Rz=float((Vin-(Vin*Tolleranza/100)-Vz)/(Iz1+0.02))
                R=float(arrotondamento(Rz))
                PR=roundpot((Iz1+0.02)*(Iz1+0.02)*R)
                Rl=float(Vz/Iz1)
                Rl=arr_diff(Rl)
                PRl=roundpot(Rl*Iz1*Iz1)
                x=((Vmax/R-Iz1)*0.2637+Vz)
                y=(Vmin/R-Iz1)
                z=x-y
                PSRR=round(((z*0.2637+Vz)/(Vz*100))*100,2)
                Iz=((Vin-Vz)/R)-0.02
                TL=int((25*Vz*Iz)+Tambiente)
                Diodo=str(diodizener[Vz])
                Resistenzacarico= 'Load resistence: ' + str(Rl)+' Ω   ±5%  '+ str(PRl)+'W   100ppm  250/400V '
                Resistenza= 'Resistence: ' + str(R)+' Ω   ±5%  '+ str(PR) +'W   100ppm  250/400V '
                sx=60
                sy=410
                oDiodo=Label(win, text= "Diode:   " + Diodo+ ' ('+str(Vz)+'V), Lead Temperature='+str(TL))
                oDiodo.place(x=sx, y=sy)
                oRl=Label(win, text=Resistenzacarico)
                oRl.place(x=sx, y=sy+40)
                oR=Label(win, text=Resistenza)
                oR.place(x=sx, y=sy+80)
                oPSRR=Label(win, text='PSRR esteemed:  '+str(PSRR))
                oPSRR.place(x=sx, y=sy+120)
    except ValueError:
        errorinputs()

#Help window
def help():
    Whelp=Tk()
    Whelp.title('Help')
    Whelp.iconbitmap(r'favicon.ico')
    Whelp.resizable(width=False, height=False)
    Whelp.geometry('800x440')
    text=HTMLLabel(Whelp, html="""
        <p><strong>HELP</strong></p>
        <p>This is a
        program written by two Kennedy guys to size the components useful for the
        realization of a power supply in parallel with the use of a Zener diode.</p>
        <p><strong> Input values:</strong></p>
        <p>
            <strong><em>input voltage: </em></strong>
        </p>
        <p>Here the
        nominal input voltage of the circuit must be entered, it cannot be less than
        the output voltage.</p>
        <p>
            <strong><em> tolerance:</em></strong>
        </p>
        <p>Here the
        tolerance of the input voltage must be entered, usually 20%, higher values
        &#8203;&#8203;are not recommended as they lead to inaccurate results.</p>
        <p>
            <strong><em> working temperature:</em></strong>
        </p>
        <p>Is the
        temperature to which the circuit will be exposed.</p>
        <p>
            <strong><em> output voltage:</em></strong>
        </p>
        <p>Is the
        desired voltage on the load, it will be rounded as not all the diodes are
        present.</p>
        <p>
            <strong><em> output current:</em></strong>
        </p>
        <p>Is the
        desired current on the load, it will also be rounded.</p>
        <p></p>
        <p><strong> You have to hit calculate to perform the
        calculations, remember to hit calculate every time you update the inputs!</strong></p>
        <p><strong> NOTES:</strong></p>
        <p><strong> The resistors have been chosen from the E12
        decade, all components can be found on the Mouser website, very high powers
        could be found for high input voltages.</strong></p>
        <p><strong> For any suggestions, problems, contact us:
        marcovitalibiscontin@gmail.com</strong></p>
        <p></p>
            """)
    text.pack(pady=20, padx=20)  

#Finestra
spx=160
win = Tk()
win.title('Parallel stabilizer sizing')
win.iconbitmap(r'favicon.ico')
win.resizable(width=False, height=False)
win.geometry('380x620')
wTensioneiniziale=Label(win, text='Input voltage')
wUMTI=Label(win, text='[V]')
wUMTI.place(x=spx+100, y=30)
wTensioneiniziale.place(x=20, y=30)
wtensioneiniziale=Entry(win, width=15, bd=3)
wtensioneiniziale.place(x=spx, y=30)
wTolleranza=Label(win, text='Voltage tolerance')
wTolleranza.place(x=20, y=70)
wUMT=Label(win, text='[%]')
wUMT.place(x=spx+100, y=70)
wtolleranza=Entry(win, width=15, bd=3)
wtolleranza.place(x=spx, y=70)
wTambiente=Label(win, text='Working temperature ')
wTambiente.place(x=20, y=110)
wUMTa=Label(win, text='[°C]')
wUMTa.place(x=spx+100, y=110)
wtambiente=Entry(win, width=15, bd=3)
wtambiente.place(x=spx, y=110)
wTensioneuscita=Label(win, text='Output voltage')
wTensioneuscita.place(x=20, y=150)
wUMTU=Label(win, text='[V]')
wUMTU.place(x=spx+100, y=150)
wtensioneuscita=Entry(win, width=15, bd=3)
wtensioneuscita.place(x=spx, y=150) 
wCorrenteuscita=Label(win, text='Output current [mA]')
wCorrenteuscita.place(x=20, y=190)
wUMCU=Label(win, text='[mA]')
wUMCU.place(x=spx+100, y=190)
wcorrenteuscita=Entry(win, width=15, bd=3)
wcorrenteuscita.place(x=spx, y=190)
btn=Button(win, text="Calculate", command=output)
btn.place(x=spx+20,y=330)
help=Button(win, text="Help", fg="blue", borderwidth=0, command=help)
#help = Label(win, text="Help", fg="blue", cursor="hand2", help)
#help.bind("<Button-1>", lambda e: callback("http://www.mouser.it"))
help.place(x=spx*2,y=10)

#image
frame = Frame(win, width=100, height=200)
frame.pack()
frame.place(x=spx-45, y=230)
img= Image.open("Zener finale.jpg")
img = img.resize((180, 90), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)
label = Label(frame, image = img)
label.pack()
#link
link1 = Label(win, text="Mouser Link", fg="blue", cursor="hand2")
link1.bind("<Button-1>", lambda e: callback("http://www.mouser.it"))
link1.place(x=spx+110, y=570)
win.mainloop()