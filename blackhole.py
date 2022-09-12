from vpython import *
from random import randint, uniform
import numpy as np
from math import ceil

scene = canvas(background=color.white)
# scene.visible = False
scene.resizable = False
scene.width = 1920
scene.height = 1079
# scene.width = scene.height = 0

running = False
# momentum_ = vec(160, 0, 0)
# L = 4*10**10
# L = 4e10

blackhole_mass = 0  
first_launch = True

"""---------- Переменные ----------"""
scene.forward = vec(0,0,-1)
DEFAULT_CAMERA_POS = scene.camera.pos
DEFAULT_CAMERA_AXIS = scene.camera.axis
ACCRETION_DISK_LAYERS = 30
DISK = ""
MODEL_RATE = 100
blackhole_config_list = [""]
object_config_list = [""]
wg = []
XYZ_ENABLED = False
OBJECTS_MAKE_TRAIL = True
OBJECTS_TRAIL_LENGTH = 100
OBJECTS_TRAIL_RADIUS = 1
latest_selected_blackhole_config_index = 0
latest_selected_object_config_index = 0
first_import = True
nowhit = None
lasthit = None
lastcolor = tuple([0, 0, 0])
C = 63241.25
G = 39.41
# L = (2 * G * 4297000) / (C ** 2)
L = 10
print(f"L: {L}")
scene.range = 8*L
object_preview = [0, 0]
object_checked = 0
momentum_ = vector(0, 0, 0)
xyz_curve = 0
info_text = info_object_text = info_camera = ""
nowhit_pos = 0
nowhit_oldpos = 0
stars_names = []
color_list = [color.red, color.orange, color.yellow, color.green, color.cyan, color.blue, color.magenta, color.purple,  color.white]
"""--------------------------------"""
# light_ring = ring(pos=vector(0,0,0), axis=vec(0, 0, 1), radius=2.5*L, thickness=L/16, emissive=True)

xyz_curve = curve(color=color.red, name="xyz")
xyz_curve.append(vec(0, 0, 0))
xyz_curve.append(vec(2*L, 0, 0))
xyz_curve.append(vec(0, 0, 0))
xyz_curve.append(vec(0, 0, 0), color=color.green)
xyz_curve.append(vec(0, 2*L, 0), color=color.green)
xyz_curve.append(vec(0, 0, 0), color=color.green)
xyz_curve.append(vec(0, 0, 0), color=color.blue)
xyz_curve.append(vec(0, 0, 2*L), color=color.blue)
xyz_curve.append(vec(0, 0, 0), color=color.blue)

# blackhole = sphere(pos=vec(0, 0, 0), radius=L, mass=1000, momentum=vec(0, 0, 0), make_trail=True,texture=textures.kosmos)
# blackhole = sphere(pos=vec(0, 0, 0), radius=L, color=color.gray(0.05),mass=1000, momentum=vec(0, 0, 0), make_trail=True, shininess=0,name="blackhole", emissive=True)
ri = ring(pos=vector(0,0,0), axis=vec(0, 0, 1), radius=1.5*L+L/8, thickness=L/8, emissive=True, name="ring")
# ri = extrusion(path=[vec(0,0,-L/100), vec(0,0,L/100)],shape=shapes.circle(radius=1.5*L), color=color.black, opacity=0.5, shininess=0)
void= sphere(pos=vec(0, 0, 0), radius=1.5*L, color=color.black, make_trail=True, shininess=1, name="void", emissive=True)
blackhole = sphere(pos=vec(0, 0, 0), radius=L, color=color.black, mass=4297000, make_trail=True, shininess=0, name="blackhole", opacity=1,emissive=True)
# s = sphere(pos=vec(0, 0, 0), radius=1.5*L, color=color.white, make_trail=True, shininess=1, opacity=0.5, emissive=True)

# bg = box(pos=vec(0,0,0), shininess=0, color=color.white, texture="https://img5.goodfon.ru/wallpaper/nbig/7/ca/kosmos-zviozdy-vselennaia-space-stars-universe.jpg", size=vec(50e10, 50e10, 50e10))

def cosmos_bg():
    global bg
    x = scene.camera.pos.x
    y = scene.camera.pos.y
    z = scene.camera.pos.z
    maxx = max(x, y, z)
    step = ((bg.size.x-x)*10+100e10)
    scene.lights = []
    scene.lights.append(local_light(pos=vec(step,0,0), color=color.white))
    scene.lights.append(local_light(pos=vec(-step,0,0), color=color.white))
    scene.lights.append(local_light(pos=vec(0, step,0), color=color.white))
    scene.lights.append(local_light(pos=vec(0, -step,0), color=color.white))
    scene.lights.append(local_light(pos=vec(0,0,step), color=color.white))
    scene.lights.append(local_light(pos=vec(0,0,-step), color=color.white))
    
    bg.size = vec(step, step, step)

def handle_click():
    global nowhit, lasthit, lastcolor, nowhit_pos, nowhit_oldpos
    if lasthit != None:
        lasthit.color = vec(*lastcolor)
    nowhit = scene.mouse.pick
    if nowhit != None and (nowhit.name == "blackhole" or nowhit.name == "void" or nowhit.name == "xyz" or nowhit.name == "ring"):
        nowhit = None
    if nowhit:
        nowhit_oldpos = nowhit.pos
        lasthit = nowhit
        lastcolor = tuple([lasthit.color.x, lasthit.color.y, lasthit.color.z])
        nowhit.color = 5*nowhit.color


