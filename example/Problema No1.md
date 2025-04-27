---
title: Tarea No2 Problema 1
tags:
  - fea
  - beam
  - hinge
summary: Determinar la matriz de rigidez de una viga con articulaciones
---
# Descripcion
El elemento tipo viga-columna mostrado en la figura esta rotulado en el nodo 1 (no puede transmitir momento de flexión). Por lo tanto, el elemento tiene solo 3 grados de libertad, tal como se muestra. Derivar la matriz de rigidez para este elemento resolviendo directamente la ecuación diferencial y aplicando las condiciones de borde adecuadas.

![[attachments/Problema No1 2025-03-30 17.08.57.excalidraw.png|300]]
%%[[attachments/Problema No1 2025-03-30 17.08.57.excalidraw.md|🖋 Edit in Excalidraw]]%%

# Desarrollo
## Solución de la ODE
Considerando solo la parte homogenea de la ecuacion diferencial, tenemos,
$$
EI \frac
{d^4u}
{dx^4}=0
$$
Lo cual resulta en una ecuacion diferencial homogenea de cuarto grado, misma que puede ser resuleta a traves de coeficientes.

La forma fuerte de la ecuación diferencia es,
$$
u(x)=\frac
{C_1}
{6} x^3+
\frac
{C_2}
{2} x^2+
C_3x+C_4
$$
La solucion de la ODE requiere de $4$ condiciones de borde.
$$
\begin{aligned}
u(0) &= u_1 \\
u''(0) &= 0 \\
u(L) &= u_2 \\
u'(L) &= u_3
\end{aligned}
$$
Lo que resulta en,
$$
\begin{aligned}
C_1 &= \frac
{3}
{L^3} \left[
u_3 L -(u_2-u_1)
\right] \\
C_2 &= 0 \\
C_3 &=\frac
{3}
{2L}(u_2-u_1) \frac
{1}
{2} u_3 \\
C_4 &= u_1 \\

\end{aligned}
$$
Reemplazando en la ecuacion,
$$
u(x)=
\frac
{x^3}
{2L^3}
\left[
(u_3L-(u_2-u_1))
\right]
+x
\left(
\frac
{3}
{2L}(u_2-u_1)-
\frac
{1}
{2}u_3
\right)
+u_1
$$
Agrupando la ecuacion en terminos de los desplazamientos, tenemos:
$$
u(x)=
\left(
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x
\right) u_1+
\left(
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L} x
\right) u_2 +
\left(
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x
\right)u_3
$$
Siendo las funciones de forma del elemento,
$$
[N(x)]=
\begin{bmatrix}
\left(
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x
\right) &
\left(
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L} x
\right) &
\left(
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x
\right)
\end{bmatrix}
$$

### Calculo de los Coeficientes de Rigidez
Buscamos determinar los coeficientes de rigidez del sistema local, donde,
$$
[K_L]=
\begin{bmatrix}
K_{11} & K_{12} & K_{13} \\
K_{21} & K_{22} & K_{23} \\
K_{31} & K_{32} & K_{33} \\
\end{bmatrix}
$$

Nota: Donde la rigidez $k_{ij}$ corresponde a la fuerza requerida en el nudo $i$ para obtener un desplzamiento unitario en el nudo $j$ cuando todos los demas grados de libertad se encuentran restringidos. Y de acuerdo con el teorema de reciprocidad de Maxwell y Betti sabemos que $k_{ij}=k_{}$ji

#### Desplazamiento Unitario $u_1$
Por lo tanto los desplazamientos impuestos en la viga son:
$$
\begin{aligned}
u_1 &= 1 \\
u_2 &= 0 \\
u_3 &= 0
\end{aligned}
$$
Lo que resulta en,
$$
\begin{aligned}
u(x) &=
\left(
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x
\right) u_1+
\left(
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L} x
\right) u_2 +
\left(
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x
\right)u_3 \\
u(x) &= 
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x \\
u'(x) &= \frac
{-3}
{2L^3}x^2+\frac
{3}
{2L}

