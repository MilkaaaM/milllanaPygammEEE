from customtkinter import *
from socket import*
import threading

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.title('LogiTalk')
        self.label = None
        self.entry = None
        self.username = "Milana"


        # меню
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -5

        self.btn = CTkButton(self, text='▶️', command=self.toggle_show_menu, width=30)
        self.btn.place(x=0, y=0)

        # main
        self.chat_field = CTkTextbox(
            self,
            font=('Arial', 14),
            state = "disabled"
        )

        self.chat_field.place(x=0, y=0)

        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', height=40)
        self.message_entry.place(x=0, y=0)

        self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)
        self.send_button.place(x=0, y=0)

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.conect(('localhost', 8080))

        threading.Thread(target = self.recv_message(), daemch = False).start()

        self.adaptive_ui()


    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f"{self.username}: {message}")

            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass

        self.message_entry.delete(0, END)

        print("Повідомлення відправлено!")


    def recv_message(self):
        buffer = ""
        while True:
            print("Чекаю повідомлення")
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break

                buffer = chunk.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.split())
            except:
                break



    def add_message(self, text):
        self.chat_field.configure(state="normal")
        self.chat_field.insert(END, text + '\n')
        self.chat_field.configure(state="disabled")



    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='▶️')
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='◀️')
            self.show_menu()

            self.label = CTkLabel(self.menu_frame, text='Імʼя')
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack()

    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)

        if self.menu_frame.winfo_width() < 200 and self.is_show_menu:
            self.after(10, self.show_menu)

        elif self.menu_frame.winfo_width() > 40 and not self.is_show_menu:
            self.after(10, self.show_menu)

            if self.label:
                self.label.destroy()
                self.label = None

            if self.entry:
                self.entry.destroy()
                self.entry = None

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())

        self.chat_field.place(x=self.menu_frame.winfo_width(), y=0)

        self.chat_field.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width(),
            height=self.winfo_height() - 40
        )

        self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)

        self.message_entry.place(
            x=self.menu_frame.winfo_width(),
            y=self.send_button.winfo_y()
        )

        self.message_entry.configure(
            width=self.winfo_width()
                  - self.menu_frame.winfo_width()
                  - self.send_button.winfo_width()
        )

        self.after(50, self.adaptive_ui)


win = MainWindow()
win.mainloop()

