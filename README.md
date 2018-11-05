# wagtail2
## My own wagtail 2 site.

Based on [bakerydemo](https://github.com/wagtail/bakerydemo) for wagtail 2. I've included some mods over [Puput Blog](https://github.com/APSL/puput).

#### It has also some experiments like:
* Icon picker on admin interface (icons available in menubar)
* Recaptcha for forms.
* twitter panel on pages.
* Disqus comments for the blog
* TinyMCE editor (+ some WhitelistRules for bootstrap 4)
* Multilingual layer based on [wagtail modeltranslation](https://github.com/infoportugal/wagtail-modeltranslation).
with own tab interface to manage languages (works on snippets, inline panels, ...)

Template is based on [Bootstrap 4](https://getbootstrap.com) but it has some adjustments like [Creative Tim](https://www.creative-tim.com) free bootstrap themes. SCSS is available.

* Next steps:
	1. Docker functionality.
	2. Go to Production, now my site is down (now works with docker)
	3. Enable API.

### Example .env file
```
DATABASE_URL=postgres://user:password@host-or-dockerservice:5432/databasename
DATABASE_URL_PROD=postgres://user:password@host-or-dockerservice/databasename
DJANGO_SECRET_KEY=write your own secret key here
DJANGO_LOG_LEVEL=INFO
RECAPTCHA_PUBLIC_KEY=xxxxxxx
RECAPTCHA_PRIVATE_KEY=xxxxxx
DJANGO_ALLOWED_HOSTS=separed;hosts
```
### Services: docker-compose.yml (persistent db)
```
version: '2'
services:
  postgresdb:
    image: postgres:latest
    container_name: serv_postgresdb
    restart: always
    volumes:
      - ./databases/postgres/data:/var/lib/postgresql/data
    ports:
      - 5432:5432
    environment:
      - POSTGRES_USER=username
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=postgres
  adminer:
    image: adminer
    container_name: serv_adminer
    restart: always
    ports:
      - 8091:8080
networks:
  default:
    external:
      name: my_network
``  
      
Enjoy ;)