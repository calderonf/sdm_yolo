from ctypes import *
import math
import random
import cv2

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    return (ctype * len(values))(*values)

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


# subclassing the ctypes.Structure class to add new features
class _Structure(Structure):
    def __repr__(self):
        """
        Print the fields
        """
        res = []

        for field in self._fields_:
            res.append('%s=%s' % (field[0], repr(getattr(self, field[0]))))

        return self.__class__.__name__ + '(' + ','.join(res) + ')'

class IplTileInfo(_Structure):
    _fields_ = []

class IplROI(_Structure):
    _fields_ = \
    [
        # 0 - no COI (all channels are selected)
        # 1 - 0th channel is selected ...
        ('coi', c_int),
        ('xOffset', c_int),
        ('yOffset', c_int),
        ('width', c_int),
        ('height', c_int),
    ]

# ipl image header
class IplImage(_Structure):
    def __repr__(self):
        """
        Print the fields
        """
        res = []

        for field in self._fields_:
            if field[0] in ['imageData', 'imageDataOrigin']:
                continue

            res.append('%s=%s' % (field[0], repr(getattr(self, field[0]))))

        return self.__class__.__name__ + '(' + ','.join(res) + ')'

IplImage._fields_ = [
    ("nSize", c_int),
    ("ID", c_int),
    ("nChannels", c_int),
    ("alphaChannel", c_int),
    ("depth", c_int),
    ("colorModel", c_char * 4),
    ("channelSeq", c_char * 4),
    ("dataOrder", c_int),
    ("origin", c_int),
    ("align", c_int),
    ("width", c_int),
    ("height", c_int),
    ("roi", POINTER(IplROI)),
    ("maskROI", POINTER(IplImage)),
    ("imageID", c_void_p),
    ("tileInfo", POINTER(IplTileInfo)),
    ("imageSize", c_int),
    ("imageData", c_char_p),
    ("widthStep", c_int),
    ("BorderMode", c_int * 4),
    ("BorderConst", c_int * 4),
    ("imageDataOrigin", c_char_p)]


class iplimage_t(_Structure):
    _fields_ = \
    [
        ('ob_refcnt', c_ssize_t),
        ('ob_type',  py_object),
        ('ipl_ptr', POINTER(IplImage)),
        ('data', py_object),
        ('offset', c_size_t)
    ]





lib = CDLL("../libdarknet.so", RTLD_GLOBAL)
#lib = CDLL("libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

make_boxes = lib.make_boxes
make_boxes.argtypes = [c_void_p]
make_boxes.restype = POINTER(BOX)

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

num_boxes = lib.num_boxes
num_boxes.argtypes = [c_void_p]
num_boxes.restype = c_int

make_probs = lib.make_probs
make_probs.argtypes = [c_void_p]
make_probs.restype = POINTER(POINTER(c_float))

detect = lib.network_predict
detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

network_detect = lib.network_detect
network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

#image ipl_to_image(IplImage* src)
ipl_2_image= lib.ipl_to_image
ipl_2_image.argtypes = [POINTER(IplImage)]
ipl_2_image.restype = IMAGE



ipl_in2_image=lib.ipl_into_image
ipl_in2_image.argtypes = [POINTER(IplImage),IMAGE]

save_image =lib.save_image
save_image.argtypes = [IMAGE, c_char_p]

rgbgr_image=lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

"""
void ipl_into_image(IplImage* src, image im)
{
    unsigned char *data = (unsigned char *)src->imageData;
    int h = src->height;
    int w = src->width;
    int c = src->nChannels;
    int step = src->widthStep;
    int i, j, k;

    for(i = 0; i < h; ++i){
        for(k= 0; k < c; ++k){
            for(j = 0; j < w; ++j){
                im.data[k*w*h + i*w + j] = data[i*step + j*c + k]/255.;
            }
        }
    }
}
"""





def get_ndarray_dimensions(img):
    # getting image shape information
    img_shape = img.shape
    img_shape_length = len(img_shape)

    # validating parameters
    if img_shape_length <= 1 or img_shape_length > 3:
        raise ArgumentError('Invalid image information. We support images with 1, 2 or 3 channels only.')

    # getting the amount of channels
    nc = 1 if img_shape_length == 2 else img_shape[2]

    # building the processed image
    h, w = img_shape[0], img_shape[1]

    # returning the height, width and nChannels
    return h, w, nc


def get_iplimage_ptr(img):
    # None is considered as the NULL pointer
    if img is None:
        return None     # the same thing as 'return img'

    # getting image dimensions and data
    height, width, n_channels = get_ndarray_dimensions(img)
    img_data = img.tostring()

    # creating the image header
    cv_img = cv2.cv.CreateImageHeader((width, height), cv2.cv.IPL_DEPTH_8U, n_channels)
    width_step = img.dtype.itemsize * n_channels * width  # creating the famous 'width_step' parameter
    cv2.cv.SetData(cv_img, None, width_step)

    # setting the data (img is a numpy array)
    ipl = iplimage_t.from_address(id(cv_img))
    ipl_img_ptr = ipl.ipl_ptr.contents
    ipl_img_ptr.imageData = img_data

    # returning the OpenCV2.2 compatible image (IplImage*)
    return ipl_img_ptr,cv_img


