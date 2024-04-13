
# OSIQ ATS

**This is still a WIP**

## Quickstart

Setup and run locally. You will need `git`, `poetry` `httpie` (optional).

### Setup
```shell
% git clone https://github.com/adnantium/osiq_ats.git
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

Go to: http://127.0.0.1:8000/ for DRF interface

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
* User permissions for access to API endpoints is based the user's group from `groups.json` fixture
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


### Application Design
* Using Django's User and Groups models
* The 4 permissions sets are associated to a User via Group membership
* Built with Django Rest Framework because it is by far the most popular choice. 
  * It is getting a little bloated (just like Django)
* Permission check are done thru DRF's permissions module
* Permissioning is configured at the API level which enforces authentication, not within the code for each endpoint
* Using ModelViewSet for endpoints because it offers good extensibility and works well with DRF UI.

### Interesting pylint messages
* `views.py:26:4: W0221: Variadics removed in overriding 'ApplicantViewSet.create' method (arguments-differ)`
* `tests.py:20:4: W0102: Dangerous default value [] as argument (dangerous-default-value)`

### TODO
- [X] Setup docker
- [X] Ensure unused HTTP methods are deactivated for each endpoint
- [X] Add design and implementation notes to README
- [X] Check with `pylint`
- [X] Verify formatting with `black` (mostly done)
- [ ] Switch to postgres (currently using sqllite)
- [ ] Check with `mypy`
- [ ] Verify completeness of test coverage
- [ ] Switch to `pytest`

