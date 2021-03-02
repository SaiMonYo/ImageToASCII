import PIL.Image
import PIL.ImageEnhance
import time
import math
import string



class ASCII_GENERATOR():
    def __init__(self, file, CHARS, width, cont = None, fileadd = '', showSteps = False):
        #width of the image
        self.width =        width
        #charset for the ascii art
        self.CHARS =        CHARS
        #filename of the image
        self.file =         file
        #error checking
        self.noFile =       False
        try:
            #opens if the image is present
            self.image =    PIL.Image.open(file)
        except:
            #error handling
            print("ERROR - NO FILE FOUND")
            self.noFile =   True
            return
        #contrast for image default is None
        self.cont =         cont
        #used later for holding of ascii art
        self.string =       ''
        self.picture =      ''
        #what wants to be added to name of file - good for testing
        self.fileadd =      fileadd
        self.showSteps = showSteps
        
    def imageResizer(self):
        #gets the width and height of the image that has been opened
        w, h = self.image.size
        #this is so we can get the ratio of the height to width
        #and divide by the ratio of the height to width of an ascii char which is 1.5 
        ratio = h / w / 1.5
        #gets the new height which will be the width wanted * ratio above
        nheight = int(self.width * ratio)
        #resized image = the image resized by the new height and width
        rimage = self.image.resize((self.width, nheight))
        self.image = rimage

    '''DONT USE BUT BUILT OWN CONVERTER TO GREY'''
    def greyifier(self):
        self.builtingrey = False
        pixels = self.image.load()
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                #uses equation from https://en.wikipedia.org/wiki/Grayscale
                # Y' = 0.2126R' + 0.7152G' + 0.0722B'
                pixel = pixels[i,j]
                y = 0
                y += pixel[0] * 0.2126
                y += pixel[1] * 0.7152
                y += pixel[2] * 0.0722
                pixels[i,j] = (int(y))
                
        

    def pixelToASCII(self):
        #getting the values of all the pixels
        pixels = self.image.getdata()
        characters = ''
        for pixel in pixels:
            #getting the corresponding index for the pixel values
            index = round(pixel/(255/len(self.CHARS)))-1
            #preventing rollover as -1 causes it to start indexing from end
            index = index if index != -1 else 0
            #creating a long string of all the ASCII
            characters += self.CHARS[index]
        
        #one line list comprehension - needed the prevention of rollover so didnt work well
        #characters = ''.join([self.CHARS[round(pixel/(255/len(self.CHARS)))-1] for pixel in pixels])
        self.string = characters

    def formatter(self):
        count = len(self.string)
        formatted = ''
        #from 0 to length of the string in steps of the width
        #meaning its processing row by row
        for i in range(0, count, self.width):
            #adding pixels that form a row
            formatted += self.string[i:i+self.width] + '\n'
        
        self.picture = formatted

    def addContrast(self, amm):
        if amm == None:
            return
        #adds contrast
        self.image = PIL.ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(amm)

    def main(self):
        if self.noFile:
            #handles error
            return
        #gets start time
        if self.showSteps:
            self.image.show()
        start = time.time()
        #dds contrast
        self.addContrast(self.cont)
        if self.showSteps:
            self.image.show()
        #resizes
        self.imageResizer()
        if self.showSteps:
            self.image.show()
        #converts to greyscale
        self.image = self.image.convert("L")
        if self.showSteps:
            self.image.show()
        #converts pixels to ascii
        self.pixelToASCII()
        #formats it
        self.formatter()
        #gets file name to write to
        split = self.file.split('.')
        asciifilename = split[0] + "_ascii" + self.fileadd + ".txt"
        #asciifilename = "test" + self.fileadd + ".txt"

        #writes to file
        #will write to the same folder as the file was in
        with open(asciifilename,"w") as f:
            f.write(self.picture)
        end = time.time()
        print(f"finished in {end-start}s")

    
'''characters - first two work better the longer char set needs more testing and fine tuning'''
#CHARS = '@#&%?"*+;:.'
CHARS = '.:;+*"?%&#@'
#CHARS = '#£0L.'
#CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
#CHARS = CHARS[::-1]


#1000 creates a file of around 1mill characters
#need notepad++ to view 
WIDTH = 1000

gen = ASCII_GENERATOR("knight.jpg", CHARS, WIDTH)

gen.main()


