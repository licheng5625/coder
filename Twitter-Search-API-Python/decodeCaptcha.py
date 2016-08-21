import sys
import io

import requests
import PIL.Image
import tesserwrap


#: https://github.com/gregjurman/tesserwrap
tesseract = tesserwrap.Tesseract()
tesseract.set_variable("tessedit_char_whitelist", "abcdefghijklmnopqrstuvwxyz")

def distinguish_captcha(image_url, show_origin_image=True):
    #: preprocess
    image_bytes = requests.get(image_url).content
    origin_image = PIL.Image.open(io.BytesIO(image_bytes))
    image = origin_image.point(lambda p: p * 1.5)\
        .point(lambda p: 255 if p > 200 else 0)\
        .convert("1")
    #: distinguish the text
    text = tesseract.ocr_image(image)
    #: show the origin image
    #if show_origin_image:
        #origin_image.show()
    text.replace(' ','')
    return text.strip()
def decode_captcha(origin_image):
    image = origin_image.point(lambda p: p * 1.5)\
        .point(lambda p: 255 if p > 200 else 0)\
        .convert("1")
    text = tesseract.ocr_image(image)
    text=text.replace(' ','')
    return text.strip()


def main():
    #url = raw_input("Please input the url of captcha:\n > ").strip()
    #print >> sys.stderr, ">>> Press Ctrl + C to stop."
    #print >> sys.stderr, ">>> Press any key to continue."
    #while True:
        #raw_input()
    import requests
    url=str("http://sitereview.bluecoat.com/rest/captcha.jpg?1470834655096")
    result= distinguish_captcha(url)
    print(result)

# if __name__ == "__main__":
#     try:
#         print(main())
#     except KeyboardInterrupt:
#         print(">>> Exit.", file=sys.stderr)