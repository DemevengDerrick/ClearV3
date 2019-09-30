#import tkinter libary
from tkinter import *
from tkinter.filedialog import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.mlab as ml
#create windows
window=Tk()
window.title("Clear v2.0")
window.iconbitmap('image\logo_Clear_Survey.ico')
#window.configure(background="white")


def plot():
    Station=appCode.get()
    CodeStation=station.get()
    CodeReference=reference.get()
    CodeMesur=mesure.get()
    output.delete(0.0,END)        
    doc=fileName.get()

    try:
        doc=open(doc)
        if  Station=="":
            Station="1"
        if  CodeStation=="":
            CodeStation="1"
        if  CodeReference=="":
            CodeReference="3"
        if  CodeMesur=="":
            CodeMesur="4"          
    except:
        output.insert(END,"The file directory could not be found. Enter a valid directory.")
    
    x=[]
    y=[]
    z=[]
    Z=[]
    for line in doc:
        if line.startswith("DATABASE"):
            break
    j=1  
    for line in doc:
       #delete undesired lines 
       if not line.startswith(("	POINTS(")):
           if line.startswith(("		THEMINFO")):
               break

           else:
               line=line.strip()
               line=line.strip(" ")
               liste=line.split()
#               print(liste)
               i=0
               for lis in liste:
                   liste[i]=lis.strip(", ")
                   i+=1
#                   print(liste)
               del liste[5:9]
               del liste[0:1]
               print(liste[1],liste[2])
               if (liste[1] =='')| (liste[2] ==''):
                   pass
               else:
                   
               
                   x.append(float(liste[1]))
                   y.append(float(liste[2]))
                   Z.append(float(liste[3]))
                   z.append(liste[0])
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    Zi = ml.griddata(x, y, Z, xi, yi, interp='linear')            
    fig=plt.figure()
    sub1 = fig.add_subplot(221)
    sub2 = fig.add_subplot(222, projection='3d')
    sub3 = fig.add_subplot(223)
    sub4 = fig.add_subplot(224)
    sub1.scatter(x,y,marker='o', color='red')
    sub2.plot_trisurf(x, y, Z, color='white', edgecolors='green', alpha=0.5)
    b=sub3.contour(xi, yi, Zi, 15, linewidths=0.5, colors='k')
    sub4.contour(xi, yi, Zi, 15, linewidths = 0.5, colors = 'k')
    a=sub4.pcolormesh(xi, yi, Zi, cmap = plt.get_cmap('rainbow'))
    plt.colorbar(a,ax=sub4)
    
  
    plt.clabel(b, fontsize=10, inline=1,fmt = '%1.0f',ticks=10)
    sub4.set_title("Colored Contours")
    sub4.set_ylabel("Nord (m)")
    sub4.set_xlabel("East (m)")
    sub1.set_title("2D Preview")
    sub3.set_title("Contours")
    sub3.set_ylabel("Nord (m)")
    sub3.set_xlabel("East (m)")
    sub1.set_title("2D Preview")
    sub2.set_title("MNT preview")
    sub1.set_xlabel("East (m)")
    sub1.set_ylabel("Nord (m)")
    sub2.set_xlabel("East (m)")
    sub2.set_ylabel("Nord (m)")
    sub2.set_zlabel("Height (m)")
    for i, txt in enumerate(z):
        sub1.annotate(txt.strip('\"'),(x[i],y[i]))
    plt.show()
#                   print(liste)

               
               

    
#photo
#photo1=PhotoImage(file="good.PNG")
#Label(window, image=photo1).grid(row=0,column=2, sticky=W)

#command functions


