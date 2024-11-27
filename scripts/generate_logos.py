"""Generate PNG logos from SVG for DisasterConnect."""
import os
import cairosvg

def generate_logos():
    # Get the absolute path to the resources directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resources_dir = os.path.join(base_dir, 'resources', 'images')
    svg_path = os.path.join(resources_dir, 'logo.svg')

    # Define sizes for different use cases
    sizes = {
        'icon': 32,
        'small': 64,
        'medium': 128,
        'large': 256,
        'splash': 512
    }

    # Generate PNGs for each size
    for name, size in sizes.items():
        output_path = os.path.join(resources_dir, f'logo_{name}.png')
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            output_width=size,
            output_height=size
        )
        print(f"Generated {name} logo: {output_path}")

if __name__ == '__main__':
    generate_logos()
