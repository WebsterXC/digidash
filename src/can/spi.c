#include <bcm2835.h>
#include <stdio.h>
#include <stdlib.h>

// Commands
#define MCP_WRITE   0x02
#define MCP_WRTXB   0x40
#define MCP_READ    0x03
#define MCP_RESET   0xC0
#define MCP_STATUS  0xA0
#define MCP_RXSTTS  0xB0
#define MCP_RTS_ALL 0x87
#define MCP_BITMOD  0x05


static void mcp__init__(

static inline int mcp_write(uint8_t address, uint8_t byte){
	uint8_t *codes = (uint8_t *)malloc(sizeof(uint8_t) * 3);
	codes[0] = MCP_WRITE;
	codes[1] = address;
	codes[2] = byte;

	bcm_2835_spi_transfern(codes, 3);
	return 0;
}	

// Creates a new array containing the result from read register.
// Pass an uninitialised pointer and read address.
static inline void mcp_read(uint8_t *copy, uint8_t address){
	uint8_t value;

	uint8_t *codes = (uint8_t *)malloc(sizeof(uint8_t) * 3);
	codes[0] = MCP_READ;
	codes[1] = address;
	codes[2] = 0xFF;

	bcm_2835_spi_transfern(codes, 3);

	copy = codes;

	return;
}

int main(int argc, char **argv){

	if(!bcm2835_init()){
		printf("Initialisation failed. Exiting...\n");
		return 1;
	}

	if(!bcm2835_spi_begin()){
		printf("SPI clock startup failure.\n");
		return 2;
	}

	bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);  // MSB first in transactions
	bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
	bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_512);  //488.28kHz
	bcm2835_spi_chipSelect(BCM2835_SPI_CS0);		     // ChipSel #0
	bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);     // CS active LOW	

	// Fill a buffer and then read from it
	// WRITE command to address 0x36, followed by data
	uint8_t buffer = [MCP_WRITE, 0x36, 0x00, 0x01, 0x05];

	// Transfer command to fill TX Buffer
	bcm2835_spi_transfern(&buffer, 5);

	// Ready to Send TX Buffer
	bcm2835_spi_transfer(MCP_RTS_ALL);

	// Try to read RX Buffer
	int r = has_message();
	
	return 0;
}
