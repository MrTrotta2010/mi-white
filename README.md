# Am I White Enough For Twitter?
Have you ever wondered if you're white enough to appear in a thumbnail automatically cropped by Twitter? Well, wonder no more!

"Am I White Enough For Twitter?", or "mi white" for short, is meant as a criticism towards algorithmic racism and targets especially Twitter’s cropping algorithm, which often behaves in racially biased ways (if you don’t know what we’re talking about, [click here](https://www.dw.com/en/twitter-image-cropping-racist-algorithm/a-55085160))

#### How does it work?
mi white receives a picture as input and uses OpenCV to calculate it's crop in a purposefully bad way, exagerating a specific situation to expose algorithmic racial biases.

### Pre-requisites
- Python 3
- Django (for Web Application)
- OpenCV 4 (compiled from font, to include _Saliency_ module)
- Numpy
- Argparse (for Command Line Utility)

### How to run the Command Line Utility
```$ python3 mi_white -f <path of input image> -o <optional: path to save cropped image> ``` 
