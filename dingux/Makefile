TARGET = sdlpal.dge

HOST = mipsel-linux-uclibc-

SOURCES = . ./adplug
CFILES = $(foreach dir, $(SOURCES), $(wildcard $(dir)/*.c))
CPPFILES = $(foreach dir, $(SOURCES), $(wildcard $(dir)/*.cpp))
OFILES = $(CFILES:.c=.o) $(CPPFILES:.cpp=.o)

CFLAGS = -g -Wall -O2 `sdl-config --cflags` -DDINGOO -DPAL_CLASSIC -DPAL_HAS_PLATFORM_SPECIFIC_UTILS -I.
CXXFLAGS = $(CFLAGS)
LDFLAGS = `sdl-config --libs`

$(TARGET): $(OFILES)
	$(HOST)g++ $(OFILES) -o $@ $(LDFLAGS)

%.o: %.c
	$(HOST)gcc $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(HOST)g++ $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OFILES)