scene.bind("mousedown", handle_click)

"""------------ Общие виджеты ------------"""
# # Фунцкия для вкл/выкл модели
def toggle_running(b):
    global running, info_text
    running = not running
    if running:
        info_text.text = f"<span id='info-text'>> Пуск</span>"  
        b.text = "Пауза"
    else:
        info_text.text = f"<span id='info-text'>> Пауза</span>"  
        b.text = "Пуск"

      


# Функция для запуска
def start():
    global stars, wg, nowhit, stars_names, stars_pos, hitlist, stars_balls, stars_balls_hitlist, MODEL_RATE, OBJECTS_MAKE_TRAIL, scene, OBJECTS_TRAIL_LENGTH, stars_pos, xyz_curve
    xyz_curve.visible = False
    s = wg[0][1]
    wg[0][2].text = '{0:d}'.format(s.value)
    MODEL_RATE = s.value = 100
    reset_camera_position()
    OBJECTS_TRAIL_LENGTH = 100 
    s = wg[0][3]
    s.value = OBJECTS_TRAIL_LENGTH
    wg[0][4].text = '{0:d}'.format(s.value)
    for i in range(len(stars)):
        stars[i].visible = False
        stars[i].force = 0
        stars[i].mass = 0
        stars[i].radius = 0
        stars[i].pos = vec(0, 0, 0)
        stars[i].clear_trail()
        hitlist.append(i)
    for i in range(len(stars_balls)):
        stars_balls[i].visible = False
        stars_balls[i].force = 0
        stars_balls[i].mass = 0
        stars_balls[i].radius = 0
        stars_balls[i].pos = vec(0, 0, 0)
        stars_balls[i].clear_trail()
        stars_balls_hitlist.append(i)
    index = ''
    if nowhit != None:
        index = stars.index(nowhit)
    hitlist.sort()
    stars_balls_hitlist.sort()
    hitlist = hitlist[::-1]
    stars_balls_hitlist = stars_balls_hitlist[::-1]
    if index in hitlist:
        nowhit = None
    for i in hitlist:
        del stars[i]
        del stars_names[i]
        del stars_pos[i]
    for i in stars_balls_hitlist:
        del stars_balls[i]
    hitlist = []
    stars_balls_hitlist = []
    print(stars)
    

def toggle_xyz():
    global XYZ_ENABLED, xyz_curve
    XYZ_ENABLED = not XYZ_ENABLED
    xyz_curve.visible = XYZ_ENABLED
    info_text.text = f"<span id='info-text'>> XYZ = {XYZ_ENABLED}</span>"  



# Функция для сброса положения камеры
def reset_camera_position():
    global DEFAULT_CAMERA_AXIS, DEFAULT_CAMERA_POS, scene, info_text
    scene.camera.axis = DEFAULT_CAMERA_AXIS
    scene.forward = vec(0, 0, -1)
    scene.camera.pos = DEFAULT_CAMERA_POS
    scene.range = 8*L
    info_text.text = f"<span id='info-text'>> Сброс</span>"  


# Фунцкия для изменения скорости модели
def change_rate(s):
    global wg, MODEL_RATE, info_text
    wg[0][2].text = '{0:d}'.format(s.value)
    MODEL_RATE = s.value
    info_text.text = f"<span id='info-text'>> Скорость модели = {MODEL_RATE}</span>"  


# Функция для вкл/выкл следа объектов
def toggle_trail():
    global OBJECTS_MAKE_TRAIL, info_text
    OBJECTS_MAKE_TRAIL = not OBJECTS_MAKE_TRAIL
    for obj in scene.objects:
        if obj.name not in ["ring", "void", "blackhole", "xyz"]:
            print(obj.name)
            obj.clear_trail()
            obj.make_trail = OBJECTS_MAKE_TRAIL
    info_text.text = f"<span id='info-text'>> OBJECTS_MAKE_TRAIL = {OBJECTS_MAKE_TRAIL}</span>"  


# Фунцкия для изменения длины следа объектов
def change_trail_length(s):
    global wg, scene, info_text, OBJECTS_TRAIL_LENGTH
    wg[0][4].text = '{0:d}'.format(s.value)
    for obj in scene.objects:
        obj.retain = s.value
    OBJECTS_TRAIL_LENGTH = s.value

    info_text.text = f"<span id='info-text'>> Длина следа объектов = {OBJECTS_TRAIL_LENGTH}</span>"  


# Фунцкия для изменения радиуса следа объектов
def change_trail_radius(s):
    global wg, scene, info_text, OBJECTS_TRAIL_RADIUS
    wg[0][6].text = '{:.2f}'.format(s.value)
    OBJECTS_TRAIL_RADIUS = s.value
    for obj in scene.objects:
        obj.trail_radius = round(OBJECTS_TRAIL_RADIUS, 1)
    info_text.text = f"<span id='info-text'>> Радиус следа объектов = {round(OBJECTS_TRAIL_RADIUS, 1)}</span>"  
