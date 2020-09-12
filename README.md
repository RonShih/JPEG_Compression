# JPEG_algorithm
DCT compression
流程:
1. 對圖片分RGB三通道
2. 對每個通道以16*16的block切割
3. 每個block去做DCT
4. 得出16*16的DCT coefficient的table並透過自定義的quantization table量化
5. 量化完做Zig-Zag 後面會呈現一堆0，計算尾數0的總數，然後寫檔
6. 最後用IDCT還原圖像
7. 計算其PSNR 值

