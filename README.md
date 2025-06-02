# Manual: Despliegue de una API y su BBDD (Postgres) en EC2 (AWS)

## Requisitos previos

- Cuenta de AWS
- Par de claves para acceder por SSH
- Código de tu API (por ejemplo FastAPI) en GitHub o comprimido
- Conocimiento básico de Linux/terminal

## Paso 1: Crear una instancia EC2

1. Accede a AWS EC2
2. Clic en **Launch Instance**
3. Elige una imagen:  
   Recomendado: Ubuntu Server 22.04 LTS
4. Tipo de instancia:  
   Recomendado: t2.micro (gratis en capa gratuita)
5. Par de claves:  
   Selecciona uno existente o crea uno nuevo
6. Configurar el grupo de seguridad:  
   Permitir puertos 22 (SSH) y 8000 (tu API) o 80/443 si usarás Nginx (Para el FrontEnd)
7. Lanzar la instancia

![image](https://github.com/user-attachments/assets/71d3263c-17a4-45c0-b9de-53169dafb749)

## Paso 1.1: Reservar y asociar una Elastic IP para IP pública fija

Para evitar que la IP pública de tu instancia cambie al reiniciar o detener la instancia, crea y asigna una Elastic IP siguiendo estos pasos:

1. En la consola de AWS, ve a **EC2 → Elastic IPs** (en la sección *Network & Security*).

2. Haz clic en **Allocate Elastic IP address** y confirma la asignación.

3. Selecciona la Elastic IP recién creada, haz clic en **Actions → Associate Elastic IP address**.

4. En el campo **Resource type**, selecciona **Instance**.

5. Elige tu instancia EC2 creada previamente.

6. En **Private IP address**, selecciona la IP privada de la instancia (normalmente la única disponible).

7. Haz clic en **Associate**.

Ahora tu instancia tendrá una IP pública fija que puedes usar para conectarte y acceder a tu API.

![image](https://github.com/user-attachments/assets/61e903f5-4dae-40ec-a77f-ebde357c0921)


## Paso 2: Conectarse a la instancia

Ejemplo
```bash
ssh -i <nombre del archivo clave> <DNS público proporcionado por AMW>
ssh -i "Stockify.pem" ubuntu@ec2-107-22-235-180.compute-1.amazonaws.com
````
![image](https://github.com/user-attachments/assets/85fae009-25d8-4a96-a938-7a43e3e4e346)

![image](https://github.com/user-attachments/assets/dceb4d3a-7957-450a-8b40-c55f9a9d85df)


## Paso 3: Creamos una carpeta y clonamos tu API desde GitHub
```bash
git clone https://github.com/usuario/mi-api.git
cd mi-api
```

## Paso 3.1: Crear archivo .env con variables de entorno
```bash
# Variables para PostgreSQL
POSTGRES_DB=stockify
POSTGRES_USER=stockify_user
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_SERVER=db
POSTGRES_PORT=5432


# Variables para la API y servicios externos
JWT_SECRET_KEY=tu_clave_secreta_jwt

STRIPE_SECRET_KEY=tu_clave_secreta_stripe
STRIPE_SECRET_WEBHOOK_KEY=tu_clave_webhook_stripe

```

## Paso 4: Construimos y levantamos contenedor de Docker
```bash
docker-compose up -d --build
```


## Paso 5: Con alembic generamos las tablas de la BBDD
```bash
docker exec -it stockify_api alembic upgrade head
```


## Sugerencia adicional: Para verificar que los contenedores estén funcionando
```bash
docker exec -it stockify_api alembic upgrade head
```

## Para acceder desde el navegador:
```bash
Accede desde navegador: http://<IP_ELÁSTICA>:8000
```

Ejemplo de URL pública
```bash
http://107.22.235.180:8000/docs  ← Swagger UI
```
![image](https://github.com/user-attachments/assets/eb7ca1b8-5ebe-41ba-8700-93422f66c050)




