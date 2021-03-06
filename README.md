# Ansible Deploy Template
This Ansible playbook deploys a Django website (with nginx and Gunicorn) to a cloud server.

## Using the playbook

**BEFORE RUNNING THE PLAYBOOK**
* Install Ansible
     * **NOTE** Ansible isn't currently support on Windows. You can get around this by installing a Ubuntu terminal through WSL. The Ubuntu website has a [walkthrough](https://ubuntu.com/tutorials/ubuntu-on-windows) for installation.
* Install django-environ
* Ensure your Django settings file is set up for secure running on a server
  * DEBUG, SECRET_KEY, and HOSTS should be got from .env file
  * [django-environ docs](https://django-environ.readthedocs.io/en/latest/)
* Update `site.yml` with 
  * PYTHON_VERSION: Change from python3.8 if required 
  * WSGI_DIRECTORY: The directory name where the for the project wsgi.py file
  * REPO_URL: The URL for the git repo
  * REPO_BRANCH: The branch name of the git repo to be cloned
* Update `production` and `staging` files with your:
  * Production and staging servers
  * For both servers also specify the ssh username that will be used to log in to your server
* **If using different SSL cert**
  * Update `nginx.conf.j2` replacing location/names of SSL cert and key if necessary


**RUNNING THE PLAYBOOK**
  * Navigate to the playbook folder in the Ubuntu terminal
  * Run the playbook using `ansible-playbook site.yml -kK -i staging`
    * Change `staging` to `production` to deploy to production server
    * -kK asks for your ssh password & your sudo password when you run the playbook.
    * `ansible.cfg` sets the default server to staging if `-i <servers>` is not included

## What the playbook does
Basic Ansible playbook to deploy a Django website (with nginx and Gunicorn) using Ansible

In the process of working through Test-Driven-Development with Python, I was unable to successfully automate the deployment using Fabric as was suggested in the [book](https://www.obeythetestinggoat.com/book/chapter_automate_deployment_with_fabric.html). Ansible was suggested as an alternative in the appendices. 

This playbook does a lot of the steps outlined in the section of [chapter 10: Thinking about automation](https://www.obeythetestinggoat.com/book/chapter_making_deployment_production_ready.html#_thinking_about_automating). 

**Provisioning**
* Adds the deadsnakes repository 
* Installs nginx, git, python3.#, python3.#-venv
* Adds nginx config for virtual host
* Adds Systemd job for Gunicorn (including unique SECRET_KEY)

**Deployment**
* Create directory for site and set owner to {{ ansible_ssh_user }}
* Clone latest version from git to ~/sites/<website_name>
* Create virtualenv if not present
* Update pip to latest version
* Install gunicorn and django-environ
* Install requirements.txt 
* Create .env on server with SECRET_KEY, DEBUG and SITENAME
* manage.py migrate for database
* collectstatic for static files
* Restart nginx
* Restart gunicorn 

## Possible future additions
- Run the functional tests on the site
- Figure out how to safely store passwords to allow running without `-kK` 
