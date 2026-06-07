import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import calendar
from adresse_book import AdressBook

class CalendarWidget(tk.Frame):
    def __init__(self, parent, on_date_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_date_select = on_date_select
        self.current_date = datetime.date.today()
        self.selected_date = self.current_date
        
        self.year = self.current_date.year
        self.month = self.current_date.month
        
        self.months_fr = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
            7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        self.days_fr = ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
        
        self.bg_color = "white"
        self.primary_color = "#2196F3"
        self.accent_color = "#BBDEFB"
        self.text_color = "#333333"
        self.header_bg = "#F5F5F5"
        
        self.config(bg=self.bg_color, bd=1, relief=tk.SOLID)
        self.create_widgets()
        self.draw_calendar()
        
    def create_widgets(self):
        # Header (Month navigation)
        header = tk.Frame(self, bg=self.header_bg, pady=5)
        header.pack(fill=tk.X)
        
        self.btn_prev = tk.Button(header, text="<", font=("Helvetica", 10, "bold"), 
                                  command=self.prev_month, bd=0, bg=self.header_bg, fg=self.primary_color,
                                  activebackground=self.accent_color, cursor="hand2")
        self.btn_prev.pack(side=tk.LEFT, padx=10)
        
        self.lbl_month = tk.Label(header, text="", font=("Helvetica", 10, "bold"), bg=self.header_bg, fg=self.text_color)
        self.lbl_month.pack(side=tk.LEFT, expand=True)
        
        self.btn_next = tk.Button(header, text=">", font=("Helvetica", 10, "bold"), 
                                  command=self.next_month, bd=0, bg=self.header_bg, fg=self.primary_color,
                                  activebackground=self.accent_color, cursor="hand2")
        self.btn_next.pack(side=tk.RIGHT, padx=10)
        
        # Days of week names
        days_frame = tk.Frame(self, bg=self.bg_color)
        days_frame.pack(fill=tk.X, pady=(5, 0))
        for day in self.days_fr:
            lbl = tk.Label(days_frame, text=day, font=("Helvetica", 9, "bold"), bg=self.bg_color, fg="#757575", width=4)
            lbl.pack(side=tk.LEFT, expand=True)
            
        # Grid frame for the days numbers
        self.grid_frame = tk.Frame(self, bg=self.bg_color)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def draw_calendar(self):
        # Clear previous grid
        for child in self.grid_frame.winfo_children():
            child.destroy()
            
        self.lbl_month.config(text=f"{self.months_fr[self.month]} {self.year}")
        
        cal = calendar.monthcalendar(self.year, self.month)
        
        for r_idx, week in enumerate(cal):
            for c_idx, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.grid_frame, text="", bg=self.bg_color, width=4, height=1)
                    lbl.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                else:
                    day_date = datetime.date(self.year, self.month, day)
                    is_selected = (day_date == self.selected_date)
                    is_today = (day_date == datetime.date.today())
                    
                    if is_selected:
                        bg = self.primary_color
                        fg = "white"
                        font_weight = "bold"
                    elif is_today:
                        bg = "#E3F2FD"
                        fg = self.primary_color
                        font_weight = "bold"
                    else:
                        bg = "#F8F9FA"
                        fg = self.text_color
                        font_weight = "normal"
                        
                    btn = tk.Button(self.grid_frame, text=str(day), font=("Helvetica", 9, font_weight),
                                    bg=bg, fg=fg, bd=0, width=4, height=1, relief=tk.FLAT, cursor="hand2",
                                    command=lambda d=day_date: self.select_date(d))
                    btn.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                    
                    if not is_selected:
                        self.bind_hover(btn, bg, "#E2E6EA" if not is_today else "#BBDEFB")
                        
    def bind_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))
        
    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()
        
    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()
        
    def select_date(self, date):
        self.selected_date = date
        self.draw_calendar()
        self.on_date_select(date)