def process(): 
    Station=appCode.get()
    CodeStation=station.get()
    CodeReference=reference.get()
    CodeMesur=mesure.get()
    output.delete(0.0,END)
    #output.insert(END,appcode)
            
    doc=fileName.get()

    try:
        doc=open(doc)
        if  Station=="":
            Station="1"
        if  CodeStation=="":
            CodeStation="1"
        if  CodeReference=="":
            CodeReference="3"
        if  CodeMesur=="":
            CodeMesur="4"          
    except:
        output.insert(END,"The file directory could not be found. Enter a valid directory.")
      
           
    doc2=open("Temp_result.txt","w")
    
    if int(Station)==1:
                    
        for line in doc:
            if line.startswith("		1,	"):
                break
            
        for line in doc:
           #delete undesired lines 
           if not line.startswith(("	SETUP","		STN_NO","	END","	SLOPE(TgtNo, TgtID, CfgNo, Hz, Vz, SDist, RefHt, Date, Ppm, ApplType, Flags)","END","	SLOPE (TgtNo, TgtID, CfgNo, Hz, Vz, SDist, RefHt, Date, Ppm, ApplType, Flags)")):
              liste=line.split() 
           #delete undesired columns
              if len(liste)==2: 
                  del liste[0]
                  delimiter=''
                  line=delimiter.join(liste)+","
              else:
                  del liste[7:11]
                  del liste[2]
                  del liste[0]
                  delimiter=''
                  line="\n"+delimiter.join(liste)+"\n"
              #print(line) 
              doc2.write(line)
        doc2.close()
         
        doc2=open("Temp_result.txt")
        doc3=asksaveasfile(mode="w" , defaultextension=".txt") 
        print(doc3)
        n=0
        m=0
         
        for lin in doc2:
            if not lin.strip():continue#enleve les lignes vides
            list=lin.split()#decompose les lingnes en liste
            n=n+1
            #print(len(lin))
            #ajout des codes
            if len(lin)<25:
                list=[CodeStation+","]+list
                delimiter=''
                lin=delimiter.join(list)+"\n"
                m=n+1
            elif n==m:
                list=[CodeReference+","]+list
                delimiter=''
                lin=delimiter.join(list)+"\n"
            else:
                 list=[CodeMesur+","]+list
                 delimiter=''
                 lin=delimiter.join(list)+"\n" 
            print(lin)
            output.insert(END,lin)
            doc3.write(lin)
        doc3.close()
        text=str(doc3)
        words=text.split()
        output.insert(END,"-----------------------------------------------------------------------------")
        output.insert(END,".....processing complete. check in your file"+words[1]+" for TXT result......")
#        photo1=PhotoImage(file="good.PNG")
#        Label(window, image=photo1).grid(row=0,column=2, sticky=W)     
    elif int(Station)==2: 
        
        for line in doc:
            if line.startswith("	1	"):
               break
        for line in doc:
        #delete undesired lines
            if not line.startswith(("	SLOPE","	SETUP","	STN_NO","	END","	SLOPE(TgtNo	TgtID	CfgNo	Hz	Vz	SDist	RefHt	Date	Ppm	ApplType	Flags)","END","	SLOPE (TgtNo, TgtID, CfgNo, Hz, Vz, SDist, RefHt, Date, Ppm, ApplType, Flags)")):
                liste=line.split()
        #delete undesired columns
                if len(liste)==2:
                    del liste[0]
                    delimiter=''
                    line=delimiter.join(liste)+","
                else:
                    del liste[7:11]
                    del liste[2]
                    del liste[0]
                    delimiter=","
                    line="\n"+delimiter.join(liste)+"\n" 
                print(line)
                #output.insert(END,line)
                doc2.write(line)
        doc2.close()
        
        doc2=open("Temp_result.txt")
        doc3=asksaveasfile(mode="w" , defaultextension=".txt")
        
        n=0
        m=0
        
        for lin in doc2:
            if not lin.strip():continue#enleve les lignes vides
            list=lin.split()#decompose les lingnes en liste
            n=n+1
            #print(len(lin))
            #ajout des codes
            if len(lin)<25:
                list=[CodeStation+","]+list
                delimiter=''
                lin=delimiter.join(list)+"\n"
                m=n+1
            elif n==m:
                list=[CodeReference+","]+list
                delimiter=''
                lin=delimiter.join(list)+"\n"
            else:
                list=[CodeMesur+","]+list
                delimiter=''
                lin=delimiter.join(list)+"\n"
            print(line)
            output.insert(END,lin)
            doc3.write(lin)
        doc3.close()
        print("--------------------------------------------------------------")
        print(".....processing complete, check in your file location for TXT result......")
        text=str(doc3)
        words=text.split()
        output.insert(END,"-----------------------------------------------------------------------------")
        output.insert(END,".....processing complete. check in your file"+words[1]+" for TXT result......")
		
    else:
        output.insert(END,"Chose a station Code between 1 and 2")
            
        
