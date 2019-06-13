#Created by Laren Spear in Summer 2018
#To test this script, type "calculations.py N_Ni2_Ag1_H_1" (as an example) with any database item
#To update the database or create the database from scratch, use jsonupdater.py, which runs this script

#import modules
import sys
import os.path
import os
import numpy
from numpy import *
import scipy.stats
import glob
import re
import json
import commands
import ase.io
import ase.data
import ase

#Global variables
code_path = "./codes.txt"
db_path = "/home/fri/public_html/fridb/database"
total_info = dict({"M1":None, "M2":None, "Run":None, "S/N":None, "SiteA":None,"SiteB":None, "result_type":None, "result":None, "metadata":None, "url":{"s1":None, "s2":None}, "distance":None, "deform":None})
global entry_type
entry_type = 'entry' #can be bare bimetallic, appended bimetallic, bare pure, appended pure, other
s= 0

#Reads in user who submitted the calculations
def getUser(path):
    userName = "unknown"
    if os.path.isfile(path+"/metadata.txt"):
        lines = open (path+"/metadata.txt", 'r').readlines()
        userName = lines[0].strip()
        return userName
    else:
        return userName

#Breaks up database path into properties based on name of database entry
def parseCode(value):
    global entry_type
    spl = value.split('_')
    fspl = re.split('(\d+)',spl[1])
    sspl = re.split('(\d+)',spl[2])
    if len(sys.argv) == 2:
        if len(fspl) > 1:
            entry_type = 'appended bimetallic'
            return dict({'M1':fspl[0], 'M2':sspl[0], 'S/N':spl[0], 'Run':spl[4], 'SiteA': fspl[1], 'SiteB':sspl[1], 'Append':spl[3]})
        elif len(spl) == 4:
            entry_type = '1'
            if spl[-1] == 'B':
                entry_type = 'bare pure'
            else:
                entry_type = 'appended pure'
            return dict({'M1':fspl[0], 'M2':sspl[0], 'S/N':spl[0], 'Run':None, 'SiteA': None,'SiteB':None, 'Append':spl[3]})
        else:
            entry_type = 'bare bimetallic'
            return dict({'M1':fspl[0], 'M2':sspl[0], 'S/N':spl[0], 'Run':spl[4], 'SiteA': None,'SiteB':None, 'Append':spl[3]})
    else:
        entry_type = 'other'
        return dict({'M1':spl[1], 'M2':spl[2], 'S/N':spl[0], 'Append':spl[3]})

#Gets energy from the outcar file (used for binding energy)
def get_outcar_energy(filename):
    status, result = commands.getstatusoutput("grep 'energy(sigma->0)' %s" % filename)
    #status, result = commands.getstatusoutput("grep 'energy  without entropy' %s" % filename)
    if status != 0:
        return 0
    try:
        energy = float(result.split("\n")[-1].split()[-1])
    except NameError:
        energy = 0
    return energy

#Take 3D distance appended atom moves and converts it to 2D distance
#Computes average over 5 structures, returns average of that array and standard error
def get_2D_distance(x):
    distances_array = []
    for i in range(1,6):
        if len(sys.argv[1]) == 13:
            nano_path = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],i)
        elif len(sys.argv[1]) == 11:
            nano_path = "%s_%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],x['Append'], i)
        else:
            nano_path = "%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],x['Append'])
        subs = glob.glob(db_path + '/' + nano_path+'/*')
        subs.sort(key = lambda s: os.path.getmtime(s))
        newest_sub = subs[-1]
        p = ase.io.read(newest_sub + '/' + 'CONTCAR')
        pos = p.get_positions()
        dist_dict = {}
        if x['S/N'] == 'N':
            for i in range(0,79):
                dist_dict[i] = numpy.linalg.norm(pos[79] - pos[i])
            dist_dict2 = {y:x for x,y in dist_dict.iteritems()}
            dist_list = dist_dict2.keys()
            dist_list.sort()
            final_appended = pos[79]
            A = pos[dist_dict2[dist_list[0]]]
            B = pos[dist_dict2[dist_list[1]]]
            C = pos[dist_dict2[dist_list[2]]]
            hollow_site_center = numpy.add(numpy.add(A,B),C) / 3
            displacement_3D = final_appended - hollow_site_center
        elif x['S/N'] == 'S':
            for i in range(0,36):
                dist_dict[i] = numpy.linalg.norm(pos[36] - pos[i])
            dist_dict2 = {y:x for x,y in dist_dict.iteritems()}
            dist_list = dist_dict2.keys()
            dist_list.sort()
            final_appended = pos[36]
            A = pos[dist_dict2[dist_list[0]]] #3 closest atoms
            B = pos[dist_dict2[dist_list[1]]]
            C = pos[dist_dict2[dist_list[2]]]
            hollow_site_center = (A+B+C)/3
            hollow_site_ase = ase.Atom(1, hollow_site_center)
            p.append(hollow_site_ase)
            displacement_3D = p.get_distance(36, 37, mic=True,vector=True)
        normal_vector = numpy.cross(B-A, C-A) / numpy.linalg.norm(numpy.cross(B-A, C-A))
        distance_2D = numpy.linalg.norm(displacement_3D - numpy.dot(displacement_3D,normal_vector)*normal_vector)
        distances_array.append(distance_2D)
    avg_dist = numpy.mean(distances_array)
    std_dist = scipy.stats.sem(distances_array)
    return avg_dist, std_dist