\end{aligned} 

$$
El momento a lo largo de la viga corresponde a,
$$
\begin{aligned}
M(x) &= -EI u''(x) \\
M(x) &= EI \left(
\frac
{3}
{L^3}x
\right)
\end{aligned}
$$
Y el cortante,
$$
\begin{aligned}
V(x) &= -EI u'''(x) \\
V(x) &= \frac
{3EI}
{L^3}
\end{aligned}
$$
Esto hace que los coeficientes de rigidez para este desplazamiento sean,
$$
K_{11}=\frac
{3EI}
{L^3}
$$
$$
K_{21}=\frac
{-3EI}
{L^3}
$$
$$
K_{31}=\frac
{3EI}
{L^2}
$$

#### Desplazamiento Unitario $u_2$
Por lo tanto los desplazamientos impuestos en la viga son:
$$
\begin{aligned}
u_1 &= 0 \\
u_2 &= 1 \\
u_3 &= 0
\end{aligned}
$$
Lo que resulta en,
$$
\begin{aligned}
u(x) &=
\left(
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x
\right) u_1+
\left(
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L} x
\right) u_2 +
\left(
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x
\right)u_3 \\
u(x) &= 
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L}x \\
u'(x) &= \frac
{3}
{2L^3}x^2-\frac
{3}
{2L}

\end{aligned} 

$$
El momento a lo largo de la viga corresponde a,
$$
\begin{aligned}
M(x) &= -EI u''(x) \\
M(x) &= EI \left(
\frac
{-3}
{L^3}x
\right)
\end{aligned}
$$
Y el cortante,
$$
\begin{aligned}
V(x) &= -EI u'''(x) \\
V(x) &= \frac
{-3EI}
{L^3}
\end{aligned}
$$
Esto hace que los coeficientes de rigidez para este desplazamiento sean,
$$
K_{21}=\frac
{-3EI}
{L^3}
$$
$$
K_{21}=\frac
{3EI}
{L^3}
$$
$$
K_{32}=\frac
{-3EI}
{L^2}
$$