def exit():
    window.destroy()
    
def reset():
    appCode.delete(0,END)
    station.delete(0,END)
    reference.delete(0,END)
    mesure.delete(0,END)
    output.delete(0.0,END)
    
    
def brows():
    fileName.delete(0,END)
    output.delete(0.0,END)
    filename=askopenfilename(filetypes=(("Index files",".IDX"),("All files",".*")))
    fileName.insert(END,filename)
    
#def Stats():
#
#    window2=Tk()
#    window2.title("data Statistics")
#    window2.iconbitmap('image\idx2txt.ico')
#    frame1=Frame(window2)
#    frame1.grid(row=1,column=0)    
#    
#    doc2=open("Temp_result.txt")
#    
#    for lin in doc2:
#        if not lin.strip():continue#enleve les lignes vides
#        liste=lin.split()#decompose les lingnes en liste
#        
#        for i in range(1,len(liste)):
#            print(max(liste))
#        
#    
#    def plot():
#        plt.scatter([1,2,3,4,5,6,7,8,9],[9,8,7,6,5,4,3,2,1])
#        plt.title("Hi distribution")
#        plt.xlabel("Number of points")
#        plt.ylabel("Hi (m)")
#    
#    def exit():
#        window2.destroy()
#        
#    #labels
#    Label(window2).grid(row=0,column=0,sticky=W)
#    Label(window2).grid(row=2,column=0,sticky=W)
#    Label(frame1).grid(row=2,column=0,sticky=W)
#    Label(frame1).grid(row=5,column=0,sticky=W)
#    Label(frame1).grid(row=8,column=0,sticky=W) 
#    Label(frame1).grid(row=11,column=0,sticky=W)
#    Label(frame1).grid(row=14,column=0,sticky=W)
#    Label(frame1, text="Hc min:").grid(row=0,column=0,sticky=W)
#    Label(frame1, text="Hc max:").grid(row=1,column=0,sticky=W)
#    Label(frame1, text="Dist min:").grid(row=3,column=0,sticky=W)
#    Label(frame1, text="Dist max:").grid(row=4,column=0,sticky=W)   
#    Label(frame1, text="Hi min:").grid(row=6,column=0,sticky=W)
#    Label(frame1, text="Hi max:").grid(row=7,column=0,sticky=W)
#    Label(frame1, text="Vz min:").grid(row=9,column=0,sticky=W)
#    Label(frame1, text="Vz max:").grid(row=10,column=0,sticky=W)
#    Label(frame1, text="Hz min:").grid(row=12,column=0,sticky=W)
#    Label(frame1, text="Hz max:").grid(row=13,column=0,sticky=W) 
#    #Buttons Window2
#    Button(frame1, text="Graph", width=12, command=plot).grid(row=15,column=0,sticky=W)
#    Button(frame1, text="Exit", width=12, command=exit).grid(row=15,column=1,sticky=E)    
#    #output text
#    Hc_min=Text(frame1, width=20, height=1, bg="white")
#    Hc_min.grid(row=0,column=1)
#    Hc_max=Text(frame1, width=20, height=1, bg="white")
#    Hc_max.grid(row=1,column=1)
#    
#    dist_min=Text(frame1, width=20, height=1, bg="white")
#    dist_min.grid(row=3,column=1)
#    dist_max=Text(frame1, width=20, height=1, bg="white")
#    dist_max.grid(row=4,column=1) 
#    
#    Hi_min=Text(frame1, width=20, height=1, bg="white")
#    Hi_min.grid(row=6,column=1)
#    Hi_max=Text(frame1, width=20, height=1, bg="white")
#    Hi_max.grid(row=7,column=1) 
#
#    Vz_min=Text(frame1, width=20, height=1, bg="white")
#    Vz_min.grid(row=9,column=1)
#    Vz_max=Text(frame1, width=20, height=1, bg="white")
#    Vz_max.grid(row=10,column=1) 
#
#    Hz_min=Text(frame1, width=20, height=1, bg="white")
#    Hz_min.grid(row=12,column=1)
#    Hz_max=Text(frame1, width=20, height=1, bg="white")
#    Hz_max.grid(row=13,column=1)      
#    
#    window2.mainloop()
    
