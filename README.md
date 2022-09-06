# GOITeens management backend system

Developed for GOITeens
## API Reference

#### Tables field's for form-data:
| Table | Columns   |
| :-------- | :------- |
| `managers` | `'id', 'name', 'description', 'login', 'password'` |
| `status` | `'id', 'name', 'color'` |
| `slots` | `'id', 'name', 'date', 'time', 'manager_id', 'status_id', 'week_day'`|
| `courses` | `'id', 'name', 'description'` |
| `results` | `'id', 'name', 'description', 'color'` |
| `groups` | `'id', 'course_id', 'name', 'timetable'` |
| `appointments` | `'id', 'zoho_link', 'slot_id', 'course_id', 'name', 'comments', 'cancel_type'` | 
| `roles` | `'id', 'name', 'description'` |
| `users` | `'id', 'description', 'login', 'password', 'role_id'` |
| `weeks` | `'id', 'date_start', 'date_finish'` |
| `templates` | `'id', 'manager_id', 'template'` |

--

#### Get items

```http
  GET /table_name
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `table name` | `string` | **Required**.           |

| Table | Description    |
| :-------- | :------- |
| `managers` | `show managers list` |
| `statuses` | `show statuses list` |
| `slots` | `show slots list` |
| `courses` | `show courses list` |
| `results` | `show results list` |
| `groups` | `show groups list` |
| `appointments` | `show appointments list` |

--

#### Register item

```http
  POST /register_{column}
```
| Column | Description    |
| :-------- | :------- |
| `manager` | `add manager to table` |
| `status` | `add status to table` |
| `slot`  | `add slot to table` |
| `course` | `add course to table` |
| `result` | `add result to table` |
| `group` | `add group to table` |
| `appointment` | `add appointment to table` |
| `role` | `add role to table` |
| `user` | `add user to table` |


##### Example
```http
  POST /register_manager
```
![](https://i.imgur.com/9v5JMtH.png "")

--

#### Remove item

```http
  DELETE /remove_{column}/{int:element_id}
```
| Column | Description    |
| :-------- | :------- |
| `manager` | `remove manager from table` |
| `status` | `remove status from table` |
|  `slot` | `remove slot from table` |
| `course` | `remove course from table` |
| `result` | `remove result from table` |
| `group` | `remove group from table` |
| `appointment` | `remove appointment from table` |
| `role` | `remove role from table` |
| `user` | `remove user from table` |


##### Example
```http
  DELETE /remove_manager/1
```
![](https://i.imgur.com/5HR0Dva.png "")


--
#### Update item
```http
  PUT /update_{column}/{int:element_id}
```
| Column | Description    |
| :-------- | :------- |
| `manager` | `update manager table data` |
| `status` | `update status table data` |
|  `slot` | `update slot table data` |
| `course` | `update course table data` |
| `result` | `update result table data` |
| `group` | `update group table data` |
| `appointment` | `update appointment table data` |
| `role` | `update role table` |
| `user` | `update user table` |


##### Example
```http
  PUT /update_manager/2
```
![](https://i.imgur.com/x4mO0KQ.png "")



--
### Get user by id
```http
  GET /user/{int:user_id}
```

##### Example
```http
  GET /user/1
```
![](https://i.imgur.com/CTPtlaA.png "")


--
### Get users by role
```http
  GET /users/{string:role_name}
```

#### Example
```http
  GET /users/admin
```
![](https://i.imgur.com/uIIuk7M.png "")


--
### Get manager slots by manager id and date
```http
  GET /slots/{int:manager_id}/{string:slot_date}
```

#### Example
```http
  GET /slots/2/11.07.2022
```
![](https://i.imgur.com/sKqcLGM.png "")


--
## EXTRA routes
### Week table routes
> Week table data
[click](#heading)

```http
  POST /week/register
```

#### Example
![](https://i.imgur.com/hFJAS5R.png "")

---
#### Remove week
```http
  DELETE /week/remove/{int: week_id}
```

#### Example
```http
  DELETE /week/remove/2
```
![](https://i.imgur.com/QehmzxE.png "")

---
#### Get weeks list
```http
  GET /weeks
```
#### Example
![](https://i.imgur.com/1niKc28.png "")

---
#### Get active(current) week id
```http
  GET /active_week_id
