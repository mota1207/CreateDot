#!/usr/bin/env python3
"""
Dot Text Generator - A tkinter-based GUI application for creating dot matrix text.

This application provides a user-friendly interface for generating text using dot patterns.
Features include customizable font size, dot shapes, dot size, and spacing adjustments
with real-time preview.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io


class DotTextGenerator:
    """Main application class for the Dot Text Generator."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Dot Text Generator")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.current_image = None
        self.preview_image = None
        
        # Initialize UI
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        
        # Generate initial preview
        self.update_preview()
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        
        # Left panel for settings
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        
        # Text input
        ttk.Label(self.settings_frame, text="Text to Convert:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.text_input = scrolledtext.ScrolledText(self.settings_frame, height=4, width=30)
        self.text_input.insert("1.0", "Hello\nWorld!")
        
        # Font size
        ttk.Label(self.settings_frame, text="Font Size:").grid(row=2, column=0, sticky="w", pady=(10, 5))
        self.font_size_var = tk.IntVar(value=24)
        self.font_size_scale = ttk.Scale(
            self.settings_frame, 
            from_=12, to=72, 
            variable=self.font_size_var,
            orient="horizontal"
        )
        self.font_size_label = ttk.Label(self.settings_frame, text="24")
        
        # Dot shape
        ttk.Label(self.settings_frame, text="Dot Shape:").grid(row=4, column=0, sticky="w", pady=(10, 5))
        self.dot_shape_var = tk.StringVar(value="circle")
        self.dot_shape_combo = ttk.Combobox(
            self.settings_frame,
            textvariable=self.dot_shape_var,
            values=["circle", "square", "diamond"],
            state="readonly"
        )
        
        # Dot size
        ttk.Label(self.settings_frame, text="Dot Size:").grid(row=6, column=0, sticky="w", pady=(10, 5))
        self.dot_size_var = tk.IntVar(value=3)
        self.dot_size_scale = ttk.Scale(
            self.settings_frame,
            from_=1, to=10,
            variable=self.dot_size_var,
            orient="horizontal"
        )
        self.dot_size_label = ttk.Label(self.settings_frame, text="3")
        
        # Spacing
        ttk.Label(self.settings_frame, text="Dot Spacing:").grid(row=8, column=0, sticky="w", pady=(10, 5))
        self.spacing_var = tk.IntVar(value=5)
        self.spacing_scale = ttk.Scale(
            self.settings_frame,
            from_=1, to=15,
            variable=self.spacing_var,
            orient="horizontal"
        )
        self.spacing_label = ttk.Label(self.settings_frame, text="5")
        
        # Right panel for preview
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="Preview", padding="10")
        
        # Create canvas with scrollbars
        self.canvas_frame = ttk.Frame(self.preview_frame)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=500, height=400)
        
        # Scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Bottom panel for buttons
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.update_button = ttk.Button(self.button_frame, text="Update Preview", command=self.update_preview)
        self.save_button = ttk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.reset_button = ttk.Button(self.button_frame, text="Reset Settings", command=self.reset_settings)
    
    def setup_layout(self):
        """Arrange widgets in the layout."""
        # Main frame
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Settings panel (left)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Settings widgets
        self.text_input.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.font_size_scale.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        self.font_size_label.grid(row=3, column=1, sticky="w")
        
        self.dot_shape_combo.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.dot_size_scale.grid(row=7, column=0, sticky="ew", padx=(0, 10))
        self.dot_size_label.grid(row=7, column=1, sticky="w")
        
        self.spacing_scale.grid(row=9, column=0, sticky="ew", padx=(0, 10))
        self.spacing_label.grid(row=9, column=1, sticky="w")
        
        # Configure settings frame columns
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        # Preview panel (right)
        self.preview_frame.grid(row=0, column=1, sticky="nsew")
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure canvas frame
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Button panel (bottom)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.update_button.pack(side="left", padx=(0, 10))
        self.save_button.pack(side="left", padx=(0, 10))
        self.reset_button.pack(side="left")
    
    def bind_events(self):
        """Bind event handlers."""
        # Auto-update on text change
        self.text_input.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # Scale change events
        self.font_size_scale.bind('<Motion>', self.on_font_size_change)
        self.font_size_scale.bind('<ButtonRelease-1>', self.on_font_size_change)
        
        self.dot_size_scale.bind('<Motion>', self.on_dot_size_change)
        self.dot_size_scale.bind('<ButtonRelease-1>', self.on_dot_size_change)
        
        self.spacing_scale.bind('<Motion>', self.on_spacing_change)
        self.spacing_scale.bind('<ButtonRelease-1>', self.on_spacing_change)
        
        # Combobox change
        self.dot_shape_combo.bind('<<ComboboxSelected>>', lambda e: self.update_preview())
    
    def on_font_size_change(self, event):
        """Handle font size scale change."""
        self.font_size_label.config(text=str(self.font_size_var.get()))
        self.update_preview()
    
    def on_dot_size_change(self, event):
        """Handle dot size scale change."""
        self.dot_size_label.config(text=str(self.dot_size_var.get()))
        self.update_preview()
    
    def on_spacing_change(self, event):
        """Handle spacing scale change."""
        self.spacing_label.config(text=str(self.spacing_var.get()))
        self.update_preview()
    
    def text_to_dots(self, text, font_size, dot_shape, dot_size, spacing):
        """Convert text to dot matrix representation."""
        try:
            # Create a temporary image to render text
            temp_img = Image.new('RGB', (800, 600), 'white')
            draw = ImageDraw.Draw(temp_img)
            
            # Try to use a default font, fallback to built-in if not available
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except (OSError, IOError):
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                except (OSError, IOError):
                    font = ImageFont.load_default()
            
            # Draw text
            draw.text((10, 10), text, fill='black', font=font)
            
            # Convert to grayscale and then to numpy array
            gray_img = temp_img.convert('L')
            img_array = np.array(gray_img)
            
            # Find text bounds
            rows, cols = np.where(img_array < 255)
            if len(rows) == 0:
                return Image.new('RGB', (100, 100), 'white')
            
            min_row, max_row = rows.min(), rows.max()
            min_col, max_col = cols.min(), cols.max()
            
            # Crop to text area
            text_array = img_array[min_row:max_row+1, min_col:max_col+1]
            
            # Sample points based on spacing
            sampled_rows = range(0, text_array.shape[0], spacing)
            sampled_cols = range(0, text_array.shape[1], spacing)
            
            # Calculate output image size
            output_width = len(sampled_cols) * (dot_size * 2 + 2)
            output_height = len(sampled_rows) * (dot_size * 2 + 2)
            
            # Create output image
            output_img = Image.new('RGB', (output_width, output_height), 'white')
            draw_output = ImageDraw.Draw(output_img)
            
            # Draw dots
            for i, row in enumerate(sampled_rows):
                for j, col in enumerate(sampled_cols):
                    if text_array[row, col] < 128:  # Dark pixel
                        x = j * (dot_size * 2 + 2) + dot_size
                        y = i * (dot_size * 2 + 2) + dot_size
                        
                        self.draw_dot(draw_output, x, y, dot_size, dot_shape)
            
            return output_img
            
        except Exception as e:
            print(f"Error in text_to_dots: {e}")
            # Return a simple error image
            error_img = Image.new('RGB', (200, 100), 'white')
            draw = ImageDraw.Draw(error_img)
            draw.text((10, 10), "Error generating\ndot text", fill='red')
            return error_img
    
    def draw_dot(self, draw, x, y, size, shape):
        """Draw a dot at the specified position."""
        if shape == "circle":
            draw.ellipse([x-size, y-size, x+size, y+size], fill='black')
        elif shape == "square":
            draw.rectangle([x-size, y-size, x+size, y+size], fill='black')
        elif shape == "diamond":
            points = [(x, y-size), (x+size, y), (x, y+size), (x-size, y)]
            draw.polygon(points, fill='black')
    
    def update_preview(self):
        """Update the preview canvas with the current settings."""
        try:
            text = self.text_input.get("1.0", "end-1c")
            if not text.strip():
                text = "Sample"
            
            font_size = self.font_size_var.get()
            dot_shape = self.dot_shape_var.get()
            dot_size = self.dot_size_var.get()
            spacing = self.spacing_var.get()
            
            # Generate dot image
            self.current_image = self.text_to_dots(text, font_size, dot_shape, dot_size, spacing)
            
            # Convert to PhotoImage for display
            self.preview_image = ImageTk.PhotoImage(self.current_image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.preview_image)
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            print(f"Error updating preview: {e}")
            messagebox.showerror("Error", f"Failed to update preview: {e}")
    
    def save_image(self):
        """Save the current image to a file."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save. Please generate a preview first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_image.save(filename)
                messagebox.showinfo("Success", f"Image saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
    
    def reset_settings(self):
        """Reset all settings to default values."""
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", "Hello\nWorld!")
        
        self.font_size_var.set(24)
        self.font_size_label.config(text="24")
        
        self.dot_shape_var.set("circle")
        
        self.dot_size_var.set(3)
        self.dot_size_label.config(text="3")
        
        self.spacing_var.set(5)
        self.spacing_label.config(text="5")
        
        self.update_preview()


def main():
    """Main entry point of the application."""
    root = tk.Tk()
    app = DotTextGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()