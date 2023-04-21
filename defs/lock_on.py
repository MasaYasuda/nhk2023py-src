def lock_on(stats,Target,Target_type,typeofnow,x,y):
    size=stats.shape[0]

    for i in range(size):
        x_min=stats[i][0]
        x_max=x_min+stats[i][2]
        y_min=stats[i][1]
        y_max=y_min+stats[i][3]


        if x_min<x & x<x_max:
            if y_min<y & y<y_max:
                num=0
                check=0
                loT=len(Target)
                print("end1")
                while Target[num]!=0:
                    if num<loT-1:
                        num+=1
                    else:
                        print("Too many targets!!")
                        return Target,Target_type

                Target[num]=i+1
                Target_type[num]=typeofnow
                print(str(i+1)+"を予約リストに入れました")
                return Target,Target_type
    
    print("non pole.")
    return Target,Target_type
