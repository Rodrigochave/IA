#include <stdio.h>
#include <stdlib.h>

int comparar(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int n, i;
    printf("Numero de personas: ");
    scanf("%d", &n);

    int tiempos[n];
    printf("Ingresa los tiempos de cruce:\n");
    for(i = 0; i < n; i++)
        scanf("%d", &tiempos[i]);

    // Ordenar tiempos de menor a mayor
    qsort(tiempos, n, sizeof(int), comparar);

    int total = 0;
    int izq = n - 1;
    int primero = 1; // para manejar formato de "; "

    while(izq >= 3) {
        int a = tiempos[0];     // más rápido
        int b = tiempos[1];     // segundo más rápido
        int x = tiempos[izq-1]; // penúltimo más lento
        int y = tiempos[izq];   // más lento

        int opcion1 = 2*b + a + y;
        int opcion2 = 2*a + x + y;

        if(opcion1 <= opcion2) {
            if(!primero) printf("; ");
            printf("(%d,%d) -> %d; %d <- %d; (%d,%d) -> %d; %d <- %d", 
                   a, b, b, a, a, x, y, y, b, b);
            total += opcion1;
            primero = 0;
        } else {
            if(!primero) printf("; ");
            printf("(%d,%d) -> %d; %d <- %d; (%d,%d) -> %d; %d <- %d",
                   a, y, y, a, a, a, x, x, a, a);
            total += opcion2;
            primero = 0;
        }
        izq -= 2;
    }

    if(izq == 2) {
        if(!primero) printf("; ");
        printf("(%d,%d) -> %d; %d <- %d; (%d,%d) -> %d",
               tiempos[0], tiempos[1], tiempos[1],
               tiempos[0], tiempos[0],
               tiempos[0], tiempos[2], tiempos[2]);
        total += tiempos[0] + tiempos[1] + tiempos[2];
    } else if(izq == 1) {
        if(!primero) printf("; ");
        printf("(%d,%d) -> %d", tiempos[0], tiempos[1], tiempos[1]);
        total += tiempos[1];
    } else if(izq == 0) {
        if(!primero) printf("; ");
        printf("(%d) -> %d", tiempos[0], tiempos[0]);
        total += tiempos[0];
    }

    printf(". Total = %d\n", total);

    return 0;
}
