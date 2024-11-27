"""Create logo for DisasterConnect using PIL."""
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(size):
    # Create a new image with a white background
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (44, 62, 80)  # Dark blue
    accent_color = (231, 76, 60)  # Red
    highlight_color = (52, 152, 219)  # Light blue
    
    # Draw main circle
    circle_margin = size // 20
    circle_size = size - (2 * circle_margin)
    draw.ellipse(
        [circle_margin, circle_margin, circle_margin + circle_size, circle_margin + circle_size],
        fill=primary_color
    )
    
    # Draw location pin
    pin_width = size // 3
    pin_height = size // 2
    pin_top = size // 4
    
    # Pin shape coordinates
    pin_shape = [
        (size//2 - pin_width//2, pin_top),  # Top left
        (size//2 + pin_width//2, pin_top),  # Top right
        (size//2, pin_top + pin_height)      # Bottom point
    ]
    draw.polygon(pin_shape, fill=accent_color)
    
    # Draw cross in pin
    cross_size = pin_width // 3
    cross_center = (size//2, pin_top + pin_width//2)
    draw.rectangle(
        [
            cross_center[0] - cross_size//6, cross_center[1] - cross_size//2,
            cross_center[0] + cross_size//6, cross_center[1] + cross_size//2
        ],
        fill='white'
    )
    draw.rectangle(
        [
            cross_center[0] - cross_size//2, cross_center[1] - cross_size//6,
            cross_center[0] + cross_size//2, cross_center[1] + cross_size//6
        ],
        fill='white'
    )
    
    # Draw signal waves
    wave_center = (size//2, pin_top + pin_width//2)
    for i in range(3):
        wave_radius = pin_width//2 + (i * size//8)
        draw.arc(
            [
                wave_center[0] - wave_radius,
                wave_center[1] - wave_radius//2,
                wave_center[0] + wave_radius,
                wave_center[1] + wave_radius//2
            ],
            -45, 225,
            fill=highlight_color,
            width=max(size//50, 1)
        )
    
    return img

def generate_all_logos():
    # Get the absolute path to the resources directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resources_dir = os.path.join(base_dir, 'resources', 'images')
    
    # Create resources/images directory if it doesn't exist
    os.makedirs(resources_dir, exist_ok=True)
    
    # Generate logos in different sizes
    sizes = {
        'icon': 32,
        'small': 64,
        'medium': 128,
        'large': 256,
        'splash': 512
    }
    
    for name, size in sizes.items():
        logo = create_logo(size)
        output_path = os.path.join(resources_dir, f'logo_{name}.png')
        logo.save(output_path, 'PNG')
        print(f"Generated {name} logo: {output_path}")

if __name__ == '__main__':
    generate_all_logos()
