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

def add_fingers(x,y, l, w):
    try:
        print(len(req_srf))
        rs.DeleteObjects(req_srf)
    except:
        pass
    req_srf=[]
    #one-sided
    ch_num=random.choice([2,3,4])
    ch_sided=random.choice(['one','two'])
    if(ch_sided=='one'):
        ch_lr=random.choice(['left','right'])
        ch_num=random.choice([2,3,4])
        for i in range(ch_num):
            if(ch_num==2):
                poly=block_hor(x,y-(w+10)*i,l,w,ch_lr)
                srf=add_srf(poly,42)
                req_srf.append(srf)
            elif(ch_num==3):
                poly=block_hor(x,y-(w+10)*i,l,w,ch_lr)
                srf=add_srf(poly,28)
                req_srf.append(srf)
            else:
                poly_g=block_hor(x,y-(w+10)*i,l,w,ch_lr)
                srf_g=add_srf(poly_g,14)
                req_srf.append(srf_g)
                poly_f=block_hor(x,y-(w+10)*i,l/2,w,ch_lr)
                rs.MoveObject(poly_f,[0,0,14])
                srf_f=add_srf(poly_f,14)
                req_srf.append(srf_f)
    else:
        ch_num=random.choice([2,3,4])
        if(ch_num==2):
            poly_le=block_hor(x,y-(w+10)*0,l,w,'left')
            srf_le=add_srf(poly_le,42)
            req_srf.append(srf_le)
            poly_ri=block_hor(x,y-(w+10)*0,l,w,'right')
            srf_ri=add_srf(poly_ri,42)
            req_srf.append(srf_ri)
        elif(ch_num==3):
            ch_an=random.choice(['top','down'])
            if(ch_an=='top'):
                #L=1 R=2
                poly_le_0=block_hor(x,y-(w+10)*0,l,w,'left')
                srf_0=add_srf(poly_le_0,28)
                poly_le_1=block_hor(x,y-(w+10)*1,l,w,'left')
                srf_1=add_srf(poly_le_1,28)
                poly_ri=block_hor(x,y-(w+10)*0,l,w,'right')
                srf_2=add_srf(poly_ri,28)    
                req_srf.append(srf_0)
                req_srf.append(srf_1)
                req_srf.append(srf_2)                
            else:
                #L=2 R=1
                poly_le=block_hor(x,y-(w+10)*0,l,w,'left')
                srf_3=add_srf(poly_le,28)
                poly_ri_0=block_hor(x,y-(w+10)*0,l,w,'right')
                srf_4=add_srf(poly_ri_0,28)
                poly_ri_1=block_hor(x,y-(w+10)*1,l,w,'right')
                srf_5=add_srf(poly_ri_1,28)            
                req_srf.append(srf_3)
                req_srf.append(srf_4)
                req_srf.append(srf_5)
        else:
            ch_num_left=random.choice([1,2,3,4])
            if(ch_num_left==1):
                poly_g_le=block_hor(x,y-(w+10)*0,l,w,'left')
                srf_0=add_srf(poly_g_le,14)
                poly_f_le=block_hor(x,y-(w+10)*0,l/2,w,'left')
                rs.MoveObject(poly_f_le,[0,0,14])
                srf_1=add_srf(poly_f_le,14)              
                req_srf.append(srf_0)
                req_srf.append(srf_1)
                for i in range(3):
                    poly_g_ri=block_hor(x,y-(w+10)*i,l,w,'right')
                    srf_loop_0=add_srf(poly_g_ri,14)
                    poly_f_ri=block_hor(x,y-(w+10)*i,l/2,w,'right')
                    rs.MoveObject(poly_f_ri,[0,0,14])
                    srf_loop_1=add_srf(poly_f_ri,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)
            elif(ch_num_left==2):
                for i in range(2):
                    poly_g_le=block_hor(x,y-(w+10)*i,l,w,'left')
                    srf_loop_0=add_srf(poly_g_le,14)
                    req_srf.append(srf_loop_0)
                    poly_f_le=block_hor(x,y-(w+10)*i,l/2,w,'left')
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    req_srf.append(srf_loop_1)
                    poly_g_ri=block_hor(x,y-(w+10)*i,l,w,'right')
                    srf_loop_2=add_srf(poly_g_ri,14)
                    req_srf.append(srf_loop_2)
                    poly_f_ri=block_hor(x,y-(w+10)*i,l/2,w,'right')
                    rs.MoveObject(poly_f_ri,[0,0,14])
                    srf_loop_3=add_srf(poly_f_ri,14)
                    req_srf.append(srf_loop_3)
            elif(ch_num_left==3):
                poly_g_ri=block_hor(x,y-(w+10)*0,l,w,'right')
                srf_0=add_srf(poly_g_ri,14)
                poly_f_ri=block_hor(x,y-(w+10)*0,l/2,w,'right')
                rs.MoveObject(poly_f_ri,[0,0,14])
                srf_l=add_srf(poly_f_ri,14)   
                req_srf.append(srf_0)
                req_srf.append(srf_l)
                for i in range(3):
                    poly_g_le=block_hor(x,y-(w+10)*i,l,w,'left')
                    srf_loop_0=add_srf(poly_g_le,14)
                    poly_f_le=block_hor(x,y-(w+10)*i,l/2,w,'left')
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    req_srf.append(srf_loop_0)
                    req_srf.append(srf_loop_1)                    
            else:
                ch_lr_=random.choice(['left','right'])
                for i in range(2):
                    poly_g_le=block_hor(x,y-(w+10)*i,l,w,ch_lr_)
                    srf_loop_0=add_srf(poly_g_le,14)
                    req_srf.append(srf_loop_0)                    
                    poly_f_le=block_hor(x,y-(w+10)*i,l/2,w,ch_lr_)
                    rs.MoveObject(poly_f_le,[0,0,14])
                    srf_loop_1=add_srf(poly_f_le,14)
                    req_srf.append(srf_loop_1)
    return req_srf

