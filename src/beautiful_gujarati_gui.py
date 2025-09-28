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

class ModernGujaratiConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔤 Multi-Font Gujarati Converter - Professional")
        self.root.geometry("1100x850")
        self.root.minsize(900, 700)
        
        # Modern colors
        self.colors = {
            'primary': '#1976D2',      # Professional Blue
            'secondary': '#388E3C',    # Success Green
            'accent': '#F57C00',       # Warning Orange
            'error': '#D32F2F',        # Error Red
            'bg_main': '#F5F5F5',      # Light Gray
            'bg_card': '#FFFFFF',      # White
            'text_primary': '#212121', # Dark Gray
            'text_secondary': '#757575', # Medium Gray
            'border': '#E0E0E0'        # Light Border
        }
        
        self.conversion_running = False
        self.session = None
        self.current_font = 'shree0768'
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure custom styles for ttk widgets"""
        self.style = ttk.Style()
        
        # Try to use a modern theme
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 18, 'bold'),
                           foreground=self.colors['primary'])
        
        self.style.configure('Heading.TLabel', 
                           font=('Segoe UI', 12, 'bold'),
                           foreground=self.colors['text_primary'])
        
        self.style.configure('Info.TLabel', 
                           font=('Segoe UI', 9),
                           foreground=self.colors['text_secondary'])
        
        self.style.configure('Action.TButton', 
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 10))
        
        self.style.configure('Convert.TButton', 
                           font=('Segoe UI', 12, 'bold'),
                           padding=(30, 15))
        
        # Configure frame styles
        self.style.configure('Card.TFrame', relief='solid', borderwidth=1)
        self.style.configure('Card.TLabelFrame', relief='solid', borderwidth=1)
        
    def setup_ui(self):
        # Main container
        self.root.configure(bg=self.colors['bg_main'])
        
        # Create main canvas for scrolling
        canvas = tk.Canvas(self.root, bg=self.colors['bg_main'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame with padding
        main_frame = ttk.Frame(scrollable_frame, style='Card.TFrame', padding="25")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section
        self.create_header(main_frame)
        
        # Font selection section
        self.create_font_selection(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Settings section
        self.create_settings_section(main_frame)
        
        # Convert button
        self.create_convert_button(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Output section
        self.create_output_section(main_frame)
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, padding="0 0 20 0")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Main title
        title_label = ttk.Label(header_frame, 
                               text="🔤 Multi-Font Gujarati Converter",
                               style='Title.TLabel')
        title_label.pack(anchor="center")
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                 text="Convert Unicode Gujarati to 35+ Non-Unicode Fonts",
                                 style='Info.TLabel')
        subtitle_label.pack(anchor="center", pady=(5, 0))
        
        # Separator
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill="x", pady=(15, 0))
        
    def create_font_selection(self, parent):
        """Create font selection section"""
        font_frame = ttk.LabelFrame(parent, text="🎨 Font Selection", padding="20")
        font_frame.pack(fill="x", pady=(0, 20))
        
        # Font selection row
        select_frame = ttk.Frame(font_frame)
        select_frame.pack(fill="x", pady=(0, 15))
        
        # Font label
        ttk.Label(select_frame, text="Select Font:", 
                 style='Heading.TLabel').pack(side="left", padx=(0, 15))
        
        # Font dropdown
        self.font_var = tk.StringVar(value='shree0768')
        self.font_combo = ttk.Combobox(select_frame, 
                                      textvariable=self.font_var,
                                      state='readonly', 
                                      width=35,
                                      font=('Segoe UI', 10))
        
        # Populate font dropdown
        font_list = get_font_list()
        self.font_combo['values'] = [f"{name} ({key})" for key, name in font_list]
        self.font_combo.set("Shree-Guj-0768 (shree0768)")
        self.font_combo.bind('<<ComboboxSelected>>', self.on_font_change)
        self.font_combo.pack(side="left", padx=(0, 20))
        
        # Font info button
        ttk.Button(select_frame, text="ℹ️ Font Info", 
                  command=self.show_font_info,
                  style='Action.TButton').pack(side="left")
        
        # Font preview
        preview_frame = ttk.Frame(font_frame)
        preview_frame.pack(fill="x")
        
        ttk.Label(preview_frame, text="Font Family:", 
                 style='Info.TLabel').pack(side="left", padx=(0, 10))
        
        self.font_preview = ttk.Label(preview_frame, 
                                     text="Shree-Guj-0768, Shree-Guj-0768W",
                                     style='Info.TLabel',
                                     font=('Segoe UI', 9, 'italic'))
        self.font_preview.pack(side="left")
        
    def create_input_section(self, parent):
        """Create input text section"""
        input_frame = ttk.LabelFrame(parent, text="📝 Input Text (Unicode Gujarati)", padding="20")
        input_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Input text area
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.input_text = scrolledtext.ScrolledText(text_frame, 
                                                   height=8, 
                                                   font=('Noto Sans Gujarati', 12),
                                                   wrap=tk.WORD,
                                                   relief='solid',
                                                   borderwidth=1)
        self.input_text.pack(fill="both", expand=True)
        
        # Button row
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="📁 Load File", 
                  command=self.load_from_file,
                  style='Action.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="📝 Sample Text", 
                  command=self.add_sample_text,
                  style='Action.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="🗑️ Clear", 
                  command=self.clear_input,
                  style='Action.TButton').pack(side="left")
        
        # Character count
        self.char_count_label = ttk.Label(button_frame, 
                                         text="Characters: 0",
                                         style='Info.TLabel')
        self.char_count_label.pack(side="right")
        
        # Bind text change to update character count
        self.input_text.bind('<KeyRelease>', self.update_char_count)
        
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Conversion Settings", padding="20")
        settings_frame.pack(fill="x", pady=(0, 20))
        
        # Settings grid
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill="x")
        
        # Min delay
        ttk.Label(settings_grid, text="Min Delay (seconds):",
                 style='Heading.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.min_delay_var = tk.StringVar(value=str(MIN_DELAY))
        ttk.Entry(settings_grid, textvariable=self.min_delay_var, 
                 width=8, font=('Segoe UI', 10)).grid(row=0, column=1, padx=(0, 30))
        
        # Max delay
        ttk.Label(settings_grid, text="Max Delay (seconds):",
                 style='Heading.TLabel').grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.max_delay_var = tk.StringVar(value=str(MAX_DELAY))
        ttk.Entry(settings_grid, textvariable=self.max_delay_var, 
                 width=8, font=('Segoe UI', 10)).grid(row=0, column=3, padx=(0, 30))
        
        # Chunk size
        ttk.Label(settings_grid, text="Chunk Size:",
                 style='Heading.TLabel').grid(row=0, column=4, sticky="w", padx=(0, 10))
        self.chunk_size_var = tk.StringVar(value=str(CHUNK_SIZE))
        ttk.Entry(settings_grid, textvariable=self.chunk_size_var, 
                 width=8, font=('Segoe UI', 10)).grid(row=0, column=5)
        
        # Info text
        info_label = ttk.Label(settings_frame,
                              text="💡 Higher delays reduce the chance of IP bans but make conversion slower",
                              style='Info.TLabel')
        info_label.pack(anchor="w", pady=(15, 0))
        
    def create_convert_button(self, parent):
        """Create the main convert button"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(0, 20))
        
        self.convert_btn = ttk.Button(button_frame, 
                                     text="🔄 Convert Text", 
                                     command=self.start_conversion,
                                     style='Convert.TButton')
        self.convert_btn.pack(anchor="center")
        
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = ttk.LabelFrame(parent, text="📊 Progress", padding="20")
        progress_frame.pack(fill="x", pady=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, 
                                       mode='determinate',
                                       length=400)
        self.progress.pack(fill="x", pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, 
                                     text="Ready to convert",
                                     style='Info.TLabel')
        self.status_label.pack(anchor="center")
        
    def create_output_section(self, parent):
        """Create output section"""
        output_frame = ttk.LabelFrame(parent, text="📤 Converted Output (Non-Unicode Font)", padding="20")
        output_frame.pack(fill="both", expand=True)
        
        # Output text area
        text_frame = ttk.Frame(output_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.output_text = scrolledtext.ScrolledText(text_frame, 
                                                    height=8,
                                                    font=('Shree-Guj-0768', 12),
                                                    wrap=tk.WORD,
                                                    relief='solid',
                                                    borderwidth=1)
        self.output_text.pack(fill="both", expand=True)
        
        # Output buttons
        button_frame = ttk.Frame(output_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="💾 Save File", 
                  command=self.save_to_file,
                  style='Action.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="📋 Copy", 
                  command=self.copy_to_clipboard,
                  style='Action.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="👁️ Preview", 
                  command=self.preview_font,
                  style='Action.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="🗑️ Clear", 
                  command=self.clear_output,
                  style='Action.TButton').pack(side="left")
        
        # Output stats
        self.output_stats_label = ttk.Label(button_frame, 
                                           text="Output: 0 characters",
                                           style='Info.TLabel')
        self.output_stats_label.pack(side="right")
        
    def update_char_count(self, event=None):
        """Update character count"""
        text = self.input_text.get('1.0', tk.END).strip()
        count = len(text)
        self.char_count_label.config(text=f"Characters: {count:,}")
        
    def on_font_change(self, event=None):
        """Handle font selection change"""
        selected = self.font_combo.get()
        if '(' in selected:
            font_key = selected.split('(')[1].rstrip(')')
            self.current_font = font_key
            
            # Update font preview
            font_info = get_font_info(font_key)
            self.font_preview.config(text=font_info['font_family'])
            
            # Update output text font
            try:
                first_font = font_info['font_family'].replace('"', '').split(',')[0].strip()
                self.output_text.config(font=(first_font, 12))
            except:
                self.output_text.config(font=('Courier New', 12))
                
    def show_font_info(self):
        """Show detailed font information"""
        font_info = get_font_info(self.current_font)
        
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Font Information - {font_info['name']}")
        info_window.geometry("600x400")
        info_window.configure(bg=self.colors['bg_card'])
        
        # Info frame
        info_frame = ttk.Frame(info_window, padding="30")
        info_frame.pack(fill="both", expand=True)
        
        # Font details
        ttk.Label(info_frame, text=f"📝 Font Name: {font_info['name']}", 
                 font=('Segoe UI', 14, 'bold')).pack(anchor="w", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"🔑 Key: {self.current_font}", 
                 font=('Segoe UI', 10)).pack(anchor="w", pady=(0, 5))
        
        ttk.Label(info_frame, text=f"👥 Font Family: {font_info['font_family']}", 
                 font=('Segoe UI', 10)).pack(anchor="w", pady=(0, 5))
        
        ttk.Label(info_frame, text=f"🌐 API URL: {font_info['url']}", 
                 font=('Segoe UI', 10)).pack(anchor="w", pady=(0, 15))
        
        # Sample preview
        ttk.Label(info_frame, text="📖 Font Preview:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor="w", pady=(10, 5))
        
        sample_text = self.output_text.get('1.0', tk.END).strip() or "આ ફોન્ટનું નમૂનો"
        
        preview_text = tk.Text(info_frame, height=6, font=(font_info['font_family'].split(',')[0].replace('"', '').strip(), 14))
        preview_text.pack(fill="x", pady=(5, 15))
        preview_text.insert('1.0', sample_text)
        preview_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(info_frame, text="✅ Close", 
                  command=info_window.destroy,
                  style='Action.TButton').pack(anchor="center")
        
    def add_sample_text(self):
        """Add sample Gujarati text"""
        sample = ("ગુજરાતી ભાષામાં લખાયેલ આ ટેક્સ્ટ છે. આ ફોન્ટ કન્વર્ટરનું પરીક્ષણ કરવા માટે છે. "
                 "તમે અહીં તમારો પોતાનો ટેક્સ્ટ લખી શકો છો અને વિવિધ ફોન્ટમાં કન્વર્ટ કરી શકો છો.")
        
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
                
    def clear_input(self):
        """Clear input text"""
        self.input_text.delete('1.0', tk.END)
        self.update_char_count()
        
    def clear_output(self):
        """Clear output text"""
        self.output_text.delete('1.0', tk.END)
        self.output_stats_label.config(text="Output: 0 characters")
        
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
                
    def copy_to_clipboard(self):
        """Copy output to clipboard"""
        if not self.output_text.get('1.0', tk.END).strip():
            messagebox.showwarning("Warning", "No converted text to copy!")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get('1.0', tk.END))
        messagebox.showinfo("Success", "✅ Text copied to clipboard!")
        
    def preview_font(self):
        """Show font preview window"""
        font_info = get_font_info(self.current_font)
        preview_text = self.output_text.get('1.0', tk.END).strip()
        
        if not preview_text:
            preview_text = "આ ફોન્ટનું પ્રીવ્યૂ - This is a font preview"
            
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"🔤 Font Preview - {font_info['name']}")
        preview_window.geometry("700x500")
        preview_window.configure(bg=self.colors['bg_card'])
        
        # Preview frame
        preview_frame = ttk.Frame(preview_window, padding="30")
        preview_frame.pack(fill="both", expand=True)
        
        # Header
        ttk.Label(preview_frame, 
                 text=f"🔤 {font_info['name']} Font Preview",
                 font=('Segoe UI', 16, 'bold')).pack(anchor="center", pady=(0, 20))
        
        # Font info
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Family: {font_info['font_family']}", 
                 font=('Segoe UI', 10)).pack(anchor="w")
        
        # Preview text area
        try:
            first_font = font_info['font_family'].replace('"', '').split(',')[0].strip()
            preview_widget = tk.Text(preview_frame, 
                                   height=12, 
                                   font=(first_font, 16),
                                   wrap=tk.WORD,
                                   relief='solid',
                                   borderwidth=1)
        except:
            preview_widget = tk.Text(preview_frame, 
                                   height=12, 
                                   font=('Courier New', 16),
                                   wrap=tk.WORD,
                                   relief='solid',
                                   borderwidth=1)
            
        preview_widget.pack(fill="both", expand=True, pady=(0, 20))
        preview_widget.insert('1.0', preview_text)
        preview_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(preview_frame, text="✅ Close", 
                  command=preview_window.destroy,
                  style='Action.TButton').pack(anchor="center")
        
    def start_conversion(self):
        """Start the conversion process"""
        if self.conversion_running:
            messagebox.showwarning("Warning", "⚠️ Conversion already in progress!")
            return
            
        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "⚠️ Please enter some text to convert!")
            return
            
        # Start conversion in separate thread
        self.conversion_running = True
        self.convert_btn.config(text="⏳ Converting...", state='disabled')
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
                text=f"🔄 Converting {total_chunks} chunks using {font_info['name']}..."))
            
            results = []
            
            with requests.Session() as session:
                for i, chunk in enumerate(chunks):
                    try:
                        # Update UI
                        self.root.after(0, lambda i=i: self.progress.config(value=i))
                        self.root.after(0, lambda i=i, total=total_chunks: self.status_label.config(
                            text=f"🔄 Processing chunk {i+1}/{total} - {((i+1)/total)*100:.1f}% complete"))
                        
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
                text=f"✅ Conversion complete! {len(final_text):,} characters converted to {font_info['name']}"))
            
        except Exception as e:
            self.root.after(0, lambda e=e: messagebox.showerror("Error", f"❌ Conversion failed: {e}"))
            self.root.after(0, lambda: self.status_label.config(text="❌ Conversion failed"))
        finally:
            self.conversion_running = False
            self.root.after(0, lambda: self.convert_btn.config(text="🔄 Convert Text", state='normal'))
            
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
                # Add delay
                delay = random.uniform(min_delay, max_delay)
                if retry > 0:
                    delay = delay * (2 ** retry)
                time.sleep(delay)
                
                # User agents
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                ]
                
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                
                resp = session.post(api_url, data={"modify_string": chunk}, headers=headers, timeout=30)
                
                if resp.status_code == 200:
                    # Ensure proper encoding
                    resp.encoding = 'utf-8'
                    converted_text = resp.text
                    
                    # Validate response
                    if len(converted_text.strip()) == 0:
                        return chunk  # Fallback
                    elif any(ord(char) < 32 and char not in '\n\r\t' for char in converted_text[:50]):
                        # Try different decoding
                        try:
                            converted_text = resp.content.decode('utf-8')
                        except:
                            return chunk  # Fallback
                    
                    return converted_text
                    
                elif resp.status_code in [403, 429]:  # IP ban or rate limit
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
                
        return chunk  # Fallback to original

def main():
    root = tk.Tk()
    app = ModernGujaratiConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()