#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define PWM_CTRL_ADDR    0xC40000D0
#define PWM_CLOCK_ADDR   0xC4080108
#define PWM_PERIOD_ADDR  0xC408002C
#define PWM_CTRL2_ADDR   0xC4080030
#define PWM_DUTY_ADDR    0xC4080034

void write_pwm(unsigned int addr, unsigned int value) {
    int fd = open("/dev/mem", O_RDWR | O_SYNC);
    if (fd < 0) {
        fprintf(stderr, "Failed to open /dev/mem\n");
        exit(1);
    }

    void *map_base = mmap(0, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, addr & ~(4096-1));
    if (map_base == (void *) -1) {
        fprintf(stderr, "Failed to map memory\n");
        close(fd);
        exit(1);
    }

    volatile unsigned int *reg = (volatile unsigned int *)((char *)map_base + (addr & (4096-1)));
    *reg = value;

    munmap(map_base, 4096);
    close(fd);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <address> <value>\n", argv[0]);
        return 1;
    }

    unsigned int addr = strtoul(argv[1], NULL, 0);
    unsigned int value = strtoul(argv[2], NULL, 0);

    // Validate addresses
    switch(addr) {
        case PWM_CTRL_ADDR:
        case PWM_CLOCK_ADDR:
        case PWM_PERIOD_ADDR:
        case PWM_CTRL2_ADDR:
        case PWM_DUTY_ADDR:
            write_pwm(addr, value);
            printf("OK\n");
            break;
        default:
            fprintf(stderr, "Invalid PWM address\n");
            return 1;
    }

    return 0;
}
