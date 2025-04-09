# Psychological Evaluation using AI, project by Austin Pichardo & Timothy Lindsay from PCTVS


# These are the python libraries and modules we are using for this project

from tkinter import * #Tkinter is the standard GUI toolkit for python
from PIL import ImageTk, Image #Pillow is a fork of the Python Imaging Library (PIL)
import customtkinter #Custom tkinter module to customize tkinter widgets
import statistics # To get the mode for the most dominant emotion among other data
import cv2 # Library used to access the camera and detect the users face
from deepface import DeepFace # Used in conjunction with CV2 to detect the users emotions
import speech_recognition as sr # Used to detect the users speech to answer questions
import random # Used to determine what questions the user is asked
import openai # Used to access OpenAI's ChatGPT API, specifically version 0.28.0
import threading # Used to run the speech recognition in a separate thread
from tkinter import messagebox # Used to display error messages to the user

# Root configuration
root = Tk()
root.title("Nasa Hunch")
root.geometry('1200x720')
root.resizable(0, 0)
root.iconbitmap(r'images\nasa logo.ico')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, minsize=600)
root.grid_columnconfigure(1, weight=1)

# Beggining Image Frame
begginingImageFrame = LabelFrame(root, bd=0)
begginingImageFrame.grid(row=0, column=0, sticky="nsew")
begginingImageFrame.grid_rowconfigure(0, weight=1) 
begginingImageFrame.grid_columnconfigure(0, weight=1)

my_img1 = ImageTk.PhotoImage(Image.open(r"""images\n2.png"""))
my_Label = Label(begginingImageFrame, image=my_img1)
my_Label.grid(row=0, column=0, sticky="")

# Questions Frame
questionsFrame = customtkinter.CTkFrame(root, fg_color="#341539")
questionsFrame.grid(row=0, column=1, sticky="nsew")
questionsFrame.grid_columnconfigure((0, 2), weight=1)
questionsFrame.grid_columnconfigure(1, weight=2)
questionsFrame.grid_rowconfigure((0, 6), weight=1)

# Welcome label
welcome_label = customtkinter.CTkLabel(questionsFrame, text="WELCOME!", text_color="white", font=("Arial", 15))
welcome_label.grid(row=1, column=1, pady=10)

# Name entry
name = None
nameEntry = customtkinter.CTkEntry(questionsFrame, placeholder_text="Name", width=200, font=("Arial", 12))
nameEntry.grid(row=2, column=1, pady=10)

# Age Entry
age = None
ageEntry = customtkinter.CTkEntry(questionsFrame, placeholder_text="Age", width=200)
ageEntry.grid(row=3, column=1, pady=10)

# UUPIC entry
uupic = None
uupicEntry = customtkinter.CTkEntry(questionsFrame, placeholder_text="UUPIC", width=200)
uupicEntry.grid(row=4, column=1, pady=10)

# Enter button
def basicInforTransition():
    global name
    global uupic
    global age

    # Getting data from entry boxes
    name = nameEntry.get()
    age = ageEntry.get()
    uupic = uupicEntry.get()

    # CHecking if the data is valid
    if name == "":
        messagebox.showerror("Error", "Please enter a name")
    elif age == "" or age.isnumeric() == False:
        messagebox.showerror("Error", "Please enter a valid age")
    elif uupic == "" or uupic.isnumeric() == False:
        messagebox.showerror("Error", "Please enter a valid UUPIC")
    else:
        welcome_label.destroy()
        nameEntry.destroy()
        ageEntry.destroy()
        uupicEntry.destroy()
        enterButton.destroy()
        backgroundQuestions()

enterButton = customtkinter.CTkButton(questionsFrame, text="ENTER", command=basicInforTransition)
enterButton.grid(row=5, column=1, pady=10)

def inDepthQuestionsTransition():
    global question1
    global question2
    global question3
    global question4
    global question5

    # Getting data from text boxes
    question1 = question1TextBox.get('0.0', END).strip()
    question2 = question2TextBox.get('0.0', END).strip()
    question3 = question3TextBox.get('0.0', END).strip()
    question4 = question4TextBox.get('0.0', END).strip()
    question5 = question5TextBox.get('0.0', END).strip()

    # Checking if the data is valid
    if question1 == "":
        messagebox.showerror("Error", "Please answer all questions. Missing response: Question 1")
    elif question2 == "":
        messagebox.showerror("Error", "Please answer all questions. Missing response: Question 2")
    elif question3 == "":
        messagebox.showerror("Error", "Please answer all questions. Missing response: Question 3")
    elif question4 == "":
        messagebox.showerror("Error", "Please answer all questions. Missing response: Question 4")
    elif question5 == "":
        messagebox.showerror("Error", "Please answer all questions. Missing response: Question 5")
    else:
        question1Label.grid_forget()
        question2Label.grid_forget()
        question3Label.grid_forget()
        question4Label.grid_forget()
        question5Label.grid_forget()
        question1TextBox.grid_forget()
        question2TextBox.grid_forget()
        question3TextBox.grid_forget()
        question4TextBox.grid_forget()
        question5TextBox.grid_forget()
        questionEntryButton.grid_forget()
        my_Label.grid_forget()
        mainScreen()