"""------------ Виджеты чёрной дыры ------------"""
def blackhole_config_write():
    global blackhole_config_list
    f = open("./blackhole_config.txt", mode='w', encoding='utf-8')
    print(f"config_write {blackhole_config_list}")
    for l in blackhole_config_list: 
        f.write(f"{l[0]}!{l[1]}!{l[2]}\n")  
    f.close()
    build_widgets()


def get_blackhole_configs():
    global blackhole_config_list
    blackhole_config_list = []
    f = open("./blackhole_config.txt", mode='r', encoding='utf-8')
    for line in f:
        l = line.strip().split("!")
        l[1] = eval(l[1])
        blackhole_config_list.append(l)
    f.close()
    blackhole_config_choices = []
    print(f"# Кфг черной дыры {blackhole_config_list}")
    for i in range(len(blackhole_config_list)):
        s = f"{blackhole_config_list[i][0]} - {blackhole_config_list[i][1]} Msun - радиус {blackhole_config_list[i][2]} "
        if not i:
            s += " (default)"
        blackhole_config_choices.append(s)
    return blackhole_config_choices


def blackhole_choose_config(m):
    global xyz_curve, latest_selected_blackhole_config_index, scene, blackhole_config_list, ri, void, blackhole, L
    latest_selected_blackhole_config_index = m.index
    blackhole.mass = float(blackhole_config_list[m.index][1])
    L = float(blackhole_config_list[m.index][2])
    blackhole.radius = L
    scene.range = 8*L
    ri.radius=1.5*L+L/8
    ri.thickness=L/8
    void.radius=1.5*L
    xyz_curve.radius = L/16
    xyz_curve.visible = False
    print(f"{m.index})  {blackhole.mass}, {blackhole.radius}")


def blackhole_delete_config(b):
    global wg, blackhole_config_list
    index = wg[1][0].index
    del blackhole_config_list[index]
    if index == latest_selected_blackhole_config_index:
        wg[1][0].index = 0
        blackhole.mass = int(int(blackhole_config_list[0][1]))
    blackhole_config_write()


def blackhole_add_config(b):
    global blackhole_config_list, wg
    wg[1][6].text = ""
    name = wg[1][2].text
    mass = wg[1][3].number
    radius = wg[1][4].text
    print(f"create bh cfg {name}, {mass}")
    if name and mass and radius != "":
        wg[1][2].text = ""
        wg[1][3].text = ""
        wg[1][4].text = ""
        radius = float(radius)
        if radius == 0:
            radius = round((2 * G * mass) / (C ** 2), 5)
        blackhole_config_list.append([name, mass, radius])
        print("blackhole cfg list", blackhole_config_list)
        blackhole_config_write()
    else:
        wg[1][6].text = "\t<span style='color:red;font-weight:600;font-size:16px'>Неккоректный ввод!</span>"


"""------------ Виджеты объекта ------------"""
def object_config_write():
    global object_config_list
    f = open("./object_config.txt", mode='w', encoding='utf-8')
    for l in object_config_list:
        s = "!".join(l)
        f.write(f"{s}\n")
    f.close()
    build_widgets()


def get_object_configs():
    global object_config_list
    object_config_list = []
    f = open("./object_config.txt", mode='r', encoding='utf-8')
    for line in f:
        l = line.strip().split("!")
        # l[1] = eval(l[1])
        object_config_list.append(l)
    f.close()
    object_config_choices = ["Выберите конфигурацию"]
    print(f"# Кфг объекта {object_config_list}")
    for i in range(len(object_config_list)):
        s = object_config_list[i][0]
        if not i:
            s += " (default)"
        object_config_choices.append(s)
    return object_config_choices


def object_choose_config(m):
    global latest_selected_object_config_index
    latest_selected_object_config_index = m.index
    print(f"choose config {latest_selected_object_config_index}")
    if m.index != 0:
        wg[2][3].disabled = False
        wg[2][4].disabled = False
        wg[2][5].disabled = False
        wg[2][6].disabled = False
        wg[2][7].disabled = False
        wg[2][2].text   = object_config_list[latest_selected_object_config_index-1][0]
        wg[2][3].text   = object_config_list[latest_selected_object_config_index-1][1]
        wg[2][4].text   = object_config_list[latest_selected_object_config_index-1][2]
        wg[2][5].text   = object_config_list[latest_selected_object_config_index-1][3]
        wg[2][6].text   = object_config_list[latest_selected_object_config_index-1][4]
    else:
        wg[2][2].text  = ""
        wg[2][3].text  = ""
        wg[2][4].text  = ""
        wg[2][5].text  = ""
        wg[2][6].text  = ""
        wg[2][3].disabled = True
        wg[2][4].disabled = True
        wg[2][5].disabled = True
        wg[2][6].disabled = True
        wg[2][7].disabled = True
        


def object_delete_config(b):
    global wg, object_config_list, latest_selected_object_config_index
    index = wg[2][0].index
    del object_config_list[index]
    latest_selected_object_config_index = 0
    wg[2][0].index = 0 
    print(f"cfg list {object_config_list}")
    object_config_write()


