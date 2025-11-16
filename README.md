# HOW IT'S GOING

![intro quiz](https://github.com/tkeytiki/LangV_translation/blob/master/progress%20images/quiz.gif)

![https://github.com/tkeytiki/LangV_translation/blob/master/progress%20images/shop.png](https://raw.githubusercontent.com/tkeytiki/LangV_translation/refs/heads/master/progress%20images/shop.png)

![save and load screen](https://github.com/tkeytiki/LangV_translation/blob/master/progress%20images/saveload.png)

![level up screen](https://raw.githubusercontent.com/tkeytiki/LangV_translation/refs/heads/master/progress%20images/levelup.png)

![https://github.com/tkeytiki/LangV_translation/blob/master/progress%20images/lambdamenu.png](https://raw.githubusercontent.com/tkeytiki/LangV_translation/refs/heads/master/progress%20images/lambdamenu.png)


# TODO

- ~~Create English character table~~
- ~~Convert font bmp to bpp~~
- ~~Font insertion~~
- ~~Convert English script to custom hex encoding~~
- ~~Insert script into game file~~
- ~~Check how many chars can fit in a row~~
- ~~Check if longer script length than original breaks game (shift bits into "empty" block)~~
- ~~Complete overhaul of project, using an ASM hook instead of dual font~~
- ~~Figure out how to skip name screen~~
- ~~Does the B8 char actually work as intended? Nope...~~
- ~~Finishing repointing script~~
- ~~ASM hack the level up screen because the strings are dumb~~
- ~~Fix Load screen formatting and get rid of that N~~
- ~~Put in the rest of the item icons~~
- ~~Finish script to repoint system files~~
- Actually translate everything
- Create a patch!

# completed translations
- Intro Quiz
- Save/load screen and memory card related text
- Title screen and all sub-menus
- Battle preparation menus and unit select menu
- Level up text
- Class names and unit types
- Troop names, descriptions
- Item names, descriptions
- Summon names, descriptions
- Spell names, descriptions
- Tooltips

Some UI text is probably still weird because without context I wasn't sure how to translate it and I haven't yet come across it in the actual game yet... will be fixed in time

## currently in progress
- Scenario 1
- Tutorial

# project contents


## charactertables

Contains the table files for the English font to be inserted and the original Japanese. Table files contain characters and their corresponding hex encodings. 
After the project overhaul langvsingle.tbl is the only relevant English font table.
>The Japanese table file is needed in the translation process to extract scripts and look up the hex code for the argument to one of the control codes, which need to be preserved in the English script file.

## engscript

Contains the translated English script files. Each are formatted to retain the control codes from the original Japanese scripts' binaries. 

## font

Contains all font related files. 

- **oneletterfont.bin**: binary font file ready to be inserted into the game. It only contains basic English characters and symbols, and thus there is a script in **format_bmp.py** for adding new characters to the font on an as needed basis.

  >To insert the font into your SYSTEM.BIN file, place your SYSTEM.BIN file in **gamefiles\\input\\** and run **generate_system_file.py**

## gamefiles

- **input**: This is where you will put the original game files, such as SYSTEM.BIN.
- **output**: This is where all patched game files will be generated.


## how to use

- Place the **SYSTEM.BIN**, **SCEN.DAT**, and **SLPS_18.19** files in the **gamefiles\\input\\** folder
- Run **MAIN.py**
- Insert the newly created files in **gamefiles\\output\\** back into the game using a software such as CDMage

**Currently only the intro quiz has been translated. Other text data will appear as gibberish, including menu text.**

>When the translation is finished I plan to make a patch...
# info

## data locations (in case i die)

### font
The font is at the very beginning of the **SYSTEM.BIN** file. Since there are infinite kanji, the original Japanese font file is way longer than our English one, so we can just paste it over the old one.

### menu text, etc
This is all also located in the **SYSTEM.BIN** file. The master pointer table that points to other pointer tables (which are followed by lists of text strings) is located at **0x8010**.
>The offsets in the sub-pointer tables are multiplied by 2 before being added to the base offset

### scripts
All pointers for scenario data blocks are 8 bytes long each and located at the very beginning of the **SCEN.DAT** file. When repointing these they MUST be repointed to 0x800 byte aligned addresses or the game will hang.

The scripts are also stored in **SCEN2.DAT**, which we theorize contains hard mode data for the scenarios.  

- **Scene 0 offsets:**
  - **800:** beginning of scenario block
    - adding the word at 0x0 (40) and the word at 0x7c (1AB4) gives the offset (1AF4), add this to 800 (22F4) to get the address of the pointer table containing pointers to individual dialog lines
    - these seem to be values unique to this block as I tried calculating the same offset with other blocks and it did not lead to a pointer table
    - I will probably just manually search for each pointer table
  - **962:** pointer table containing pointers to pointers in the dialog pointer table mentioned below. we shouldn't need to mess with these
  - **22F4:** offset to the pointer table containing pointers to dialog lines. these are what we will be repointing
    - 0x0: the 4 bytes here contain the offset at which the final dialog ends   
    - 0x04: beginning of offsets, each pointer is stored in 2 bytes
  - **2490:** the script begins
- **Scene 1:**
    - **pointer table:** ee46
    - **script address:** ef76 
- **Scene 2:** 
    - **pointer table:** 32ab8
    - **script address:** 32bca 
- **Scene 3:** 
    - **script address:** 4e940 
> The game stores data in Little Endian, use Little Endian when writing pointer addresses
