from PIL import Image  # Import the Pillow library for image processing


def resize_image(input_path, output_path, size):
    """
    Resize an image to the specified size and save it to a new file.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the resized image.
        size (tuple): New size as (width, height).
    """
    try:
        # Open the input image file
        with Image.open(input_path) as img:
            print(f"Opened image: {input_path}")
            # Resize the image to the specified size
            img = img.resize(size)
            print(f"Resized image to: {size}")
            # Save the resized image to the output path
            img.save(output_path)
            print(f"Image saved to {output_path}")
    except Exception as e:
        # Print an error message if something goes wrong
        print(f"Failed to process image: {e}")
