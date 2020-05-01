from PIL import ImageGrab
import numpy as np
import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import time

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass


def label_object(frame, message, position):
    position = (position[0], position[1] - 10)
    return cv2.putText(frame, message,  position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2 )


def find_gumpas(frame, processed_frame, draw = True):
    w, h = gumpa_template.shape[::-1]
    
    #processed_img =  cv2.Canny(processed_frame, threshold1 = 200, threshold2=300)
    #gumpa_temp = cv2.Canny(gumpa_template, threshold1 = 200, threshold2=300)
    res = cv2.matchTemplate(processed_frame, gumpa_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.55
    loc = np.where( res >= threshold)
    print(res.max())
    for pt in zip(*loc[::-1]):
        pt = (pt[0]-int(w/4), pt[1]-int(h))
        if draw:
            print(pt)
            cv2.rectangle(frame, pt,
                          (pt[0] + int(1.5*w),
                           pt[1]+ int(2.5*h)), 
                           (0,0,255),
                           2)
            label_object(frame, "GUMPA", pt)
        processed_frame[pt[1]:pt[1]+ int(2.5*h), pt[0]:pt[0]+ 2*w] = 0
    return processed_frame, frame

def find_pipes(frame, processed_frame, draw = True):
    w, h = pipe_template.shape[::-1]
    
    res = cv2.matchTemplate(processed_frame, pipe_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        if draw:
            cv2.rectangle(frame, pt, (pt[0] + w, frame.shape[0]), (0,0,255), 2)
            label_object(frame, "PIPE", pt)
        processed_frame[pt[1]:, pt[0]:pt[0]+w] = 0

    return processed_frame, frame
    
    

def process_image(image):
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    #processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    return processed_img

def detect_moviment(previous_frame, current_frame):
    pass


def screen_record(region =None): 
    last_time = time.time()
    if region:
            xleft,ytop,x2, y2, = region
            
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    lol=0
    while(lol != -1):
        try:
            frame =  np.array(ImageGrab.grab(bbox=(xleft*1.25,ytop*1.25, x2*1.25, y2*1.25)))
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            processed_frame = process_image(frame)
            floor = processed_frame[int(-0.1*frame_height):int(-0.05*frame_height),:]
            #print('FPS: {}'.format(1/(time.time()-last_time)))
            last_time = time.time()
            #lines = cv2.HoughLinesP(processed_frame, 1, np.pi/180, 180, 20, 15)
            #draw_lines(processed_frame,lines)
            contours, hierarchy = cv2.findContours(processed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_idx = np.where(hierarchy[0][:,3]!=np.inf)[0]
             
            processed_frame, frame = find_pipes(frame, processed_frame)
            processed_frame, frame = find_gumpas(frame, processed_frame)
            cv2.imshow('window', frame[:,:,::-1])
            #[:,:,::-1]
            '''
            connectivity = 4
            nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(processed_frame, connectivity, cv2.CV_32S)
            sizes = stats[1:, -1]; nb_components = nb_components - 1
            min_size =50 #threshhold value for objects in scene
            for i in range(0, nb_components):
                if sizes[i] <= min_size: 
                # draw the bounding rectangele around each object
                    cv2.rectangle(frame, (stats[i][0],stats[i][1]),(stats[i][0]+stats[i][2],stats[i][1]+stats[i][3]), (0,255,0), 2)
            cv2.imshow('window', frame)

            
            
            template = cv2.imread('C:\\Users\\alves\\OneDrive\\Documentos\\Dev\\Super-Mario-Bot\\Super-Mario-Bot\\templates\\mario_color.png', 0)
            template = cv2.resize(template, (50,60), interpolation = cv2.INTER_AREA)

            w, h= template.shape[::-1]
            methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

            for meth in [9]:
                
                method = eval(methods[0])
                img = frame
            
                # Apply template Matching
                res = cv2.matchTemplate(processed_frame[:,:int(-0.4*frame_width)] ,template,method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > 0:
                    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                        top_left = min_loc
                    else:
                        top_left = max_loc
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                
                    cv2.rectangle(processed_frame,top_left, bottom_right, 255, 2)
                
                processed_frame = cv2.putText(processed_frame, str(max_val),  (50, 50) , cv2.FONT_HERSHEY_SIMPLEX,  
                                    1, (255, 0, 0) , 1, cv2.LINE_AA) 
            cv2.imshow('window', processed_frame)
            #[:,:,::-1]
        
            
            for j in contours_idx:
            #for cnt in contours:
                #print(j, len(contours))
                cnt = contours[j]
                cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
                x,y,w,h = cv2.boundingRect(cnt)
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imshow('window', processed_frame)
           '''
            lol +=1
            previous_frame = frame
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        except Exception as e:
            print(e)
            traceback.print_exc()
            return hierarchy, contours, frame
    return processed_frame
import sys
import traceback

pipe_template = cv2.imread('..\\templates\\mario_pipe_color.png',0)
            

gumpa_template = cv2.imread('..\\templates\\gumpa_face.png',0)
gumpa_template = cv2.resize(gumpa_template, (int(gumpa_template.shape[0]*0.8), int(gumpa_template.shape[1]*0.8)), interpolation = cv2.INTER_AREA)

if __name__ == "__main__":
    print("Starting")
    region = [310, 241, 919, 654]
    if region:
            xleft,ytop,x2, y2, = region
    time.sleep(2)
    err = screen_record(region)
 
    template_x = gumpa_template.shape[0]
    template_y = gumpa_template.shape[1]
    similarity_max = np.inf
    
    for i in range(err.shape[0] - template_x):
        for j in range(err.shape[1] - template_y):
            similarity = np.abs(err[i:i+template_x, j:j+template_y] - gumpa_template).mean()
            if similarity < similarity_max:
                similarity_max = similarity
                
    def show(img):
        cv2.imshow('window2', img)
        cv2.waitKey()