import cv2 as cv
import numpy as np

def floodfill(i,j,dp,n,m,maze,visited):

    if i == n-1 and j == m-1:
        return 0
    
    if i == n or j == m or i == -1 or j == -1:
        return 10000000
    if visited[i][j] == 1:
        return 10000000
    if maze[i][j] == 0:
        dp[i][j] = 10000000
        return 10000000
    if dp[i][j]!=-1:
        return dp[i][j]
    visited[i][j] = 1
    ans = min(floodfill(i+1,j,dp,n,m,maze,visited),floodfill(i,j+1,dp,n,m,maze,visited),floodfill(i-1,j,dp,n,m,maze,visited),floodfill(i,j-1,dp,n,m,maze,visited)) + 1
    dp[i][j] = ans
    visited[i][j] = 0
    return ans  

rasta = []
def draw_path(i,j,dp,img,n,m):
    if i == n-1 and j == m-1:
        return

    rasta.append((i,j))
    if i+1!=n and dp[i+1][j] == dp[i][j] - 1:
        draw_path(i+1,j,dp,img,n,m)
    elif i!=0 and dp[i-1][j] == dp[i][j] - 1:
        draw_path(i-1,j,dp,img,n,m)
    elif j!=0 and dp[i][j-1] == dp[i][j] - 1:
        draw_path(i,j-1,dp,img,n,m)
    else:
        draw_path(i,j+1,dp,img,n,m)

n = int(input('Number Of Rows In The Picture: '))
m = int(input('Number Of Columns In The Picture: '))
img_path = input('Name of the file: ')
imgog = cv.imread(img_path)
img = cv.resize(imgog, (n,m), interpolation = cv.INTER_AREA)
bw = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
maze = cv.adaptiveThreshold(bw,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
maze = np.where(maze==255,1,0)
        
dp = [[-1]*m for _ in range(n)]
visited = [[0]*m for _ in range(n)]
dp[n-1][m-1] = 0
floodfill(0,0,dp,n,m,maze,visited)
draw_path(0,0,dp,img,n,m)
rasta.append((20,20))
rasta
for i,j in rasta:
    img[i][j][1] = 255
    img[i][j][0] = 0
    img[i][j][2] = 0

imgback = cv.resize(img,(420,420),interpolation = cv.INTER_AREA)
cv.imwrite('Path.png',imgback)
cv.imshow('Original Maze',imgog)
cv.imshow('Path',imgback)
cv.waitKey(0)