def copy_iplimage_ptr(img,ipl_img_ptr_in,cv_img):
    if img is None:
        return None     # the same thing as 'return img'
    ipl = iplimage_t.from_address(id(cv_img))
    ipl_img_ptr = ipl.ipl_ptr.contents
    #ipl_img_ptr = ipl_img_ptr_in
    ipl_img_ptr.imageData = img.tostring()
    return ipl_img_ptr


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, image, thresh=.24, hier_thresh=.5, nms=.3):
    print ('cargando imagen')    
    im = load_image(image, 0, 0)
    print (type(im))
    print ('Imagen cargada')
    save_image(im,"detected")
    boxes = make_boxes(net)
    probs = make_probs(net)
    num =   num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res
    
def detect_img(net, meta, im, thresh=.24, hier_thresh=.5, nms=.3):
    #print ('cargando imagen')    
    #im = load_image(image, 0, 0)
    #print (type(im))
    #print ('Imagen cargada')
    boxes = make_boxes(net)
    probs = make_probs(net)
    num =   num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    #free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res
    
if __name__ == "__main__":
    #net = load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
    #im = load_image("data/wolf.jpg", 0, 0)
    #meta = load_meta("cfg/imagenet1k.data")
    #r = classify(net, meta, im)
    #print r[:10]
    #net = load_net("../cfg/tiny-yolo-voc.cfg", "../tiny-yolo-voc.weights", 0)
    #meta = load_meta("../cfg/voc_py.data")
    
    net = load_net("../cfg/yolo-voc.cfg", "../yolo-voc.weights", 0)
    meta = load_meta("../cfg/voc_py.data")
    r = detect(net, meta, "../data/person.jpg")
    
    print (r)
    imgFile = cv2.imread("../data/person.jpg")
    

    
    for i in range(0,len(r)):
        w=int(r[i][2][2])
        h=int(r[i][2][3])
        x=int(r[i][2][0])-w/2
        y=int(r[i][2][1])-h/2
        cv2.rectangle(imgFile, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
    
    cv2.imshow('dst_rt', imgFile)        
    cv2.waitKey(500)    

    
    #primera vez
    
    imgFile2 = cv2.imread("../data/eagle.jpg")
    tama=imgFile2.shape
    imgImported=make_image(tama[1],tama[0],tama[2])
    
    
    imgFileptr,iplimg=get_iplimage_ptr(imgFile2)    
    ipl_in2_image(imgFileptr,imgImported)
    rgbgr_image(imgImported)
    #save_image(imgImported,"eagle_detect")
    r = detect_img(net, meta, imgImported) 
    print (r)
    for i in range(0,len(r)):
        w=int(r[i][2][2])
        h=int(r[i][2][3])
        x=int(r[i][2][0])-w/2
        y=int(r[i][2][1])-h/2
        cv2.rectangle(imgFile2, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
    cv2.imshow('dst_rt2', imgFile2)        
    cv2.waitKey(1) 

    print ('copiar apuntador')
    
    for mm in range (0,10):
        imgFile3 = cv2.imread("../data/eagle2.jpg")
        tama=imgFile3.shape
        #imgImported=make_image(tama[1],tama[0],tama[2])
        imgFileptr=copy_iplimage_ptr(imgFile3,imgFileptr,iplimg)
        
        ipl_in2_image(imgFileptr,imgImported)
        #save_image(imgImported,"dog_detect")
        r = detect_img(net, meta, imgImported) 
        
        print (r)
        
        for i in range(0,len(r)):
            w=int(r[i][2][2])
            h=int(r[i][2][3])
            x=int(r[i][2][0])-w/2
            y=int(r[i][2][1])-h/2
            cv2.rectangle(imgFile3, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
        
        cv2.imshow('dst_rt3', imgFile3)   
        print ('voy en ciclo' +str(mm)   )  
        cv2.waitKey(2) 
    

    print ('Saliendo...')
    cv2.destroyAllWindows()
    
    
    """
    
        source=imgFile.copy()
    bitmap = cv2.cv.CreateImageHeader((source.shape[1], source.shape[0]), cv2.cv.IPL_DEPTH_8U, 3)
    if len(source.shape)==3:
        cv2.cv.SetData(bitmap, source.tostring(),source.dtype.itemsize * 3 * source.shape[1])    
    else:
        print("Posible error no se si soporta imagenes en blanco y negro")
        cv2.cv.SetData(bitmap, source.tostring(),source.dtype.itemsize * 1 * source.shape[1])  
    #bitmap2=get_iplimage_ptr(source)
    """
    
    
    
    
    
    
    
    
    
    
    

