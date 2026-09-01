# MTPU - Magic Thermal Printing Utility

A desktop application for generating and printing Magic: The Gathering cards via thermal printer.

## System Overview

MTPU is a modular Tkinter-based application that fetches card images from the Scryfall API and prints them to a thermal printer. The system is divided into three main components:

- **Main Application** (`mtpu.py`): Entry point that loads utility modules and manages the printer selection
- **Utilities** (`utilities/`): Feature modules for different card generation modes (Momir, Sorcerer)
- **Tools** (`tools/`): Shared functionality for image processing and printing

## Components

### Main Application (`mtpu.py`)
- Loads utility modules dynamically from the `utilities/` directory
- Provides a printer cycle button (top-right corner) to switch between available printers
- Displays card images and manages the main UI window

### Utilities
- **Momir** (`utilities/momir.py`): Generates random creatures by converted mana cost (CMC)
- **Sorcerer** (`utilities/sorcerer.py`): Generates random sorceries by CMC
- **Tokens** (`utilities/tokens.py`): Displays a searchable list of all token types from Scryfall, with click-to-preview and a "Print Token" button
- Each utility creates its own Toplevel window with appropriate selection controls

### Tools
- **Image Printer** (`tools/image_printer.py`): Handles thermal printing using Windows API (win32print)
- **Utils** (`tools/utils.py`): Shared functions for API requests and image downloading

## API

**Scryfall API** (https://api.scryfall.com)
- Used to fetch random card images based on type and CMC
- Requires custom User-Agent header: `MTPU/1.0 (Magic Thermal Printing Utility)` 
- Endpoint example: `https://api.scryfall.com/cards/random?q=type:creature+cmc:1`

## Dependencies

- `tkinter`: GUI framework
- `PIL/Pillow`: Image processing
- `requests`: HTTP requests for Scryfall API
- `win32print`/`win32ui`: Windows printer API

## Usage

1. Run `python mtpu.py`
2. Select a utility mode (Momir, Sorcerer, or Tokens)
3. **Momir/Sorcerer**: Click CMC buttons to generate random cards
4. **Tokens**: Click a token name to preview, then "Print Token" to print
5. Use the printer icon (top-right) to cycle through available printers
6. Cards are automatically printed to the selected printer
