int distance;

int startTime;
int curTime;
float dt;

boolean isRunning;

int generationTime;
int generationFactor;

PFont font;

Grid grid;

void setup() {
  // Set params
  int gridSize = 25;
  int cubeSize = 10;
  int cubePadding = 5;
  
  // Globals
  startTime = millis();
  curTime = millis();
  distance = 750;
  isRunning = true;
  generationTime = 1000; // 1 second per generation
  generationFactor = 1; // user can speed up or slow down time
  
  // Setup font drawing
  font = createFont("Arial", 16, true);
  textFont(font);
  
  // Set window size
  size(640, 640, P3D); 
  
  // Setup Grid
  grid = new Grid(gridSize, cubeSize, cubePadding);
  camera(grid.mid, grid.mid, grid.mid + distance, grid.mid, grid.mid, grid.mid, 0, 1, 0);
}

void draw() {
  background(0); 
  stroke(0);
  if(isRunning) {
    curTime = millis();
    dt = float((curTime - startTime))/float(startTime);
    if(curTime - startTime > (generationTime / generationFactor)) {
      grid.update();
      startTime = millis(); 
    }
  }
  grid.show(dt);
  camera(mouseX, height/2, distance, grid.mid, grid.mid, grid.mid, 0, 1, 0);
  // Draw text on screen
  fill(255);
  textMode(SCREEN);
  String out = "Generation Speed: " + generationFactor + "x";
  text(out, 0, height - 16);
} 

// Make sure you click in the scene before trying to press keys...
void keyReleased() {
  if(key == ' ') {
    isRunning = !isRunning;
  } else if(key == '1') {
    generationFactor = 1; 
  } else if(key == '2') {
     generationFactor = 2; 
  } else if(key == '3') {
     generationFactor = 3; 
  }
}

// Class definitions
class Cube {
  color curColor;
  color aliveColor;
  
  float xPos;
  float yPos;
  float zPos;
  float mySize;
  
  boolean isAlive;
    
  Cube(color tC, float tXPos, float tYPos, float tZPos, float tS, boolean tAlive) {
    aliveColor = tC;
    if(tAlive) {
      curColor = aliveColor;
    } else {
      curColor = color(255);
    }
    xPos = tXPos;
    yPos = tYPos;
    zPos = tZPos;
    mySize = tS;
    isAlive = tAlive;
  }
  
  void update(float dt) {
    pushMatrix();
    if(isAlive) {
      fill(aliveColor);
      stroke(0);
    } else {
      noFill();
      noStroke();
    }
    translate(xPos, yPos, zPos);
    box(mySize);
    popMatrix();
  }
  
  void kill() {
    //curColor = color(0);
    isAlive = false;
  }
  
  void spawn() {
    //curColor = aliveColor;
    isAlive = true;
  }
  
}

class Grid {
  int mySize;
  int cubeSize;
  int cubePadding;
  
  float mid;
  
  Cube[][][] cubes;
  
  Grid(int tSize, int tCubeSize, int tCubePadding) {
    mySize = tSize;
    cubeSize = tCubeSize;
    cubePadding = tCubePadding;
    cubes = new Cube[mySize][mySize][mySize];
    
    int curX, curY, curZ, seed;
     for(int xc = 0; xc < mySize; xc++) {
      for(int yc = 0; yc < mySize; yc++) {
        for(int zc = 0; zc < mySize; zc++) {
          curX = xc * (cubeSize + cubePadding);
          curY = yc * (cubeSize + cubePadding);
          curZ = zc * (cubeSize + cubePadding);
          seed = int(random(100));
          cubes[xc][yc][zc] = new Cube(color(255, 25, 10), curX, curY, curZ, cubeSize, (seed >= 1 && seed <= 15));
        }
      } 
    } 
    
    mid = (mySize * (cubeSize + cubePadding)) / 2.0;
  }
  
  void show(float dt) {
    for(int i = 0; i < cubes.length; i++) {
      for(int j = 0; j < cubes[i].length; j++) {
        for(int k = 0; k < cubes[i][j].length; k++) {
          cubes[i][j][k].update(dt);
        } 
      }
    }  
  }

  void update() {
    for(int i = 0; i < cubes.length; i++) {
      for(int j = 0; j < cubes[i].length; j++) {
        for(int k = 0; k < cubes[i][j].length; k++) {
          play(i, j, k);
        } 
      }
    }  
  }
  
  void play(int i, int j, int k) {
    int n = getNumAliveNeighbors(i, j, k);
    if(cubes[i][j][k].isAlive) {
      if(n < 2) {
        cubes[i][j][k].kill();
      } else if(n > 3) {
        cubes[i][j][k].kill();
      }
    } else {
      if(n == 3) {
        cubes[i][j][k].spawn();
      } 
    }
  }
  
  int getNumAliveNeighbors(int i, int j, int k) {
    int count = 0;
    for(int cx = i - 1; cx <= i + 1; cx++) {
      for(int cy = j - 1; cy <= j + 1; cy++) {
        for(int cz = k - 1; cz <= k + 1; cz++) {
          if(cx > 0 && cx < cubes.length && cy > 0 && cy < cubes[0].length && cz > 0 && cz < cubes[0][0].length) {
            if(cx != i && cy != j && cz != k) {
              if(cubes[cx][cy][cz].isAlive) {
                count++;  
              }
            }
          }
        } 
      } 
    }
    return count;
  }
    
}
