import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
from tkinter.filedialog import askopenfilename

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("img1.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        
        border = tk.LabelFrame(self, text='Login', bg='ivory', bd = 10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx = 150, pady=150)
        
        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width = 30, bd = 5)
        T1.place(x=180, y=20)
        
        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='ivory')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width = 30, show='*', bd = 5)
        T2.place(x=180, y=80)
        
        def verify():
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i  = 0
                    for e in info:
                        u, p =e.split(",")
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(ThirdPage)
                            i = 1
                            break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")
         
        B1 = tk.Button(border, text="Submit", font=("Arial", 15), command=verify)
        B1.place(x=320, y=115)
        
        def register():
            window = tk.Tk()
            window.resizable(0,0)
            window.configure(bg="deep sky blue")
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial",15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 200, y=10)
            
            l2 = tk.Label(window, text="Password:", font=("Arial",15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x = 200, y=60)
            
            l3 = tk.Label(window, text="Confirm Password:", font=("Arial",15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x = 200, y=110)
            
            def check():
                if t1.get()!="" or t2.get()!="" or t3.get()!="":
                    if t2.get()==t3.get():
                        with open("credential.txt", "a") as f:
                            f.write(t1.get()+","+t2.get()+"\n")
                            messagebox.showinfo("Welcome","You are registered successfully!!")
                    else:
                        messagebox.showinfo("Error","Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                    
            b1 = tk.Button(window, text="Sign in", font=("Arial",15), bg="#ffc22a", command=check)
            b1.place(x=170, y=150)
            
            window.geometry("470x220")
            window.mainloop()
            
        B2 = tk.Button(self, text="Register", bg = "dark orange", font=("Arial",15), command=register)
        B2.place(x=1000, y=20)

class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='white')
        
        #Label = tk.Label(self, text="Store some content related to your \n project or what your application made for. \n All the best!!", bg = "orange", font=("Arial Bold", 25))
        #Label.place(x=40, y=150)
        w2 = tk.Label(self, text="Terrain Classification", bg="white"  ,fg="black"  ,width=30  ,height=1,font=('times', 30, 'italic bold underline'))
        w2.place(x=300,y=10)  
        
        '''
        l=Button(self,text="Build Training Model", command=self.buildModel, bg="red"  ,fg="white"  ,width=20  ,height=1,font=('times', 20, 'italic bold underline'))
        l.place(x=200,y=200)
        '''
        k=tk.Button(self,text="Browse For Input Image", command=self.showImgg, bg="white"  ,fg="black"  ,width=20  ,height=1,font=('times', 20, 'italic bold underline'))
        k.place(x=800,y=200)
        
        t=tk.Button(self,text="Classify Test Image", command=self.Classify, bg="white"  ,fg="black"  ,width=20  ,height=1,font=('times', 20, 'italic bold underline'))
        t.place(x=800,y=300)
        
        Button = tk.Button(self, text="Home",bg = "dark orange", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=1100, y=50)
        
        Button = tk.Button(self, text="Back",bg = "dark orange", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=50, y=50)
        
    def Classify(self):
        print("Classify the Test Image")
        #from tensorflow.keras.models import Model
        from tensorflow.keras.models import load_model
        #from keras.models import load_model
        model = load_model('terrain_model.h5')
        
        #Compiling the model
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        #(model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy']))
        #Making New Prediction
        import numpy as np
        from tensorflow.keras.preprocessing import image
        
        test_image = image.load_img(self.load,target_size = (64,64,3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image,axis = 0)
        result = model.predict(test_image)
        print(result)
        print(result[0][0])        
        
        if result[0][0] == 1.0:
            a = "Cloudy   "
            print("Cloudy")
       
        elif result[0][1] == 1.0:
            a = "Desert    "
            print("Second")
            
        elif result[0][2] == 1.0:
            a = "GreenArea"
            print("Second")
            
        elif result[0][3] == 1.0:
            a = "Water  "
            print("Water")
        
        s = tk.Label(self, text=a, font=('arial',12))
        s.place(x=850,y=500)
        
    def showImgg(self):
        self.load = askopenfilename(filetypes=[("Image File",'.jpeg .jpg .png')])
        
        
        im = Image.open(self.load)
        
        im = im.resize((300, 150))
    
        render = ImageTk.PhotoImage(im)
        
        

        # labels can be text or images
        img = tk.Label(self, image=render,width=300,height=150)
        img.image = render
        img.place(x=100, y=250)
        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        window.grid_rowconfigure(0, minsize = 800)
        window.grid_columnconfigure(0, minsize = 1300)
        
        self.frames = {}
        for F in (FirstPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(FirstPage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")
            
app = Application()
app.maxsize(1300,800)
app.mainloop()