def backgroundQuestions():
    # Initial Questions:
    global question1TextBox
    global question2TextBox
    global question3TextBox
    global question4TextBox
    global question5TextBox

    global question1Label
    global question2Label
    global question3Label
    global question4Label
    global question5Label
    global questionEntryButton

    # Question 1
    question1Label = customtkinter.CTkLabel(questionsFrame, text="Are you currently experiencing any notable psychological symptoms?", text_color="white", fg_color="transparent", font=("Arial", 15))
    question1Label.grid(row=0, column=0, padx=10, sticky="w")
    question1LabelElaboration = customtkinter.CTkLabel(questionsFrame, text="(if yes please elaborate)", text_color="white", fg_color="transparent", font=("Arial", 15))
    question1LabelElaboration.grid(row=1, column=0, padx=10, sticky="w")
    question1TextBox = customtkinter.CTkTextbox(questionsFrame, width=300, height=75)
    question1TextBox.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

    # Question 2
    question2Label = customtkinter.CTkLabel(questionsFrame, text="Are you currently taking medications? (if yes please elaborate)", text_color="white", fg_color="transparent", font=("Arial", 15))
    question2Label.grid(row=3, column=0, padx=10, pady=5, sticky="w")  
    question2TextBox = customtkinter.CTkTextbox(questionsFrame, width=300, height=75)
    question2TextBox.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")  

    # Question 3
    question3Label = customtkinter.CTkLabel(questionsFrame, text="Have you been diagnosed or treated for any mental health conditions in the past?", text_color="white", fg_color="transparent", font=("Arial", 15))
    question3Label.grid(row=5, column=0, padx=10, sticky="w")  
    question3LabelElaboration = customtkinter.CTkLabel(questionsFrame, text="(if yes please elaborate)", text_color="white", fg_color="transparent", font=("Arial", 15))
    question3LabelElaboration.grid(row=6, column=0, padx=10, sticky="w")
    question3TextBox = customtkinter.CTkTextbox(questionsFrame, width=300, height=75)
    question3TextBox.grid(row=7, column=0, columnspan=4, padx=10, pady=5, sticky="ew")  

    # Question 4
    question4Label = customtkinter.CTkLabel(questionsFrame, text="Any history of mental health disorders in your family? (if yes please elaborate)", text_color="white", fg_color="transparent", font=("Arial", 15))
    question4Label.grid(row=8, column=0, padx=10, pady=5, sticky="w")  
    question4TextBox = customtkinter.CTkTextbox(questionsFrame, width=300, height=75)
    question4TextBox.grid(row=9, column=0, columnspan=4, padx=10, pady=5, sticky="ew") 

    # Question 5
    question5Label = customtkinter.CTkLabel(questionsFrame, text="Any use of drugs or alcohol in the past month? (if yes please elaborate)", text_color="white", fg_color="transparent", font=("Arial", 15))
    question5Label.grid(row=10, column=0, padx=10, pady=5, sticky="w")  
    question5TextBox = customtkinter.CTkTextbox(questionsFrame, width=300, height=75)
    question5TextBox.grid(row=11, column=0, columnspan=4, padx=10, pady=5, sticky="ew")  

    # Enter button
    questionEntryButton = customtkinter.CTkButton(questionsFrame, text="ENTER", command=inDepthQuestionsTransition)
    questionEntryButton.grid(row=12, column=0, columnspan=3, pady=5, sticky="ew")  


emotions_detected = []
def open_camera():
    face_cascade = cv2.CascadeClassifier(r"haar_cascade.xml")
    _,frame = video.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x,y,w,h in face:
        img = cv2.rectangle(frame,(x, y),(x+w, y+h),(0, 0, 255), 1)
        try:
            analyze = DeepFace.analyze(frame,actions=['emotion']) # Deepface analyzes the emotion
            # print(analyze[0]['dominant_emotion'])
            emotions_detected.append(analyze[0]['dominant_emotion'])
        except:
            print("No face")

    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
  
    # Capture the latest frame and transform to image 
    captured_image = Image.fromarray(opencv_image)
        
    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
  
    # Displaying photoimage in the label 
    label_widget.photo_image = photo_image 
  
    # Configure image in the label 
    label_widget.configure(image=photo_image) 
  
    # Repeat the same process after every 10 seconds 
    label_widget.after(10, open_camera) 

