# Rubiks-Cube
This is my first practical application of my matricies / linear algebra object i made a while ago

The game is made entirely in python and pygame with no external assets or images

There is a compiled exe in the repository but if you wish to run the python code make sure to install pygame beforehand using:
```bash
pip install pygame
```

# Controls
1. ![leftclick](https://github.com/omar-elsherbiny/Rubiks-Cube/assets/137009632/72b8a47a-5e4f-419b-a802-23d1ef74e625)<br>`left click and drag` to rotate a layer in the cube
    - red piece is the piece first selected
    - green piece is the piece you are hovering on
    - blue pieces are the selected layer to rotate based on the common operations between the red and green piece

3. ![scrolldown](https://github.com/omar-elsherbiny/Rubiks-Cube/assets/137009632/1ee3b262-4ec0-4af4-b903-a40dfe4bfcb7)<br>`scroll down` to switch the mode to rotate any layer clockwise

4. ![scrollup](https://github.com/omar-elsherbiny/Rubiks-Cube/assets/137009632/4c0f4451-d1e9-4671-b1f8-a51a2b20d0e1)<br>`scroll up` to switch the mode to rotate any layer anti-clockwise / counter-clockwise

5. ![rightclick](https://github.com/omar-elsherbiny/Rubiks-Cube/assets/137009632/a8090461-aace-4e79-84f1-e4a0968f347c)<br>`right click and drag` to pan around the cube
    - the basis vectors at the bottom are the current orientation of the cube 
    (white on top, green infront, and red on the side), though it changes if you make and operation on the middle layers of the cube

6. ![scroll](https://github.com/omar-elsherbiny/Rubiks-Cube/assets/137009632/7b9435fa-ecc9-4f81-9d35-50c618287e07)<br>`scroll button` is just an extra feature to make a random operation on the cube

# Scramble
The default values in the `scramble.json` is :
```json 
"set_scramble":false,
"scramble":""
```
If you wish to set a manual scramble, set it to true and the scramble you wish<br>
example:
```json 
"set_scramble":true,
"scramble":"r` f b` u"
```
Setting it to `true` and `""` will make the cube solved