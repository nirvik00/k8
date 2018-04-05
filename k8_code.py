import rhinoscriptsyntax as rs
import math
import os
import random
import operator
from operator import itemgetter


def block_ver(x, y, l, w, LR, UD):
    # give loc x, y, L, -w/2 to w/2, {'left','right','mid'}, h={0,1,2}
    le=l
    if(LR=='left' and UD=='up'):
        p0=[x,y,0]
        p1=[x-le,y,0]
        p2=[x-le,y+w,0]
        p3=[x,y+w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='mid' and UD=='up'):
        p0=[x-le/2,y,0]
        p1=[x+le/2,y,0]
        p2=[x+le/2,y+w,0]
        p3=[x-le/2,y+w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='right' and UD=='up'):
        p0=[x,y,0]
        p1=[x+le,y,0]
        p2=[x+le,y+w,0]
        p3=[x,y+w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='left' and UD=='down'):
        p0=[x,y,0]
        p1=[x-le,y,0]
        p2=[x-le,y-w,0]
        p3=[x,y-w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='right' and UD=='down'):
        p0=[x,y,0]
        p1=[x+le,y,0]
        p2=[x+le,y-w,0]
        p3=[x,y-w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='mid' and UD=='down'):
        p0=[x-le/2,y,0]
        p1=[x+le/2,y,0]
        p2=[x+le/2,y-w,0]
        p3=[x-le/2,y-w,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly

def add_srf(poly,hi):
    L=rs.AddLine([0,0,0],[0,0,hi])
    srf=rs.AddPlanarSrf(poly)
    f_srf=rs.ExtrudeSurface(srf,L)
    rs.DeleteObjects([poly,L,srf])
    return f_srf

def add_top(x,y):
    ch_lmr=random.choice(['left','mid','right'])
    poly0=block_ver(x,y,81,125,ch_lmr,'up')
    srf0=add_srf(poly0,28)
    ch_lr=random.choice(['left','right'])
    poly1=None
    if(ch_lr=='right'):
        poly1=block_ver(x+11,y,86,73.6,ch_lr,'down')
    else:
        poly1=block_ver(x,y,86,73.6,ch_lr,'down')
    srf1=add_srf(poly1,14)
    return [srf0,srf1]

def add_spine(x,y):
    poly=block_ver(x,y,-11,-500,'left','up')
    srf=add_srf(poly,1)
    return srf

def block_hor(x, y, l, w, LR):
    if(LR=='left'):
        le=l
        x+=10#corridor width
        y-=w/2
        p0=[x,y-w/2,0]
        p1=[x+le,y-w/2,0]
        p2=[x+le,y+w/2,0]
        p3=[x,y+w/2,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly
    elif(LR=='right'):
        le=l
        #x+=10#corridor width
        y-=w/2
        p0=[x,y-w/2,0]
        p1=[x-le,y-w/2,0]
        p2=[x-le,y+w/2,0]
        p3=[x,y+w/2,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly

def add_fingers(x,y):
    req_srf=[]
    #one-sided
    ch_num=random.choice([2,3,4])
    ch_sided=random.choice(['one','two'])
    if(ch_sided=='one'):
        ch_lr=random.choice(['left','right'])
        ch_num=random.choice([2,3,4])
        for i in range(ch_num):
            if(ch_num==2):
                poly=block_hor(x,y-(65+10)*i,200,65,ch_lr)
                srf=add_srf(poly,42)
                req_srf.append(srf)
            elif(ch_num==3):
                poly=block_hor(x,y-(65+10)*i,200,65,ch_lr)
                srf=add_srf(poly,28)
                req_srf.append(srf)
            else:
                poly_g=block_hor(x,y-(65+10)*i,200,65,ch_lr)
                add_srf(poly_g,14)
                poly_f=block_hor(x,y-(65+10)*i,100,65,ch_lr)
                rs.MoveObject(poly_f,[0,0,14])
                srf=add_srf(poly_f,14)
                req_srf.append(srf)
    else:
        ch_num=random.choice([2,3,4])
        if(ch_num==2):
            poly_le=block_hor(x,y-(65+10)*0,200,65,'left')
            add_srf(poly_le,42)
            poly_ri=block_hor(x,y-(65+10)*0,200,65,'right')
            srf=add_srf(poly_ri,42)
            req_srf.append(srf)
        elif(ch_num==3):
            ch_an=random.choice(['top','down'])
            if(ch_an=='top'):
                #L=1 R=2
                poly_le_0=block_hor(x,y-(65+10)*0,200,65,'left')
                srf_0=add_srf(poly_le_0,28)
                poly_le_1=block_hor(x,y-(65+10)*1,200,65,'left')
                srf_1=add_srf(poly_le_1,28)
                poly_ri=block_hor(x,y-(65+10)*0,200,65,'right')
                srf_2=add_srf(poly_ri,28)    
                req_srf.append(srf_0)
                req_srf.append(srf_1)
                req_srf.append(srf_2)                
            else:
                #L=2 R=1
                poly_le=block_hor(x,y-(65+10)*0,200,65,'left')
                srf_3=add_srf(poly_le,28)
                poly_ri_0=block_hor(x,y-(65+10)*0,200,65,'right')
                srf_4=add_srf(poly_ri_0,28)
                poly_ri_1=block_hor(x,y-(65+10)*1,200,65,'right')
                srf_5=add_srf(poly_ri_1,28)            
                req_srf.append(srf_3)
                req_srf.append(srf_4)
                req_srf.append(srf_5)
        else:
            ch_num_left=random.choice([1,2,3,4])
            if(ch_num_left==1):
                poly_g_le=block_hor(x,y-(65+10)*0,200,65,'left')
                srf_0=add_srf(poly_g_le,14)
                poly_f_le=block_hor(x,y-(65+10)*0,100,65,'left')
                rs.MoveObject(poly_f_le,[0,0,14])
                srf_1=add_srf(poly_f_le,14)              
                req_srf.append(srf_0)
                req_srf.append(srf_1)
                for i in range(3):
                    poly_g_ri=block_hor(x,y-(65+10)*i,200,65,'right')
                    srf_loop_0=add_srf(poly_g_ri,14)
                    poly_f_ri=block_hor(x,y-(65+10)*i,100,65,'right')
                    rs.MoveObject(poly_f_ri,[0,0,14])
                    srf_loop_1=add_srf(poly_f_ri,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)
            elif(ch_num_left==2):
                for i in range(2):
                    poly_g_le=block_hor(x,y-(65+10)*i,200,65,'left')
                    srf_loop_0=add_srf(poly_g_le,14)
                    poly_f_le=block_hor(x,y-(65+10)*i,100,65,'left')
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    poly_g_ri=block_hor(x,y-(65+10)*i,200,65,'right')
                    srf_loop_2=add_srf(poly_g_ri,14)
                    poly_f_ri=block_hor(x,y-(65+10)*i,100,65,'right')
                    rs.MoveObject(poly_f_ri,[0,0,14])
                    srf_loop_3=add_srf(poly_f_ri,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)
                    req_srf.append(srf_loop_2)
                    req_srf.append(srf_loop_3)
            elif(ch_num_left==3):
                poly_g_ri=block_hor(x,y-(65+10)*0,200,65,'right')
                srf_0=add_srf(poly_g_ri,14)
                poly_f_ri=block_hor(x,y-(65+10)*0,100,65,'right')
                rs.MoveObject(poly_f_ri,[0,0,14])
                srf_l=add_srf(poly_f_ri,14)   
                req_srf.append(srf_0)
                req_srf.append(srf_l)
                for i in range(3):
                    poly_g_le=block_hor(x,y-(65+10)*i,200,65,'left')
                    srf_loop_0=add_srf(poly_g_le,14)
                    poly_f_le=block_hor(x,y-(65+10)*i,100,65,'left')
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)                    
            else:
                ch_lr_=random.choice(['left','right'])
                for i in range(2):
                    poly_g_le=block_hor(x,y-(65+10)*i,200,65,ch_lr_)
                    srf_loop_0=add_srf(poly_g_le,14)
                    poly_f_le=block_hor(x,y-(65+10)*i,100,65,ch_lr_)
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)
    return req_srf

def plot(n,m):
    srf_li=[]
    counter=-1
    a=700
    b=800
    for i in range(n):
        for j in range(m):
            counter+=1
            X=i*a
            Y=j*b
            srf_top=add_top(X,Y)#up from 0,0
            #rs.AddTextDot(counter,[X,Y,0])
            srf_top_gym=srf_top[0]
            srf_top_band=srf_top[1]
            srf_li.append(srf_top_gym)
            srf_li.append(srf_top_band)
            
            #going down from y=0 => subtract 73.6 : bottom of top
            Y-=73.6
            #corridor after top
            Y-=10
            rs.AddLine([X,Y,0],[X+100,Y,0])
            srf_spine=add_spine(X,Y+73.6+10)
            srf_li.append(srf_spine)
            
            #finger 1
            srf_fingers=add_fingers(X,Y)
            if(len(srf_fingers)==0):
                #print(counter, len(srf_fingers))
                print(srf_fingers)
                
            for k in srf_fingers:
                srf_li.append(k)
            
            # reached bottom
            Y-=100
            rs.AddLine([X,Y,0],[X+100,Y,0])
            #spine
            rs.AddLine([i*a,j*b,0],[i*a,j*b-600,0])
            
            rs.ObjectColor(srf_top_gym, (255,33,3))
            rs.ObjectColor(srf_top_band, (150,33,3))
            
    return srf_li




rs.EnableRedraw(False)
output=plot(10,10)
rs.EnableRedraw(True)