# Get the most dominant emotion
def getEmotion():
    mostDominantEmotion = statistics.mode(emotions_detected)
    print(mostDominantEmotion)
    return mostDominantEmotion


def mainScreen():
    begginingImageFrame.destroy()
    questionsFrame.destroy()

    root.rowconfigure(0, weight=1) 
    root.rowconfigure(1, weight=1)  
    root.columnconfigure(0, weight=2) 
    root.columnconfigure(1, weight=4)
    root.columnconfigure(2, weight=1) 

    # Camera Frame to display the user's face
    global cameraFrame
    cameraFrame = LabelFrame(root, bd=1, background="#341539")
    cameraFrame.grid(row=0, column=0, sticky="nsew")

    global video
    global label_widget
    video = cv2.VideoCapture(0)
    label_widget = Label(cameraFrame, bg="#341539") 
    label_widget.pack(pady=10, padx=10, fill="both", expand=True)
    open_camera()

    # Psychological Evaluation Frame to display the user's responses to the questions
    global psychEvalFrame
    psychEvalFrame = LabelFrame(root, bd=1)
    psychEvalFrame.grid(row=0, column=1, rowspan=2, sticky="nsew", columnspan=3) 

    global psychEvalEntryBox
    psychEvalEntryBox = customtkinter.CTkTextbox(psychEvalFrame)
    psychEvalEntryBox.place(relwidth=1, relheight=1)
    
    psychEvalEntryBox.insert("0.0", f'Name: {name}\n')
    psychEvalEntryBox.insert("end", f'Age: {age}\n')
    psychEvalEntryBox.insert("end", f'UUPIC: {uupic}\n')
    psychEvalEntryBox.insert("end", f'Question 1: Are you currently experiencing any notable psychological symptoms?\n\n{question1}\n\n')
    psychEvalEntryBox.insert("end", f'Question 2: Are you currently taking medications?\n\n{question2}\n\n')
    psychEvalEntryBox.insert("end", f'Question 3: Have you been diagnosed or treated for any mental health conditions in the past?\n\n{question3}\n\n')
    psychEvalEntryBox.insert("end", f'Question 4: Any history of mental health disorders in your family?\n\n{question4}\n\n')
    psychEvalEntryBox.insert("end", f'Question 5: Any use of drugs or alcohol in the past month?\n\n{question5}\n\n')
    psychEvalEntryBox.configure(state="disabled")

    # Chatbox to display the conversation between the user and our computer generated questions
    global chatbox
    chatbox = LabelFrame(root, bd=1, background="#341539")
    chatbox.grid(row=1, column=0, sticky="nsew")

    global micQuestionLabel
    global yesButton
    global noButton
    micQuestionLabel = customtkinter.CTkLabel(chatbox, text="Do you have a microphone and are you in a noise free environment?", text_color="white", font=("Arial", 15))
    micQuestionLabel.pack(pady=10)
    yesButton = customtkinter.CTkButton(chatbox, text="Yes", command=lambda: voiceControlPermission("y"))
    yesButton.pack(pady=10)
    noButton = customtkinter.CTkButton(chatbox, text="No", command=lambda: voiceControlPermission("n"))
    noButton.pack()

def waithere():
    var = IntVar()
    root.after(3000, var.set, 1)
    print("waiting...")
    root.wait_variable(var)


# Module used to recognize the user's spaeech. Here we used threading to run the speech recognition in the background
global rdata
global is_listening
rdata = []
is_listening = False
global response
response = ""
def recognize_speech():
    global rdata
    global response
    global is_listening
    question = ["How are you today?","Is there anything you're feeling upset about today?","Has everything been alright?","Tell me about your day!"]
    rQuestion = random.choice(question)
    rdata.append(rQuestion)
    chatboxTextBox.insert("0.0", rQuestion)
    chatboxTextBox.insert("end", "\nspeak something...")
    chatboxTextBox.configure(state="disabled")
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while is_listening:
            try:
                audio_data = recognizer.listen(source)
                response = recognizer.recognize_google(audio_data)
                print("Response: " + response)
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
                #chatboxTextBox.insert("end", "Sorry, could not understand audio.")
            except sr.RequestError as e:
                print("Error: Could not request results from Google Speech Recognition service; {0}".format(e))
                #chatboxTextBox.insert("end", "Error: Could not request results from Google Speech Recognition service;")