#### Desplazamiento Unitario $u_3$
Por lo tanto los desplazamientos impuestos en la viga son:
$$
\begin{aligned}
u_1 &= 0 \\
u_2 &= 0 \\
u_3 &= 1
\end{aligned}
$$
Lo que resulta en,
$$
\begin{aligned}
u(x) &=
\left(
\frac
{-1}
{2L^3}x^3+\frac
{3}
{2L}x
\right) u_1+
\left(
\frac
{1}
{2L^3}x^3-\frac
{3}
{2L} x
\right) u_2 +
\left(
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x
\right)u_3 \\
u(x) &= 
\frac
{1}
{2L^2}x^3-\frac
{1}
{2}x \\
u'(x) &= \frac
{3}
{2L^2}x^2-\frac
{1}
{2}
\end{aligned} 
$$
El momento a lo largo de la viga corresponde a,
$$
\begin{aligned}
M(x) &= -EI u''(x) \\
M(x) &= EI \left(
\frac
{3}
{L^2}x
\right)
\end{aligned}
$$
Y el cortante,
$$
\begin{aligned}
V(x) &= -EI u'''(x) \\
V(x) &= \frac
{3EI}
{L^2}
\end{aligned}
$$
Esto hace que los coeficientes de rigidez para este desplazamiento sean,
$$
K_{31}=\frac
{3EI}
{L^3}
$$
$$
K_{32}=\frac
{-3EI}
{L^3}
$$
$$
K_{33}=\frac
{3EI}
{L}
$$

#### Matriz de Rigidez Barra Articulada
Esto resulta en la siguiente matriz de rigidez para la barra articulada,

$$
[K_L]=
\begin{bmatrix}
3EI/L^3 & -3EI/L^3 & 3EI/L^2 \\
-3EI/L^3 & 3EI/L^3 &-3EI/L^2 \\
3EI/L^2 & -3EI/L^2 & 3EI/l \\
\end{bmatrix}
$$

![[attachments/RigidezArticulada.png|600]]
%%[[attachments/RigidezArticulada|🖋 Edit in Excalidraw]]%%

## Solución Matricial
Las posibles configuraciones de la viga son,

![[attatchments/Bernoulli-Euler2DBeamSystems.png]]

%%[[Bernoulli-Euler 2D Beam Systems | 2D Beam System]]%%

En este caso se va a considerar a la viga axialmente rigida, por lo tanto se desprecia el grado de libertad $u_1$,

Las matrices de interpolacion para una viga de Bernoulli-Euler en su configuracion basica esta dada por,

$$
N(x)=
\begin{bmatrix}
N_1(x) &
N_2(x)
\end{bmatrix}
\begin{bmatrix}
u_1 \\
u_2
\end{bmatrix}
$$
$$
[N(x)]=
\begin{bmatrix}
\left(
- \frac{1}{L^2}x^3+\frac{2}{L}x^2-x
\right)
 & 
 \left(
- \frac{1}{L^2}x^3+\frac{1}{L}x^2
\right)

\end{bmatrix}
$$

Lo que resulta en la siguiente matriz de rigidez basica,
$$
[K_b]=
\begin{bmatrix}
 4EI/L & 2EI/L \\
 2EI/L & 4EI/L
\end{bmatrix}
$$

Las Matrices de transformacion son,
$$
[T_{bl}] = 
\begin{bmatrix}
1/L & 1 & -1/L & 0 \\
1/L & 0 & -1/L & 1
\end{bmatrix}
$$
$$
[T_{lg}]=
\left[
\begin{array}
\cos\theta & \sin\theta  & 0 & 0   \\
-\sin\theta & \cos\theta & 0 & 0  \\
0 & 0 & \cos\theta & \sin\theta  \\
0 & 0 & -\sin\theta & \cos\theta   \\
\end{array}
\right]
$$

### Condensación Estatica
Podemos encontrar la matriz de rigidez del elemento articulado a partir del procedimiento de condensación estático de la matriz de rigidez.
$$
\begin{aligned}\
[F_b] &= [K_b] [u_b] \\

\end{aligned}
$$
Donde, en la barra articulada van a existir elementos del vector de fuerza iguales a $0$, lo que resulta en,
$$
\begin{bmatrix}
F_b^{C} \\
0
\end{bmatrix} = 
\begin{bmatrix}
K_b^{CC} & K_b^{C0} \\
K_b^{0C} & K_b^{00}
\end{bmatrix}
\begin{bmatrix}
u_b^{C} \\
u_b^{0}
\end{bmatrix}
$$
La expansion de las matrices resulta en,
$$
[F_b^{C}]=[K_b^{CC}][u_b^{C}]+[K_b^{C0}][u_b^{0}]
$$
$$
0=[K_b^{0C}][u_b^{C}]+[K_b^{C0}][u_b^{0}]
$$
Donde los desplazamientos correspondientes a los grados de libertad donde las fuerzas son $0$ son,
$$
[u_b^{0}]=-[K_b^{C0}]^{-1}[u_b^C][K_b^{0C}]
$$
Reemplazando esto en la primera ecuación,
$$
[F_b^{C}]=[K_b^{CC}][u_b^{C}]-[K_b^{C0}][K_b^{C0}]^{-1}[u_b^C][K_b^{0C}]
$$
$$
[F_b^{C}]=
\left(
\underbrace{
[K_b^{CC}]-[K_b^{C0}][K_b^{C0}]^{-1}[K_b^{0C}]
}_{\text{RIGIDEZ CONDENSADA}}
\right)
[u_b^C]
$$
Lo que resulta en que la matriz de rigidez del elemento con la articulacion es:
$$
K_{b}^{\text{ARTICULADA}}=[K_b^{CC}]-[K_b^{C0}][K_b^{C0}]^{-1}[K_b^{0C}]
$$