def create_object(b):
    global wg, object_config_list, stars_names, latest_selected_object_config_index, object_preview, blackhole, L, color_list
    name     = wg[2][2].text
    mass     = float(wg[2][3].text)
    radius   = float(wg[2][4].text)
    momentum = vec(*[float(s) for s in wg[2][5].text.split()])
    pos = vec(*[float(s) for s in wg[2][6].text.split()])
    color = color_list[wg[2][7].index]
    if name not in stars_names:
        stars_names.append(name)
    else:
        i = 1
        name1 = f"{name}_{i}"
        while name1 in stars_names:
            i += 1
            name1 = f"{name}_{i}"
        name = name1
        stars_names.append(name)
    sp = sphere(pos=pos, name=name, mass=mass, radius=radius, momentum=momentum,color=color, trail_radius=radius/4, retain=OBJECTS_TRAIL_LENGTH, make_trail=True)
    stars.extend([sp])
    stars_pos.append([sp.momentum])
    wg[2][9].text = f"Создан объект {name}"
    


def object_create_momentum():
    pass



def object_add_config(b):
    global object_config_list, wg
    wg[2][16].text = ""
    name =      wg[2][10].text
    mass =      wg[2][11].text
    radius =    wg[2][12].text
    momentum =  wg[2][13].text
    pos =       wg[2][14].text
    if name and mass and radius and momentum and pos:
        wg[2][10].text = ""
        wg[2][11].text = ""
        wg[2][12].text = ""
        wg[2][13].text = ""
        wg[2][14].text = ""
        object_config_list.append([name, mass, radius, momentum, pos])
        object_config_write()
    else:
        wg[2][16].text = "\t<span style='color:red;font-weight:600;font-size:18px'>Неккоректный ввод!</span>"



def empty_function():
    pass


# Функция для создания виджетов для управления моделью 
def build_general_widgets():
    global wg, OBJECTS_TRAIL_RADIUS
    wg.append([])
    wtext(text="<h3>  Общие настройки</h3>\n    ")
    # 0 0
    wg[0].append(button(text="Пуск", bind=toggle_running))
    wtext(text="  ")
    button(text="Рестарт", bind=start)
    wtext(text="  ")
    button(text="Сбросить положение камеры", bind=reset_camera_position)
    wtext(text="\n    Скорость:        ")
    # 0 1
    wg[0].append(slider(min=1, max=1000, value=MODEL_RATE, length=400, step=1, bind=change_rate, right=15))
    # 0 2
    wg[0].append(wtext(text='{0:d}'.format(wg[0][1].value)))
    wtext(text="\n    Длина следа: ")
    # 0 3
    wg[0].append(slider(min=0, max=1000, value=OBJECTS_TRAIL_LENGTH, length=400, step=1, bind=change_trail_length, right=15))
    # 0 4
    wg[0].append(wtext(text='{0:d}'.format(wg[0][3].value)))
    wtext(text="\n    Радиус следа: ")
    # 0 5
    wg[0].append(slider(min=0.1, max=20, value=OBJECTS_TRAIL_RADIUS, length=400, step=0.1, bind=change_trail_radius, right=15))
    # 0 6
    wg[0].append(wtext(text='{:.1f}'.format(wg[0][5].value)))
    wtext(text="\n")


