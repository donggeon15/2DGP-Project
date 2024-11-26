objects = [[] for _ in range(4)]
collision_pairs = { }

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

def remove_collisions_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collisions_object(o)
            del o # 메모리에서 객체 자체를 삭제
            return
    print(f'CRETICAL: 존재하지않는 객체{o}를 지우려고 합니다.')

def clear():
    global objects
    global collision_pairs
    objects = [[] for _ in range(4)]
    collision_pairs = { }

def collide(a, b):
    al, ab, ar, at = a.get_bb()
    bl, bb, br, bt = b.get_bb()

    if al > br: return False
    if ar < bl: return False
    if at < bb: return False
    if ab > bt: return False

    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collisions():
    # game_world 에 등록된 충돌 정보를 바탕으로 실제 정보를  수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    print(f'{group} collision')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)