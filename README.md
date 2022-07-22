
# GOITeens management backend system

Developed for GOITeens


## API Reference

#### Get items

```http
  GET /table_name
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `table name` | `string` | **Required**.              |

| Table | Description    |
| :-------- | :------- |
| `managers` | `show managers list` |
| `statuses` | `show statuses list` |
| `slots` | `show slots list` |
| `courses` | `show courses list` |
| `results` | `show results list` |
| `groups` | `show groups list` |
| `appointments` | `show appointments list` |

##
#### Tables field's for form-data:
| Table | Columns   |
| :-------- | :------- |
| `managers` | `'id', 'name', 'description', 'login', 'password'` |
| `status` | `'id', 'name', 'color'` |
| `slots` | `'id', 'name', 'date', 'time', 'manager_id', 'status_id'` |
| `courses` | `'id', 'name', 'description'` |
| `results` | `'id', 'name', 'description', 'color'` |
| `groups` | `'id', 'course_id', 'name', 'timetable'` |
| `appointments` | `'id', 'zoho_link', 'slot_id', 'course_id', 'name', 'comments'` | 
| `roles` | `id`, `name`, `description` |
| `users` | `id`, `description`, `login`, `password`, `role_id` |

##


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

##

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


##
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



##
#### Get user by id
```http
  GET /user/{int:user_id}
```

##### Example
```http
  GET /user/1
```
![](https://i.imgur.com/CTPtlaA.png "")


##
#### Get users by role
```http
  GET /users/{string:role_name}
```

#### Example
```http
  GET /users/admin
```
![](https://i.imgur.com/uIIuk7M.png "")


##
#### Get manager slots by manager id and date
```http
  GET /slots/{int:manager_id}/{string:slot_date}
```

#### Example
```http
  GET /slots/2/11.07.2022
```
![](https://i.imgur.com/sKqcLGM.png "")