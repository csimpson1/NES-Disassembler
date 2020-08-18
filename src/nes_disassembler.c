/*
 * nes_disassembler.c
 *
 *  Created on: Jul. 20, 2020
 *      Author: csimp
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct commonFlags {
		int prgRomSize; //size of the PRG ROM (program code) in 16 KB blocks
		int chgRomSize; //size of the CHR ROM (graphics) in 8KB blocks
		bool vertMirroring; //specifies the mirroring mode. false: horizontal, true: vertical
		bool batBackedPrgRam; //specifies if cartridge contains battery backed PRG RAM, or another persistant memory
		bool trainer; //specifies if the cart contains a 512 byte trainer region at $7000 - $71FF
		bool ignoreMirrorMode; //ignores the above mirroring bit, instead provide 4 screen VRAM
		int mapper; //defines which mapper the cart uses
};

struct iNesHeader {
	struct commonFlags flags;
	bool vsUnisystem; //defines if the game is meant to be played on the VS Unisystem (NES Arcade System)
	bool playchoice10; //defines if the game is PlayChoice-10, and contains 8KB of hint screen data after the CHR RAM data
	int prgRamSize; //defines the size of PRG RAM
	bool isPalTvSystem; //defines which TV system game is for. false: NTSC true: PAL
	/*
	 * We are ignoring byte 10 in this specification. The docs here
	 * https://wiki.nesdev.com/w/index.php/INES#Flags_10
	 * say this byte is not a part of the official spec
	 */

};

struct nes20header {
		struct commonFlags flags;

};




void parse_header();

int main(){

	char fileName[] = "C:\\Users\\csimp\\Documents\\Roms\\Super_Mario_Bros.txt";
	FILE *fp;

	fp = fopen(fileName, "r");

	if (fp == NULL){
			perror("Error when opening the file.\n");
			return(-1);
	}

	int headerLen = 32; // Default size for .nes files
	char* header = (char*) calloc(headerLen + 1, sizeof(char));

	if(header == NULL){
		perror("Error when allocating memory\n");
		return(-2);
	}

	fread(header, sizeof(char),32,fp);

	printf("The first 32 chars of the file are %s\n\n", header);



	/*
	printf("The contents of the %s file are :\n", fileName);

	while ((ch = fgetc(fp)) != EOF){
		printf("%c", ch);
	}
	*/


	fclose(fp);
	return(0);

}
