from datetime import datetime
from typing import List

from PIL import Image

from queryes import get_all_data_from_device, get_thermalimage_by_dates, extract_data_from_thermalimage_response


def from_data_to_image(data: List[List], image_name: str) -> None:
    """
    Saves image to 'images/' dir
    """
    img = Image.new('RGB', (32, 24), color='black')
    minimum = 100
    maximum = 0
    for row in data:
        for cell in row:
            minimum = min(minimum, cell)
            maximum = max(maximum, cell)

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            img.putpixel((j, i), ((int(255 * (1 - (maximum - cell) / (maximum - minimum)))), 0, 0))

            img.save(f'images/{image_name}.png')


if __name__ == "__main__":
    date_from = datetime(year=2018, month=10, day=10, hour=11, minute=55)
    date_to = datetime(year=2018, month=10, day=10, hour=12, minute=0)
    all_data = get_all_data_from_device(get_thermalimage_by_dates, {'date_from': date_from, 'date_to': date_to},
                                        extract_data_from_thermalimage_response)
    for image_name, a_picture_data in all_data:
        from_data_to_image(a_picture_data, image_name)
