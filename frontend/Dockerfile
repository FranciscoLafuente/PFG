FROM node:12.2.0-alpine

ENV http_proxy http://flafuente:Yaesnavidad10@10.74.255.120:8080/
ENV https_proxy http://flafuente:Yaesnavidad10@10.74.255.120:8080/

# instalar un simple servidor http para servir nuestro contenido estático
RUN npm install -g http-server

# hacer la carpeta 'app' el directorio de trabajo actual
WORKDIR /app

# copiar 'package.json' y 'package-lock.json' (si están disponibles)
COPY package*.json ./

# instalar dependencias del proyecto
RUN npm install

# copiar los archivos y carpetas del proyecto al directorio de trabajo actual (es decir, la carpeta 'app')
COPY . .

# construir aplicación para producción minificada
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]