#Computes RMS atom motion and max atom motion between optimized bare and optimized appended structures
#Thresholds at 0.25 for RMS and 1.2 for max, based on database analysis. These are loosely defined.
#If 3 or more structures of the 5 are too deformed by either metric, returns null for both metrics
#Otherwise, returns average RMS and max atom motion
def compare_geometries(x):
    deformation_array_RMS = []
    deformation_array_max = []
    for i in range(1,6):
        if entry_type == 'appended bimetallic':
            appended_path = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],i)#Makes Appended Directory Path
            bare_path = "%s_%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],'B', i) #Makes Bare Path
        elif entry_type == 'appended pure':
            appended_path = "%s_%s_%s_%s" %(x['S/N'], x['M1'], x['M2'], x['Append'])
            bare_path = "%s_%s_%s_%s" %(x['S/N'], x['M1'], x['M2'], 'B')
        else:
            return
        subs = glob.glob(db_path + '/' + appended_path+'/*')
        subs.sort(key = lambda s: os.path.getmtime(s))
        newest_sub = subs[-1]
        g = ase.io.read(newest_sub + '/' + 'CONTCAR')
        geometry_appended = g.get_positions()
        if x['S/N'] == 'N':
            geometry_appended = geometry_appended[0:78]
        elif x['S/N'] == 'S':
            geometry_appended = geometry_appended[0:35]
        subs2 = glob.glob(db_path + '/' + bare_path + '/*')
        subs2.sort(key = lambda s: os.path.getmtime(s))
        newest_sub2 = subs2[-1]
        g2 = ase.io.read(newest_sub2 + '/' + 'CONTCAR')
        geometry_bare = g2.get_positions()
        if x['S/N'] == 'N':
            geometry_bare = geometry_bare[0:78]
        elif x['S/N'] == 'S':
            geometry_bare = geometry_bare[0:35]
        abs_geometry_difference = abs(geometry_appended - geometry_bare)
        mean_abs_geometry_difference = abs_geometry_difference.mean()
        RMS_geometry_difference = numpy.sqrt(((geometry_appended - geometry_bare) ** 2).mean())
        max_geometry_difference = numpy.amax(abs_geometry_difference)
        if RMS_geometry_difference > 0.25:
            pass
        else:
            deformation_array_RMS.append(RMS_geometry_difference)
        if max_geometry_difference > 1.2:
            pass
        else:
            deformation_array_max.append(max_geometry_difference)
    if len(deformation_array_RMS) < 3 or len(deformation_array_max) < 3:
        return None, None
    else:
        return numpy.mean(deformation_array_RMS), numpy.mean(deformation_array_max)

#Calculates average binding energy for the 5 structures
#Returns average binding energy and standard error    
def get_binding_energy(x):
    BEarray = []
    if entry_type == 'appended bimetallic':
        appended_path = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],x['Run'])#Makes Appended Directory Path
        bare_path = "%s_%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],'B', x['Run']) #Makes Bare Path
        for i in range(1,6):
            appended_path_new = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],i)
            bare_path_new = "%s_%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],'B', i)
            subs = glob.glob(db_path + '/' + appended_path_new +'/*')
            subs.sort(key = lambda s: os.path.getmtime(s))
            newest_sub = subs[-1]
            subs2 = glob.glob(db_path + '/' + bare_path_new +'/*')
            subs2.sort(key = lambda s: os.path.getmtime(s))
            newest_sub2 = subs2[-1]
            if x['Append'] == 'O':
                subs3 = glob.glob(db_path + '/' + 'O_sng' + '/*')
            elif x['Append'] == 'H':
                subs3 = glob.glob(db_path + '/' + 'H_sng' + '/*')
            subs3.sort(key = lambda s: os.path.getmtime(s))
            newest_sub3 = subs3[-1]
            binding_energy = get_outcar_energy(newest_sub + '/OUTCAR') - get_outcar_energy(newest_sub2 + '/OUTCAR') - 0.5*(get_outcar_energy(newest_sub3 + '/OUTCAR'))
            BEarray.append(binding_energy)
        avg_BE = numpy.mean(BEarray)
        std_bind = scipy.stats.sem(BEarray)
    elif entry_type == 'appended pure':
        appended_path = "%s_%s_%s_%s" %(x['S/N'], x['M1'], x['M2'], x['Append'])
        bare_path = "%s_%s_%s_%s" %(x['S/N'], x['M1'], x['M2'], 'B')
        subs = glob.glob(db_path + '/' + appended_path +'/*')
        subs.sort(key = lambda s: os.path.getmtime(s))
        newest_sub = subs[-1]
        subs2 = glob.glob(db_path + '/' + bare_path +'/*')
        subs2.sort(key = lambda s: os.path.getmtime(s))
        newest_sub2 = subs2[-1]
        if x['Append'] == 'O':
            subs3 = glob.glob(db_path + '/' + 'O_sng' + '/*')
        elif x['Append'] == 'H':
            subs3 = glob.glob(db_path + '/' + 'H_sng' + '/*')
        subs3.sort(key = lambda s: os.path.getmtime(s))
        newest_sub3 = subs3[-1]
        binding_energy = get_outcar_energy(newest_sub + '/OUTCAR') - get_outcar_energy(newest_sub2 + '/OUTCAR') - 0.5*(get_outcar_energy(newest_sub3 + '/OUTCAR'))
        avg_BE = binding_energy
        std_bind = 0
    return avg_BE, std_bind

