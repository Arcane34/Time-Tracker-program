#imports
import pygame, random, math, sys, time

#initialising pygame window
pygame.init()
width  = (800,800)
win = pygame.display.set_mode(width)
clock = pygame.time.Clock()
run = True


#function for reading the points from file, where if the file does not exist points are set to 0
def read():
    try:
        with open("progress.txt","r") as file:
            contents=file.readline()
            contents=contents.strip()
            points = int(contents)
    except:
        points = 0

    return(points)



#function for writing the new value for total points to a file at the end of the program
def write(points):
    with open("progress.txt","w") as file:
        file.write(str(points))
    
            


#this is tha particle class that handles the motion and display of the particles on the screen
class particle:
    #initializing starting parameters of the particle
    def __init__(self,x,y, number):
        #position
        self.x = x
        self.y = y
        #velocity
        self.x_vel = 5*(random.randint(0,20)/10 -1)
        self.y_vel = 5*(random.randint(0,20)/10 -1)
        #acceleration
        self.x_a = 0
        self.y_a = 0
        #initializing angle for later use in velocity change calulations
        self.angle = 0
        self.size_vel = 0
        #defining size and colour on the type of particle it is, particles worth 1 are white and small, particles worth 100 are red and big
        if number == 1:
            self.particleType = 1
            self.colour = (255,0,0)
            self.size = 10
        else:
            self.particleType = 0
            self.colour = (255,255,255)
            self.size = 3

    #unused acceleration function that makes it so the particles orbit the centre of the window
    def accelerate(self):
        a = 0
        xDiff = (width[0]/2)-self.x
        if xDiff < 0:
            xNeg = xDiff * -1
        else:
            xNeg = xDiff
        
        yDiff = (width[1]/2)-self.y
        if yDiff<0:
            yNeg = yDiff * -1
        else:
            yNeg = yDiff
        
        if xDiff == 0:
            self.angle = math.pi / 2
        else:
            self.angle = math.atan(yNeg/xNeg)


            #if ((xDiff)**2+(yDiff)**2) or ((xDiff)**2+(yDiff)**2) > 5:
             #   a = 10000/((xDiff)**2+(yDiff)**2)**1/2
            self.x_a = 1*math.cos(self.angle)
            self.y_a = 1*math.sin(self.angle)

            
            
            if xDiff < 0:
                self.x_a = self.x_a * -1
            if yDiff < 0:
                self.y_a = self.y_a * -1

            #print(xDiff,yDiff,self.y_a,self.x_a,self.angle)
            self.x_vel += self.x_a
            self.y_vel += self.y_a
        
    def draw(self):
        #updating particle position
        self.x += self.x_vel
        self.y += self.y_vel

        #whenever a particle hits a boundary it will bounce off of the wall so its velocity needs to be changed respectively
        if  not(100 < self.x < 700):
            self.x_vel = self.x_vel * -1
        if  not(100 < self.y < 700):
            self.y_vel = self.y_vel * -1

        #self.size_vel -= random.randint(-2,0)
            
        #reducing particle size over time however size velocity is set to 0 so unused currently
        self.size -= self.size_vel
        
        #pygame.draw.rect(win,(255,255,255),(self.x-self.size/2,self.y-self.size/2,self.size,self.size))
        
        #function for drawing the particle as a circle
        pygame.draw.circle(win,self.colour,(self.x,self.y),self.size)



