import cv2
import numpy as np
#import copy

def blobs(img_G,upper):
    
    nLabels, labelImages, stats, centroids = cv2.connectedComponentsWithStats(img_G)
#    print(stats.shape)
#    print(stats)

    stats_T=np.array(stats).T
    stats_in=np.where(stats_T[-1]>upper)

    stats2=stats[stats_in]
    centroids2=centroids[stats_in]
    nLabels2=np.count_nonzero(stats_T[-1]>upper)


    return nLabels2, labelImages, stats2, centroids2


            
            
        
    
    
    
    
    

#img = cv2.imread("./filtered_images/5_img_judged.png",0)

#nLabels, labelImages, stats, centroids = blobs(img, 250000)



#cv2.imwrite("./test.png",labelImages)