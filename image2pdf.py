from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os

from threading import Thread
from customtkinter import(
    CTk,
    CTkFrame,
    CTkButton,
    CTkCheckBox,
    CTkTextbox,
    CTkProgressBar,
    filedialog,
)

Folder_path = os.path.dirname(__file__)
os.chdir(Folder_path)
List_of_logs = []

class MainFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#333333",
            corner_radius=0,
        )
        if __name__ == '__main__':
            self.pack(fill="both", expand=True)

        self.selected_images = None
        self.output_pdf_name = None


        ############################################ Add images Button
        self.select_images_button = CTkButton(
            master=self,
            text="\u2b71" + "  UPLOAD FILES ",
            font=("Times New Roman", 16),
            fg_color="#203f68",
            hover_color="#30578b",
            width=150,
            height=30,
            corner_radius=5,
            command=self.select_images,
        )
        self.select_images_button.pack(side="top", anchor="w", padx=20, pady = (50,0))

        ############################################ Confirm Checkbox
        self.confirm = CTkCheckBox(
            master=self,
            text="Confirm",
            font=("Times New Roman", 14),
            checkbox_height=20,
            checkbox_width=20,
            border_width=2,
            border_color="#4A4A4A",
            corner_radius=5,
        )
        self.confirm.pack(side="top", anchor="w", padx = 30, pady=(20,0))


        ############################################ Selected Files Textbox
        self.selected_files_textbox = CTkTextbox(
            master=self,
            font=("Times New Roman", 16),
            text_color="gray",
            activate_scrollbars=False,
            fg_color="#404040",
            width=500,
            height=300,
        )
        self.selected_files_textbox.insert("0.0", "No file selected")
        self.selected_files_textbox.configure(state="disabled", cursor="arrow")  # Read-only
        self.selected_files_textbox.pack(side="top", anchor="w", padx=20, pady=(10,0))

        
        ############################################ Clear Selected files button
        self.clear_textbox_button = CTkButton(
            master=self,
            text="\u2b71" + "  Clear files ",
            font=("Times New Roman", 16),
            fg_color="#203f68",
            hover_color="#30578b",
            width=150,
            height=30,
            corner_radius=5,
            command=self.clear_textbox,
        )
        self.clear_textbox_button.pack(side="left", anchor="nw", padx=(90,20), pady=65)
        


        ############################################ Save PDF to System Button
        self.save_pdf_button = CTkButton(
            master=self,
            text="\u2b73" + "  Convert",
            font=("Times New Roman", 16),
            fg_color="#203f68",
            hover_color="#30578b",
            width=150,
            height=30,
            corner_radius=5,
            command=self.images_to_pdf,
        )
        self.save_pdf_button.pack(side="left", anchor="nw", pady=65)


        ############################################ Error Logs Textbox
        self.error_textbox = CTkTextbox(
            master=self,
            font=("Times New Roman", 16),
            activate_scrollbars=False,
            text_color="orange",
            fg_color="#333333",
            width=200,
            height=20,
        )
        self.error_textbox.configure(state="disabled", cursor="arrow")
        


        ############################################ Converting Progress Bar
        self.progress_bar = CTkProgressBar(
            master=self,
            width=300,
            height=30,
            border_width=1,
            border_color="#383838",
            corner_radius=0,
            fg_color="#202020",
            progress_color="#4d5868",
            orientation="horizontal"
        )
    

    def select_images(self):
        filetypes = [('All Image Files', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp')]

        temp_selected_images = ''
        if self.selected_images:
            temp_selected_images = [file for file in self.selected_images]

        self.selected_images = filedialog.askopenfilenames(filetypes=filetypes)

        if not self.selected_images:
            self.selected_images = temp_selected_images
        
        text=''
        for filename in self.selected_images:
            text += filename+'\n'

        self.add_text_to_textbox(self.selected_files_textbox, text)
    
    def add_text_to_textbox(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

    def clear_textbox(self):
        self.selected_images=None
        self.add_text_to_textbox(self.selected_files_textbox, text="")

    def images_to_pdf(self):
        confirmed = self.confirm.get()
        if self.selected_images and confirmed:
            def converting():
                self.output_pdf_name = filedialog.asksaveasfilename(defaultextension="*.pdf", filetypes=[("PDF files", "*.pdf")])
                if self.output_pdf_name:
                    if self.output_pdf_name[-4:] != '.pdf':
                        self.output_pdf_name += '.pdf'
                    
                    self.error_textbox.place_forget()
                    self.select_images_button.configure(state="disabled")
                    self.save_pdf_button.configure(state="disabled")
                    self.clear_textbox_button.configure(state="disabled")

                    self.progress_bar.set(0)
                    self.progress_bar.place(x=120,y=445)

                    def update_progress_bar(progress):
                        self.progress_bar.set(progress)
                        self.progress_bar.update_idletasks()
                    
                    images2pdf(self.selected_images, self.output_pdf_name, update_progress_bar)
                    self.after(0, self.reset_mainframe)
            try:
                Thread(target=converting).start()
            except Exception as err:
                List_of_logs.append(err+"\n")

            
        else:
            self.error_textbox.place(x=180,y=445)
            if not confirmed:
                self.add_text_to_textbox(self.error_textbox, "please confirm")
            else:
                self.add_text_to_textbox(self.error_textbox, "please select images")
    
    def reset_mainframe(self):
        self.destroy()
        
        if __name__ != '__main__':
            new_mainframe = MainFrame(self.master)
            for tab in self.master.tabs_dict:
                if self.master.tabs_dict[tab] == self:
                    self.master.tabs_dict[tab] = new_mainframe
            if len(self.master.last_active_tab) > 0:
                if self.master.tabs_dict[self.master.last_active_tab[-1]] == new_mainframe:
                    new_mainframe.pack(fill="both", expand=True)
        else:
            new_mainframe = MainFrame(self.master)
    
    

## Pre-existing example
def images2pdf(image_paths, output_pdf, progressbarfunction=None):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    page_width, page_height = letter

    for progress, img_path in enumerate(image_paths):
        img = Image.open(img_path)
        img.thumbnail((page_width, page_height))
        img_width, img_height = img.size

        # Calculate image position to center it on the page
        x_offset = (page_width - img_width) / 2
        y_offset = (page_height - img_height) / 2

        if progressbarfunction:
            progress = (progress + 1) / len(image_paths)
            progressbarfunction(progress)

        c.drawImage(img_path, x_offset, y_offset, width=img_width, height=img_height)
        c.showPage()

    c.save()


# Source: My github FileManager repo
def Unique_Path(Path):
    Path_already_exist = True
    k = 1
    
    UniquePath = Path
    UniquePath2, extension = os.path.splitext(Path)
    while Path_already_exist:
        if os.path.exists(UniquePath):
            UniquePath = UniquePath2 + f'({k})' + extension
            k+=1
        else:
            Path_already_exist = False
    return UniquePath

def write_log_file(file):
    match os.name:
        case "nt":
            with open(file, "w") as f:
                f.write('')
            os.system(f'attrib +h {file}')
        case _:
            file = f'.{file}'
            with open(file, "w") as f:
                f.write('')
    
    with open(file, 'a') as f:
        for i in List_of_logs:
            f.write(i)
if len(List_of_logs) > 0:
    logsfile = Unique_Path('logsfile.txt')     
    write_log_file(logsfile)

if __name__ == '__main__':
    root = CTk()
    root.geometry("700x700")
    root.title("png2pdf")
    root.iconbitmap(bitmap="frog.ico")
    
    app = MainFrame(root)

    root.mainloop()