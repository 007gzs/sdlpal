TARGET = boot

HOST = powerpc-eabi-

SOURCES = . .. ../adplug
CFILES = $(foreach dir, $(SOURCES), $(wildcard $(dir)/*.c)) 
CPPFILES = $(foreach dir, $(SOURCES), $(wildcard $(dir)/*.cpp))
OFILES = $(CFILES:.c=.o) $(CPPFILES:.cpp=.o)

CFLAGS = -g -Wall -O2 `sdl-config --cflags` -DGEKKO -DPAL_HAS_PLATFORM_SPECIFIC_UTILS -I.
CXXFLAGS = $(CFLAGS)
LDFLAGS = `sdl-config --libs` -DGEKKO -mrvl

$(TARGET): $(OFILES)
	$(HOST)g++ $(OFILES) -o $@.elf $(LDFLAGS)
	elf2dol $(TARGET).elf $(TARGET).dol

%.o: %.c
	$(HOST)gcc $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(HOST)g++ $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET).elf $(TARGET).dol $(OFILES)