# Функция для создания виджетов для настройки черной дыры
def build_blackhole_widgets():
    global wg
    arr = get_blackhole_configs()
    wg.append([])
    wtext(text="<hr style='margin-top:30px; color:black;background-color:black;height:1px;border-width:0;line-height:0px;'>")
    wtext(text="<h3>  Настройки чёрной дыры</h3>\n    ")
    wtext(text="Выберите конфигурацию черной дыры:    ")
    
    # 1 0
    wg[1].append(menu(choices=arr, index=0, bind=blackhole_choose_config, disabled=False))
    blackhole_choose_config(wg[1][0])
    wtext(text="\t\t\t\t\t\t\t\t\t\t\t\t\t")
    button(text="Обновить", bind=build_widgets)
    wtext(text="  ")
    
    # 1 1
    wg[1].append(button(text="Удалить", bind=blackhole_delete_config))
    wtext(text="<hr style='height:1px;border-width:0;color:#aaaaaa;background-color:#aaaaaa;\
        margin:0px;margin-top:24px;margin-bottom:18px;font-size:0px;line-height:0px;'>")
    wtext(text="<b style='font-weight: 800; font-size: 16px'>    Добавить конфигурацию черной дыры:</b> \n    ")
    wtext(text="Введите название конфига: ")
    
    # 1 2
    wg[1].append(winput(type="string", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    ")
    wtext(text="Масса объекта: ")
    
    # 1 3
    wg[1].append(winput(type="numeric", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    ")
    wtext(text="Радиус: ")
    
    # 1 4
    wg[1].append(winput(type="string", text="", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    ")
    
    # 1 5
    wg[1].append(button(text="Добавить", bind=blackhole_add_config))
    
    # 1 6
    wg[1].append(wtext(text=""))


# Функция для создания виджетов для генератора объекта(-ов)
def build_object_widgets():
    global wg
    cfg = get_object_configs()
    wg.append([])
    wtext(text="<hr style='margin-top:30px; color:black;background-color:black;height:1px;border-width:0;line-height:0px;'>")
    wtext(text="<h3>  Генератор объектов</h3>\n    Выберите конфигурацию объекта:    ")
    
    # 2 0
    wg[2].append(menu(choices=cfg, index=latest_selected_object_config_index, bind=object_choose_config, disabled=False))
    wtext(text="\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")                                                                                       # 1 3
    button(text="Обновить", bind=build_widgets)
    wtext(text="  ")
    
    # 2 1
    wg[2].append(button(text="Удалить", bind=object_delete_config))
    wtext(text="\n    Название конфигурации: ")
    
    # 2 2
    wg[2].append(winput(type="string", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Масса:")
    
    # 2 3
    wg[2].append(winput(type="numeric", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Радиус:")
    
    # 2 4
    wg[2].append(winput(type="numeric", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Направление(x y z):")
    
    # 2 5
    wg[2].append(winput(bind=empty_function, type="string", width=300, disabled=False))
    wtext(text="\n    Позиция(x, y, z): ")
    
    # 2 6
    wg[2].append(winput(type="string", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Цвет:")
    
    # 2 7
    wg[2].append(menu(choices=["Красный",\
         "Оранжевый",\
         "Желтый",\
         "Зеленый",\
         "Голубой",\
         "Синий",\
         "Розовый",\
         "Фиолетовый",\
         "Белый"], index=0, bind=empty_function, disabled=False))
    wtext(text="\n    ")
    
    # 2 8
    wg[2].append(button(text="Создать", bind=create_object))
    
    # 2 9
    wg[2].append(wtext(text=""))
    wtext(text="<hr style='height:1px;border-width:0;color:#aaaaaa;background-color:#aaaaaa;margin:0px;margin-top:24px;margin-bottom:18px;font-size:0px;line-height:0px;'>")
    wtext(text="<b style='font-weight: 800; font-size: 16px'>    Добавить конфигурацию объекта:</b>")
    wtext(text="\n    Название конфигурации: ")
    
    # 2 10
    wg[2].append(winput(type="string", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Масса:")
    
    # 2 11
    wg[2].append(winput(type="numeric", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Радиус:")
    
    # 2 12
    wg[2].append(winput(type="numeric", bind=empty_function, disabled=True, width=300))
    wtext(text="\n    Направление(x y z):")
    
    # 2 13
    wg[2].append(winput(bind=empty_function, type="string", width=300, disabled=False))
    wtext(text="\n    Позиция(x, y, z): ")
    
    # 2 14
    wg[2].append(winput(type="string", bind=empty_function, disabled=True, width=300))
    
    wtext(text="\n    ")
    # 2 15
    wg[2].append(button(text="Добавить", bind=object_add_config))
    
    # 2 16
    wg[2].append(wtext(text=""))

    wtext(text="""<script>
ele = document.getElementsByTagName('input');
for (e of ele){
    e.style.setProperty('font-family', 'Nunito');
}
</script>""")
    wg[2][2].disabled = True
    wg[2][3].disabled = True
    wg[2][4].disabled = True
    wg[2][5].disabled = True
    wg[2][6].disabled = True
    wg[2][7].disabled = True


def check_widgets():
    global wg
    if wg[1][0].index == 0:
        wg[1][1].disabled = True
    else:
        wg[1][1].disabled = False
    if wg[2][0].index == 0:
        wg[2][1].disabled = True
        wg[2][9].disabled = True
    else:
        wg[2][1].disabled = False
        wg[2][9].disabled = False
    

# Создание всех виджетов
def build_widgets():
    global wg, first_launch, info_text, info_object_text, info_camera
    if not first_launch:
        # for group in wg:
        #     for widget in group:    
        #         if isinstance(widget, wtext):
        #             widget.text = ""
        #         else:
        #             widget.delete()
        wtext(text="""<script>
$('div span').replaceWith(function(){
     return $("").text();
});
$('div button').replaceWith(function(){
    return $("").text();
});
$('div select').replaceWith(function(){
    return $("").text();
});
$('div input').replaceWith(function(){
    return $("").text();
});
</script>""")
    wtext(text='<hr style="height:1px;border-width:0;color:black;background-color:black;margin:0px;line-height:0px;">')
    wtext(text="""<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu+Mono:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');
*{font-family: 'Nunito', sans-serif;font-size: 16px;cursor: default;}
body{
    margin:0;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
div{line-height: 30px;}
h3{margin-bottom: 0;margin-top:30px;font-size:25px;}
input[type=text]{cursor: text;position:absolute;left:400px;margin:5px;font-family: 'Nunito';}
input[type=radio]{cursor: pointer;}
select{width:300px;position:absolute;left:400px;margin:2.5px;}
.wtext-radio{color:rgb(178, 178, 178);}
input.input-exception{left:20px;}
button:hover{cursor: pointer;}
#info-obj {
    position: absolute;
    right: 5;
    color: white;
    top: 5;
    font-size: 15px;
    line-height: 15px;
    font-family: 'Ubuntu Mono', monospace;
    text-align: right;
}
#info-text {
    position: absolute;
    left: 5;
    color: lime;
    top: 5;
    font-size: 15px;
    line-height: 15px;
    font-family: 'JetBrains Mono';
}
#info-cam {
    position: absolute;
    left: 5;
    color: white;
    top: 1065;
    font-size: 10px;
    line-height: 1;
    font-family: 'JetBrains Mono';
}
</style>""")
    wtext(text="""<script>
ele = document.getElementsByTagName('body');    
ele[0].setAttribute("oncontextmenu", "return false;");
</script>""")
    wg = []
    first_launch = False
    
    build_general_widgets()
    build_blackhole_widgets()
    build_object_widgets()
    info_text = wtext(text="<span id='info-text'> </span>")    
    info_object_text = wtext(text="<span id='info-obj'> </span>")    
    info_camera = wtext(text="<span id='info-cam'> </span>")    

def incorrect_input_blackhole_config():
    pass


build_widgets()


def convert_to_little_balls(ball):
    global stars_balls
    r = ball.radius 
    ball.opacity = 1
    # n_balls = randint(int(r/4/L), int(r/3/L))
    # r_balls = r/n_balls * uniform(0.1, 0.2)
    n_balls = ceil(5)
    r_balls = r/n_balls
    mass = ball.mass / 24**2.5
    xx, yy, zz = ball.pos.x, ball.pos.y, ball.pos.z
    ball.visible = False
    for x in np.arange(xx-(2*n_balls*r_balls-r_balls), xx+(2*n_balls*r_balls), 2.1*r_balls):
        for y in np.arange(yy-(2*n_balls*r_balls-r_balls), yy+(2*n_balls*r_balls), 2.1*r_balls):
            for z in np.arange(zz-(2*n_balls*r_balls-r_balls), zz+(2*n_balls*r_balls), 2.1*r_balls):
                if (abs(x-xx)+r_balls/1.25)**2 + (abs(y-yy)+r_balls/1.25)**2 + (abs(z-zz)+r_balls/1.25)**2 <= r**2:
                    stars_balls.append(simple_sphere(pos=vec(x,y,z), opacity=0.8, radius=r_balls, color=ball.color, mass=mass, momentum=0.0001*ball.momentum))


def spawn_object(vv):
    sphere(pos=vv, radius=L/4, color=color.green)


def create_accretion_disk():
    """----- Диск -----"""
    global DISK
    DISK = ""
    n_layers = ACCRETION_DISK_LAYERS
    r = L*2.5
    r_ball = L/100
    disk_balls = []
    disk_patterns = []
    step = 2.5 * r_ball
    
    print(f"\n-- Запуск создания диска --\n")
    
    counter = 0
    # b1 = simple_sphere(radius=L/60, pos=vec(0, 0, 0), color=color.yellow, emissive=True, visible=True)
    b1 = simple_sphere(radius=r_ball, pos=vec(0, 0, 0), color=color.yellow, emissive=True, visible=False, opacity=1)
    for i in range(n_layers):
        copy = b1.clone(pos = vec(r, 0, 0))
        copy.opacity -= 0+ (1/n_layers * i)
        copy.color = color.orange
        disk_balls.append(copy)
        r += step
        print(f"Диск: создание шариков {i+1}/{n_layers}")
        
    print("\n-- Диск: создание шариков завершено --\n")
    r -= step 
    copyy = simple_sphere(pos=vec(-r,0,0), opacity=0.000001, radius=0.000001, color=color.yellow)
    disk_balls.append(copyy)
    disk_sector = compound(disk_balls)

    disk_balls = []
    b1.visible = False
    step_angle = 1
    for i in range(360//step_angle):
        copy = disk_sector.clone(pos=disk_sector.pos)
        copy.rotate(angle=radians(i*step_angle), axis=vec(0,1,0))
        copy.opacity = uniform(0.5, 1)
        disk_balls.append(copy)
        print(f"Диск: генерация диска {i+1}/{360//step_angle}")
    print(f"\n-- Диск: генерация диска завершена --\n")
    # for i in range(360):
    #     copy = disk_patterns[i%len(disk_patterns)].clone(pos=disk_patterns[i%len(disk_patterns)].pos)
    #     copy.rotate(angle=radians(i), axis=vec(0,1,0))
    #     disk_balls.append(copy)
    #     print(f"Диск: генерация диска {i+1}/{360}")
    DISK = compound(disk_balls, name="DISK")
    DISK.pos = vec(0,0,0)
    DISK.rotate(angle=radians(90), axis=vec(0,1,0))
    disk_sector.visible = False
    disk_sector.delete()
    copy.visible = False
    copy.delete()

stars = []
stars_balls = []
stars_pos = []
hitlist = []
stars_balls_hitlist = []


# sputnik0 = simple_sphere(pos=vector(0, 120, 0), radius=1, color=color.red, trail_radius=1/2, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, name="s2", momentum=vec(700, 0, 0), make_trail=True)
# stars.extend([sputnik0])
# stars_pos.append([sputnik0.momentum])
# stars_names.append(sputnik0.name)
# sputnik0 = simple_sphere(pos=vector(0, -120, 0), radius=1, color=color.yellow, trail_radius=1/2, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, name="s2_1", momentum=vec(-800, 0, 0), make_trail=True)
# stars.extend([sputnik0])
# stars_pos.append([sputnik0.momentum])
# stars_names.append(sputnik0.name)
# sputnik0 = simple_sphere(pos=vector(100, 0, 0), radius=1, color=color.green, trail_radius=1/2, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, name="s2_2", momentum=vec(0, 900, 0), make_trail=True)
# stars.extend([sputnik0])
# stars_pos.append([sputnik0.momentum])
# stars_names.append(sputnik0.name)
# sputnik0 = simple_sphere(pos=vector(-100, 0, 0), radius=1, color=color.blue, trail_radius=1/2, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, name="s2_3", momentum=vec(0, -1000, 0), make_trail=True)
# stars.extend([sputnik0])
# stars_pos.append([sputnik0.momentum])
# stars_names.append(sputnik0.name)
# sputnik1 = sphere(pos=vector(70, 50, 0), radius=0.5, color=color.blue, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, momentum=vec(-600, 100, 0), make_trail=True)
# sputnik2 = sphere(pos=vector(50, -40, 0), radius=5, color=color.green, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, momentum=vec(-200, 0, 550), make_trail=True)
# sputnik3 = sphere(pos=vector(50, 0, 0), radius=5, color=color.red, mass=430000000, retain=OBJECTS_TRAIL_LENGTH, momentum=vec(0, 0, 0), make_trail=True)
# sputnik3 = sphere(pos=vector(-100, 0, 0), radius=5, color=color.blue, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, momentum=vec(0, 0, C/100), make_trail=True)
# sputnik4 = sphere(pos=vector(0, 0, -100), radius=5, color=color.white, mass=0.65, retain=OBJECTS_TRAIL_LENGTH, momentum=vec(-C/100, 0, 0), make_trail=True)
# sputnik1 = simple_sphere(pos=vector(0, -4, 0), radius=0.1, color=color.white,
#                       mass=10, retain=retain_, momentum=momentum_, make_trail=True)
# sputnik2 = simple_sphere(pos=vector(-1, -2, 0), radius=0.1, color=color.white,
#                      mass=10, retain=retain_, momentum=momentum_, make_trail=True)
# sputnik3 = simple_sphere(pos=vector(0, 1, 0), radius=0.1, color=color.white,
#                      mass=10, retain=retain_, momentum=momentum_, make_trail=True)
# stars.extend([sputnik1, sputnik2, sputnik3, sputnik4])
# sputnik1 = simple_sphere(pos=vec(0, -4, 0), radius=0.1*L, color=color.white,
#                       mass=10, retain=retain_, momentum=momentum_, make_trail=True)
# sputnik2 = simple_sphere(pos=vec(-1, -2, 0), radius=0.1*L, color=color.white,
#                      mass=10, retain=retain_, momentum=momentum_, make_trail=True)
# sputnik3 = simple_sphere(pos=vec(0, 1, 0), radius=0.1*L, color=color.white,
#                      mass=10, retain=retain_, momentum=momentum_, make_trail=True)

# black_list = []

def gravitationalForce(p1, p2):
    G = 39.41
    rVector = p1.pos - p2.pos
    rMagnitude = mag(rVector)
    rHat = rVector / rMagnitude
    F = (- rHat * G * p1.mass * p2.mass )/ rMagnitude ** 2
    return F

dt = 0.001

# create_accretion_disk()
print("-- Запуск главного цикла --")
scene.visible = True
scene.background = color.black
def keyInput(evt):
    global wg, info_text, nowhit
    s = evt.key
    if s == "\n"    :
        toggle_running(wg[0][0])
    if s == "\\":
        info_text.text = f"<span id='info-text'></span>"  
    if s == "[":
        if wg[0][1].value >= 11:
            wg[0][1].value -= 10
            change_rate(wg[0][1])
    if s == "]":
        if wg[0][1].value <= 990:
            wg[0][1].value += 10
            change_rate(wg[0][1])
    if s == ";":
        if wg[0][1].value >= 2:
            wg[0][1].value -= 1
            change_rate(wg[0][1])
    if s == "'":
        if wg[0][1].value <= 999:
            wg[0][1].value += 1
            change_rate(wg[0][1])
    if s == "}" or s == "{":
        wg[0][1].value = 100
        change_rate(wg[0][1])
        info_text.text = f"<span id='info-text'>> Сброс скорости модели({wg[0][1].value}) </span>"  
    if s == "T":
        print("toggle trail")
        toggle_trail()
    if s == "o":
        if wg[0][3].value >= 11:
            wg[0][3].value -= 10
            change_trail_length(wg[0][3])
    if s == "p":
        if wg[0][3].value <= 990:
            wg[0][3].value += 10
            change_trail_length(wg[0][3])
    if s == "k":
        if wg[0][3].value >= 2:
            wg[0][3].value -= 1
            change_trail_length(wg[0][3])
    if s == "l":
        if wg[0][3].value <= 999:
            wg[0][3].value += 1
            change_trail_length(wg[0][3])
    if s == "O" or s == "P":
        wg[0][3].value = 50
        change_trail_length(wg[0][3])
        info_text.text = f"<span id='info-text'>> Сброс длины следа объектов({wg[0][3].value}) </span>"  
    if s == "backspace":
        reset_camera_position()
    if s == "x":
        toggle_xyz()
    if s == "?":
        start()
        info_text.text = f"<span id='info-text'>> Сброс настроек </span>"  
    if s == "u":
        if wg[0][5].value >= 2:
            wg[0][5].value -= 1
            change_trail_radius(wg[0][5])
    if s == "i":
        if wg[0][5].value <= 19:
            wg[0][5].value += 1
            change_trail_radius(wg[0][5])
    if s == "h":
        if wg[0][5].value >= 0.2:
            wg[0][5].value -= 0.1
            change_trail_radius(wg[0][5])
    if s == "j":
        if wg[0][5].value <= 19.9:
            wg[0][5].value += 0.1
            change_trail_radius(wg[0][5])
    if s == "U" or s == "I":
        wg[0][5].value = 3.0
        change_trail_radius(wg[0][5])
        info_text.text = f"<span id='info-text'>> Сброс радиуса следа объектов</span>"  


scene.bind('keydown', keyInput)
pos_old = scene.camera.pos
while 1:
    check_widgets()
    rate(wg[0][1].value)
    index = ""
    cpos = scene.camera.pos
    ri.axis = cpos
    info_camera.text = f"<span id='info-cam'>{round(cpos.x, 5), round(cpos.y, 5), round(cpos.z, 5)}</span>"
    if nowhit == None:
        info_object_text.text = f"<span id='info-obj'></span>"  
    else:
        lpos = nowhit.pos
        index = stars.index(nowhit)
        d = stars_pos[index][-1]
        x = d.x
        y = d.y
        z = d.z
        s = round(sqrt(x*x+y*y+z*z), 5)
        col = nowhit.color
        colx = col.x
        coly = col.y
        colz = col.z
        if nowhit != None:
            info_object_text.text = f"""<span id='info-obj'>Конфигурация: <b style="color:rgb({colx*100}%, {coly*100}%, {colz*100}%)">{nowhit.name}</b>"""
            info_object_text.text += "\nПозиция: {:.5f}x {:.5f}y {:.5f}z".format(round(lpos.x, 5), round(lpos.y, 5), round(lpos.z, 5))
            info_object_text.text += "\nСкорость: {:.5f} а.е./год".format(s)
            info_object_text.text += "\nРасстояние до черной дыры: {:.5f} а.е.".format(round(mag(lpos), 5))
            info_object_text.text += "\nМасса: {:.5f} Msun".format(nowhit.mass)
            info_object_text.text += "\nРадиус: {:.5f} а.е.".format(nowhit.radius)
            info_object_text.text += "</span>"
    
    if running:
        # DISK.rotate(angle=radians(wg[0][1].value/100), axis=vec(0,1,0))
        for (i, s1) in enumerate(stars):
            if i in hitlist: continue
            force = gravitationalForce(s1, blackhole)
            for (j, s2) in enumerate(stars):
                if j in hitlist or i == j: continue
                # print(f"calc {i}, {j}")
                distance = mag(s1.pos - s2.pos)
                collided = (distance < (s1.radius+s2.radius))
                if collided:
                    info_text.text = f"<span id='info-text'>> Столкновение {s1.name} и {s2.name}</span>"
                    s1.visible = False
                    s2.visible = False
                    s1.force = 0
                    s2.force = 0
                    s1.mass = 0
                    s2.mass = 0
                    s1.radius = 0
                    s2.radius = 0
                    s1.pos = vec(0, 0, 0)
                    s2.pos = vec(0, 0, 0)
                    s1.clear_trail()
                    s2.clear_trail()
                    hitlist.append(i)
                    hitlist.append(j)
                    break
                force += gravitationalForce(s1, s2)
            if i not in hitlist:
                s1.force = force
                s1.momentum = s1.momentum + s1.force * dt
                s1.pos = s1.pos + s1.momentum / s1.mass * dt
                stars_pos[i].append(s1.momentum / s1.mass)
                x = s1.pos.x
                y = s1.pos.y
                z = s1.pos.z
                length = sqrt(x**2 + y**2 + z**2) - s1.radius
                if sqrt(x**2 + y**2 + z**2) - s1.radius < 1*L:
                    convert_to_little_balls(s1)
                    s1.visible = False
                    s1.force = 0
                    s1.mass = 0
                    s1.radius = 0
                    s1.pos = vec(0, 0, 0)
                    s1.clear_trail()
                    hitlist.append(i)
        for (i, ball) in enumerate(stars_balls):
            if i not in hitlist:
                force = gravitationalForce(ball, blackhole)
                ball.force = force
                ball.momentum = ball.momentum + ball.force * dt
                ball.pos = ball.pos + ball.momentum / ball.mass * dt       
                x = ball.pos.x
                y = ball.pos.y
                z = ball.pos.z
                length = sqrt(x**2 + y**2 + z**2) - ball.radius
                if length <= 1.5*L or 1.5*L > mag(ball.pos - blackhole.pos):
                    ball.visible = False
                    ball.force = 0
                    ball.mass = 0
                    ball.radius = 0
                    ball.pos = vec(0, 0, 0)
                    ball.clear_trail()
                    stars_balls_hitlist.append(i)
        hitlist.sort()
        hitlist = hitlist[::-1]
        stars_balls_hitlist.sort()
        stars_balls_hitlist = stars_balls_hitlist[::-1]
        if index in hitlist:
            nowhit = None
        for i in hitlist:
            del stars[i]
            del stars_names[i]
            del stars_pos[i]
        for i in stars_balls_hitlist:
            del stars_balls[i]
        hitlist = []
        stars_balls_hitlist = []