#building Frame
guiFrame1=Frame(window)
guiFrame1.grid(row=5,column=0,sticky=W)

guiFrame2=Frame(window)
guiFrame2.grid(row=2,column=0,sticky=W)


#labels
Label(window, text="Welcome to Clear v2.0. Application developed for the cleaning and codification of IDX files").grid(row=0,column=0,sticky=W)
Label(window).grid(row=1,column=0,sticky=W)
Label(window, text="For TCR300, TCR400, TCR700, TCR800, TS Code Apparatus=1").grid(row=3,column=0,sticky=W)
Label(window, text="For Builders and TS06plus Code Apparatus=2").grid(row=4,column=0,sticky=W)
Label(guiFrame2, text="File directory:").grid(row=0,column=0,sticky=W)
#Label(guiFrame1, text="Save directory:").grid(row=9,column=0,sticky=W)

Label(guiFrame1).grid(row=0,column=0,sticky=W)
Label(guiFrame1, text="Code of Apparatus:").grid(row=1,column=0,sticky=W)

Label(guiFrame1).grid(row=2,column=0,sticky=W)
Label(guiFrame1, text="Code of Station:").grid(row=3,column=0,sticky=W)

Label(guiFrame1).grid(row=4,column=0,sticky=W)
Label(guiFrame1, text="Code of Reference:").grid(row=5,column=0,sticky=W)

Label(guiFrame1).grid(row=6,column=0,sticky=W)
Label(guiFrame1, text="Code of mesure:").grid(row=7,column=0,sticky=W)

Label(guiFrame1, width=3).grid(row=10,column=3,sticky=W)

Label(window, text="Credit: Demeveng Derrick       Email:demeveng@gmail.com         Tel: 695900764").grid(row=7,column=0)

#creat text entry
fileName=Entry(guiFrame2, width=56, bg="white")
fileName.grid(row=0,column=1,sticky=W)

#Save=Entry(guiFrame1, width=50, bg="white")
#Save.grid(row=9,column=1,sticky=W)

appCode=Entry(guiFrame1, width=20, bg="white")
appCode.grid(row=1,column=1,sticky=W)

Label(guiFrame1).grid(row=2,column=1,sticky=W)
station=Entry(guiFrame1, width=20, bg="white")
station.grid(row=3,column=1,sticky=W)

Label(guiFrame1).grid(row=4,column=1,sticky=W)
reference=Entry(guiFrame1, width=20, bg="white")
reference.grid(row=5,column=1,sticky=W)

Label(guiFrame1).grid(row=6,column=1,sticky=W)
mesure=Entry(guiFrame1, width=20, bg="white")
mesure.grid(row=7,column=1,sticky=W)

#button window1
Label(guiFrame1).grid(row=8,column=1,sticky=W)
Button(guiFrame1, text="Process", width=12, command=process).grid(row=10,column=2,sticky=W)
Button(guiFrame1, text="Exit",width=12, command=exit, cursor="pirate").grid(row=10,column=5,sticky=W)
#Button(guiFrame1, text="Stats",width=12, command=Stats, cursor="").grid(row=10,column=4,sticky=W)
Button(guiFrame1, text="Reset",width=12, command=reset).grid(row=10,column=1,sticky=W)
Button(guiFrame2, text="Open",width=12, command=brows, cursor="heart").grid(row=0,column=2,sticky=W)
Button(guiFrame1, text="Preview data",width=12, command=plot).grid(row=10,column=6,sticky=W)
#Button(guiFrame1, text="Save",width=12, command=save).grid(row=9,column=2,sticky=N)


#create textbox
output=Text(window, width=63, height=5, wrap=WORD)
output.grid(row=6,column=0,sticky=W)


#keeps the window open 
window.mainloop()