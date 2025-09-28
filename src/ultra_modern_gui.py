import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import time
import random
import json
import threading
from pathlib import Path
from datetime import datetime
from font_mapping import GUJARATI_FONTS, get_font_list, get_font_info

# Settings
CHUNK_SIZE = 200
MIN_DELAY = 2
MAX_DELAY = 5
MAX_RETRIES = 3

class UltraModernGujaratiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Ultra-Modern Gujarati Font Converter Pro")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 750)
        
        # Ultra-smooth modern color scheme with gradients
        self.colors = {
            'primary': '#667EEA',       # Soft Indigo
            'primary_dark': '#5A67D8',  # Deeper Indigo
            'primary_light': '#9F7AEA', # Light Purple
            'secondary': '#38B2AC',     # Soft Teal
            'accent': '#ED8936',        # Warm Orange
            'error': '#E53E3E',         # Soft Red
            'warning': '#DD6B20',       # Warm Orange
            'success': '#38A169',       # Forest Green
            'bg_primary': '#1A202C',    # Soft Dark Blue
            'bg_secondary': '#2D3748',  # Warm Gray
            'bg_card': '#4A5568',       # Soft Gray
            'bg_light': '#F7FAFC',      # Pure Light
            'text_primary': '#F7FAFC',  # Soft White
            'text_secondary': '#E2E8F0', # Light Gray
            'border': '#718096',        # Soft Border
            'hover': '#A0AEC0',         # Light Hover
            'shadow': '#0000001A'       # Soft Shadow
        }
        
        self.conversion_running = False
        self.session = None
        self.current_font = 'shree0768'
        self.dark_mode = True
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure ultra-modern styles"""
        self.style = ttk.Style()
        
        # Use clam theme as base
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        # Configure dark theme styles
        if self.dark_mode:
            self.configure_dark_theme()
        else:
            self.configure_light_theme()
            
    def configure_dark_theme(self):
        """Configure dark theme styles"""
        # Main window background
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure styles for smooth dark theme
        self.style.configure('Dark.TFrame', 
                           background=self.colors['bg_secondary'],
                           borderwidth=0, relief='flat')
        
        self.style.configure('Card.TFrame', 
                           background=self.colors['bg_card'],
                           borderwidth=0, relief='flat')
        
        self.style.configure('Dark.TLabel', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10))
        
        self.style.configure('Title.TLabel', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['primary_light'],
                           font=('Segoe UI', 20, 'bold'))
        
        self.style.configure('Heading.TLabel', 
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 12, 'bold'))
        
        self.style.configure('Info.TLabel', 
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 9))
        
        # Smooth button styles with gradients
        self.style.configure('Modern.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 12))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['primary_light']),
                                ('pressed', self.colors['primary_dark'])])
        
        self.style.configure('Convert.TButton',
                           background=self.colors['secondary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 14, 'bold'),
                           padding=(50, 25))
        
        self.style.map('Convert.TButton',
                      background=[('active', '#4FD1C7'),
                                ('pressed', '#319795')])
        
        # Smooth LabelFrame styles
        self.style.configure('Dark.TLabelframe',
                           background=self.colors['bg_card'],
                           borderwidth=0,
                           relief='flat')
        
        self.style.configure('Dark.TLabelframe.Label',
                           background=self.colors['bg_card'],
                           foreground=self.colors['primary_light'],
                           font=('Segoe UI', 11, 'bold'))
        
        # Smooth entry styles
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           insertcolor=self.colors['primary_light'])
        
        # Smooth combobox styles
        self.style.configure('Modern.TCombobox',
                           fieldbackground=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           background=self.colors['bg_secondary'],
                           borderwidth=0)
        
    def configure_light_theme(self):
        """Configure light theme styles"""
        self.root.configure(bg=self.colors['bg_light'])
        # Light theme configurations would go here
        
    def setup_ui(self):
        """Setup the main UI"""
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True)
        
        # Create header
        self.create_header(main_container)
        
        # Create main content area with sidebar
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left sidebar for controls
        sidebar = tk.Frame(content_frame, bg=self.colors['bg_secondary'], width=350)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Right main area for text
        main_area = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        main_area.pack(side="right", fill="both", expand=True)
        
        # Setup sidebar components
        self.create_sidebar_content(sidebar)
        
        # Setup main area components
        self.create_main_content(main_area)
        
    def create_header(self, parent):
        """Create the smooth modern header"""
        header = tk.Frame(parent, bg=self.colors['bg_secondary'], height=120)
        header.pack(fill="x", padx=30, pady=(30, 30))
        header.pack_propagate(False)
        
        # Header content with smooth padding
        header_content = tk.Frame(header, bg=self.colors['bg_secondary'])
        header_content.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Title with smooth gradient effect
        title_frame = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        title_frame.pack(anchor="center")
        
        title_label = tk.Label(title_frame, 
                              text="🚀 Ultra-Smooth Gujarati Converter Pro",
                              font=('Segoe UI', 26, 'bold'),
                              fg=self.colors['primary_light'],
                              bg=self.colors['bg_secondary'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="✨ Convert Unicode Gujarati to 35+ Fonts with Elegant Design ✨",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack(pady=(8, 0))
        
        # Smooth theme toggle button
        theme_btn = tk.Button(header_content,
                             text="🌙" if self.dark_mode else "☀️",
                             command=self.toggle_theme,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 14),
                             relief='flat',
                             padx=15,
                             pady=8,
                             cursor='hand2')
        theme_btn.pack(anchor="ne")
        
        # Add smooth hover effects
        theme_btn.bind("<Enter>", lambda e: theme_btn.config(bg=self.colors['hover']))
        theme_btn.bind("<Leave>", lambda e: theme_btn.config(bg=self.colors['bg_card']))
        
    def create_sidebar_content(self, parent):
        """Create sidebar with controls"""
        # Add padding
        padded_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        padded_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Font Selection
        self.create_font_section(padded_frame)
        
        # Settings Section
        self.create_settings_section(padded_frame)
        
        # Convert Button
        self.create_convert_section(padded_frame)
        
        # Progress Section
        self.create_progress_section(padded_frame)
        
        # Quick Actions
        self.create_quick_actions(padded_frame)
        
    def create_font_section(self, parent):
        """Create smooth font selection section"""
        font_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        font_card.pack(fill="x", pady=(0, 25), padx=5)
        
        # Smooth header with padding
        header = tk.Label(font_card, 
                         text="🎨 Font Selection",
                         font=('Segoe UI', 14, 'bold'),
                         fg=self.colors['primary_light'],
                         bg=self.colors['bg_card'])
        header.pack(pady=(20, 15))
        
        # Font dropdown with smooth styling
        self.font_var = tk.StringVar(value='shree0768')
        
        font_frame = tk.Frame(font_card, bg=self.colors['bg_card'])
        font_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.font_combo = ttk.Combobox(font_frame, 
                                      textvariable=self.font_var,
                                      state='readonly',
                                      style='Modern.TCombobox',
                                      font=('Segoe UI', 10))
        
        # Populate fonts
        font_list = get_font_list()
        self.font_combo['values'] = [f"{name}" for key, name in font_list]
        self.font_combo.set("Shree-Guj-0768")
        self.font_combo.bind('<<ComboboxSelected>>', self.on_font_change)
        self.font_combo.pack(fill="x", pady=(0, 12))
        
        # Smooth font preview with better spacing
        self.font_preview = tk.Label(font_card,
                                    text="✨ Shree-Guj-0768, Shree-Guj-0768W ✨",
                                    font=('Segoe UI', 9, 'italic'),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_card'],
                                    wraplength=300)
        self.font_preview.pack(padx=20, pady=(0, 20))
        
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='solid', bd=1)
        settings_card.pack(fill="x", pady=(0, 20))
        
        # Header
        header = tk.Label(settings_card, 
                         text="⚙️ Conversion Settings",
                         font=('Segoe UI', 12, 'bold'),
                         fg=self.colors['text_primary'],
                         bg=self.colors['bg_card'])
        header.pack(pady=(15, 10))
        
        # Settings grid
        settings_frame = tk.Frame(settings_card, bg=self.colors['bg_card'])
        settings_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Min delay
        tk.Label(settings_frame, text="Min Delay:", 
                font=('Segoe UI', 9, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        self.min_delay_var = tk.StringVar(value=str(MIN_DELAY))
        min_delay_entry = ttk.Entry(settings_frame, 
                                   textvariable=self.min_delay_var,
                                   style='Modern.TEntry',
                                   width=8)
        min_delay_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        
        # Max delay
        tk.Label(settings_frame, text="Max Delay:", 
                font=('Segoe UI', 9, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).grid(row=1, column=0, sticky="w", pady=(0, 8))
        
        self.max_delay_var = tk.StringVar(value=str(MAX_DELAY))
        max_delay_entry = ttk.Entry(settings_frame, 
                                   textvariable=self.max_delay_var,
                                   style='Modern.TEntry',
                                   width=8)
        max_delay_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        
        # Chunk size
        tk.Label(settings_frame, text="Chunk Size:", 
                font=('Segoe UI', 9, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).grid(row=2, column=0, sticky="w")
        
        self.chunk_size_var = tk.StringVar(value=str(CHUNK_SIZE))
        chunk_entry = ttk.Entry(settings_frame, 
                               textvariable=self.chunk_size_var,
                               style='Modern.TEntry',
                               width=8)
        chunk_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        
        settings_frame.columnconfigure(1, weight=1)
        
    def create_convert_section(self, parent):
        """Create smooth convert button section"""
        convert_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        convert_card.pack(fill="x", pady=(0, 25), padx=5)
        
        self.convert_btn = tk.Button(convert_card,
                                    text="🚀 CONVERT TEXT",
                                    command=self.start_conversion,
                                    bg=self.colors['secondary'],
                                    fg='white',
                                    font=('Segoe UI', 14, 'bold'),
                                    relief='flat',
                                    pady=20,
                                    cursor='hand2')
        self.convert_btn.pack(fill="x", padx=25, pady=25)
        
        # Add smooth hover effects with transitions
        def on_enter(e):
            self.convert_btn.config(bg='#4FD1C7', font=('Segoe UI', 15, 'bold'))
            
        def on_leave(e):
            if not self.conversion_running:
                self.convert_btn.config(bg=self.colors['secondary'], font=('Segoe UI', 14, 'bold'))
        
        self.convert_btn.bind("<Enter>", on_enter)
        self.convert_btn.bind("<Leave>", on_leave)
        
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='solid', bd=1)
        progress_card.pack(fill="x", pady=(0, 20))
        
        # Header
        header = tk.Label(progress_card, 
                         text="📊 Progress",
                         font=('Segoe UI', 12, 'bold'),
                         fg=self.colors['text_primary'],
                         bg=self.colors['bg_card'])
        header.pack(pady=(15, 10))
        
        # Progress content
        progress_content = tk.Frame(progress_card, bg=self.colors['bg_card'])
        progress_content.pack(fill="x", padx=15, pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_content, 
                                       mode='determinate',
                                       style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill="x", pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(progress_content,
                                    text="Ready to convert",
                                    font=('Segoe UI', 9),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_card'])
        self.status_label.pack()
        
    def create_quick_actions(self, parent):
        """Create smooth quick actions section"""
        actions_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        actions_card.pack(fill="x", pady=(0, 25), padx=5)
        
        # Header with smooth styling
        header = tk.Label(actions_card, 
                         text="⚡ Quick Actions",
                         font=('Segoe UI', 14, 'bold'),
                         fg=self.colors['primary_light'],
                         bg=self.colors['bg_card'])
        header.pack(pady=(20, 15))
        
        # Action buttons with smooth styling
        actions_frame = tk.Frame(actions_card, bg=self.colors['bg_card'])
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Smooth buttons with hover effects
        buttons_data = [
            ("📁 Load File", self.load_from_file),
            ("📝 Sample Text", self.add_sample_text),
            ("💾 Save Output", self.save_to_file)
        ]
        
        for text, command in buttons_data:
            btn = tk.Button(actions_frame,
                           text=text,
                           command=command,
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['text_primary'],
                           font=('Segoe UI', 10, 'bold'),
                           relief='flat',
                           pady=12,
                           cursor='hand2')
            btn.pack(fill="x", pady=(0, 8))
            
            # Add smooth hover effects
            def make_hover(button):
                def on_enter(e):
                    button.config(bg=self.colors['hover'])
                def on_leave(e):
                    button.config(bg=self.colors['bg_secondary'])
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)
            
            make_hover(btn)
        
    def create_main_content(self, parent):
        """Create smooth main content area"""
        # Input section with smooth styling
        input_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        input_card.pack(fill="both", expand=True, pady=(0, 25), padx=10)
        
        # Smooth input header
        input_header = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_header.pack(fill="x", padx=25, pady=(20, 15))
        
        tk.Label(input_header, 
                text="📝 Input Text (Unicode Gujarati)",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['primary_light'],
                bg=self.colors['bg_card']).pack(side="left")
        
        self.char_count_label = tk.Label(input_header,
                                        text="Characters: 0",
                                        font=('Segoe UI', 10),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['bg_card'])
        self.char_count_label.pack(side="right")
        
        # Smooth input text area
        input_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        self.input_text = scrolledtext.ScrolledText(input_frame,
                                                   height=12,
                                                   font=('Noto Sans Gujarati', 13),
                                                   wrap=tk.WORD,
                                                   bg=self.colors['bg_secondary'],
                                                   fg=self.colors['text_primary'],
                                                   insertbackground=self.colors['primary_light'],
                                                   selectbackground=self.colors['primary'],
                                                   relief='flat',
                                                   bd=0,
                                                   padx=15,
                                                   pady=15)
        self.input_text.pack(fill="both", expand=True)
        self.input_text.bind('<KeyRelease>', self.update_char_count)
        
        # Output section with smooth styling
        output_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        output_card.pack(fill="both", expand=True, padx=10)
        
        # Smooth output header
        output_header = tk.Frame(output_card, bg=self.colors['bg_card'])
        output_header.pack(fill="x", padx=25, pady=(20, 15))
        
        tk.Label(output_header, 
                text="📤 Converted Output (Non-Unicode Font)",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['primary_light'],
                bg=self.colors['bg_card']).pack(side="left")
        
        self.output_stats_label = tk.Label(output_header,
                                          text="Output: 0 characters",
                                          font=('Segoe UI', 10),
                                          fg=self.colors['text_secondary'],
                                          bg=self.colors['bg_card'])
        self.output_stats_label.pack(side="right")
        
        # Smooth output text area
        output_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        output_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                    height=12,
                                                    font=('Shree-Guj-0768', 13),
                                                    wrap=tk.WORD,
                                                    bg=self.colors['bg_secondary'],
                                                    fg=self.colors['text_primary'],
                                                    insertbackground=self.colors['primary_light'],
                                                    selectbackground=self.colors['primary'],
                                                    relief='flat',
                                                    bd=0,
                                                    padx=15,
                                                    pady=15)
        self.output_text.pack(fill="both", expand=True)
        
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.dark_mode = not self.dark_mode
        messagebox.showinfo("Theme", "Theme toggle feature coming soon! 🚀")
        
    def update_char_count(self, event=None):
        """Update character count"""
        text = self.input_text.get('1.0', tk.END).strip()
        count = len(text)
        self.char_count_label.config(text=f"Characters: {count:,}")
        
    def on_font_change(self, event=None):
        """Handle font selection change"""
        selected = self.font_combo.get()
        
        # Find the font key based on the display name
        for key, name in get_font_list():
            if name == selected:
                self.current_font = key
                break
                
        # Update font preview
        font_info = get_font_info(self.current_font)
        self.font_preview.config(text=font_info['font_family'])
        
        # Update output text font
        try:
            first_font = font_info['font_family'].replace('"', '').split(',')[0].strip()
            self.output_text.config(font=(first_font, 12))
        except:
            self.output_text.config(font=('Courier New', 12))
            
    def add_sample_text(self):
        """Add sample Gujarati text"""
        sample = ("🚀 આ આધુનિક ગુજરાતી ફોન્ટ કન્વર્ટર છે!\n\n"
                 "ગુજરાતી ભાષામાં લખાયેલ આ ટેક્સ્ટ છે. આ ફોન્ટ કન્વર્ટરનું પરીક્ષણ કરવા માટે છે. "
                 "તમે અહીં તમારો પોતાનો ટેક્સ્ટ લખી શકો છો અને વિવિધ ફોન્ટમાં કન્વર્ટ કરી શકો છો.\n\n"
                 "✨ આ કન્વર્ટર 35+ વિવિધ ગુજરાતી ફોન્ટને સપોર્ટ કરે છે!\n"
                 "🎨 સુંદર UI સાથે આધુનિક ડિઝાઇન\n"
                 "⚡ ઝડપી કન્વર્ઝન અને પ્રોગ્રેસ ટ્રેકિંગ\n"
                 "🛡️ IP બેન પ્રોટેક્શન અને રિઝ્યૂમ ફીચર")
        
        self.input_text.delete('1.0', tk.END)
        self.input_text.insert('1.0', sample)
        self.update_char_count()
        self.status_label.config(text="✅ Sample text added")
        
    def load_from_file(self):
        """Load text from file"""
        file_path = filedialog.askopenfilename(
            title="Select Gujarati Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete('1.0', tk.END)
                self.input_text.insert('1.0', content)
                self.update_char_count()
                self.status_label.config(text=f"✅ Loaded: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")
                
    def save_to_file(self):
        """Save output to file"""
        if not self.output_text.get('1.0', tk.END).strip():
            messagebox.showwarning("Warning", "No converted text to save!")
            return
            
        font_info = get_font_info(self.current_font)
        default_name = f"converted_{font_info['name'].lower().replace(' ', '_')}.txt"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Converted Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.output_text.get('1.0', tk.END))
                messagebox.showinfo("Success", f"✅ File saved: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
                
    def start_conversion(self):
        """Start the conversion process"""
        if self.conversion_running:
            messagebox.showwarning("Warning", "⚠️ Conversion already in progress!")
            return
            
        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "⚠️ Please enter some text to convert!")
            return
            
        # Start conversion
        self.conversion_running = True
        self.convert_btn.config(text="⏳ CONVERTING...", state='disabled', bg=self.colors['warning'])
        self.output_text.delete('1.0', tk.END)
        
        thread = threading.Thread(target=self.convert_text, args=(input_text,))
        thread.daemon = True
        thread.start()
        
    def convert_text(self, text):
        """Convert text using API"""
        try:
            chunks = self.chunk_text(text)
            total_chunks = len(chunks)
            font_info = get_font_info(self.current_font)
            
            self.root.after(0, lambda: self.progress.config(maximum=total_chunks, value=0))
            self.root.after(0, lambda: self.status_label.config(
                text=f"🚀 Converting {total_chunks} chunks using {font_info['name']}..."))
            
            results = []
            
            with requests.Session() as session:
                for i, chunk in enumerate(chunks):
                    try:
                        # Update UI
                        self.root.after(0, lambda i=i: self.progress.config(value=i))
                        self.root.after(0, lambda i=i, total=total_chunks: self.status_label.config(
                            text=f"⚡ Processing chunk {i+1}/{total} - {((i+1)/total)*100:.1f}% complete"))
                        
                        converted = self.convert_chunk_with_session(session, chunk, font_info['url'])
                        results.append(converted)
                        
                        # Add converted text to output progressively
                        self.root.after(0, lambda conv=converted: 
                                      self.output_text.insert(tk.END, conv))
                        
                        # Update output stats
                        current_length = len("".join(results))
                        self.root.after(0, lambda length=current_length: 
                                      self.output_stats_label.config(text=f"Output: {length:,} characters"))
                        
                    except Exception as e:
                        error_msg = f"❌ Failed to convert chunk {i+1}: {e}"
                        self.root.after(0, lambda msg=error_msg: messagebox.showerror("Conversion Error", msg))
                        break
                        
            # Final update
            final_text = "".join(results)
            self.root.after(0, lambda: self.progress.config(value=total_chunks))
            self.root.after(0, lambda: self.status_label.config(
                text=f"🎉 Conversion complete! {len(final_text):,} characters converted to {font_info['name']}"))
            
        except Exception as e:
            self.root.after(0, lambda e=e: messagebox.showerror("Error", f"❌ Conversion failed: {e}"))
            self.root.after(0, lambda: self.status_label.config(text="❌ Conversion failed"))
        finally:
            self.conversion_running = False
            self.root.after(0, lambda: self.convert_btn.config(
                text="🚀 CONVERT TEXT", 
                state='normal', 
                bg=self.colors['secondary']))
            
    def chunk_text(self, text):
        """Split text into chunks"""
        chunk_size = int(self.chunk_size_var.get())
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
    def convert_chunk_with_session(self, session, chunk, api_url):
        """Convert a single chunk using the specified API URL"""
        min_delay = float(self.min_delay_var.get())
        max_delay = float(self.max_delay_var.get())
        
        for retry in range(MAX_RETRIES):
            try:
                delay = random.uniform(min_delay, max_delay)
                if retry > 0:
                    delay = delay * (2 ** retry)
                time.sleep(delay)
                
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                ]
                
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                
                resp = session.post(api_url, data={"modify_string": chunk}, headers=headers, timeout=30)
                
                if resp.status_code == 200:
                    resp.encoding = 'utf-8'
                    converted_text = resp.text
                    
                    if len(converted_text.strip()) == 0:
                        return chunk
                    elif any(ord(char) < 32 and char not in '\n\r\t' for char in converted_text[:50]):
                        try:
                            converted_text = resp.content.decode('utf-8')
                        except:
                            return chunk
                    
                    return converted_text
                    
                elif resp.status_code in [403, 429]:
                    if retry == MAX_RETRIES - 1:
                        raise RuntimeError(f"Rate limited/IP banned after {MAX_RETRIES} attempts")
                    continue
                else:
                    if retry == MAX_RETRIES - 1:
                        raise RuntimeError(f"API error {resp.status_code}")
                    continue
                    
            except requests.exceptions.RequestException as e:
                if retry == MAX_RETRIES - 1:
                    raise RuntimeError(f"Network error: {e}")
                continue
                
        return chunk

def main():
    root = tk.Tk()
    app = UltraModernGujaratiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()