class RendezvousViewInterface:
    def get_selected_date(self) -> datetime.date:
        raise NotImplementedError

    def get_selected_contact_name(self) -> str:
        raise NotImplementedError

    def set_contact_names(self, names: list):
        raise NotImplementedError

    def set_initial_contact(self, name: str):
        raise NotImplementedError

    def show_slots(self, time_slots: list, booked: dict):
        raise NotImplementedError

    def show_error(self, title: str, message: str):
        raise NotImplementedError

    def show_warning(self, title: str, message: str):
        raise NotImplementedError

    def show_info(self, title: str, message: str):
        raise NotImplementedError

    def confirm_booking(self, time: str, date_display: str, name: str) -> bool:
        raise NotImplementedError

    def confirm_cancellation(self, time: str, date_display: str, name: str) -> bool:
        raise NotImplementedError


class RendezvousPresenter:
    def __init__(self, view: RendezvousViewInterface, model: AdressBook, initial_contact_name: str = None):
        self.view = view
        self.model = model
        self.initial_contact_name = initial_contact_name
        self.time_slots = [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
            "16:00", "16:30", "17:00", "17:30"
        ]

    def on_load(self):
        self.model.load_contacts()
        names = [c.nom for c in self.model.contacts]
        self.view.set_contact_names(names)
        
        if self.initial_contact_name and self.initial_contact_name in names:
            self.view.set_initial_contact(self.initial_contact_name)
        
        self.refresh_slots()

    def on_date_changed(self, date):
        self.refresh_slots()

    def refresh_slots(self):
        selected_date = self.view.get_selected_date()
        date_str = selected_date.isoformat()
        booked = self.model.get_rendezvous_for_date(date_str)
        self.view.show_slots(self.time_slots, booked)

    def on_book_clicked(self, time: str):
        selected_name = self.view.get_selected_contact_name()
        if not selected_name:
            self.view.show_warning("Avertissement", "Veuillez sélectionner un contact d'abord.")
            return

        contact_info = self.model.get_contact_by_name(selected_name)
        if not contact_info:
            self.view.show_error("Erreur", "Contact introuvable.")
            return

        selected_date = self.view.get_selected_date()
        date_display = selected_date.strftime("%d/%m/%Y")
        confirm = self.view.confirm_booking(time, date_display, selected_name)

        if confirm:
            date_str = selected_date.isoformat()
            success = self.model.add_rendezvous(contact_info["id"], date_str, time)
            if success:
                self.view.show_info("Succès", "Rendez-vous enregistré avec succès !")
                self.refresh_slots()
            else:
                self.view.show_error("Erreur", "Ce créneau a déjà été réservé.")

    def on_cancel_clicked(self, time: str, patient_name: str):
        selected_date = self.view.get_selected_date()
        date_display = selected_date.strftime("%d/%m/%Y")
        confirm = self.view.confirm_cancellation(time, date_display, patient_name)

        if confirm:
            date_str = selected_date.isoformat()
            success = self.model.delete_rendezvous(date_str, time)
            if success:
                self.view.show_info("Succès", "Rendez-vous annulé.")
                self.refresh_slots()
            else:
                self.view.show_error("Erreur", "Impossible d'annuler ce rendez-vous.")


