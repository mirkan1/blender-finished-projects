TEXT_FILE = "C://Users//Raq//Desktop//My projects//marco animation//DNA//"
TOTAL_FILES = 18037

def write():
    p = open("Marco_R1_001.txt", "r")
    p = p.readlines()[5:]
    for i in range(0, len(p[5:])):
        if i%4 == 0:
            with open(TEXT_FILE + "DNA" + str(i) + ".txt", 'w') as r:
                r.write(p[i])

def read():
    arr = []
    for i in range(round(TOTAL_FILES / 4)):
        with open(TEXT_FILE + "DNA" + str(i*4) + ".txt", 'r') as r:
            line = r.readlines()[0].split('\n')[0]
            arr.append(line)
    return arr

def main():
    from math import floor
    arr = []
    file_read_arr = read()

    for j in file_read_arr[:1]:
        out = [j[i:i+floor(len(j) / 6)] for i in range(0, len(j), floor(len(j) / 6))]
        plane = out[0]
        sphere = out[1]
        sphere001 = out[2]
        sun = out[3]
        cube = out[4]
        cube001 = out[5]

    plane_count = 0
    sphere_count = 0
    sphere001_count = 0
    sun_count = 0
    cube_count = 0
    cube001_count = 0

    for j in file_read_arr:
        out = [j[i:i+floor(len(j) / 6)] for i in range(0, len(j), floor(len(j) / 6))]
        for i in out:
            try:
                if i == plane:
                    arr.append("Plane")
                    plane_count+=1
                elif i == sphere:
                    arr.append("Sphere")
                    sphere_count+=1
                elif i == sphere001:
                    arr.append("Sphere.001")
                    sphere001_count+=1
                elif i == sun:
                    #change background
                    arr.append("Sun")
                    sun_count+=1
                elif i == cube:
                    arr.append("Cube")
                    cube_count+=1
                elif i == cube001:
                    arr.append("Cube.001")
                    cube001_count+=1
            except:
                pass

    #import pdb;pdb.set_trace()
    print(f"cube001 >>> {cube001_count}\ncube >>> {cube_count}\nsun >>> {sun_count}\nsphere001 >>> {sphere001_count}\nsphere >>> {sphere_count}\nplane >>> {plane_count}")
    return arr

main()