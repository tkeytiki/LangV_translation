# TODO

- ~~Create English character table~~
- ~~Convert font bmp to bpp~~
- ~~Font insertion~~
- ~~Convert English script to custom hex encoding~~
- **Insert script into game file**
- Check how many chars can fit in a row
- Check if longer script length than original breaks game (shift bits into "empty" block)
- Create a patch!

# project contents


## charactertables

Contains the table files for the English dual font to be inserted and the original Japanese. Table files contain characters and their corresponding hex encodings. 
>The Japanese table is not used in my scripts but is here as a reference for anyone that might need it.
>It's needed in the translation process to extract scripts and look up the hex code for the argument to one of the control codes, which need to be preserved in the English script file.

## engscript

Contains the translated English script files. Each are formatted to retain the control codes from the original Japanese scripts' binaries. 

## font

Contains all font related files. **psx6x12dualtry.bmp** is the English dual font in bmp image format. The game's font file is not formatted as a .bmp, so we have to convert it to the game's format. 
Running **format_bmp.py** will output a file here:

- **font.bin**: binary font file ready to be inserted into the game

  >We may need to make changes to the font, as when I first loaded it into the game some characters were cut off or bleeding into each other.
  >After making changes to the .bmp file in an image editing program, just save it and rerun **format_bmp.py**.

## gamefiles

- **input**: This is where you will put the original game files, such as SYSTEM.BIN.
- **output**: The **inject_font.py** script will make a copy of the game file, overwrite the font, and output the new SYSTEM.BIN to this folder

 >This is where the original game script files and output script files will have to be as well, haven't gotten that far yet x_X

## hexscript

English scripts that have been converted into binary files by **eng_to_hex** will populate here, ready to be inserted into the game files.

## eng_to_hex.py

Converts English script files to hexidecimal/binary.

## format_bmp.py

Formats .bmp file to binary that can be inserted into the game.

## inject_font.py

Injects the font into the game's SYSTEM.BIN file, which does not come included!! 
>You'll have to extract your own from your game and put it in the **gamefiles/input** directory.

# info

## data locations (in case i die)

### font
The font is at the very beginning of the **SYSTEM.BIN** file. Since there are infinite kanji, the original Japanese font file is way longer than our English one, so we can just paste it over the old one.

### scripts
Scripts are located in the game's **SCEN.DAT** file. The same scripts are stored in **SCEN2.DAT**, which we theorize contains hard mode data for the scenarios. Each scenario seems to be stored in a non-uniformly sized block (which is strange considering some end in trailing zeroes which suggest "empty" space resulting from pre-determined data sizing), the offsets of which are stored in 8 byte words listed in a pointer table at the beginning of the **SCEN.DAT** file. 

- **Scenario 1 offsets:**
  - **800:** beginning of scenario block
    - adding the word at 0x0 (40) and the word at 0x7c (1AB4) gives the offset (1AF4), add this to 800 (22F4) to get the address of the pointer table containing pointers to individual dialog lines
    - these seem to be values unique to **Scenario 1** as I tried calculating the same offset with other scenarios and it did not lead to a pointer table
  - **962:** pointer table containing pointers to pointers in the dialog pointer table mentioned below. we shouldn't need to mess with these
  - **22F4:** offset to the pointer table containing pointers to dialog lines. these are what we will be repointing
    - 0x0: the 4 bytes here contain the offset at which the final dialog ends   
    - 0x04: beginning of offsets, each pointer is stored in 2 bytes
  - **2490:** the script begins
- **Scenario 2:** ef76 (76ef)
- **Scenario 3:** 32bca (ca2b03)
- **Scenario 4:** 4e940 (40e904)
> The game stores data in Little Endian, use it when trying to search for addresses in the binaries (to find the pointer table hopefully...)
