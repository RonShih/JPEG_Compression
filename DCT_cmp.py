import cv2
import numpy as np
from os.path import getsize

def zigzag(input): #zigzag algorithm ref: https://github.com/getsanjeev/compression-DCT/blob/master/zigzag.py
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    vmax = input.shape[0]
    hmax = input.shape[1]
    #print(vmax ,hmax )
    i = 0
    output = np.zeros(( vmax * hmax))
    while ((v < vmax) and (h < hmax)):
        if ((h + v) % 2) == 0:                 # going up
            if (v == vmin):
            	#print(1)
                output[i] = input[v, h]        # if we got to the first line
                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        
                i = i + 1
            elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
            	#print(2)
            	output[i] = input[v, h] 
            	v = v + 1
            	i = i + 1
            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
            	#print(3)
            	output[i] = input[v, h] 
            	v = v - 1
            	h = h + 1
            	i = i + 1
        else:                                    # going down
        	if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
        		#print(4)
        		output[i] = input[v, h] 
        		h = h + 1
        		i = i + 1
        	elif (h == hmin):                  # if we got to the first column
        		#print(5)
        		output[i] = input[v, h] 
        		if (v == vmax -1):
        			h = h + 1
        		else:
        			v = v + 1
        		i = i + 1
        	elif ((v < vmax -1) and (h > hmin)):     # all other cases
        		#print(6)
        		output[i] = input[v, h] 
        		v = v + 1
        		h = h - 1
        		i = i + 1
        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
        	#print(7)        	
        	output[i] = input[v, h] 
        	break
    #print ('v:',v,', h:',h,', i:',i)
    return output

def PSNR(str):
    org = cv2.imread('img.bmp')
    out = cv2.imread(str)
    sp = org.shape
    mse = 0
    for i in range (sp[0]):
        for j in range (sp[1]):
            for k in range (sp[2]):
               mse += (int(org[i,j,k]) - int(out[i,j,k]))**2
    mse /= sp[0]*sp[1]*sp[2]
    psnr = 10*np.log10(255**2/mse)
    return psnr

#qfactor = int(input("Enter quantization factor: "))#quanetization factor
qfactor = [1,2,4]
img = cv2.imread('img.bmp')
block_size = 16
for qf in range(len(qfactor)):
    q_table = ([[10, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120],
            [10, 15, 20, 25, 30, 35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150],
            [15, 20, 25, 30, 35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180],
            [20, 25, 30, 35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210],
            [25, 30, 35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240],
            [30, 35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270],
            [35 ,40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300],
            [40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330],
            [50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360],
            [60, 70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390],
            [70, 80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420],
            [80, 90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450],
            [90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480],
            [100, 110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510],
            [110, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 510, 510, 540],
            [120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 510, 540, 540, 570]])#quantization table
    print ("quantization factor = ", qfactor[qf])
    for i in range(block_size):#quantization table *= quantization factor
        for j in range(block_size):
            q_table[i][j] *= qfactor[qf]

    sp = img.shape #padding
    bottom = block_size - (sp[0] % block_size) #height
    right = block_size - (sp[1] % block_size) #width
    print("original img (height, width) =", "(", sp[0], ",", sp[1], ")", "padding size", bottom, right)
    p_img = cv2.copyMakeBorder(img, 0, bottom, 0 ,right, cv2.BORDER_REPLICATE) #padding邊緣
    sp = p_img.shape
    print("padding img (height, width) =", "(", sp[0], ",", sp[1], ")")

    fp = open("qfactor="+str(qfactor[qf])+".txt", "w")# 開啟檔案 "w" 複寫
    idct_img = p_img
    total_zero = 0
    for y in range(int(sp[0]/block_size)):#image blocking => DCT => Quantization => (write file)=> dequantization => IDCT => build image
        for x in range(int(sp[1]/block_size)):
            for k in range(sp[2]):
                #crop_img = p_img[:, :, k]#提出每個channel的img
                crop_img = p_img[y*block_size: y*block_size+block_size, x*block_size: x*block_size+block_size, k] #blocking:從初始位置切到最後位置的yx
                crop_img = np.float32(crop_img) #要轉成float不然不能用
                dct_img = cv2.dct(crop_img) #轉換成dct
                q_dct = np.zeros((block_size, block_size), dtype=int) #q_dct為dct_img量化後的結果 
                for i in range(block_size): #run every coefficient(pixel) in dct_img
                    for j in range(block_size):
                        if(dct_img[i,j] < 0):
                            q_dct[i,j] = 0
                        else:
                            q_dct[i,j] = np.floor(dct_img[i,j]/q_table[i][j])#quantization 註記:這邊q_table輸出要用[i][j]，用[i,j]會出錯
                                    
                M = np.zeros((block_size, block_size), dtype=int)
                M = zigzag(q_dct)#每個16 * 16的block做zigzag後存到M內(M為1D array)
                flag = 0 #檢查尾數是否都為0 以特殊符號替代尾數的0
                last = 0 #記錄最後一個非0的index(1-D array)，代表下一個index開始為一連串尾數0
                for i in range(block_size * block_size): #run every coefficient(pixel) in dct_img
                    if(M[i] == 0):
                        flag = 0
                    else:
                        flag = 1
                        last = i
                total_zero += block_size * block_size - last - 1 #計算0總數

                for i in range(last+1): #將陣列寫入至檔案
                    fp.write(str(int(M[i])) + " ") 
                    if(i == last):
                        fp.write("E ")
               
                d_block = np.zeros((block_size, block_size), dtype=int) #Dequantize 用前面沒有zigzag過的就好(q_dct)=>為了做IDCT成像
                for i in range(block_size):
                    for j in range(block_size):
                        d_block[i,j] = q_dct[i,j] * q_table[i][j]#d_block => dequantization後
                
                idct_block = cv2.idct(np.float32(d_block))
                idct_img[y*block_size: y*block_size+block_size, x*block_size: x*block_size+block_size, k] = idct_block

    #print(idct_img)
    print("qfactor=" + str(qfactor[qf]) + " write file done...")
    cv2.imwrite("qfactor=" + str(qfactor[qf]) + ".bmp", idct_img)
    print("qfactor=" + str(qfactor[qf]) + " write img done...")
    fp.close()# 關閉檔案
    print("qfactor=" + str(qfactor[qf]) + " zero count = " + str(total_zero))
    path = "qfactor=" + str(qfactor[qf]) + ".txt"
    size = getsize(path)
    print("Size of " + path + " = " + str(size) + " bytes\n")

print('PSNR (qfactor=1): ' + str(PSNR('qfactor=1.bmp')))
print('PSNR (qfactor=2): ' + str(PSNR('qfactor=2.bmp')))
print('PSNR (qfactor=4): ' + str(PSNR('qfactor=4.bmp')))