global speeachThread
def voiceControlPermission(answer):
    global voiceControl
    global is_listening
    if answer == "y":
        voiceControl = "yes"
    else:
        voiceControl = "no"
    
    micQuestionLabel.pack_forget()
    yesButton.pack_forget()
    noButton.pack_forget()

    global chatboxTextBox
    global rdata
    chatboxTextBox = customtkinter.CTkTextbox(chatbox, width=300, height=75)
    chatboxTextBox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    if voiceControl == "yes":
        global speeachThread
        is_listening = True
        speeachThread = threading.Thread(target=recognize_speech)
        speeachThread.start()
        enterTextButton = customtkinter.CTkButton(chatbox, text="Enter", command=lambda: endingScreen("yes mic"))
        enterTextButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    else:
        question = ["How are you today?", "Is there anything you're feeling upset about today?", "Has everything been alright?", "Tell me about your day!"]
        rQuestion = random.choice(question)
        chatboxTextBox.insert("0.0", f'{rQuestion} (Type Below)\n')
        enterTextButton = customtkinter.CTkButton(chatbox, text="Enter", command=lambda: endingScreen("no mic"))
        enterTextButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        rdata = [rQuestion]

    chatbox.grid_columnconfigure(0, weight=1)
    chatbox.grid_rowconfigure(0, weight=1)
    chatbox.grid_rowconfigure(1, weight=1)


def endingScreen(mic):
    global is_listening
    global response
    global speeachThread
    if mic == "no mic":
        response = chatboxTextBox.get("0.0", END)
        rdata.append(response)
        if rdata[0] != rdata[1][0:len(rdata[0]) + 1]:
            rdataDataApppend = rdata[0] + "\n" + response + "\n"
            rdata.pop()
            rdata.append(rdataDataApppend)
        print(rdata)
        rdata[1] = rdata[1][(len(rdata[0]) + 1):-1]
        print(rdata[1])
    else:
        is_listening = False
        speeachThread.join()
        rdata.append(response)
        print("Rdata:", rdata)

    cameraFrame.destroy()
    chatbox.destroy()
    psychEvalFrame.destroy()
    video.release()

    mostDominantEmotion = getEmotion()

    # API key
    # Unfortunately, I cannot provide my API key for security reasons. Please use your own OpenAI API key.

    # Function to generate evaluation using OpenAI's ChatGPT API
    def generate_text(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Chatgpt model
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    # Putting the data all together to generate the final evaluation
    initData = [f"Name: {name}", f"Age {age}", f'UUPIC: {uupic}', f'Question 1: Are you currently experiencing any notable psychological symptoms? {question1}', f'Question 2: Are you currently taking medications? {question2}', f'Question 3: Have you been diagnosed or treated for any mental health conditions in the past?\n{question3}', f'Question 4: Any history of mental health disorders in your family? {question4}', f'Question 5: Any use of drugs or alcohol in the past month? {question5}']
    prompt = "This program is made for completing a psychological evaluation. Make sure to not include any text formatting like bolding or italics in your response. The user has answered a few questions already: " + str(initData) + "This is the most dominant facial expression: " + mostDominantEmotion + ' and this is their response to the question "' + str(rdata[0]) + '": ' + str(rdata[1]) + '". Format it like this and at the end add an evaluation based on the data provided: Patient Information: Name: UUID: Age: (LINE DASHES TO SEPERATE LINES______________________________________) History of Mental Health Disorders in Patients Family: Pre-existing Pyshcologocial Conditions: Medications: (LINE DASHES TO SEPERATE LINES______________________________________) Notable Symptoms: Recent use of Substances: (LINE DASHES TO SEPERATE LINES______________________________________) Current Mood: Question Responses (The question and response I gave after giving the most dominant emotion): (LINE DASHES TO SEPERATE LINES______________________________________)'
    output = generate_text(prompt)

    root.grid_rowconfigure(0, weight=1)  
    root.grid_rowconfigure(1, weight=1) 
    root.grid_rowconfigure(2, weight=1) 
    root.grid_columnconfigure(0, weight=1)  
    root.grid_columnconfigure(1, weight=1)   

    bg_image = Image.open(r"""images\nasa-background.png""")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = customtkinter.CTkLabel(root, image=bg_photo, text="")
    bg_label.place(relwidth=1, relheight=1)  

    # GPT Output Textbox
    gptOutputTextBox = customtkinter.CTkTextbox(root, width=700, height=200, corner_radius=10, border_width=2)
    gptOutputTextBox.insert("0.0", output)
    gptOutputTextBox.configure(state='disabled')
    gptOutputTextBox.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")


root.mainloop()