```
#### Example
![](https://i.imgur.com/4ZoxlFR.png "")

---
### Manager planning routes
#### Get manager slots for current week
```http
  GET /current_week/{int: manager_id}
```
#### Example
```http
  GET /current_week/1
```

![](https://i.imgur.com/0PgWTD4.png "")
---

#### Get manager slots by week id
```http
  GET /get_week/{int: manager_id}/{int: week_id}
```
#### Example
```http
  GET /get_week/1/1
```
![](https://i.imgur.com/N99Noe3.png "")
---

#### Update slot's status_id if exists. If not exists - create new slot
```http
  POST /update_slot/{int: manager_id}/{int: week_id}/{int: week_day}/{int: hour}/{int: new_status}
```
#### Example
```http
  POST /update_slot/1/1/0/8/2
```
![](https://i.imgur.com/RgJ9Dxr.png "")

If slot does not exist
![](https://i.imgur.com/WwRoMet.png "")

**RESULT**
![](https://i.imgur.com/0vK43Ra.png "")

---

#### Get manager's week template
```http
  GET /get_template/{int: manager_id}
```

#### Example
```http
  GET /get_template/1
```
![](https://i.imgur.com/mlCH3C7.png "")

---

#### Save new manager's template
```http
  POST /save_template/{int: manager_id}/{string: template}
```

#### Example
```http
  POST /save_template/1/
        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],
        
        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],

        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],

        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],

        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],

        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],

        [
            {"color": 0,"time": 8},
            {"color": 0,"time": 9},
            {"color": 0,"time": 10},
            {"color": 0,"time": 11},
            {"color": 0,"time": 12},
            {"color": 0,"time": 13},
            {"color": 0,"time": 14},
            {"color": 0,"time": 15},
            {"color": 0,"time": 16},
            {"color": 0,"time": 17},
            {"color": 0,"time": 18},
            {"color": 0,"time": 19},
            {"color": 0,"time": 20},
            {"color": 0,"time": 21},
            {"color": 0,"time": 22}
        ],
    ]
```
---
### Manager work
#### Get current work week
```http
  GET /current_work_week/{int: manager_id}
```

#### Example
```http
  GET /current_work_week/1
```
![](https://i.imgur.com/sjWG3Vw.png "")
---
#### Start consultation
```http
  POST(PUT) /start_consultation/{int: week_id}/{int: week_day}/{int: time}/{int: manager_id}
```

#### Example
```http
  POST(PUT) /start_consultation/1/3/12/5
```
![](https://i.imgur.com/7agfUYs.png "")

---
#### Post consultation result
```http
  POST /consultation_result/{int: slot_id}/{int: consultation_result}/{int: group_id}/{string: message}
```
#### Example
```http
  POST /consultation_result/2/7/1/Раніше писав на js
```

![](https://i.imgur.com/aUPZueu.png "")

---
### Confirmator
#### Get current appointments, that need to be confirmed now
```http
  GET /current_information
```
---
#### Get current appointments, that need to be confirmed
```http
  GET /get_confirmation/{int:week_id}/{int:day}/{int:half}
```
#### Example
```http
  GET /get_confirmation/1/1/1
```
---
#### Set confirmation to slot
```http
  PUT /set_confirmation/{int:slot_id}/{int:status}/{string:message}
```
#### Example
```http
  =Ї

---
#### Cancel confirmation to slot
```http
  PUT /set_cancel_confirmation/{int:slot_id}/{int:cancel_type}/{string:message}
```
#### Example
```http
  PUT /set_cancel_confirmation/1/1/weak
```
---
#### Move the appointment to slot
```http
  PUT /set_postpone_confirmation/{int:slot_id}/{int:appointment_id}
```
#### Example
```http
  PUT /set_postpone_confirmation/1/1
```
---
### Caller
#### Get caller current week
```http
  GET /caller_current_week
```
---
#### Get avaliable managers
```http
  GET /avaliable_managers/{int:week_id}/{int:day_id}/{int:hour}
```
---
#### Create appointment
```http
  POST, PUT /create_appointment/{int:week_id}/{int:day}/{int:hour}/{int:course_id}/{string:crm_link}/{string:phone}/{int:age}/{int:manager_id}
```
### Superadmin
#### available managers
```http
  GET /superadmin_managers/{string:date}/{int:half}
```
#### search by crm_link
```http
  GET /search/
  form-data{
  crm_link: string
  }
```
