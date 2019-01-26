def reach_goal(utilty,start):
        stop_counter = len(utilty) * len(utilty)
        iterator = start
        while (utilty[iterator[0]][iterator[1]] != 1 and stop_counter != 0) :
            
            max_num = 0.0
            #0 : Down, 1 : Up, 2 : Left, 3 : Right
            direction = 0
            #Down
            if iterator[0] + 1 < len(utilty) and utilty[iterator[0] + 1][iterator[1]] >= max_num :
                max_num = utilty[iterator[0] + 1][iterator[1]]
                direction = 0
            #Up
            if iterator[0] - 1 >= 0 and utilty[iterator[0] - 1][iterator[1]] >= max_num :
                max_num = utilty[iterator[0] - 1][iterator[1]]
                direction = 1
            #Left
            if iterator[1] - 1 >= 0 and utilty[iterator[0]][iterator[1] - 1] >= max_num :
                max_num = utilty[iterator[0]][iterator[1] - 1]
                direction = 2
            #Right
            if iterator[1] + 1 < len(utilty) and utilty[iterator[0]][iterator[1] + 1] >= max_num :
                max_num = utilty[iterator[0]][iterator[1] + 1]
                direction = 3
            
            if direction == 0 :
                print("Move Down")
                iterator = [iterator[0] + 1,iterator[1]]
            elif direction == 1 :
                print("Move Up")
                iterator = [iterator[0] - 1,iterator[1]]
            elif direction == 2 :
                print("Move Left")
                iterator = [iterator[0],iterator[1] - 1]
            else:
                print("Move Right")
                iterator = [iterator[0],iterator[1] + 1]
            
            stop_counter-=1

if __name__ == "__main__" :
    ut = [[0, 0.1, 0.2, 0.3],[0.2, 0.3,0.4,0.5],[0.3,0.4,0.45,0.5],[0.4,0.44,0.48,1]]
    reach_goal(ut, (0,0))