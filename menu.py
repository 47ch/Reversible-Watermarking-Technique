# import customtkinter as ctk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# from reversible_data_hiding.image_encryption2 import encrypt_image
# from reversible_data_hiding.data_embedding import data_embedding_paper

# class Menu(ctk.CTkTabview):
#     def __init__(self, parent):
#         super().__init__(master=parent)
#         self.grid(row=0, column=0, sticky='nsew')

#         self.my_font = ctk.CTkFont(family="Helvetica", weight="bold")
#         # Add tabs
#         self.add('Watermarking')
#         self.add('Statistics')

#         # Add frames
#         WatermarkingFrame(self.tab('Watermarking'))


# class WatermarkingFrame(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(master=parent)
#         self.pack(expand=True, fill='both')

#         # Add watermarking method selection
#         self.method_label = ctk.CTkLabel(self, text="Choose Watermarking Algorithm:", font=("Helvetica", 12))
#         self.method_label.pack(pady=10)

#         self.method_var = ctk.StringVar(value="Algorithm 1")
#         self.method_menu = ctk.CTkOptionMenu(self, values=["Algorithm 1", "Algorithm 2"], variable=self.method_var)
#         self.method_menu.pack(pady=10)

#         # Add input box for watermark text
#         self.text_input_label = ctk.CTkLabel(self, text="Enter the text to watermark:", font=("Helvetica", 12))
#         self.text_input_label.pack(pady=10)

#         self.text_input = ctk.CTkEntry(self, width=200)
#         self.text_input.pack(pady=10)

#         # Add button to choose image
#         self.image_path = None
#         self.choose_image_button = ctk.CTkButton(self, text="Choose Image", command=self.open_image_dialog)
#         self.choose_image_button.pack(pady=10)

#         # Add submit button
#         self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_watermark)
#         self.submit_button.pack(pady=20)

#         # Image output panel
#         self.output_canvas = ctk.CTkCanvas(self, width=400, height=400)
#         self.output_canvas.pack(pady=10)

#     def open_image_dialog(self):
#         # Open dialog to choose the image
#         self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.tiff;*.png;*.jpg;*.jpeg;*.bmp")])
#         if self.image_path:
#             print(f"Selected image: {self.image_path}")

#     def submit_watermark(self):
#         if not self.image_path:
#             print("Please choose an image first.")
#             return
        
#         # Get the selected algorithm and input text
#         selected_algorithm = self.method_var.get()
#         watermark_text = self.text_input.get()
#         print(f"Selected Watermarking Algorithm: {selected_algorithm}")
#         print(f"Watermark Text: {watermark_text}")

#         if selected_algorithm == "Algorithm 1":
#             self.apply_algorithm_1(watermark_text)
#         # elif selected_algorithm == "Algorithm 2":
#         #     self.apply_algorithm_2(watermark_text)

#     def apply_algorithm_1(self, watermark_text):
#         print(f"Applying Watermarking Algorithm 1 with text: {watermark_text}")
#         try:
#             key = b'pzkUHwYaLVLml0hh'
#             encrypted_image_path = "encrypted_image.tiff"
#             embedded_image_path = "embedded_image.tiff"
            
#             # Step 1: Encrypt the image
#             encrypt_image(self.image_path, encrypted_image_path, key)

#             # Step 2: Embed the watermark text into the encrypted image
#             data_embedding_paper(encrypted_image_path, watermark_text, embedded_image_path, block_size=32, data_hiding_key=1234)

#             # Display the result
#             self.display_output_image(embedded_image_path)
        
#         except Exception as e:
#             print(f"Error during watermarking process: {e}")

#     def display_output_image(self, image_path):
#         # Load the output image and display it in the canvas
#         output_image = Image.open(image_path)
#         output_image_tk = ImageTk.PhotoImage(output_image)

#         # Clear the previous image
#         self.output_canvas.delete("all")
#         self.output_canvas.create_image(200, 200, image=output_image_tk, anchor='center')
#         self.output_canvas.image = output_image_tk  # Keep a reference to avoid garbage collection
