import pytest
from operator import itemgetter
from plasterpixels import main


@pytest.mark.parametrize(
    'pixel, pixelDiam, expectedUpper, expectedLower',
    [
        (5, 10, (2, 2), (7, 7)),
    ]
)
def testGetCircleCoord(pixel, pixelDiam, expectedUpper, expectedLower):
    circleCoords = main.getCircleCoord(pixel, pixelDiam)
    upperx, uppery, lowerx, lowery = itemgetter('upperx', 'uppery', 'lowerx', 'lowery')(circleCoords)

    assert expectedUpper == (upperx, uppery)
    assert expectedLower == (lowerx, lowery)
