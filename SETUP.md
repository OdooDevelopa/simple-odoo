<!-- ## Debug Odoo 10 by using Pycharm on Windows
*Successed on Windows 10 (64-bit)*
### Requirements:
- Git
- Pycharm IDE
- Python 2.7
- Microsoft Visual C++ Compiler for Python 2.7
- Node.js
- PostgreSQL 9.6

### Let's begin
By following this step.
1. **Clone Odoo 10 repository.**
> On Command Prompt.
```bash
$ cd <yourpath>
$ git clone -b 10.0 https://github.com/odoo/odoo.git
```
2. **Create user on PostgreSQL.**
> By using this query.
```sql
CREATE USER odoo10 WITH encrypted password 'odoo10';
ALTER USER odoo10 WITH SUPERUSER;
```
3. **Install Python requirements libs.**
> In Odoo dir you've cloned. Open and edit `requirements.txt` file.
 - Remove line contain `psycopg2` , `python-ldap` , `gevent` , `psutil`.
 - Add `pypiwin32` and save it.
 - On Command Prompt
```bash
$ cd <yourpath>/odoo
$ pip install -r requirements.txt
```
4. **Install less.js**
>On Command Prompt
```bash
$ npm install -g less
```
5. **Run Pycharm and open your Odoo source code directory**
> Edit Configuration. Click on `+` and choose Python
```
Name: Odoo 10 Debug
Check: Single instance only
Script: go to your odoo source code and choose file odoo-bin
Script parameters: --config <path-to-your-config-file>/my.conf
```
For example here is my config file `my.conf`
```config
[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo10
db_password = odoo10
; addons_path = C:\Users\your-name\AppData\Local\OpenERP S.A.\Odoo\addons\10.0, <your-odoo-path>\odoo\addons, <your-odoo-path>\addons, <your-addons-path>```

**Now Odoo is ready for runing at `localhost:8069`**

Done! Thank to this post [How configure Pycharm for debug Odoo10 on Windows](https://www.odoo.com/fr_FR/forum/aide-1/question/how-configure-pycharm-for-debug-odoo10-on-windows-119119) -->

```bash
$ @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

```bash
$ choco install -y git.install python2 vcpython27 pycharm-community nodejs.install postgresql pgadmin3
```

```bash
$ npm install -g less
```

```bash
$ psql -U postgres
> Postgres1234
```

```bash
$ CREATE USER odoo10 WITH encrypted password 'odoo10'; ALTER USER odoo10 WITH SUPERUSER;
```

-- 32 bit

```bash
$ pip install git+https://github.com/nwcell/psycopg2-windows.git@win32-py32#egg=psycopg2
```

or http://www.stickpeople.com/projects/python/win-psycopg/2.6.2/psycopg2-2.6.2.win32-py2.7-pg9.5.3-release.exe

-- 64 bit

```bash
$ pip install git+https://github.com/nwcell/psycopg2-windows.git@win64-py27#egg=psycopg2
```

or http://www.stickpeople.com/projects/python/win-psycopg/2.6.2/psycopg2-2.6.2.win-amd64-py2.7-pg9.5.3-release.exe


```bash
$ pip install Babel==2.3.4 decorator==4.0.10 docutils==0.12 ebaysdk==2.1.4 feedparser==5.2.1 greenlet==0.4.10 jcconv==0.2.3 Jinja2==2.8 lxml==3.5.0 Mako==1.0.4 MarkupSafe==0.23 mock==2.0.0 ofxparse==0.16 passlib==1.6.5 Pillow==3.4.1 psycogreen==1.0 pydot==1.2.3 pyparsing==2.1.10 pyPdf==1.13 pyserial==3.1.1 Python-Chart==1.39 python-dateutil==2.5.3 python-openid==2.2.5 pytz==2016.7 pyusb==1.0.0 PyYAML==3.12 qrcode==5.3 reportlab==3.3.0 requests==2.11.1 six==1.10.0 suds-jurko==0.6 vatnumber==1.2 vobject==0.9.3 Werkzeug==0.11.11 wsgiref==0.1.2 XlsxWriter==0.9.3 xlwt==1.1.2 xlrd==1.0.0 pypiwin32
```

```bash
$ git clone --depth=1 -b 10.0 https://github.com/odoo/odoo.git
```

```bash
$ start notepad ./odoo/debian/odoo.conf
```
db_host = localhost
db_port = 5432
db_user = odoo10
db_password = odoo10

-- Pycharm community
Paramater: -c ./debian/odoo.conf