#stopwatch class that makes a button that when clicked starts and then another click resets the stopwatch and updates the points
class stopwatch:
    #initializing stopwatch values
    def __init__(self, x, y, w, h, ic, ac, count):
        #position and size
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        #different colours for when the mouse is on the button and when it is not
        self.ic = ic
        self.ac = ac

        #start and end time variables 
        self.startTime = None
        self.endTime = None

        #time displayed
        self.trackTime = "0:0:0"

        #the number of minutes required to get a point
        self.count = count

        #points gained
        self.points = 0

        #variable to start and stop the stopwatch
        self.on = False

        #adding it to the list of stopwatch objects to be drawn
        stopwatches.append(self)

    #a function for converting the total number of seconds, to a string with hours, minutes and seconds
    def time_convert(self,sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return(str(int(hours)) + ":" + str(int(mins)) + ":" + str(int(sec)))

    #function that handles the starting and stopping of the stopwatch
    def start(self):
        #if the stopwatch isnt already on, set a start time and set the on variable to True, otherwise record the end time, then set the on variable to false
        if self.on == False:
            self.startTime = time.time()
            for i in stopwatches:
                if i.on == True:
                    i.start()
            self.on = True
        
        else:
            self.endTime = time.time()
            self.on = False
            #calculating time passed
            time_lapsed = self.endTime - self.startTime
            #self.points += int(time_lapsed // 60)

            #calculating the total points gathered from the amount of time , being the total time DIV count (so 1 point per 60 minutes)
            self.points = int(time_lapsed // self.count)
            self.trackTime = self.time_convert(time_lapsed)

            #resetting timer
            self.trackTime = "0:0:0"

            
    #function that returns the points gotten and resets the points gotten by the stopwatch
    def getPoints(self):
        points = self.points
        self.points = 0
        return(points)
        
    #function to update the visual display of the stopwatch
    def oN(self):
        timeNow = time.time()
        time_lapsed = timeNow - self.startTime
        self.trackTime = self.time_convert(time_lapsed)

    #function to finally draw the stopwatch onto the screen as a button (using the button object)
    def draw(self):
        if self.on == True:
            self.oN()
        button(self.trackTime, self.x, self.y, self.w, self.h, self.ic, self.ac, self.start)



#points class that draws the point number at the centre of the screen
class Points:
    #initialization of object
    def __init__(self,x,y, points):
        #position initialization
        self.x = x
        self.y = y
        #points initialization
        self.points = int(points)

        
    #draw function to draw the points
    def draw(self):
        #Creating the first black text that will work as the outline for the white text
        smalltext = pygame.font.Font("EnchantedLand.otf", 50)
        textsurf, textrect = text_objects(str(self.points), smalltext, (0,0,0))
        textrect.center = (self.x, self.y)
        win.blit(textsurf, textrect)

        #creating the white text that is over the text before it
        smalltext = pygame.font.Font("EnchantedLand.otf", 40)
        textsurf, textrect = text_objects(str(self.points), smalltext, (255,255,255))
        textrect.center = (self.x, self.y)
        win.blit(textsurf, textrect)
        
        
        

#function for creating a text surface for a specific text and font and then returns the surface object along with its rect  
def text_objects(text, font, colour):
    textsurface = font.render(text, True, colour)
    return textsurface, textsurface.get_rect()


#button function that draws a rect on screen 
def button(msg, x, y, w, h, ic, ac, action=None):
    #getting mouse data
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #drawing the button,checking for if the cursor is clicking on the button and changing the buttons colour if the mouse is on the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ic, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
            time.sleep(0.4)
    else:
        pygame.draw.rect(win, ac, (x, y, w, h))

    #centering and drawing the text onto the button rect
    smalltext = pygame.font.Font("EnchantedLand.otf", 40)
    textsurf, textrect = text_objects(msg, smalltext, (0,0,0))
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textsurf, textrect)




#screen update/draw function that runs for every frame
def redrawWin():
    #filling the screen with black to remove the last frame
    win.fill((0,0,0))

    #drawing every particle object in the points100 list
    for pa in points100:
        pa.draw()

    #drawing every particle object in the points list
    for p in points:
        p.draw()

    #drawing the stopwatch for adding points
    stopW.draw()

    #drawing the stopwatch for taking away points
    pointTakeAway.draw()

    #drawing the point display object at the center of the screen
    pointHolder.draw()

    #updating the pygame screen
    pygame.display.update()


#getting the points from the file
point = read()

#list for stopwatch objects
stopwatches = []

#creating point adder stopwatch object
stopW = stopwatch( 0, 700, 100,100, (155,155,155), (255,255,255), 60)

#creating point removal stopwatch object
pointTakeAway = stopwatch( 700, 700, 100,100, (155,0,0), (255,0,0), 1)

#creating the point display object
pointHolder = Points(400,400, point)

#creating points particle object list
points = []

#creating points100 particle object list
points100 = []

#main loop
while run:
    #framerate
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write(pointHolder.points)
            run = False
            sys.exit()

    #updating total points every frame from the stopwatch getPoints functions
    pointHolder.points += stopW.getPoints()
    pointHolder.points -= pointTakeAway.getPoints()

    #making sure you cannot have negative points
    if pointHolder.points < 0:
        pointHolder.points = 0

    #checking the number of 1 point particle objects and updating the particles on screen accordingly each frame
    over100 = len(points100)
    realOver100 = pointHolder.points // 100
    if len(points) < pointHolder.points % 100:
        points.append(particle(400,400, 0))
    elif len(points) > pointHolder.points % 100:
        for i in range(len(points) - (pointHolder.points %100)):
            points.pop(0)

            
    #checking the number of 100 point particle objects and updating the particles on screen accordingly each frame
    if over100 < realOver100:
        points100.append(particle(400,400, 1))
    elif over100 > realOver100:
        for i in range(over100 - realOver100):
            points100.pop(0)
    
    #redrawing window every frame
    redrawWin()


