import tkinter as tk

class RoundedCanvasFrame(tk.Frame):
    def __init__(self, master=None, corner_radius=10, **kwargs):
        self.corner_radius = corner_radius
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        self.canvas.create_polygon(
            self.corner_radius, 0,
            width - self.corner_radius, 0,
            width, self.corner_radius,
            width, height - self.corner_radius,
            width - self.corner_radius, height,
            self.corner_radius, height,
            0, height - self.corner_radius,
            0, self.corner_radius,
            fill="white", outline="", tags="rounded_frame"
        )
        self.canvas.create_arc(
            0, 0,
            self.corner_radius * 2, self.corner_radius * 2,
            start=90, extent=90,
            fill="white", outline="", tags="rounded_frame"
        )
        self.canvas.create_arc(
            width - self.corner_radius * 2, 0,
            width, self.corner_radius * 2,
            start=0, extent=90,
            fill="white", outline="", tags="rounded_frame"
        )
        self.canvas.create_arc(
            width - self.corner_radius * 2, height - self.corner_radius * 2,
            width, height,
            start=270, extent=90,
            fill="white", outline="", tags="rounded_frame"
        )
        self.canvas.create_arc(
            0, height - self.corner_radius * 2,
            self.corner_radius * 2, height,
            start=180, extent=90,
            fill="white", outline="", tags="rounded_frame"
        )

root = tk.Tk()
root.title("Rounded Frame with Canvas")
root.geometry("300x200")

# Marco redondeado con Canvas
frame = RoundedCanvasFrame(root, corner_radius=20, bg="white")
frame.pack(expand=True, fill="both", padx=20, pady=20)

root.mainloop()



#------------------------------------------------------------------------------------


import tkinter as tk

class RoundedCanvasFrame(tk.Frame):
    def __init__(self, master=None, corner_radius=10, **kwargs):
        self.corner_radius = corner_radius
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()

        # Degradado
        color1 = "#333333"  # Color más oscuro
        color2 = "#000000"  # Color más claro
        for i in range(height):
            r = int(i / height * 255)
            g = int(i / height * 255)
            b = int(i / height * 255)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

        # Bordes redondeados
        self.canvas.create_polygon(
            self.corner_radius, 0,
            width - self.corner_radius, 0,
            width, self.corner_radius,
            width, height - self.corner_radius,
            width - self.corner_radius, height,
            self.corner_radius, height,
            0, height - self.corner_radius,
            0, self.corner_radius,
            fill="", outline="white", tags="rounded_frame", smooth=True
        )
        self.canvas.create_arc(
            0, 0,
            self.corner_radius * 2, self.corner_radius * 2,
            start=90, extent=90,
            fill="", outline="white", tags="rounded_frame", style="arc", width=1, smooth=True
        )
        self.canvas.create_arc(
            width - self.corner_radius * 2, 0,
            width, self.corner_radius * 2,
            start=0, extent=90,
            fill="", outline="white", tags="rounded_frame", style="arc", width=1, smooth=True
        )
        self.canvas.create_arc(
            width - self.corner_radius * 2, height - self.corner_radius * 2,
            width, height,
            start=270, extent=90,
            fill="", outline="white", tags="rounded_frame", style="arc", width=1, smooth=True
        )
        self.canvas.create_arc(
            0, height - self.corner_radius * 2,
            self.corner_radius * 2, height,
            start=180, extent=90,
            fill="", outline="white", tags="rounded_frame", style="arc", width=1, smooth=True
        )

root = tk.Tk()
root.title("Rounded Frame with Gradient Background")
root.geometry("300x200")

# Marco redondeado con Canvas
frame = RoundedCanvasFrame(root, corner_radius=20)
frame.pack(expand=True, fill="both", padx=20, pady=20)

root.mainloop()

            