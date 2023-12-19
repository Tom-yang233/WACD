import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

def display_image(data, pixel_size=20):
    # Define color mapping for each number (0-15)
    color_mapping = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 250, 250),
        (0, 100, 0), # DarkGreen
        (255, 236, 139), # LightGoldenrod1
        (60, 179, 113), # 60 179 113
        (238, 238, 209),
        (255, 193, 37),
        (255, 193, 193),
        (255, 106, 106),
        (205, 133, 63),
        (138, 43, 226),
        (131, 111, 255),
        (0,0,0)
    ]

    # Get the dimensions of the input data
    original_width = max(len(row) for row in data)
    original_height = len(data)

    # Create a NumPy array to store RGB values
    image_array = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    # Map each number to its corresponding color
    for i in range(original_height):
        for j in range(len(data[i])):
            color = color_mapping[int(data[i][j])]
            image_array[i, j] = color

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Image Display")

    # Create a Tkinter canvas
    canvas = tk.Canvas(root, width=original_width * pixel_size, height=original_height * pixel_size)
    canvas.pack()

    # Draw rectangles for each pixel on the canvas
    for i in range(original_height):
        for j in range(len(data[i])):
            color = "#{:02x}{:02x}{:02x}".format(*image_array[i, j])
            canvas.create_rectangle(
                j * pixel_size, i * pixel_size,
                (j + 1) * pixel_size, (i + 1) * pixel_size,
                fill=color, outline="")

    # Start the Tkinter event loop
    root.mainloop()

# Example usage:
# Replace 'your_data' with your 2D list
your_data = [[], ['7', '7', '10', '12', '12', '13', '15', '13', '8', '7', '8', '12', '13', '15', '12', '10', '8', '9', '9', '9', '9', '11', '12', '12', '12', '13', '12', '15', '15', '13', '7', '8', '10', '12', '12', '12'], ['13', '13', '10', '12', '8', '8', '12', '13', '13', '13', '13'], [], ['8', '8', '12', '12', '8', '8', '9', '12', '12', '13', '13', '13', '13', '8', '8', '6'], ['13', '13', '15', '10', '7', '7', '7', '9', '11', '12', '12', '13', '13', '11', '10', '12', '12']]
# Specify the desired pixel size (e.g., 30x30 pixels for each original pixel)
display_image(your_data, pixel_size=30)
