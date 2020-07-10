import heapq
import pygame 
from tkinter import *
pygame.init()
# root = Tk()

start = (10,10)
end  =  (200,200)

def tkwindow():
    root = Tk()
    def getndestroy():
        global start
        global end
        start = (int(startX.get())+10,int(startY.get())+10)
        end = (int(endX.get())+10, int(endY.get())+10)
        root.destroy()
    ins = Label(root,text = "Enter valid starting and Ending coordinates in range [0,500]")
    labelstartx = Label(root, text="Initial X coordinate:")
    labelstarty = Label(root, text="Initial Y coordinate:")
    labelendx = Label(root, text="Final X coordinate:")
    labelendy = Label(root, text="Final Y coordinate:")
    startX = Entry(root)
    startY = Entry(root)
    endX = Entry(root)
    endY = Entry(root)
    done = Button(root,text="done",command=getndestroy,width=17,bg="cyan")
    ins.grid(row=0,column=1)
    labelstartx.grid(row=1,column=0)
    startX.grid(row=2,column=0)
    labelstarty.grid(row=1,column=2)
    startY.grid(row=2,column=2)

    labelendx.grid(row=3,column=0)
    endX.grid(row=4,column=0)
    labelendy.grid(row=3,column=2)
    endY.grid(row=4,column=2)

    done.grid(row=5,column=2)
    root.mainloop()
def instruction():
    root = Tk()
    label = Label(root,text="Draw a grid using mouse and then press Space bar to get the result\n")
    ok = Button(root,text = "ok" , command=root.destroy,bg="cyan")
    label.pack()
    ok.pack()
    root.mainloop()
ans = -1
def answer():
    global ans
    root = Tk()
    label = Label(root,text = "The shortest Distance is "+str(ans))
    finish = Button(root,text="Finish",command=root.destroy,bg="cyan")
    label.pack()
    finish.pack()
    root.mainloop()
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
screenX,screenY = (500,500)
def highlight(tup,color,screen):
    pygame.draw.rect(screen,color,(tup[0],tup[1],10,10))
def dist(tup1,tup2):
    return ((tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2)**(1/2)
def heuristic(to,frm):
    # dist(to,frm) +
    return  max(abs(frm[0]-end[0]),abs(frm[1]-end[1])) + max(abs(frm[0]-to[0]),abs(frm[1]-to[1]))
    # return dist(to,frm) + dist(frm,end)
def solution(screen):
    global ans
    run = 1
    vis = [[False for _ in range(screenX+1)] for _ in range(screenY+1)]
    X = [(0,0,start[0],start[1])] # heur,dist
    heapq.heapify(X)
    lastx,lasty = start[0],start[1]
    while run==1 and len(X) > 0:
        top = heapq.heappop(X)
        xcor,ycor = top[2],top[3]
        vis[xcor][ycor] = True
        pygame.draw.rect(screen,GREEN,(xcor,ycor,10,10))
        pygame.display.update()
        lastx,lasty = xcor,ycor
        if (xcor,ycor) == end:
            ans = top[1]
            run = 0
            print(ans)
            break
        for i in (0,4,2):
            for j in (0,4,2):
                if (i == j and (i == 2)): 
                    continue
                curx,cury = xcor+5*(i-2),ycor+5*(j-2)
                if curx < 0 or cury < 0 or curx > screenX or cury > screenY or vis[curx][cury]==True or pygame.Surface.get_at(screen,(curx,cury))[:-1] == BLUE:
                    continue
                vis[curx][cury] = True
                heapq.heappush(X,(heuristic((curx,cury),(xcor,ycor)),top[1]+dist((curx,cury),(xcor,ycor)),curx,cury))
                curx,cury = xcor+5*(j-2),ycor+5*(i-2)
                if curx < 0 or cury < 0 or curx > screenX or cury > screenY or vis[curx][cury]==True or pygame.Surface.get_at(screen,(curx,cury))[:-1] == BLUE:
                    continue
                vis[curx][cury] = True
                heapq.heappush(X,(heuristic((curx,cury),(xcor,ycor)),top[1]+dist((curx,cury),(xcor,ycor)),curx,cury))
    
        
def main():
    tkwindow()
    instruction()
    screen = pygame.display.set_mode((screenX,screenY))
    pygame.display.set_caption("SHORTEST PATH")
    screen.fill(WHITE)
    pygame.display.update()
    highlight(start,RED,screen)
    highlight(end,BLACK,screen)
    pygame.display.update()
    run = 1
    draw = 0
    mx,my = 0,0
    while run==1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and draw == 0:
                draw = 1
                mx,my = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                draw = 0
            elif event.type == pygame.MOUSEMOTION and draw == 1:
                currX,currY = pygame.mouse.get_pos()
                pygame.draw.line(screen,BLUE,(currX,currY),(mx,my),20)
                mx,my = currX,currY
                pygame.display.update()
            elif event.type == pygame.MOUSEMOTION and draw == 0:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                color = screen.get_at((mouse_x,mouse_y))
                # print(color)
        button = pygame.key.get_pressed()
        if button[pygame.K_SPACE]:
            solution(screen)
            run = 0
    pygame.time.delay(500)
    pygame.display.quit()
    pygame.quit()
    answer()
     
main()
