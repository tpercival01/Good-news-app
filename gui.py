import tkinter as tk
from tkinter import ttk
import pandas as pd
import ttkbootstrap as ttkb  # Import ttkbootstrap

class gui:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("Good News")
        self.root.geometry("400x700")
        self.root.configure(bg="#F5F5F5")  # Very light gray background

        # Apply the ttkbootstrap theme
        style = ttkb.Style("flatly")  # You can try different themes: flatly, litera, etc.

        self.display_main_feed()

    def display_main_feed(self):
        # Clear current content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top Navigation Bar
        self.top_nav = ttkb.Frame(self.root, padding=10, style="primary.TFrame")
        self.top_nav.pack(side="top", fill="x")

        self.nav_label = ttkb.Label(
            self.top_nav,
            text="Good News",
            style="primary.Inverse.TLabel",
            font=("Helvetica", 18, "bold")
        )
        self.nav_label.pack(pady=10)

        # Scrollable Content Area
        self.content_frame = ttkb.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        # Use canvas to create scrollable area
        self.canvas = tk.Canvas(self.content_frame, bg="#F5F5F5", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttkb.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttkb.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Store reference to the canvas window
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Make the scrollable_frame width match the canvas width
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.bind_mousewheel(self.canvas)
        
        # Define styles
        style = ttkb.Style()
        style.configure("primary.TFrame", background="#0D47A1")  # Deep blue navigation bar
        style.configure("primary.Inverse.TLabel", background="#0D47A1", foreground="#FFFFFF")
        style.configure("Card.TFrame",
                        background="#FFFFFF",
                        borderwidth=0,    # No border when not hovered
                        relief="flat",
                        bordercolor="#DDDDDD",
                        borderradius=10)
        style.configure("Hover.TFrame",
                        background="#E3F2FD",  # Light blue hover color
                        borderwidth=1,    # Border appears on hover
                        relief="solid",
                        bordercolor="#DDDDDD",
                        borderradius=10)
        style.configure("ArticleTitle.TLabel",
                        background="#FFFFFF",
                        foreground="#212121")
        style.configure("ArticleSnippet.TLabel",
                        background="#FFFFFF",
                        foreground="#212121")
        style.configure("HoverArticleTitle.TLabel",
                        background="#E3F2FD",
                        foreground="#212121")
        style.configure("HoverArticleSnippet.TLabel",
                        background="#E3F2FD",
                        foreground="#212121")
        style.configure("TLabel", background="#FFFFFF", foreground="#212121")

        # Make scrollbar thinner
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background="#0D47A1",
                        darkcolor="#0D47A1",
                        lightcolor="#0D47A1",
                        troughcolor="#E0E0E0",
                        bordercolor="#E0E0E0",
                        arrowcolor="#FFFFFF",
                        thickness=10)

        # Example Articles
        for idx, row in self.df.iterrows():
            article_frame = ttkb.Frame(
                self.scrollable_frame,
                style="Card.TFrame",
                padding=10
            )
            article_frame.pack(fill="x", pady=10, padx=10)
            
            title_text = row["title"]
            description_text = row["description"] if pd.notnull(row["description"]) else ""
            snippet_text = description_text[:100] + "..." if len(description_text) > 100 else description_text

            title_label = ttkb.Label(
                article_frame,
                text=title_text,
                font=("Helvetica", 12, "bold"),
                style="ArticleTitle.TLabel",
                wraplength=350
            )
            title_label.pack(fill="x")

            snippet_label = ttkb.Label(
                article_frame,
                text=snippet_text,
                font=("Helvetica", 12),
                style="ArticleSnippet.TLabel",
                wraplength=300
            )
            snippet_label.pack(fill="x", pady=(5, 0))

            # Adjust wraplength when the label size changes
            def update_wraplength(event, label=snippet_label):
                label.configure(wraplength=label.winfo_width())

            snippet_label.bind('<Configure>', update_wraplength)

            # Cursor change and style change on hover
            def on_enter(event, frame=article_frame, title=title_label, snippet=snippet_label):
                frame.configure(style="Hover.TFrame", cursor="hand1")
                title.configure(style="HoverArticleTitle.TLabel")
                snippet.configure(style="HoverArticleSnippet.TLabel")

            def on_leave(event, frame=article_frame, title=title_label, snippet=snippet_label):
                frame.configure(style="Card.TFrame", cursor="")
                title.configure(style="ArticleTitle.TLabel")
                snippet.configure(style="ArticleSnippet.TLabel")

            # Bind hover events to article_frame and labels
            widgets = [article_frame, title_label, snippet_label]
            for widget in widgets:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

            # Make each article clickable
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, idx=idx: self.open_article(idx))


    def open_article(self, idx):
        # Clear current content to display the full article
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top Navigation Bar with Back Button
        self.top_nav = ttkb.Frame(self.root, padding=10, style="primary.TFrame")
        self.top_nav.pack(side="top", fill="x")

        self.top_nav.columnconfigure(0, weight=0)
        self.top_nav.columnconfigure(1, weight=1)

        back_button = ttkb.Button(
            self.top_nav,
            text="Back",
            command=self.display_main_feed,
            style="primary.Outline.TButton"
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        article_title = self.df.loc[idx, 'title']
        article_description = self.df.loc[idx, 'description'] if pd.notnull(self.df.loc[idx, 'description']) else ''

        self.nav_label = ttkb.Label(
            self.top_nav,
            text=article_title,
            style="primary.Inverse.TLabel",
            font=("Helvetica", 12, "bold"),
            wraplength=300,
            anchor="w",
            justify="left"
        )
        self.nav_label.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        def update_nav_wraplength(event):
            new_width = self.top_nav.winfo_width() - back_button.winfo_width() - 60  # Adjust for padding
            self.nav_label.configure(wraplength=new_width)
        
        self.top_nav.bind('<Configure>', update_nav_wraplength)

        # Full Article Content
        article_content = article_description

                # Scrollable Content Area for the full article
        content_frame = ttkb.Frame(self.root)
        content_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(content_frame, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttkb.Scrollbar(content_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")

        article_frame = ttkb.Frame(canvas)
        article_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window((0, 0), window=article_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Adjust the width of the article_frame to match the canvas
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        article_label = ttkb.Label(
            article_frame,
            text=article_content,
            font=("Helvetica", 14),
            justify="left",
            padding=20,
            style="TLabel",
            wraplength=360,
            anchor="nw"
        )
        article_label.pack(padx=20, pady=20, fill="both", expand=True)

        self.bind_mousewheel(self.canvas)

        # Adjust wraplength when the label size changes
        def update_wraplength(event, label=article_label):
            label.configure(wraplength=label.winfo_width() - 40)

        article_label.bind('<Configure>', update_wraplength)

    def bind_mousewheel(self, widget):
        # Windows and Linux systems
        widget.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(event, widget))
        # macOS systems
        widget.bind_all("<Button-4>", lambda event: self.on_mousewheel(event, widget))
        widget.bind_all("<Button-5>", lambda event: self.on_mousewheel(event, widget))

    def on_mousewheel(self, event, widget):
        if event.num == 4 or event.delta > 0:
            widget.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            widget.yview_scroll(1, "units")
