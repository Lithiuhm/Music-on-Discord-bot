<p align="center">
  <img src="https://media.tenor.com/3mBWfM4MP84AAAAC/discord-discord-ping.gif" alt="animated"/>
</p>

---

# Music on Discord bot (Python)

Seguro quieres tener un bot o que tu bot de Discord te proporcione toda la música que quiras tener, tanto de Youtube como de Spotify. Bueno pues aquí te traigo lo que justo necesitabas, con este código podrás hacer esto!

Obviamente tenemos que tener creado previamente nuestro bot sino puedes verte cualquier video, también te dejo el código de lo mínimo que tiene que tener un bot de discord para funcionar. sin más que decir empezamos.

---
# Instalación

## Discord

Primero que todo debes tener la librería de Discord.py instalada, para ello ejecutamos este comando en una consola.

### Pip
```bash
pip install discord
```
### Windows
```bash
py -3 -m pip install -U discord.py
```
### Linux
```bash
python3.10 -m pip install -U Wavelink
```

## WaveLink

Ahora bien, vamos a usar una librería WaveLink que es un wrapper de Lavalink, robusto y potente para Discord.py. Wavelink presenta una API totalmente asíncrona que es intuitiva y fácil de usar con soporte integrado de Spotify y equilibrio de grupo de nodos.

Usamos el siguiente comando para instalarlo:

### Pip
```bash
pip install wavelink
```
### Windows
```bash
py -3.10 -m pip install -U Wavelink
```
### Linux
```bash
python3.10 -m pip install -U Wavelink
```

# Configuración

Ahora necesitamos una access key de Spotify para poder obtener música de este servicio, para ello entramos a la web developers de Spotify y creamos una app.

### Spotify developers Key
```bash
https://developer.spotify.com/dashboard
```
Una vez creada la app veremos algo así

<img src="/images/img1.png"/>

Debemos poner estos dos datos en las siguiente partes del código

<img src="/images/img2.png"/>

### Wavelink Server

Ahora debemos elegir un servidor de Wavelink para ello vamos a hacer uso de una página donde hay personas que hostean el servidor Lavalink. Usaremos el servicio encriptado (SSL).

```bash
https://lavalink-list.darrennathanael.com/SSL/lavalink-with-ssl/
```
Elegimos un servidor de los mostrados y lo siguiente es introducirlo en el código

<img src="/images/img3.png"/>

### Token del bot

Si ya tienes un bot creado y configurado puedes saltarte este paso, sino puedes ir a la página de Discord developer portal y crear una aplicación, en la parte de bot copias el token 

<img src="/images/img4.png"/>

Y lo pegan al final del código:

<img src="/images/img5.png"/>

# Finalización

Para comprobar que funciona, los comandos son:
```bash
-play [Lo que quieras] | -pause | -resume | -skip 
```

**¡Abierto a cualquier ayuda y commentario!**

---

# Documentación

### Discord python
```bash
https://discordpy.readthedocs.io/en/stable/
```

### Wavelink
```bash
https://wavelink.readthedocs.io/en/latest/index.html
```

### Lavalink List Github
```bash
https://github.com/DarrenOfficial/lavalink-list
```

---

# Descargo de responsabilidad

No me hago cargo del mal uso que se le de a esta aplicación, todo esto es con fines educativos e informativos, gracias y a disfrutarlo!

---

## Autor

- [@Lithiuhm](https://www.github.com/Lithiuhm)