def check(p,Q,poly_li,l,w):
    q=rs.AddPoint(Q)
    r0=p
    r1=[p[0]+l, p[1],0]
    r2=[p[0]+l, p[1]-w,0]
    r3=[p[0], p[1]-w,0]
    req=rs.AddPolyline([r0,r1,r2,r3,r0])
    req_cen=rs.CurveAreaCentroid(req)[0]
    sum=0
    for poly in poly_li:
        if(rs.PointInPlanarClosedCurve(q, poly)==0):
            intx=rs.CurveCurveIntersection(req, poly)
            if(intx and len(intx)>0):
                sum+=1
                rs.DeleteObject(req)
                break
        else:
            rs.DeleteObject(req)
            sum+=1
            break
    rs.DeleteObject(q)
    if sum==0:
        return [True,req]
    else:
        return [False]

def get_eval_pts(X,Y, srf_li_x, req_l, req_w):
    #40 250
    #94 145
    ini_poly=[]
    for i in srf_li_x:
        b=rs.BoundingBox(i)
        b0=b[0]
        b1=b[1]
        b2=b[2]
        b3=b[3]
        if(b0[2]==0):
            this_poly=rs.AddPolyline([b0,b1,b2,b3,b0])
            ini_poly.append(this_poly)
    req_poly=None
    r_sum=0
    k=Y
    for i in range(50):
        k-=10
        p_l_0=[X,k,0]
        p_l_1=[X-25,k,0]
        p_r_0=[X+10,k,0]
        p_r_1=[X+35,k,0]
        t_l=check(p_r_0, p_r_1, ini_poly, req_l, req_w)
        if(len(t_l)==2):
            req_poly=t_l[1]
            r_sum+=1
        else:
            t_r=check(p_l_0, p_l_1, ini_poly, -req_l-10, req_w)
            if(len(t_r)==2):
                req_poly=t_r[1]
                r_sum+=1
        if(r_sum>0):
            break
    req_poly2=rs.CopyObject(req_poly, [0,0,14])
    srf_d=add_srf(req_poly,14)    
    srf_a=add_srf(req_poly2, 14)
    rs.DeleteObjects(ini_poly)
    return [srf_d, srf_a]

