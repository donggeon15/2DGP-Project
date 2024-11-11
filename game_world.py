objects = [[] for _ in range(4)]

def add_object(o, depth):
    objects[depth].append(o)

def update():
    for layer in objects:
        for o in layer:
            o.update()

def render():
    for layer in objects:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    print(f'CRETICAL: 존재하지않는 객체{o}를 지우려고 합니다.')

def clear():
    global objects

    objects = [[] for _ in range(4)]