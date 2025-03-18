# Pixel sim

Python codes to simulate color for LED strips

```bash
git clone https://github.com/botamochi6277/pixel-sim.git
cd pixel-sim
poetry install
```

## Examples

## Colormaps

### Cyclic colormap

$$
\begin{align*}
y(t) &=  \sum_{i=0}^{n} \left( a_i \cos(2\pi f_i t) - b_i \sin(2\pi f_i t) \right) \\
&=  \sum_{i=0}^{n} \left( \sqrt{ a_i^2 + b_i^2} \sin(2\pi f_i t + \theta_i )  \right) \\
\theta_i &= \mathrm{atan2} (a_i,-b_i)
\end{align*}
$$

[colormap examples](./cyclic_colormaps.md)

encoding demo:

```bash
poetry run python scripts/encode_cyclic_colormap.py twilight
```

### Diverging colormap

$$
r = \sum_{i=0}^{n} a_i t^i
$$

[colormap examples](./diverging_colormaps.md)

## Shapes

$t$ is progress rate and $p$ is normalized position

$$
y = f(t,p)
$$

[shape examples](./shapes.md)