def plot(M,N, main_counter):
    try:
        rs.DeleteObjects(srf_list_fingers)
    except:
        pass
    try:
        rs.DeleteObjects(srf_li)
    except:
        pass
    srf_list_fingers=[]
    srf_li=[]    
    srf_gym=None
    srf_band=None
    srf_admin=None
    srf_dining=None
    srf_art=None
    srf_spine=None
    srf_din=None
    srf_lab=None    
    A=700
    B=800
    X=M*A
    Y=N*B
    #rs.AddTextDot(main_counter,[X,Y,0])
    
    srf_top=add_top(X,Y)#up from 0,0
    srf_gym=srf_top[0]
    srf_band=srf_top[1]
    srf_li.append(srf_gym)
    srf_li.append(srf_band)
    
    #going down from y=0 => subtract 73.6 : bottom of top
    spine_Y=Y-73.6
    #corridor after top
    spine_Y-=10
    srf_spine=add_spine(X,spine_Y+73.6+10)
    
    #fingers
    req_w=random.randint(65,80)
    req_l=13000/req_w
    srf_list_fingers=add_fingers(X,spine_Y,req_l,req_w)
    for srf_finger in srf_list_fingers:
        srf_li.append(srf_finger)
    
    #rest 
    req_w_adar=random.randint(94,145)
    req_l_adar=13630/req_w_adar
    srf_adar=get_eval_pts(X,Y,srf_li, req_l_adar, req_w_adar)
    srf_admin=srf_adar[0]
    srf_art=srf_adar[1]
    srf_li.append(srf_admin)
    srf_li.append(srf_art)
    req_w_dila=random.randint(40,250)
    req_l_dila=10000/req_w_dila
    srf_dila=get_eval_pts(X,Y,srf_li, req_l_dila, req_w_dila)
    srf_din=srf_dila[0]
    srf_lab=srf_dila[1]    
    srf_li.append(srf_din)
    srf_li.append(srf_lab)
    
    rs.ObjectColor(srf_gym, (255,33,3))
    rs.ObjectColor(srf_band, (150,33,3))
    rs.ObjectColor(srf_admin, (150,133,3))
    rs.ObjectColor(srf_art, (50,233,173))
    rs.ObjectColor(srf_din, (250,33,203))
    rs.ObjectColor(srf_lab, (150,193,249))
    for srf_finger in srf_list_fingers:
        rs.ObjectColor(srf_finger, (30,133,243))
    #print(main_counter, len(srf_list_fingers))
    
    
    srf_li_x=[]
    srf_li_x.append(srf_band)
    srf_li_x.append(srf_admin)
    srf_li_x.append(srf_art)
    srf_li_x.append(srf_din)
    srf_li_x.append(srf_lab)
    for srf_finger in srf_list_fingers:
        srf_li_x.append(srf_finger)
    bxb=rs.BoundingBox(srf_li_x)
    bxb_poly=rs.AddPolyline([bxb[0],bxb[1],bxb[2],bxb[3],bxb[0]])
    bsp=rs.BoundingBox(srf_spine)
    sp_poly=rs.AddPolyline([bsp[0],bsp[1],bsp[2],bsp[3],bsp[0]])
    intx_crv=rs.CurveBooleanIntersection(sp_poly,bxb_poly)
    intx_srf=add_srf(intx_crv,28)
    rs.ObjectColor(intx_srf,(255,255,255))
    rs.DeleteObjects([srf_spine,bxb_poly,sp_poly])
    return srf_li

rs.EnableRedraw(False)
global_counter=0
a=10
b=a
for i in range(a):
    for j in range(b):
        output=plot(i,j,global_counter)
        global_counter+=1
rs.EnableRedraw(True)
