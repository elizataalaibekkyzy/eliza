from cgitb import grey
import tkinter as tk;
from tkinter import Button, Label, Tk, filedialog
from classification_emotions import Classifictions;
import cv2
from model import Model;
from PIL import Image, ImageTk

model = Model.create_model()
model.load_weights('./src/model_2022-01-08.h5')


class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1200x850+150+150')
        self.window.title("Emotion Detection")
        self._exit_btn = Button(
            self.window,
            text = "exit",
            width = 20,
            command = self.window.quit,
            highlightbackground='lightgray'
        )
        self._select_btn = Button(
            self.window,
            text="upload image",
            command=self._load_image,
            width=20,
            highlightbackground='lightgray'
        )
        self._live_btn = Button(
            self.window,
            text="live detection",
            command=self._live_func,
            width=20,
            highlightbackground='lightgray'
        )

        # Positioning BUttons
        self._select_btn.place(x=580, y=650, anchor=tk.N)
        self._live_btn.place(x=580, y=680, anchor=tk.N)
        self._exit_btn.place(x=580,y=710,anchor=tk.N)

        #Capture video frames
        self._decore_frame = tk.Label(self.window, bg="grey", width=100, height=30)
        self._decore_frame.place(relx = 0.5,
                              rely = 0.4,
                              anchor = 'center')
        self.video_frame = tk.Label(self.window, text = "Upload Image", bg="grey")
        self.video_frame.place(relx = 0.5,
                              rely = 0.4,
                              anchor = 'center')

        width = 800
        height = 600
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.window.mainloop()
        pass

    def live_face_expression(self):
        self._decore_frame.destroy()
        _, img = self.cap.read()
        img = cv2.flip(img, 1)
        
        Classifictions.get_expression_classified(img, model)

        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)
        self.video_frame.after(10, self.live_face_expression)
    
    def _load_image(self):
        self._decore_frame.destroy()
        filenames = filedialog.askopenfilenames(
            title="Choose a file",
            filetypes=('image files', ('.png', '.jpg'))
        )

        if len(filenames) != 0:
            filename = filenames[0]
            if filename is not  '':
                img = cv2.imread(filename)
                
                width = int(img.shape[1])
                height = int(img.shape[0])
                scale = 100
                while scale*width/100 >= 800 or scale*height/100 >= 600:
                    scale=scale-1
                width = int(img.shape[1] * scale / 100)
                height = int(img.shape[0] * scale / 100)

                # resize image
                dim = (width, height)
                img = cv2.resize(img, dim, fx=0.5, fy=0.4)
                
                Classifictions.get_expression_classified(img, model)
                cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)
            else: print("No image selected!")
        else:
            print("Choose an Image!")
        pass

    def _live_func(self):
        self.live_face_expression()
        pass

if __name__ == '__main__':
    App()

