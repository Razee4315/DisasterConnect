from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a white background
    width = 800
    height = 800
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Define colors
    primary_color = (41, 128, 185)  # Blue
    secondary_color = (231, 76, 60)  # Red
    accent_color = (46, 204, 113)   # Green

    # Draw the main circular background
    center = (width // 2, height // 2)
    radius = 350
    draw.ellipse([
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius
    ], fill=primary_color)

    # Draw the cross symbol
    cross_width = 100
    cross_length = 500
    
    # Horizontal part of cross
    draw.rectangle([
        center[0] - cross_length//2,
        center[1] - cross_width//2,
        center[0] + cross_length//2,
        center[1] + cross_width//2
    ], fill=secondary_color)
    
    # Vertical part of cross
    draw.rectangle([
        center[0] - cross_width//2,
        center[1] - cross_length//2,
        center[0] + cross_width//2,
        center[1] + cross_length//2
    ], fill=secondary_color)

    # Draw connecting dots/circles
    dot_radius = 40
    dot_positions = [
        (center[0] - radius//2, center[1] - radius//2),
        (center[0] + radius//2, center[1] - radius//2),
        (center[0] - radius//2, center[1] + radius//2),
        (center[0] + radius//2, center[1] + radius//2)
    ]
    
    for pos in dot_positions:
        draw.ellipse([
            pos[0] - dot_radius,
            pos[1] - dot_radius,
            pos[0] + dot_radius,
            pos[1] + dot_radius
        ], fill=accent_color)

        # Draw connecting lines
        line_width = 15
        draw.line([center, pos], fill=accent_color, width=line_width)

    # Save the logo in different sizes
    sizes = {
        'large': (800, 800),
        'medium': (400, 400),
        'small': (200, 200),
        'icon': (64, 64)
    }

    output_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(output_dir, exist_ok=True)

    for name, size in sizes.items():
        resized = image.resize(size, Image.Resampling.LANCZOS)
        output_path = os.path.join(output_dir, f'logo_{name}.png')
        resized.save(output_path, 'PNG')
        print(f'Saved {name} logo to {output_path}')

if __name__ == '__main__':
    create_logo()
