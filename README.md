# Pixel sim

Python codes to simulate color for LED strips

```bash
git clone
cd
poetry install
```

## Examples

```console
# Instagram https://uigradients.com/#Instagram
python scripts/create_colormap.py #833ab4 #fd1d1d #fcb045 --is_encode=true --name Instagram --save_fig=true
```

```console
python scripts/create_colormap.py #FEAC5E #C779D0 #4bc0c8  --is_encode=true --name Atlas --save_fig=true
```

```console
python scripts/create_colormap.py #fd54E9  #FDFC47 #24FE41 --is_encode=true --name martini --save_fig=true
```

```console
python scripts/create_colormap.py #C6FFDD #FBD786 #f7797d --is_encode=true --name megatron
```

## Colormaps

### Cyclic colormap

$$
\begin{align*}
y(t) &=  \sum_{i=0}^{n} \left( a_i \cos(2\pi f_i t) - b_i \sin(2\pi f_i t) \right) \\
&=  \sum_{i=0}^{n} \left( \sqrt{ a_i^2 + b_i^2} \sin(2\pi f_i t + \theta_i )  \right) \\
\theta_i &= \mathrm{atan2} (a_i,-b_i)
\end{align*}
$$

[examples](./cyclic_colormaps.md)

### Sequential colormap

$$
r = \sum_{i=0}^{n} a_i x^i
$$

## Shapes
