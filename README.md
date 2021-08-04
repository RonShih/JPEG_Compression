## Target
This program implements JPEG algorithm using DCT compression in python.  
## Steps of DCT compression: 
1. Divide the image into R,G,B three channels.
2. Divide each channel in block manner (a block = 16*16 pixels in this program).  
3. Do DCT(Discrete Cosine Transform) to each block and get a 16*16 DCT coefficient table. 
4. Quantify this table through self-defined quantization table.  
5. Do Zig-Zag algorithm for quantified table, get the total number of 0 in this stream and write file.  
6. Do IDCT to restore the image.  
7. (optional)Derive its PSNR(Peak signal-to-noise ratio) value. 


## DCT壓縮步驟：
1. 對圖片分RGB三通道
2. 對每個通道以16*16的block切割
3. 每個block去做DCT
4. 得出16*16的DCT coefficient的table並透過自定義的quantization table量化
5. 量化完做Zig-Zag 後面會呈現一堆0，計算尾數0的總數，然後寫檔
6. 最後用IDCT還原圖像
7. 計算其PSNR 值
