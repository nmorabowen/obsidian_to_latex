---
title: "Math Expressions in Obsidian"
tags: [math, test, example]
---

# Introduction to Math in Obsidian

This document demonstrates various mathematical expressions that should be properly converted to LaTeX.

## Inline Math

Inline math expressions like $E = mc^2$ or $\alpha + \beta = \gamma$ should be preserved in their original form.

## Display Math

Display math blocks should also be preserved:

$$
\begin{aligned}
\frac{\partial u}{\partial t} &= h^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} + \frac{\partial^2 u}{\partial z^2} \right) \\
&= h^2 \nabla^2 u
\end{aligned}
$$

## Matrix Example

Matrices should be properly handled:

$$
A = \begin{pmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{pmatrix}
$$

## Equations with References

$$
\begin{equation}
E = mc^2
\end{equation}
$$

This famous equation is Einstein's formula for mass-energy equivalence.

## Images with Obsidian Format

![[sample_image.png|300]]

The image above shows a graph of the function $f(x) = x^2$.

## List with Math

Here's a list of important equations:

- The quadratic formula: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
- Euler's identity: $e^{i\pi} + 1 = 0$
- Pythagorean theorem: $a^2 + b^2 = c^2$

## Internal Links

For more information on calculus, see [[Calculus Notes|Advanced Calculus]].

## Code Block with Math Syntax

```python
def calculate_energy(mass):
    # E = mc^2
    c = 299792458  # speed of light in m/s
    return mass * (c ** 2)
```

## Comments that Should be Removed

This text is visible, but %%this comment should be removed%% in the LaTeX output.

## Nested Lists

- Main item 1
  - Subitem 1.1 with math $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$
  - Subitem 1.2
- Main item 2
  - Subitem 2.1
  - Subitem 2.2

## Conclusion

This should be sufficient to test the conversion capabilities of our tool.
