# CreateDot

A tkinter-based GUI application for creating dot matrix text. Convert any text into beautiful dot patterns with customizable settings and real-time preview.

## Features

### Intuitive Layout
- **Settings Panel (Left)**: Easy-to-use controls for text input and customization
- **Preview Area (Right)**: Real-time preview with scrollable canvas for large text
- **Action Buttons (Bottom)**: Quick access to update, save, and reset functions

### Customization Options
- **Text Input**: Multi-line text support with scrollable input area
- **Font Size**: Adjustable from 12 to 72 pixels using slider control
- **Dot Shapes**: Choose from circle, square, or diamond patterns
- **Dot Size**: Fine-tune dot size from 1 to 10 pixels
- **Spacing Control**: Adjust spacing between dots (1-15 pixels)

### Real-time Features
- **Live Preview**: Instant updates as you adjust settings
- **Scrollable Canvas**: Handle large text outputs with ease
- **Interactive Controls**: Sliders and dropdown menus for quick adjustments

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mota1207/CreateDot.git
cd CreateDot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python dot_text_generator.py
```

## Usage

1. **Enter Text**: Type your desired text in the left panel input area
2. **Adjust Settings**: Use the sliders and dropdown to customize:
   - Font size for text rendering
   - Dot shape (circle, square, diamond)
   - Dot size for visual impact
   - Spacing between dots
3. **Preview**: View real-time updates in the right panel
4. **Save**: Click "Save Image" to export your dot text as PNG or JPEG

## Requirements

- Python 3.6+
- Pillow (PIL) - Image processing
- numpy - Array operations
- tkinter - GUI framework (usually included with Python)

## Future Enhancements

The application is designed with clean class architecture to support future features:
- Additional dot shapes and patterns
- Color customization
- Export to different formats
- Batch processing capabilities
- Custom font loading

## License

This project is open source and available under the MIT License.