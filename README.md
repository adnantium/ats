
# OSIQ ATS

**This is still a WIP**

## Quickstart

Setup and run locally. You will `git`, `poetry` `httpie` (optional) which can be installed with `brew` if needed.

### Setup
```shell
% git clone https://github.com/adnantium/ats.git
....
% cd osiq_ats/
% poetry install
....
% cd ats/
% export DJANGO_SETTINGS_MODULE=ats.settings
% export PYTHONPATH=`pwd`/ats
% python manage.py migrate
....
Applying ... OK
% django-admin loaddata groups.json
Installed 4 object(s) from 1 fixture(s)
% django-admin loaddata demo_users.json
Installed 2 object(s) from 1 fixture(s)
% python manage.py createsuperuser --username admin --email admin@example.com
...
```
### Test
```shell
% python manage.py test
....
Ran 8 tests in 5.535s
OK
```

### Start up
```shell
% python manage.py runserver
....
Starting development server at http://127.0.0.1:8000/
....
```

Got to: http://127.0.0.1:8000/ for DRF interface

### Endpoints
* `GET /applicants/`
* `POST /applicants/`
* `GET /applicants/<UUID>`
* `PATCH /applicants/<UUID>/approve/`
* `PATCH /applicants/<UUID>/reject/`
* `PATCH /applicants/<UUID>/note/`

### User, groups & permissions
* Users for demo are created from `demo_users.json` fixture
  * `peter`: 
* Use permissions for access to API endpoints is based the user's group from `groups.json` fixture
* Available groups/permissions
  * `CanAddApplicants`
  * `CanViewApplicants`
  * `CanApproveApplicants`
  * `CanUpdateNote`



### Examples:
(replace <UUID> with real uuid provided after applicant is created)
* `http --auth peter:django99 -f POST http://127.0.0.1:8000/applicants/ name=Robert`
* `http --auth peter:django99 -f GET http://127.0.0.1:8000/applicants/`
* `http --auth peter:django99 -f GET http://127.0.0.1:8000/applicants/<UUID>/`
* `http --auth peter:django99 -f PATCH http://127.0.0.1:8000/applicants/<UUID>/note/ note="new note text1"`
* `http --auth peter:django99 -f PATCH http://127.0.0.1:8000/applicants/<UUID>/approve/`
* `http --auth peter:django99 -f PATCH http://127.0.0.1:8000/applicants/<UUID>/reject/`


### TODO
- [ ] Setup docker
  - [ ] Add export of `requirements.txt` from `poetry`
- [ ] Switch to postgres (currently using sqllite)
- [ ] Check with `pylint`
- [ ] Check with `mypy`
- [ ] Verify formatting with `black` (mostly done)
- [ ] Switch to `pytest`
- [ ] Ensure unused HTTP methods are deactivated for each endpoint
- [ ] Add design and implementation notes to README

