import json
import os, os.path, shutil

threshold = 0.75

def get_all_objects():
    
    all_objects = {}
    i = 0 
    with open("./camera/_object_settings.json", "r") as file:
        data = file.read()
    jsonDataAsPythonValue = json.loads(data)
    for name in jsonDataAsPythonValue['exported_object_classes']:
        with open("./results/obj.names", "a") as file:
            file.write(f'{name}\n')
        all_objects[name] = i
        i+=1
    return all_objects


def get_camera_res():
    with open("./camera/_camera_settings.json", "r") as file:
        data = file.read()
    jsonDataAsPythonValue = json.loads(data)
    width = jsonDataAsPythonValue['camera_settings'][0]['captured_image_size']['width']
    height = jsonDataAsPythonValue['camera_settings'][0]['captured_image_size']['height']
    return width, height

def get_image_res(file_name):
    from PIL import Image
    import os.path

    filename = os.path.join(f'data_train/{file_name}')
    img = Image.open(filename)
    return img.size[0], img.size[1]
    


def is_visible_object(file_name):
    visible_objects = []
    with open(file_name, "r") as file:
        data = file.read()
    jsonDataAsPythonValue = json.loads(data)
    for obj in jsonDataAsPythonValue['objects']:
        if obj['visibility'] >= threshold:
            visible_objects.append(obj)
    return visible_objects

def calculate_coordinates(obj, image_width, image_height):
    
    
    x_top = obj['bounding_box']['top_left'][1]
    y_top = obj['bounding_box']['top_left'][0]
       
    x_bottom = obj['bounding_box']['bottom_right'][1]  
    y_bottom = obj['bounding_box']['bottom_right'][0]
        
    x_final = (((x_bottom - x_top)/2+x_top)/image_width)
    y_final = (((y_bottom - y_top)/2+y_top)/image_height)
        
    width_final = ((x_bottom - x_top)/image_width)
    height_final = (((y_bottom - y_top))/image_height)
    
    if x_final <=1 and x_final > 0 and y_final <=1 and y_final > 0 and width_final <=1 and width_final > 0 and height_final <=1 and height_final > 0:
        are_correct = True
    else:
        are_correct = False
        
    return are_correct, "{:.6f} {:.6f} {:.6f} {:.6f}".format(x_final, y_final, width_final, height_final) 
   
def copy_image(image_name, path_in, path_out):
    shutil.copyfile(f'{path_in}{image_name}', f'{path_out}{image_name}')

def create_train_txt(image_name):
    with open("./results/train.txt", "a") as file:
        file.write(f'results/images/train/{image_name}\n')

def create_valid_txt(image_name):
    with open("./results/valid.txt", "a") as file:
        file.write(f'results/images/valid/{image_name}\n')

def create_data_file(all_objects):
    with open("./results/obj.data", "a") as file:
        file.write(f'classes = {len(all_objects)}\n')
        file.write("train = results/train.txt\n")
        file.write("valid = results/valid.txt\n")
        file.write("names = results/obj.names.txt\n")
        file.write("backup = backup\n")


def modify_yolo_cfg(num_classes):
    if num_classes < 2:
        max_batches = 4000
    else:
        max_batches = 2000 * num_classes
    
    file = open("yolo-obj.cfg", "rt")
    data = file.readlines()
    file.close()
    
    os.remove("yolo-obj.cfg")
    
    num_conv = 0
    
    file = open("yolo-obj.cfg", "a")   
    for line in data:
        if line != '':
            if line.split('=')[0].strip() == 'batch':
                line = f'batch={64}\n'
            if line.split('=')[0].strip() == 'subdivisions':
                line = f'subdivisions={32}\n'
            if line.split('=')[0].strip() == 'width':
                line = f'width={416}\n'
            if line.split('=')[0].strip() == 'height':
                line = f'height={416}\n'
            if line.split('=')[0].strip() == 'max_batches':
                line = f'max_batches = {max_batches}\n'
            if line.split('=')[0].strip() == 'steps':
                line = f'steps={int(0.8*max_batches)},{int(0.9*max_batches)}\n'
            if line.split('=')[0].strip() == 'classes':
                line = f'classes={num_classes}\n'     
            if line.split('=')[0].strip() == '[convolutional]':  #to takie na szybko
                num_conv += 1
            if line.split('=')[0].strip() == 'filters' and (num_conv == 59 or num_conv == 67 or num_conv == 75):  #to takie na szybko
                line = f'filters={(num_classes + 5)*3}\n'
        file.write(f'{line}')

    
   
        
#

try: 
    os.mkdir('camera')
except OSError as error: 
    print(error)
try: 
    os.mkdir('backup')
except OSError as error: 
    print(error)  
try:
    shutil.move('./data_train/_camera_settings.json', './camera/_camera_settings.json')
except OSError as error: 
    print(error)
    
try:
    os.remove('./data_valid/_camera_settings.json')
except OSError as error: 
    print(error)
    
try:
    shutil.move('./data_train/_object_settings.json', './camera/_object_settings.json')
except OSError as error: 
    print(error) 

try:
    os.remove('./data_valid/_object_settings.json')
except OSError as error: 
    print(error) 


width_camera, height_camera = get_camera_res()

width_image, height_image = get_image_res(os.listdir('./data_train/')[0])

try:
    shutil.rmtree('results')
except OSError as error: 
    print(error) 

try:
    os.mkdir('results')
except OSError as error: 
    print(error) 

try:
    os.mkdir('results/images')
except OSError as error: 
    print(error) 
try:
    os.mkdir('results/images/train')
except OSError as error: 
    print(error) 
try:
    os.mkdir('results/images/valid')
except OSError as error: 
    print(error) 



    
    
    

all_objects = get_all_objects()

create_data_file(all_objects)

modify_yolo_cfg(len(all_objects))


for file_name in os.listdir('./data_train/'):
     if file_name.endswith('.json'):
        file_name = './data_train/' + file_name
        visible_objects = is_visible_object(file_name)
        file_name = file_name.replace('./data_train/','')
        
        png_name = file_name.replace('json','png')
        copy_image(png_name, 'data_train/', 'results/images/train/')
        create_train_txt(png_name)
        
        
        file_name = file_name.replace('json','txt')
        
        with open(f"./results/images/train/{file_name}", "w+") as file:
            for obj in visible_objects:
                num_class = all_objects[obj['class']]
                are_correct, dimensions = calculate_coordinates(obj, width_image, height_image)
                if are_correct:
                    file.write(f"{num_class} {dimensions}\n")


for file_name in os.listdir('./data_valid/'):
     if file_name.endswith('.json'):
        file_name = './data_valid/' + file_name
        visible_objects = is_visible_object(file_name)
        file_name = file_name.replace('./data_valid/','')
        
        png_name = file_name.replace('json','png')
        copy_image(png_name, 'data_valid/', 'results/images/valid/')
        create_valid_txt(png_name)
        
        
        file_name = file_name.replace('json','txt')
        
        with open(f"./results/images/valid/{file_name}", "w+") as file:
            for obj in visible_objects:
                num_class = all_objects[obj['class']]
                are_correct, dimensions = calculate_coordinates(obj, width_image, height_image)
                if are_correct:
                    file.write(f"{num_class} {dimensions}\n")
