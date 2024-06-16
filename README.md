# TODO

- ~~Create English character table~~
- ~~Convert font bmp to bpp~~
- ~~Font insertion~~
- **Convert English script to custom hex encoding**
- Insert script into game file
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

### WIP

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
Scripts are located in the game's **SCEN.DAT** file. The same scripts are stored in **SCEN2.DAT**, which we theorize contains hard mode data for the scenarios. Each scenario seems to be stored in a non-uniformly sized block (which is strange considering some end in trailing zeroes which suggest "empty" space resulting from pre-determined data sizing), and I have not been able to find a pointer table that lists all script addresses. Here are some of the addresses I've gotten so far, from manually scouring the file. (Having not translated yet, not 100% sure this is accurate; I'm assuming the scenarios are in order in the file and there are no scripts that do not belong to scenarios...)

- **Scenario 1:** 2490 (Little Endian: 9024)
- **Scenario 2:** ef76 (76ef)
- **Scenario 3:** 32bca (ca2b03)
- **Scenario 4:** 4e940 (40e904)
> The game stores data in Little Endian, use it when trying to search for addresses in the binaries (to find the pointer table hopefully...)
