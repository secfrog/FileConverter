import fitz  # PyMuPDF
from PIL import Image
import io
import os

from threading import Thread
from customtkinter import(
    CTk,
    CTkFrame,
    CTkButton,
    CTkCheckBox,
    CTkTextbox,
    CTkProgressBar,
    CTkOptionMenu,
    StringVar,
    filedialog,
)

Folder_path = os.path.dirname(__file__)
os.chdir(Folder_path)
List_of_logs = []

class PDF2Image(CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#333333",
            corner_radius=0,
        )
        if __name__ == '__main__':
            self.pack(fill="both", expand=True)

        self.selected_pdfs = None
        
        ############################################ Add images Button
        self.select_pdfs_button = CTkButton(
            master=self,
            text="\u2b71" + "  UPLOAD PDFs ",
            font=("Times New Roman", 16),
            fg_color="#203f68",
            hover_color="#30578b",
            width=150,
            height=30,
            corner_radius=5,
            command=self.select_pdfs,
        )
        self.select_pdfs_button.pack(side="top", anchor="w", padx=20, pady = (50,0))

        ############################################ Confirm Checkbox
        option_menu = StringVar(value="PNG")
        self.menu = CTkOptionMenu(
            master=self,
            variable=option_menu,
            values=["PNG", "JPG", "JPEG"],
            fg_color="#1C526D",
            button_hover_color="#203f68"
        )
        self.menu.place(x=535, y=100)

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
        self.save_images_button = CTkButton(
            master=self,
            text="\u2b73" + "  Save to",
            font=("Times New Roman", 16),
            fg_color="#203f68",
            hover_color="#30578b",
            width=150,
            height=30,
            corner_radius=5,
            command=self.pdf_to_images,
        )
        self.save_images_button.pack(side="left", anchor="nw", pady=65)

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
    
    def select_pdfs(self):
        filetypes = [('PDF Files', '*.pdf')]

        temp_selected_pdfs = ''
        if self.selected_pdfs:
            temp_selected_pdfs = [file for file in self.selected_pdfs]

        self.selected_pdfs = filedialog.askopenfilenames(filetypes=filetypes)

        if not self.selected_pdfs:
            self.selected_pdfs = temp_selected_pdfs
        
        text=''
        for filename in self.selected_pdfs:
            text += filename+'\n'

        self.update_textbox(self.selected_files_textbox, text)

    def update_textbox(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

    def clear_textbox(self):
        self.selected_pdfs=None
        self.update_textbox(self.selected_files_textbox, text="No file selected")
    
    def pdf_to_images(self):
        confirmed = self.confirm.get()
        if self.selected_pdfs and confirmed:
            def converting():
                folder = filedialog.askdirectory()
                images_format = self.menu.get().lower()
                if folder:
                    self.error_textbox.place_forget()
                    self.select_pdfs_button.configure(state="disabled")
                    self.save_images_button.configure(state="disabled")
                    self.clear_textbox_button.configure(state="disabled")

                    self.progress_bar.set(0)
                    self.progress_bar.place(x=120,y=445)

                    total_pages = 0
                    for pdf in self.selected_pdfs:
                        pdf = fitz.open(pdf)
                        total_pages += pdf.page_count
                    
                    count = 0
                    for pdf in self.selected_pdfs:
                        pdfname = os.path.basename(os.path.normpath(pdf))
                        pdf_total_pages = fitz.open(pdf)
                        pdf_total_pages = pdf_total_pages.page_count
                        for page in range(pdf_total_pages):
                            count+=1
                            image_name = Unique_Path(folder+'/'+pdfname.replace(".pdf", f"{page+1}.{images_format}"))
                            pdf2image(pdf, page, image_name)

                            self.progress_bar.set((count)/total_pages)
                            self.progress_bar.update_idletasks()
            
                    self.after(0, self.reset_mainframe)
            try:
                Thread(target=converting).start()
            except Exception as err:
                List_of_logs.append(err+"\n")
        
        else:
            self.error_textbox.place(x=180,y=445)
            if not confirmed:
                self.update_textbox(self.error_textbox, "please confirm")
            else:
                self.update_textbox(self.error_textbox, "please select pdfs")

    
    def reset_mainframe(self):
        self.destroy()
        
        if __name__ != '__main__':
            new_mainframe = PDF2Image(self.master)
            for tab in self.master.tabs_dict:
                if self.master.tabs_dict[tab] == self:
                    self.master.tabs_dict[tab] = new_mainframe
            if len(self.master.last_active_tab) > 0:
                if self.master.tabs_dict[self.master.last_active_tab[-1]] == new_mainframe:
                    new_mainframe.pack(fill="both", expand=True)
        else:
            new_mainframe = PDF2Image(self.master)


## Pre-existing example
def pdf2image(pdf_path, page_num, output_path):
    pdf_document = fitz.open(pdf_path)
    
    page = pdf_document.load_page(page_num)

    pix = page.get_pixmap()

    img = Image.open(io.BytesIO(pix.tobytes()))

    img.save(f"{output_path}", "PNG")
    print(f"Page {page_num} from {pdf_path} saved as {output_path}")

    
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
    root.title("pdf2image")
    root.iconbitmap(bitmap="assets/frog.ico")
    
    app = PDF2Image(root)

    root.mainloop()