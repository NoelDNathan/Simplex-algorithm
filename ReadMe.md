# Estructura del projecto
Tenemos tres carpetas:

    - /Inputs: Es la carpeta donde se guardan los archivos que contienen los parámetros     
    iniciales que se le pasarán al simplex.

    - /Outputs: Es la carpeta donde se guarda el resultado que se ha obtenido de ejecutando
    el simplex.

    - /Code: Es la carpeta donde se encuentra el código del simplex.


# Ejecutar el simplex
Para ejecutar el simplex se deben seguir los siguientes pasos:

- En la carpeta /Inputs se debe añadir un archivo que contenga la matriz A que corresponda a los valores variables de las restricciones, el vector b que corresponda a los valores constantes de las restricciones y el vector c que corresponga a la función objetivo.
Hay archivos de ejemplo de como debe ser el formato.

- Luego, en la carpeta code, en el archivo `Execute.py`, se debe cambiar el valor de la variable `problem_name` por el nombre el archivo input que contenga la función objetivo y las restricciones que se quieran minimizar. Por defecto, la extensión de estos archivos es `.inp`, si se utiliza otra, se debe modificar la variable `ext` con el valor que se quiera como extensión.

- Por último, el código se puede ejecutar con el siguiente comando: 
```
python ./code/Execute.py
``` 

- El resultado de la ejecución se puede encontrar en la carpeta /output, el nombre que tendrá el archivo con el resultado será igual al nombre del archivo pasado como input pero con la extension `.out`.


# Analizar el resultado
- En cada iteración se indica el número de la iteración, la variable que ha entrado `q`, la variable que ha salido `p`, la `theta` y la `z`.

- Si se encuentra el óptimo, se muestra que `vb`. `xb`, `z` y `r` se han obtenido.
- Si no encuentra el óptimo, puede mostrar `unbounded problem` (problema no acotado) o `Not Feasible Problem`.

**Importante:** Los índices en el vector `vb` empiezan desde el 0.
**Importante:** En la fase 1, cuando encuentra el óptimo, el valor de la `z` no es exactamente cero por como los ordenadores computan los decimales. Su valor suele encontrarse sobre 0 +- 5 * 10^-14.