#Determines binding site based on number of neighbors
#3 neighbors is hollow site, 2 is bridge site, 1 is top site
#Works on all 5 structures and puts neighbors into array
#The mode of the array is considered the primary binding site and is returned
#Threshold 0.55 based on testing in a spreadsheet and visual inspection, can be changed
def get_binding_site(x):
    neighbors_array = []
    for i in range(1,6):
        if len(sys.argv[1]) == 13:
            nano_path = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],i)
        elif len(sys.argv[1]) == 11:
            nano_path = "%s_%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],x['Append'], i)
        else:
            nano_path = "%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],x['Append'])
        subs = glob.glob(db_path + '/' + nano_path+'/*')
        subs.sort(key = lambda s: os.path.getmtime(s))
        newest_sub = subs[-1]
        p = ase.io.read(newest_sub + '/' + 'CONTCAR')
        pos = p.get_positions()
        atomicnumbers = p.get_atomic_numbers()
        key_atoms_val_dist = {}
        key_atoms_val_atomicnumber = {}
        if x['S/N'] == 'N':
            for i in range(0,79):
                key_atoms_val_dist[i] = numpy.linalg.norm(pos[79] - pos[i])
                key_atoms_val_atomicnumber[i] = atomicnumbers[i]
        else:
            for i in range(0,36):
                key_atoms_val_dist[i] = numpy.linalg.norm(pos[36] - pos[i])
                key_atoms_val_atomicnumber[i] = atomicnumbers[i]
        key_dist_val_atoms = {y:x for x,y in key_atoms_val_dist.iteritems()}
        dist_list = key_dist_val_atoms.keys()
        dist_list.sort()
        key_closest_val_atom = {'A':key_dist_val_atoms[dist_list[0]], 'B':key_dist_val_atoms[dist_list[1]], 'C':key_dist_val_atoms[dist_list[2]]}
        neighbors = 3
        threshold = 0.55
        for i in key_closest_val_atom:
            j = key_closest_val_atom[i]
            if key_atoms_val_dist[j] > ase.data.covalent_radii[key_atoms_val_atomicnumber[j]] + ase.data.covalent_radii[ase.data.atomic_numbers[x['Append']]] + threshold:
                neighbors -= 1
        neighbors_array.append(neighbors)
    m = scipy.stats.mode(neighbors_array)
    return int(m[0])

#Takes argument and makes dictionary, then writes out JSON item
def main():
    x = parseCode(sys.argv[1])
    if x['SiteA'] == 'None' or x['Append'] == 'B':
        return
    if len(sys.argv[1]) == 13:
        nano_path = "%s_%s%s_%s%s_%s_%s" %(x['S/N'],x['M1'],x['SiteA'],x['M2'],x['SiteB'],x['Append'],x['Run'])
    elif len(sys.argv[1]) == 9:
        nano_path = "%s_%s_%s_%s" %(x['S/N'],x['M1'],x['M2'],x['Append'])
    else:
        return
    subs = glob.glob(db_path + '/' + nano_path +'/*')
    subs.sort(key = lambda s: os.path.getmtime(s))
    final_path = subs[-1]
    total_info = x
    if x['S/N'] == 'N':
        total_info['deform_RMS'], total_info['deform_max'] = compare_geometries(x)
    if x['M1'] == x['M2']:
        total_info['result'] = get_binding_energy(x)[0]
        total_info['metadata'] = "Binding Energy: %s<br>Calculated by %s<br>" %(x["result"],getUser(final_path))
    else:
        total_info['result'], total_info['std'] = get_binding_energy(x)
        total_info['metadata'] = "Average Binding Energy: %s<br>Standard Deviation: %s<br>Calculated by %s<br>" %(x["result"],x["std"],getUser(final_path))
    total_info['Neighbors'] = get_binding_site(x)
    total_info['result_type'] = x['Append'] + " Binding Energy"
    total_info['distance'], total_info['std distance'] = get_2D_distance(x)
    return json.dumps(total_info)

print main()
