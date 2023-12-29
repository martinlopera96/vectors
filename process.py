import io
import potrace
import numpy as np

from PIL import Image


def create_svg_path_string(image_path):
    d = []
    for curve in image_path:
        start = curve.start_point
        d.append(f"M {start.x} {start.y}")
        for segment in curve:
            if segment.is_corner:
                d.append(f"L {segment.c.x} {segment.c.y} {segment.end_point.x} {segment.end_point.y}")
            else:
                d.append(
                    f"C {segment.c1.x} {segment.c1.y} {segment.c2.x} {segment.c2.y} {segment.end_point.x} {segment.end_point.y}"
                )
    return " ".join(d)


def process_image(image_file, threshold):
    image = Image.open(image_file)

    if image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('L')
    else:
        image = image.convert('L')

    image_np = np.array(image)

    image_np = image_np < threshold

    bitmap = potrace.Bitmap(image_np)

    path = bitmap.trace()

    svg_data = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{image.width}" height="{image.height}">
      <path d="{create_svg_path_string(path)}" fill="black" />
    </svg>"""

    svg_io = io.BytesIO()
    svg_io.write(svg_data.encode())
    svg_io.seek(0)

    return svg_io, svg_data
