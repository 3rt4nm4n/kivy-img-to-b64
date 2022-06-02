import base64
from importlib.resources import path
from PIL import Image
from kivy.core.window import Window
from kivy.lang import Builder
import os
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform

KV = '''
#:import Clipboard kivy.core.clipboard.Clipboard
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "MDFileManager"
        elevation: 10

    FloatLayout:
    
        MDTextField:
            id: base64txt
            mode: "rectangle"
            readonly: True
            pos_hint: {'center_x': .5, 'y': .5}
            on_double_tap: Clipboard.copy(self.text)
            size_hint: [.5, .3]
            multiline: True
            helper_text: "Double tap to copy to clipboard"

        MDTextField:
            id: heightsize
            mode: "rectangle"
            pos_hint: {'center_x': .4, 'y': .3}
            size_hint: [.1, .12]
            text: "150"
            hint_text: "Height size"

        MDTextField:
            id: widthsize
            mode: "rectangle"
            pos_hint: {'center_x': .6, 'y': .3}
            size_hint: [.1, .12]
            text: "150"
            hint_text: "Width size"
   
        MDFillRoundFlatIconButton:
            text: "Upload an Image"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .1}
            on_release: app.file_manager_open()



        
'''


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            #preview=True
        )

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        PATH ="."
        if platform == "android":
          from android.permissions import request_permissions, Permission
          request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
          app_folder = os.path.dirname(os.path.abspath(__file__))
          PATH = "/storage/emulated/0" 
        self.file_manager.show(PATH)  
        self.manager_open = True

    def select_path(self, path):
        self.root.ids.base64txt.text=""
        self.exit_manager()  
        toast("Loading "+path)
        image = Image.open(path)
        image = image.convert('RGB')
        sizey=self.root.ids.heightsize.text
        sizex=self.root.ids.widthsize.text
        if not sizex and not sizey:
            resizedimage=image.resize((150,150))
        else:
            resizedimage=image.resize((int(sizex),int(sizey)))
        resizedimage.save(path+"_resized.jpg") 
        with open(path+"_resized.jpg","rb") as img_file:
        #   encode image to base64 string
            base64_string = base64.b64encode(img_file.read())
        self.root.ids.base64txt.text = base64_string
        

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

MainApp().run()