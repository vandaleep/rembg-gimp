# REMBG GIMP Plugin

A powerful GIMP 3 plugin for removing image backgrounds using the [rembg](https://github.com/danielgatis/rembg) AI model.

## 🎯 Features

- **One-click background removal** – Remove backgrounds from images with a single click
- **AI-powered** – Uses the state-of-the-art rembg model for accurate background detection
- **Progress tracking** – Visual progress indicator in GIMP while processing
- **Non-destructive** – Creates a new layer with the background-removed image
- **GIMP 3 native** – Built for GIMP 3.0+ with proper GObject introspection support
- **Batch processing ready** – Can be scripted for automated workflows

## 📋 Requirements

- **GIMP 3.0** or later
- **Python 3.7+**
- **rembg** binary (installed via pipx or pip)
- **PIL/Pillow** (installed automatically with rembg)

## 🚀 Installation

### 1. Install rembg

Using **pipx** (recommended for isolation):
```bash
pipx install "rembg[cpu,cli]"
```

Or using **pip**:
```bash
pip install "rembg[cpu,cli]"
```

### 2. Install the GIMP Plugin

**Option A: Clone this repository**
```bash
git clone https://github.com/vandaleep/rembg-gimp.git
cd rembg-gimp
mkdir ~/.config/GIMP/3.0/plug-ins/rembg-gimp
cp rembg-gimp.py ~/.config/GIMP/3.0/plug-ins/rembg-gimp/rembg-gimp.py
```

**Option B: Manual installation**
1. Download `rembg-gimp.py`
2. Place it in your GIMP plugins directory:
   - **Linux:** `~/.config/GIMP/3.0/plug-ins/`
   - **macOS:** `~/Library/Application Support/GIMP/3.0/plug-ins/`
   - **Windows:** `%APPDATA%\GIMP\3.0\plug-ins\`

*Create subfolder rembg-gimp in plug-ins directory*

### 3. Verify rembg Path (Important!)

Edit the plugin file and check the `REMBG_BINARY` path:

```python
REMBG_BINARY = "/path/to/rembg"
```

Find your rembg installation:
```bash
which rembg
# or
pipx list --json | grep rembg
```

### 4. Restart GIMP

Close and reopen GIMP. The plugin will appear in:
```
Filters → AI → Remove Background (REMBG)
```

## 📖 Usage

1. **Open an image** in GIMP
2. **Select a layer** (drawable) to process
3. Go to **Filters → AI → Remove Background (REMBG)**
4. **Wait** while GIMP shows the progress indicator
5. **New layer created** – The background-removed image appears as a new layer

### How It Works

The plugin:
1. Creates a temporary copy of your layer
2. Exports it as PNG to a temp file
3. Runs rembg's AI model for background removal
4. Loads the processed image as a new layer
5. Automatically cleans up temporary files

## 🔧 Technical Details

### Dependencies
- `gi` (GObject Introspection) – For GIMP 3.0 bindings
- `subprocess` – For calling the rembg binary
- `tempfile` – For temporary file handling
- `os` – For file operations

### Architecture
- **PlugIn base class** – Registers with GIMP's plugin system
- **ImageProcedure** – Operates on GIMP image layers
- **Progress tracking** – Real-time feedback with `Gimp.progress_*` API
- **Error handling** – Returns proper GLib.Error objects to GIMP

### Process Flow
```
Input Layer
    ↓
Create Temporary Image
    ↓
Export to PNG
    ↓
Run rembg Model
    ↓
Load Result as Layer
    ↓
Insert in Image
    ↓
Cleanup Temp Files
```

## 🐛 Troubleshooting

### "rembg command not found"
```bash
# Update the REMBG_BINARY path in the plugin:
which rembg
# Copy the path shown and update it in rembg-gimp.py
```

### Plugin doesn't appear in GIMP menu
1. Check GIMP's Python-Fu console: `Filters → Python-Fu → Console`
2. Verify the plugin file is in the correct plugins directory
3. Ensure file permissions are correct: `chmod +x rembg-gimp.py`
4. Restart GIMP completely

### "Failed to export the temporary PNG image"
- Check that the layer has valid dimensions
- Ensure GIMP has write permissions to `/tmp` directory
- Try with a different image format first

### rembg is slow (first run)
- **Expected behavior** – The first run downloads the AI model (~100 MB)
- Subsequent runs will be faster since the model is cached
- Model cache location: `~/.u2net/` or `~/.cache/rembg/`

### Out of memory errors
- Close other applications
- Work with smaller images for testing
- Consider using the GPU version: `pipx install "rembg[gpu,cli]"`

## 💻 System Requirements

### Minimum
- 4 GB RAM
- CPU: Intel i5 / AMD Ryzen 5 equivalent
- Disk: ~500 MB for model cache

### Recommended
- 8 GB RAM
- GPU with CUDA support for faster processing
- SSD for better temp file handling

## 📊 Performance

**Processing Time** (varies by image resolution):
- **Small images (800×600):** ~2-5 seconds
- **Medium images (1920×1080):** ~5-15 seconds
- **Large images (4K):** ~15-30 seconds

Times are for first run. Subsequent runs use cached AI models.

## 🎓 Learning Resources

- [GIMP 3.0 Python Documentation](https://developer.gimp.org/api/3.0/)
- [rembg GitHub Repository](https://github.com/danielgatis/rembg)
- [GObject Introspection](https://gi.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs in the Issues section
- Submit pull requests with improvements
- Suggest features

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **rembg** – [Daniel Gatis](https://github.com/danielgatis/rembg) for the amazing background removal model
- **GIMP** – The GNU Image Manipulation Program team
- **PyGObject** – For the Python bindings to GIMP

## 📞 Support

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Review GIMP's error logs: `Windows → Dockable Dialogs → Error Console`
3. Test rembg directly in terminal: `rembg i input.png output.png`
4. Open an issue on GitHub with details and error logs

---

**Enjoy removing backgrounds! 🎉**
