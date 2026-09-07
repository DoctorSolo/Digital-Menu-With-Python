import customtkinter as ctk
import theme_config
import webbrowser

from src.AIAgent_Ollama import AIAgent_Ollama
from PIL import Image, ImageTk


class GraphicInterface:
    def __init__(self):
        ctk.set_appearance_mode(theme_config.CONFIG_THEME_APLICATION)
        ctk.set_default_color_theme(theme_config.CONFIG_THEME_BUTTON)

        self.__interface()
    # END
    
    
    # This functions check if number
    def __validate_number(self, p) -> bool:
        if p == "" or p == "-":
            return True
        try:
            float(p)
            return True
        except ValueError:
            return False
    # END
    
    
    # This functions create a window
    def __interface(self):
        
        # Create Window
        window = ctk.CTk()
        window.title(theme_config.CONFIG_TITLE)
        window.geometry(theme_config.CONFIG_SIZE_CONFIG)
        # Create Icon App
        icon_image = ImageTk.PhotoImage(Image.open(theme_config.CONFIG_ICON))
        window.wm_iconphoto(True, icon_image)
        
        # 1. Create a main container. (Pather container)
        top_container = self.__create_container(window, 'top', 0, 0, 'both', True, None)
        
        # 2. Create a footer frame. (frame of back button and my profile)
        bottom_container = self.__create_container(window, 'bottom', None, None, 'x', False)
        
        
        # 4. Container Coordinates
        container_coordenates = self.__create_container(top_container, 'top', 5, 5,'both', True, None)
        
        # 5. Description Container
        description_container = self.__create_container(top_container, 'bottom')
        self.__description_container(description_container)
        
        # 6. Output Frame
        container_output = ctk.CTkScrollableFrame(description_container, fg_color="#D559BF")
        container_output.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)
        

        # Features
        out = self.__output(container_output)
        
        self.__create_empty_space(container_coordenates, out, container_output)
        
        self.__footer(window, bottom_container)
        
        window.mainloop()
    # END
    
    
    # This function create a frame for window
    def __create_container(self, space: (ctk.CTkFrame | ctk.CTk), side: str, padx: int=None, pady: int=None, fill: str='both', expand: bool=True, fg_color: str='transparent') -> ctk.CTkFrame:
        container = ctk.CTkFrame(space, fg_color="#F0C8E9")
        container.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
        return container
    # END
    
    
    # This function create a space for description
    def __description_container(self, container: ctk.CTkFrame):
        description = ctk.CTkLabel(
            container,
            text='Description:',
            anchor='w',
            font=('Arial', 30, 'bold'),
            text_color="#1A0113",
        )
        description.pack(side="top", anchor='w', expand=False, padx=(20, 0))
    # END
    
    
    # This function generate a title for a window
    def __generate_title(self, frame: ctk.CTkFrame):
        img = ctk.CTkImage(Image.open("assets/comida-rapida.png"), size=(50, 50))
        
        title = ctk.CTkLabel(
            frame,
            image=img,
            text="  Café da Manhã",
            compound='left',
            font=("Arial", 30, "bold"),
            text_color="#1A0113"
        )
        title.image = img
        title.pack(fill="x", expand=False, padx=(10, 10))
    # END
    
    
    def __output(self, frame: ctk.CTkScrollableFrame, serch: str = ""):
        if not serch:
            text = ""
        else:
            try:
                ai_agent = AIAgent_Ollama()
                text = ai_agent.generate_response(serch)
            except Exception:
                # If both failed
                text = serch
        
        output = ctk.CTkLabel(
            frame, 
            text=text,
            wraplength=600,
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF",
            fg_color="#D559BF"
            )
        output.pack (fill="x", expand=False)
        return output
    # END
    
    
    # Create a coordinate space
    def __create_empty_space(self, container: ctk.CTkFrame, out, out_container):
        
        self.__generate_title(container)
        # Create a containter for options
        container02 = ctk.CTkScrollableFrame(container, fg_color="#F0A3E2")
        container02.pack(padx=10, pady=10, fill="both", expand=True)
        
        from src.lib.lib_menu import breakfast_menu
        
        # A loop for options dictionary
        for indice, option in enumerate(breakfast_menu):
            
            row, column = divmod(indice, 2)        # Calculate the row and column for the button placement
            option_data = breakfast_menu[option]                # Get the option data
            img = ctk.CTkImage(Image.open(option_data["image"]), size=(100, 100))
            
            button = ctk.CTkButton(
                container02, # Put the button on button container
                text         = option_data["name"],    # Put here the title of each button
                image        = img,                     # Put here the logo of each button
                compound     = "left",                  # Define the position
                anchor       = "w",                     # Define the position
                font         = ("Arial", 22, "bold"),   # Configure font here
                text_color   = "#FFFFFF",             # Text title color
                #width        = 50,                     # Configure button width
                height       = 70,                      # Configure button height
                fg_color     = "#F84DD8",               # Configure button color
                # Define a command for each button
                command      = lambda n=option_data['name'], d=option_data['description'], a=option_data['allergies'], p=option_data['price']: self.__if_button_clicked(out_container, self.__message(n, d, a, p))
                )
                
            # keeps the image on button and put it on grid
            button.image = img
            button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
    # END
    
    
    def __message(self, name: str, description: str, allergies: str, price: float) -> str:
        string = f"""
            Nome: {name}\n
            Descrição: {description}\n
            Alergias: {allergies}\n
            Preço: R${price:.2f}
        """
        print(string)
        return string
    
        
    def __if_button_clicked(self, out_container, serch):
        self.__output(out_container, serch=serch)
    # END
    
    
    # <--------------->
    #     FOOTER
    # <--------------->
    
    
    def __footer(self, window, frame):
        footer = self.__create_container(frame, None, 10, 10, 'both', True, None)
        
        self.__signature(footer)
        self.__exit_button(window, footer)
    # END
    
    
    def __open_github(self, event) -> None:
        webbrowser.open('https://github.com/DoctorSolo')
    
    
    def __signature(self, container: ctk.CTkFrame) -> None:
        signature = ctk.CTkLabel(
            container,
            text=f'Autor: @DoctorSolo',
            font=('Arial',12,'italic','underline'),
            text_color="#27748C",
            cursor='hand2'
        )
        signature.bind("<Button-1>", self.__open_github)
        signature.pack(side='right', padx=30, pady=15)
        
    
    def __exit_button(self, window: ctk.CTk, frame: ctk.CTkFrame) -> None:
        img = ctk.CTkImage(Image.open("assets/seta-esquerda.png"), size=(20, 20))
        exit_button = ctk.CTkButton(frame,
            text="EXIT",
            image=img,
            compound="left",
            font=("Arial", 25, "bold"),
            text_color="#000000",
            fg_color="#F84DD8",
            command=window.destroy,
            #fg_color="#431580"
        )
        exit_button.image = img
        exit_button.pack(side='left', padx=30, pady=15)