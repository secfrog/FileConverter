import sys

from customtkinter import(
    CTk,
    CTkFrame,
    CTkButton,
    set_appearance_mode,
    set_default_color_theme,
)

from image2pdf import MainFrame

class App(CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#181818",
            corner_radius=0,
        )
        self.pack(fill="both", expand=True)

        self.tabsline = TABS_LINE(self)

        self.tabnum = 1
        self.tabs_dict = dict()
        self.last_active_tab = []
        
        self.default_tab = TAB(self.tabsline)
        self.default_main_frame = MainFrame(self)
        
        self.tabs_dict.update({self.default_tab:self.default_main_frame})
        self.last_active_tab.append(self.default_tab)
        
        self.tabsline.set_active_tab(self.default_tab)

        self.close_default_tab = CLOSE_TAB(self.default_tab)
        self.default_add_tab = ADD_TAB(self.tabsline)

        
    
    
    def manage_tabs(self, activetab): # managing tabs
        if len(self.last_active_tab) > 0:
            if activetab != self.last_active_tab[-1]:
                self.last_active_tab.append(activetab) # used when closing tab

        for tab in self.tabs_dict:
            if tab != activetab:                
                tab.configure(fg_color="#181818", hover_color="#282828")
                self.tabs_dict[tab].pack_forget()
            else:
                tab.configure(fg_color="#333333", hover_color="#333333")
                self.tabs_dict[tab].pack(fill="both", expand=True)
                
    
class TABS_LINE(CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            height=35,
            fg_color="#181818",
            corner_radius=0,
        )
        self.pack(side="top", anchor="nw", fill="x")
    
    def set_active_tab(self, tab):
        self.master.manage_tabs(tab)

class TAB(CTkButton):
    def __init__(self, master):
        super().__init__(
            master,
            text="  𓆏     New Tab",
            font=("Times New Roman", 16),
            anchor='w',
            hover=True,
            corner_radius=0,
            width=125,
            height=35,
            command=lambda: self.master.set_active_tab(self),
        )
        self.pack(fill="y", ipadx=50, side="left", anchor="nw")
        self.pack_propagate(False)

    

class CLOSE_TAB(CTkButton):
    def __init__(self, master):
        super().__init__(
            master,
            text="\u2715",
            fg_color="#333333",
            hover_color="#3D3D3D",
            width=6,
            height=6,
            corner_radius=50,
            command=self.close,
        )
        self.pack(side="right", padx=10)
    
    def close(self):
        if self.master.master.master.tabnum == 1:
            sys.exit()
        else:
            self.master.master.master.tabnum -= 1
            self.master.destroy()
            self.master.master.master.tabs_dict[self.master].destroy()
            del self.master.master.master.tabs_dict[self.master]
            self.master.master.master.last_active_tab = [tab for tab in self.master.master.master.last_active_tab if tab != self.master]
            self.master.master.master.manage_tabs(self.master.master.master.last_active_tab[-1])
    
class ADD_TAB(CTkButton):
    def __init__(self, master):
        super().__init__(
            master,
            text="+",
            font=("Times New Roman", 20),
            text_color="white",
            fg_color="#3D3D3D",
            hover_color="grey",
            width=35,
            height=35,
            corner_radius=0,
            command=self.add,
        )
        self.configure(cursor="arrow")
        self.pack(side="left", ipady=2,ipadx=3)
        self.pack_propagate(False)
    
    def add(self):
        if self.master.master.tabnum < 4:
            self.master.master.tabnum += 1
            self.destroy()
            self.master.master.tabs_dict[self.master.master.last_active_tab[-1]].pack_forget()
            newtab = TAB(self.master)
            newmainframe = MainFrame(self.master.master)
            newclosebutton = CLOSE_TAB(newtab)
            newaddbutton = ADD_TAB(self.master)
            self.master.master.tabs_dict.update({newtab:newmainframe})
            self.master.set_active_tab(newtab)



if __name__ == '__main__':
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")

    root = CTk()
    root.geometry("700x700")
    root.title("File Converter")
    root.iconbitmap(bitmap="frog.ico")

    app = App(root)
    root.mainloop()