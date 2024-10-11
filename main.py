import customtkinter as ctk
from tkinter import Label
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from image_widgets import *  # Assuming this contains your custom widgets
from menu import *  # Assuming this handles additional UI elements
from reversible_data_hiding.image_encryption2 import encrypt_image
from reversible_data_hiding.data_embedding import data_embedding_paper
from reversible_data_hiding.ch_data_extraction_ver1 import decrypt_image, data_extraction
from reversible_data_hiding.evaluate import calculate_psnr, run_experiment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        self.geometry('1000x600')
        self.title('Watermarking App')
        self.minsize(1000, 600)

        # Store user inputs
        self.secret_data = None
        self.data_hiding_key = None
        self.key = None
        self.block_size = None

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # Widget to import the image
        self.image_import = ImageImport(self, self.import_image)

        # Statistics frame placeholder
        self.statistics_frame = None

        # Run the main loop
        self.mainloop()

    def import_image(self, path):
        self.image_path = path  # Store image path
        
        # Get the file extension and check if it's supported
        supported_formats = ['tiff']
        file_extension = path.split('.')[-1].lower()

        if file_extension not in supported_formats:
            self.show_error_message("Unsupported format. Please use .tiff")
            return  # Stop further processing

        try:
            self.image = Image.open(path)
            self.image_tk = ImageTk.PhotoImage(self.image)

            # Clear grid and add output and close button
            self.image_import.grid_forget()
            self.image_output = ImageOutput(self, self.resize_image)
            self.close_button = CloseOutput(self, self.close_edit)

            # Menu for settings
            self.menu = Menu(self, self.submit_watermark, self.submit_decryption)
        
        except Exception as e:
            self.show_error_message(f"Failed to load image: {str(e)}")


    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        # Recreate the import
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):
        # Function to resize the image
        self.image_output.delete("all")
        self.image_output.create_image(event.width / 2, event.height / 2, image=self.image_tk)

    def show_error_message(self, message):
        """
        Display an error message to the user in a popup.
        """
        messagebox.showerror("Error", message)
        
    def submit_watermark(self, algorithm, watermark_text, data_hiding_key, key):
        """
        Handle encryption and watermark embedding based on the user's input.
        """
        try:
            # Ensure the image is in a supported format
            supported_formats = ['tiff']
            file_extension = self.image_path.split('.')[-1].lower()

            if file_extension not in supported_formats:
                raise ValueError("Unsupported format. Please use .tiff.")

            # Check if the key is exactly 16 bytes long
            if len(key) != 16:
                raise ValueError("Key must be 16 bytes (128 bits) long.")
            
            # Continue with the watermark embedding
            encrypted_image_path = "encrypted_image.tiff"
            embedded_image_path = "embedded_image.tiff"
            self.key = key.encode('utf-8')  # Convert the key to bytes
            self.block_size = 32
            self.data_hiding_key = int(data_hiding_key)
            self.secret_data = watermark_text

            # Encrypt the image
            encrypt_image(self.image_path, encrypted_image_path, self.key)

            # Embed the watermark text
            data_embedding_paper(encrypted_image_path, watermark_text, embedded_image_path, self.block_size, self.data_hiding_key)

            # Display the watermarked image
            self.image = Image.open(embedded_image_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_output.create_image(self.image_output.winfo_width() / 2, self.image_output.winfo_height() / 2, image=self.image_tk)

            # Update statistics tab
            if self.statistics_frame is not None:
                self.statistics_frame.set_inputs(self.secret_data, self.data_hiding_key, self.key)

        except ValueError as e:
            # Display error message for unsupported format or invalid key
            self.show_error_message(str(e))
        except Exception as e:
            # Catch any other exceptions
            self.show_error_message(f"An unexpected error occurred: {str(e)}")


    def submit_decryption(self, encrypted_image_path, key, block_size, data_hiding_key):
        try:
            # Ensure the image is in a supported format
            supported_formats = ['tiff']
            file_extension = self.image_path.split('.')[-1].lower()

            if file_extension not in supported_formats:
                raise ValueError("Unsupported format. Please use .tiff.")

            # Check if the key is exactly 16 bytes long
            if len(key) != 16:
                raise ValueError("Key must be 16 bytes (128 bits) long.")
            
            # Continue with decryption
            decrypted_image_path = "decrypted_image.tiff"
            output_image_path = "output_image_with_extracted_data.tiff"
            self.key = key.encode('utf-8')
            self.block_size = block_size
            self.data_hiding_key = int(data_hiding_key)

            # Decrypt the image and extract watermark
            decrypt_image(encrypted_image_path, decrypted_image_path, self.key)
            extracted_message = data_extraction(decrypted_image_path, output_image_path, self.block_size, self.data_hiding_key)

            # Display the decrypted image
            self.image = Image.open(output_image_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_output.create_image(self.image_output.winfo_width() / 2, self.image_output.winfo_height() / 2, image=self.image_tk)

            # Show extracted watermark message
            self.decrypted_message_label = Label(self, text=f"Extracted Message: {extracted_message}", font=("Helvetica", 12))
            self.decrypted_message_label.grid(row=1, column=1, pady=20)

            # Pass paths for statistics update
            if self.statistics_frame:
                self.statistics_frame.set_paths(self.image_path, decrypted_image_path)

        except ValueError as e:
            # Display error message for unsupported format or invalid key
            self.show_error_message(str(e))
        except Exception as e:
            # Catch any other exceptions
            self.show_error_message(f"An unexpected error occurred: {str(e)}")


class Menu(ctk.CTkTabview):
    def __init__(self, parent, submit_watermark_func, submit_decryption_func):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.my_font = ctk.CTkFont(family="Helvetica", weight="bold")

        # Add tabs
        self.add('Watermarking')
        self.add('Decryption')
        self.add('Statistics')

        # Add frames
        WatermarkingFrame(self.tab('Watermarking'), submit_watermark_func)
        DecryptionFrame(self.tab('Decryption'), submit_decryption_func)
        parent.statistics_frame = StatisticsFrame(self.tab('Statistics'))

class StatisticsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')
        self.original_image_path = None
        self.decrypted_image_path = None
        self.secret_data = None
        self.data_hiding_key = None
        self.key = None

        # PSNR and BER labels
        self.psnr_label = ctk.CTkLabel(self, text="PSNR: N/A", font=("Helvetica", 12))
        self.psnr_label.pack(pady=10)

        self.ber_label = ctk.CTkLabel(self, text="BER: N/A", font=("Helvetica", 12))
        self.ber_label.pack(pady=10)

        # Button to calculate and show statistics
        self.stat_button = ctk.CTkButton(self, text="Calculate Statistics", command=self.calculate_and_show_statistics)
        self.stat_button.pack(pady=20)

        # Placeholder for the graph
        self.canvas = None

    # Method to set paths for original and decrypted images
    def set_paths(self, original_image_path, decrypted_image_path):
        self.original_image_path = original_image_path
        self.decrypted_image_path = decrypted_image_path
        print(f"Set paths: original={self.original_image_path}, decrypted={self.decrypted_image_path}")

    # Method to set inputs from watermarking
    def set_inputs(self, secret_data, data_hiding_key, key):
        self.secret_data = secret_data
        self.data_hiding_key = data_hiding_key
        self.key = key
        print(f"Set inputs: secret_data={self.secret_data}, data_hiding_key={self.data_hiding_key}, key={self.key}")

    def calculate_and_show_statistics(self):
        # Check if paths and inputs are set
        if self.original_image_path is None or self.decrypted_image_path is None:
            print("Error: Image paths not set!")
            return

        if self.secret_data is None or self.data_hiding_key is None or self.key is None:
            print("Error: Inputs not set!")
            return

        block_sizes = [4, 8, 16, 32, 64]
        output_path = 'recovered_image.tiff'

        # Run experiment
        try:
            block_sizes, ber_values = run_experiment(self.original_image_path, output_path, self.secret_data, self.key, block_sizes, self.data_hiding_key)
        except Exception as e:
            print(f"Error during experiment: {e}")
            return

        # Calculate and show PSNR
        try:
            psnr_value = calculate_psnr(self.original_image_path, self.decrypted_image_path)
            self.psnr_label.configure(text=f"PSNR: {psnr_value:.2f} dB")
        except Exception as e:
            print(f"Error calculating PSNR: {e}")
            return

        # Update BER value (for block size 32 as an example)
        try:
            ber_value = ber_values[block_sizes.index(32)]
            self.ber_label.configure(text=f"BER: {ber_value:.2f}%")
        except Exception as e:
            print(f"Error calculating BER: {e}")
            return

        # Plot BER graph
        try:
            self.plot_ber_graph(block_sizes, [ber_values], [self.original_image_path])
        except Exception as e:
            print(f"Error plotting BER graph: {e}")

    def plot_ber_graph(self, block_sizes, ber_results, image_names):
        fig, ax = plt.subplots(figsize=(6, 4))
        for ber_values, image_name in zip(ber_results, image_names):
            ax.plot(block_sizes, ber_values, marker='o', label=image_name)

        ax.set_title('Extracted-Bit Error Rate with Respect to Block Sizes')
        ax.set_xlabel('Block Size')
        ax.set_ylabel('Extracted-bit Error Rate (%)')
        ax.grid(True)

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20)

class DecryptionFrame(ctk.CTkFrame):
    def __init__(self, parent, submit_decryption_func):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.image_path_label = ctk.CTkLabel(self, text="Enter path of encrypted image:", font=("Helvetica", 12))
        self.image_path_label.pack(pady=10)

        self.image_path_entry = ctk.CTkEntry(self, width=200)
        self.image_path_entry.pack(pady=10)

        self.key_label = ctk.CTkLabel(self, text="Enter decryption key (16 bytes):", font=("Helvetica", 12))
        self.key_label.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, width=200)
        self.key_entry.pack(pady=10)

        self.block_size_label = ctk.CTkLabel(self, text="Enter block size:", font=("Helvetica", 12))
        self.block_size_label.pack(pady=10)

        self.block_size_entry = ctk.CTkEntry(self, width=200)
        self.block_size_entry.pack(pady=10)

        self.data_hiding_key_label = ctk.CTkLabel(self, text="Enter data hiding key:", font=("Helvetica", 12))
        self.data_hiding_key_label.pack(pady=10)

        self.data_hiding_key_entry = ctk.CTkEntry(self, width=200)
        self.data_hiding_key_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Decrypt", command=lambda: submit_decryption_func(
            self.image_path_entry.get(),
            self.key_entry.get(),
            int(self.block_size_entry.get()),
            int(self.data_hiding_key_entry.get())
        ))
        self.submit_button.pack(pady=20)

