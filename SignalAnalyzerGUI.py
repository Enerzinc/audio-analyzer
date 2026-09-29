from PIL import Image
import customtkinter as ctk
import ttkbootstrap as ttk
import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import sounddevice as sd
from scipy.fftpack import fft, fftfreq
import time
from SignalProcessor import compute_fft, read_wav_file, record_audio 

from tkinter import PhotoImage
from PIL import Image, ImageTk


ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Audio Analyzer")
        self.geometry("900x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.current_theme = ctk.get_appearance_mode()
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, border_width=2)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.label1 = ctk.CTkLabel(self.main_frame, text="Audio Anaylzer", font=("Arial", 16, "bold"))
        self.label1.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        
        self.countdown_label = ctk.CTkLabel(self.main_frame, text="Record or Upload an Audio", font=("Arial", 16, "bold"))
        self.countdown_label.grid(row=6, column=0, pady=10, padx=10, sticky="se")

        self.mode_var = tk.StringVar(value="Oscilloscope")
        self.combobox = ctk.CTkComboBox(self.main_frame, values=["Oscilloscope", "Spectrum Analyzer"], width=15, variable=self.mode_var, command=self.plot_signal, state="readonly")
        self.combobox.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        
        self.button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, border_width=2)
        self.button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.mic_done = ctk.CTkImage(light_image=Image.open("images/done_mic.png"), size=(40, 40))
        self.light_mic1 = ctk.CTkImage(light_image=Image.open("images/light_mic1.png"), size=(40, 40))
        self.dark_mic1 = ctk.CTkImage(light_image=Image.open("images/dark_mic1.png"), size=(40, 40))
        
        self.light_mic2 = ctk.CTkImage(light_image=Image.open("images/light_mic2.png"), size = ((40, 40)))
        self.dark_mic2 = ctk.CTkImage(light_image=Image.open("images/dark_mic2.png"), size = ((40, 40)))
        
        self.light_restart = ctk.CTkImage(light_image=Image.open("images/light_restart.png"), size = ((40, 40)))
        self.dark_restart = ctk.CTkImage(light_image=Image.open("images/dark_restart.png"), size = ((40, 40)))
        
        self.light_plot = ctk.CTkImage(light_image=Image.open("images/light_plot.png"), size = ((40, 40)))
        self.dark_plot =ctk.CTkImage(light_image=Image.open("images/dark_plot.png"), size = ((40, 40)))
        
        self.light_upload = ctk.CTkImage(light_image=Image.open("images/light_upload.png"), size = ((40, 40)))
        self.dark_upload = ctk.CTkImage(light_image=Image.open("images/dark_upload.png"), size = ((40, 40)))
        
        self.light_clear = ctk.CTkImage(light_image=Image.open("images/light_clear.png"), size = ((40, 40)))
        self.dark_clear = ctk.CTkImage(light_image=Image.open("images/dark_clear.png"), size = ((40, 40)))
        
        self.light_save = ctk.CTkImage(light_image=Image.open("images/light_save.png"), size = ((40, 40)))
        self.dark_save = ctk.CTkImage(light_image=Image.open("images/dark_save.png"), size=((40, 40))) 
        
        #Buttons
        self.mic1 = ctk.CTkButton(self.button_frame, image=self.light_mic1, text="", width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20, command=lambda: self.record_audio_gui(1))
        self.mic2 = ctk.CTkButton(self.button_frame, image=self.light_mic2, text="", command=lambda: self.record_audio_gui(2), width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20, state = tk.DISABLED)
        self.restart = ctk.CTkButton(self.button_frame, image=self.light_restart, text="", command=self.restart_recording, width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20)
        self.upload = ctk.CTkButton(self.button_frame, image=self.light_upload, text="", command=self.upload_wav, width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20)
        self.clear = ctk.CTkButton(self.button_frame, image=self.light_clear, text="", command=self.clear_graph, width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20)
        self.save = ctk.CTkButton(self.button_frame, image=self.light_save, text="", command=self.save_graph, width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20)
        
        self.button_frame.grid_columnconfigure(tuple(range(6)), weight=1)  
        self.button_frame.grid_rowconfigure(0, weight=1)  

        self.mic1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.mic2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.restart.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.upload.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        self.clear.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        self.save.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")
        
        self.plot = ctk.CTkButton(self.main_frame, image=self.light_plot, text="", command=self.plot_signal, width=40, height=40, fg_color="#bfb5a1", hover_color="#afafaf", corner_radius=20)
        self.plot.grid(row=4, column=0, pady=10, padx=10, sticky="ew")
        
        self.theme_switch = ctk.CTkSwitch(self.main_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_switch.grid(row=6, column=0, pady=10, padx=10, sticky="sw")
        
        self.canvas_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, border_width=2, width=700, height=350)
        self.canvas_frame.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
        
        self.fig, self.ax = plt.subplots(figsize=(7, 3.5), dpi=100)
        if self.current_theme == "Dark":
            self.ax.set_facecolor("#2b2b2b")  
            self.fig.patch.set_facecolor("#2b2b2b")
            self.ax.grid(True, linestyle="--", alpha=0.6, color="white")
        else:
            self.ax.set_facecolor("#dbdbdb")  
            self.fig.patch.set_facecolor("#dbdbdb")
            self.ax.grid(True, linestyle="--", alpha=0.6, color="black")
        self.ax.set_title("Audio Analyzer")  
        self.ax.set_ylabel("Amplitude")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.audio_data1 = None  
        self.audio_data2 = None  
        self.sample_rate = 44100  
        self.timer_id = None
        # self.canvas = None
        
        record1_img = Image.open("images/light_mic1.png")
        record1_img.thumbnail((50, 50), Image.LANCZOS) 
        self.record1_img = ImageTk.PhotoImage(record1_img)
        self.update_theme()

    def toggle_theme(self):
        self.current_theme = "Dark" if self.current_theme == "Light" else "Light"
        ctk.set_appearance_mode(self.current_theme)
        self.update_theme()
        
    def update_theme(self):
        self.update_graph_theme()
        print({self.current_theme})
        if self.current_theme == "Dark":
            self.mic1.configure(image=self.dark_mic1)
            self.mic2.configure(image=self.dark_mic2)
            self.restart.configure(image=self.dark_restart)
            self.plot.configure(image=self.dark_plot)
            self.upload.configure(image=self.dark_upload)
            self.clear.configure(image=self.dark_clear)
            self.save.configure(image=self.dark_save)
            
            self.mic1.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.mic2.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.restart.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.plot.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.upload.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.clear.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            self.save.configure(fg_color="#9d9d9d", hover_color="#8d8b8b")
            
            
        else:
            self.mic1.configure(image=self.light_mic1)
            self.mic2.configure(image=self.light_mic2)
            self.restart.configure(image=self.light_restart)
            self.plot.configure(image=self.light_plot)
            self.upload.configure(image=self.light_upload)
            self.clear.configure(image=self.light_clear)
            self.save.configure(image=self.light_save)
            
            self.mic1.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.mic2.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.restart.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.plot.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.upload.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.clear.configure(fg_color="#bfb5a1", hover_color="#afafaf")
            self.save.configure(fg_color="#bfb5a1", hover_color="#afafaf")
        
        self.done_recording()
        
    def done_recording(self):
        if self.audio_data1 is not None:
            self.mic1.configure(image=self.mic_done, state=tk.DISABLED)
        else:
            if self.current_theme == "Dark":
                self.mic1.configure(image=self.dark_mic1)
            else:
                self.mic1.configure(image=self.light_mic1)
                
        if self.audio_data2 is not None:
            self.mic2.configure(image=self.mic_done)
        else:
            if self.current_theme == "Dark":
                self.mic2.configure(image=self.dark_mic2)
            else:
                self.mic2.configure(image=self.light_mic2)
    
    def update_graph_theme(self):
        if not hasattr(self, 'canvas') or self.canvas is None:
            print("Canvas is not initialized yet. Skipping theme update.")
            return  

        bg_color = "#2b2b2b" if self.current_theme == "Dark" else "#dbdbdb"
        text_color = "white" if self.current_theme == "Dark" else "black"
        grid_color = "white" if self.current_theme == "Dark" else "black"

        self.canvas.figure.patch.set_facecolor(bg_color)

        for ax in self.canvas.figure.axes:
            ax.set_facecolor(bg_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            ax.grid(color=grid_color, linestyle="--", linewidth=0.5)
            for spine in ax.spines.values():
                spine.set_edgecolor(grid_color)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color(text_color)

        self.canvas.draw()
    
    def record_audio_gui(self, input_num):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        
        def record_and_store():
            audio_data = record_audio(duration=5.0, sample_rate=44100)
            if input_num == 1:
                self.audio_data1 = audio_data
                self.mic2.configure(state=tk.NORMAL)  
                self.mic1.configure(state=tk.DISABLED) 
                self.mic1.configure(image=self.mic_done)
            else:
                self.audio_data2 = audio_data
                self.mic2.configure(image=self.mic_done)
                
            if self.audio_data1 is not None and self.audio_data2 is not None:
                self.mic1.configure(state=tk.DISABLED) 
                self.mic2.configure(state = tk.DISABLED)
                self.mic2.configure(image=self.mic_done)

        self.update_timer(5)
        threading.Thread(target=record_and_store, daemon=True).start()
        
    def restart_recording(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.audio_data1 = None
        self.audio_data2 = None
        self.mic1.configure(state=tk.NORMAL)
        self.mic2.configure(state=tk.DISABLED) 
        self.countdown_label.configure(text="")
        messagebox.showinfo("Restart", "Recordings have been reset. Please start again.")
        
        self.clear_graph()
        
        current_state = self.theme_switch.get()
        if current_state == "Dark":
            self.mic1.configure(image=self.dark_mic1, fg_color="#9d9d9d")
            self.mic2.configure(image=self.dark_mic2, fg_color="#9d9d9d")
        else:
            self.mic1.configure(image=self.light_mic1, fg_color="#bfb5a1")
            self.mic2.configure(image=self.light_mic2, fg_color="#bfb5a1")
        
    def update_timer(self, seconds_left):
        if seconds_left > 0:
            self.countdown_label.configure(text=f"Recording... {seconds_left}s left")
            self.timer_id = self.after(1000, lambda: self.update_timer(seconds_left - 1))  
        else:
            self.countdown_label.configure(text="Recording Complete!")
            self.timer_id = None 
            
    def plot_signal(self, event=None):  
        if self.audio_data1 is None or self.audio_data2 is None:
            messagebox.showwarning("No Data", "Please record or upload audio first.")
            return
        self.clear_graph()
        expected_samples = 5 * self.sample_rate  

        self.audio_data1 = np.pad(self.audio_data1, (0, max(0, expected_samples - len(self.audio_data1))))
        self.audio_data2 = np.pad(self.audio_data2, (0, max(0, expected_samples - len(self.audio_data2))))
        self.audio_data1 = self.audio_data1[:expected_samples]
        self.audio_data2 = self.audio_data2[:expected_samples]

        combined_signal = (self.audio_data1 + self.audio_data2) / 2 

        t_combined = np.linspace(0, 5, expected_samples)

        freqs1, fft_values1 = compute_fft(self.audio_data1, self.sample_rate)
        freqs2, fft_values2 = compute_fft(self.audio_data2, self.sample_rate)
        freqs_combined, fft_values_combined = compute_fft(combined_signal, self.sample_rate)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        selected_mode = self.mode_var.get()
        
        if selected_mode == "Oscilloscope":
            fig, axs = plt.subplots(1, 1, figsize=(10, 8))
            axs.plot(t_combined, self.audio_data1, color="g", linestyle=(0, (3, 10, 1, 10)), label="Signal 1")
            axs.plot(t_combined, self.audio_data2, color="m", linestyle=(0, (5, 10)), label="Signal 2")
            axs.plot(t_combined, combined_signal, linestyle="--", color="b", label="composite Signal")
            axs.set_title("Oscilloscope - Signals")
            axs.legend()
        else:
            fig, axs = plt.subplots(1, 3, figsize=(15, 5)) # 1 row, 3 columns
            for ax in axs:
                ax.set_facecolor("black")
            fig.patch.set_facecolor("black")
            axs[0].plot(freqs1, fft_values1, color="g")
            axs[0].set_title("Spectrum - Signal 1")

            axs[1].plot(freqs2, fft_values2, color="m")
            axs[1].set_title("Spectrum - Signal 2")

            axs[2].plot(freqs_combined, fft_values_combined, color="r")
            axs[2].set_title("Spectrum - Composite Signal")
            plt.tight_layout() 

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        self.update_graph_theme()

    def upload_wav(self):
        filenames = filedialog.askopenfilenames(filetypes=[("WAV files", "*.wav")])
        
        if len(filenames) != 2:
            messagebox.showwarning("Upload Error", "You must select exactly two audio files.")
            return

        messagebox.showinfo("Upload", "Both recordings are ready to be uploaded.")
        sample_rate1, self.audio_data1 = read_wav_file(filenames[0])
        sample_rate2, self.audio_data2 = read_wav_file(filenames[1])
        
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.plot_signal()
        self.done_recording()
    def clear_graph(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.fig, self.ax = plt.subplots(figsize=(7, 3.5), dpi=100)

        if self.current_theme == "Dark":
            self.ax.set_facecolor("#2b2b2b")  
            self.fig.patch.set_facecolor("#2b2b2b")
            self.ax.grid(True, linestyle="--", alpha=0.6, color="white")
            
        else:
            self.ax.set_facecolor("#dbdbdb")  
            self.fig.patch.set_facecolor("#dbdbdb")
            self.ax.grid(True, linestyle="--", alpha=0.6, color="black")

        self.ax.set_title("Audio Analyzer")  
        self.ax.set_ylabel("Amplitude")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.draw() 
        self.update_graph_theme()
            
    def save_graph(self):
        if self.canvas and self.canvas.figure:
            fig = self.canvas.figure
            has_data = any(ax.has_data() for ax in fig.axes)

            if has_data:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".jpg",
                    filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
                )
                if save_path:
                    fig.savefig(save_path, format="jpeg", dpi=300)
                    messagebox.showinfo("Success", f"Plot saved as {save_path}")
            else:
                messagebox.showwarning("Save Error", "No plot available to save. Generate a plot first.")
        else:
            messagebox.showwarning("Save Error", "No plot available to save. Generate a plot first.")
            

if __name__ == "__main__":
    app = Application()
    app.mainloop()