class RendezvousWindow(tk.Toplevel, RendezvousViewInterface):
    def __init__(self, parent, initial_contact_nom=None):
        super().__init__(parent)
        self.title("Agenda - Gestion des Rendez-vous (30 min)")
        self.geometry("820x520")
        self.resizable(False, False)
        
        # Center the window relative to parent
        self.transient(parent)
        self.grab_set()  # Make it modal
        
        self.config(bg="#F8F9FA")
        
        # Header Label
        title_lbl = tk.Label(self, text="📅 Agenda & Gestion des Rendez-vous", font=("Helvetica", 14, "bold"), bg="#F8F9FA", fg="#1976D2")
        title_lbl.pack(pady=15)
        
        # Container frame
        body_frame = tk.Frame(self, bg="#F8F9FA")
        body_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Left Panel: Calendar Selector
        left_frame = tk.Frame(body_frame, bg="#F8F9FA")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        lbl_cal = tk.Label(left_frame, text="1. Sélectionnez une date :", font=("Helvetica", 10, "bold"), bg="#F8F9FA", fg="#495057")
        lbl_cal.pack(anchor=tk.W, pady=(0, 8))
        
        self.calendar = CalendarWidget(left_frame, self.on_calendar_date_select)
        self.calendar.pack(fill=tk.X)
        
        # Right Panel: Contact selection & time slots grid
        right_frame = tk.Frame(body_frame, bg="#F8F9FA")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Patient selector card
        contact_frame = tk.LabelFrame(right_frame, text=" 2. Patient / Contact ", font=("Helvetica", 9, "bold"), bg="#F8F9FA", fg="#495057", padx=10, pady=10)
        contact_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(contact_frame, text="Choisir le contact :", font=("Helvetica", 9), bg="#F8F9FA").pack(side=tk.LEFT, padx=(0, 5))
        
        self.contact_var = tk.StringVar()
        self.combo_contact = ttk.Combobox(contact_frame, textvariable=self.contact_var, state="readonly", width=35)
        self.combo_contact.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Time Slots layout
        slots_lbl = tk.Label(right_frame, text="3. Choisissez un créneau horaire :", font=("Helvetica", 10, "bold"), bg="#F8F9FA", fg="#495057")
        slots_lbl.pack(anchor=tk.W, pady=(0, 8))
        
        self.slots_frame = tk.Frame(right_frame, bg="#F8F9FA")
        self.slots_frame.pack(fill=tk.BOTH, expand=True)
        
        # Presenter
        self.presenter = RendezvousPresenter(self, AdressBook(), initial_contact_nom)
        self.presenter.on_load()

    # --- View Interface Implementations ---
    def get_selected_date(self) -> datetime.date:
        return self.calendar.selected_date

    def get_selected_contact_name(self) -> str:
        return self.contact_var.get()

    def set_contact_names(self, names: list):
        self.combo_contact["values"] = names
        if names:
            self.combo_contact.current(0)

    def set_initial_contact(self, name: str):
        self.combo_contact.set(name)

    def show_slots(self, time_slots: list, booked: dict):
        for child in self.slots_frame.winfo_children():
            child.destroy()
            
        selected_date = self.get_selected_date()
        date_display = selected_date.strftime("%d/%m/%Y")
        lbl_date_info = tk.Label(self.slots_frame, text=f"Statut des créneaux pour le {date_display} :", font=("Helvetica", 9, "italic"), bg="#F8F9FA", fg="#6C757D")
        lbl_date_info.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        cols = 4
        for idx, time in enumerate(time_slots):
            r = (idx // cols) + 1
            c = idx % cols
            
            is_booked = time in booked
            if is_booked:
                patient_name = booked[time]["nom"]
                btn_text = f"{time}\n[{patient_name}]"
                bg = "#FFCDD2"
                fg = "#C62828"
                hover_bg = "#EF9A9A"
                cmd = lambda t=time, p=patient_name: self.presenter.on_cancel_clicked(t, p)
            else:
                btn_text = f"{time}\n(Libre)"
                bg = "#C8E6C9"
                fg = "#2E7D32"
                hover_bg = "#A5D6A7"
                cmd = lambda t=time: self.presenter.on_book_clicked(t)
                
            btn = tk.Button(self.slots_frame, text=btn_text, font=("Helvetica", 9, "bold"),
                            bg=bg, fg=fg, bd=1, relief=tk.SOLID, width=15, height=2, cursor="hand2", command=cmd)
            btn.grid(row=r, column=c, padx=5, pady=5, sticky=tk.NSEW)
            
            self.bind_hover(btn, bg, hover_bg)
            
        for i in range(cols):
            self.slots_frame.grid_columnconfigure(i, weight=1)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def confirm_booking(self, time: str, date_display: str, name: str) -> bool:
        return messagebox.askyesno(
            "Confirmer le rendez-vous",
            f"Voulez-vous réserver le créneau {time} le {date_display} pour {name} ?"
        )

    def confirm_cancellation(self, time: str, date_display: str, name: str) -> bool:
        return messagebox.askyesno(
            "Annuler le rendez-vous",
            f"Le créneau {time} le {date_display} est réservé pour {name}.\n\nVoulez-vous annuler ce rendez-vous ?"
        )

    def bind_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def on_calendar_date_select(self, date):
        self.presenter.on_date_changed(date)


if __name__ == "__main__":
    # Test standalone window execution
    root = tk.Tk()
    root.title("Test Parent")
    root.geometry("200x200")
    
    def open_rdv():
        RendezvousWindow(root)
        
    btn = tk.Button(root, text="Ouvrir l'agenda", command=open_rdv)
    btn.pack(expand=True)
    
    root.mainloop()