class WatermarkingFrame(ctk.CTkFrame):
    def __init__(self, parent, submit_watermark_func):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.method_label = ctk.CTkLabel(self, text="Choose Watermarking Algorithm:", font=("Helvetica", 12))
        self.method_label.pack(pady=10)

        self.method_var = ctk.StringVar(value="Algorithm 1")
        self.method_menu = ctk.CTkOptionMenu(self, values=["Algorithm 1", "Algorithm 2"], variable=self.method_var)
        self.method_menu.pack(pady=10)

        self.text_input_label = ctk.CTkLabel(self, text="Enter the text to watermark:", font=("Helvetica", 12))
        self.text_input_label.pack(pady=10)

        self.text_input = ctk.CTkEntry(self, width=200)
        self.text_input.pack(pady=10)

        self.data_hiding_key_label = ctk.CTkLabel(self, text="Enter data hiding key:", font=("Helvetica", 12))
        self.data_hiding_key_label.pack(pady=10)

        self.data_hiding_key_entry = ctk.CTkEntry(self, width=200)
        self.data_hiding_key_entry.pack(pady=10)

        self.key_label = ctk.CTkLabel(self, text="Enter encryption key (16 bytes):", font=("Helvetica", 12))
        self.key_label.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, width=200)
        self.key_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=lambda: submit_watermark_func(
            self.method_var.get(), self.text_input.get(), self.data_hiding_key_entry.get(), self.key_entry.get()))
        self.submit_button.pack(pady=20)

if __name__ == "__main__":
    App()
