# GUI
import tkinter as tk
from tkinter import PhotoImage
from tkinter import font

# open apk
import subprocess

# read text
from gtts import gTTS 
import pyttsx3

# Open App
import pyaudio
import wave
import speech_recognition as sr
 

#using OS
import os

import re

file_path = r'C:\\laragon\www\\GITHUB33\\aslan-aradan-chatbot\\intro\\intro.txt'
file_keywords = r'C:\\laragon\www\\GITHUB33\\aslan-aradan-chatbot\replied_voice\output.txt'
keywords_to_check = ['visual studio code', 
                     'visual studio', 
                     'visual code',
                     'studio visual',
                     'studio code',
                    ]  # Replace with your list of keywords
vscode_path = r'C:\\Users\sulaslan.setiawan\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'


def analyze_text(file_keywords, keywords):
    try:
        with open(file_keywords, 'r', encoding='utf-8') as file:
            file_content = file.read()
            print('liaaat file_keywords: ' + file_content)

            # Check if any of the keywords is present in the text
            found_keywords = [keyword for keyword in keywords if re.search(r'\b{}\b'.format(re.escape(keyword)), file_content, flags=re.IGNORECASE)]

            if found_keywords:
                # Keywords found
                print(f"The following keywords were found in the text: {', '.join(found_keywords)}")

                recording_label.config(text="Opening VS Code ...")
                play_text("Opening Visual Studio Code ...")
                root.update()

                # Add a 3000 ms (3 seconds) delay
                root.after(3000, lambda: open_vscode(vscode_path))

                recording_label.config(text="Open Completed...")

            else:
                # No keywords found
                recording_label.config(text="Wrong Keyword")
                root.update()
                play_text("Kata Kunci Salah, mohon katakan : Open Visual Studio Code ...")

                # Add a 3000 ms (3 seconds) delay
                root.after(3000, lambda: recording_label.config(text=""))

    except FileNotFoundError:
        print(f"File not found: {file_keywords}")
    except Exception as e:
        print(f"An error occurred: {e}")




def run_intro():
    file_path = r'C:\\laragon\www\\GITHUB33\\aslan-aradan-chatbot\\intro\\intro.txt'
    bahasa = "id"

    # Read text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Create gTTS object
    tts = gTTS(text=text, lang=bahasa)

    # Save as an audio file
    tts.save("intro.wav")

    # Play the audio file
    os.system("start intro.wav")



def record_audio(file_name, duration=5, sample_rate=44100, chunk_size=1024):
    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Recording...")
        recording_label.config(text="Recording...")
        root.update()

        frames = []

        for i in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)

        print("Recording complete.")
        recording_label.config(text="Recording complete.") 
        root.update()

        with wave.open(file_name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def play_audio(file_name):
    p = pyaudio.PyAudio()

    try:
        wf = wave.open(file_name, 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        print("Playing...")
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        print("Playback complete.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def convert_audio_to_text(file_name):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_name) as source:
        audio_data = recognizer.record(source)

    try:
        # text = recognizer.recognize_google(audio_data)
        text = recognizer.recognize_google(audio_data, language='id-ID')

        with open("replied_text/output.txt", "w") as output_file:
            output_file.write(text)
        print("Text saved to 'output.txt':", text)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def open_vscode(vscode_path):
    try:
        subprocess.run([vscode_path])
    except FileNotFoundError:
        print("Visual Studio Code not found. Make sure it is installed and added to the system PATH.")

def play_text(text, lang='id'):
    # Create gTTS object
    tts = gTTS(text=text, lang=lang)

    # Save as an audio file
    audio_file_path = "replied_voice/output.mp3"
    tts.save(audio_file_path)

    # Play the audio file
    os.system(f"start {audio_file_path}")

# def update_recording_label(status):
#     recording_label.config(text=status)
#     root.update()

def speak_func():
    # Record audio
    record_audio("fetched_voice/recorded_audio.wav")

    # Convert audio to text and save to file
    convert_audio_to_text("fetched_voice/recorded_audio.wav")

    # Play the recorded audio
    # play_audio("recorded_audio.wav")

    analyze_text(file_path, keywords_to_check)


# Create the main window
root = tk.Tk()
root.title("Aradan Chatbot Desktop")
root.geometry("300x500")  # Set the window size to 500x500 pixels

# Additional code to make the window always on top
root.attributes('-topmost', 1)
root.lift()

# Load image
img = PhotoImage(file="C:\laragon\www\GITHUB33\\aslan-aradan-chatbot\\assets\img\AradanBot2.png")  # Replace with the actual path to your image


# Create custom fonts
title_font = font.Font(family="Helvetica", size=20, weight="bold")
subtitle_font = font.Font(family="Helvetica", size=14, weight="normal")

# Create widgets
label_intro = tk.Label(root, text="Created By Aslan", font=title_font, relief=tk.RAISED, borderwidth=5, foreground="black")
button_intro = tk.Button(root, text="Intro", command=run_intro, relief=tk.RAISED, borderwidth=5)
image_label = tk.Label(root, image=img)

label_main = tk.Label(root, text="Click the button to run Open App")
button_main = tk.Button(root, text="Open Visual Studio Code !", command=speak_func)


recording_label = tk.Label(root, text="", font=subtitle_font)  


# Pack widgets into the window
label_intro.pack(pady=10)
button_intro.pack(pady=10)
image_label.pack(pady=10)
label_main.pack(pady=10)
button_main.pack(pady=10)
recording_label.pack(pady=10)

# Start the main loop
root.mainloop()
