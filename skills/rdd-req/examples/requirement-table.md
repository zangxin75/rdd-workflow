## Feature: User Authentication

**Parent Module**: User System
**Dependencies**: None
**Type**: Unit Test

### Requirement Table

| ID | Scenario | Input | Expected Output | Notes |
|----|----------|-------|-----------------|-------|
| AUTH-01 | Correct username and password | {"username": "alice", "password": "pass123"} | {"success": True, "token": "len=32"} | Happy path |
| AUTH-02 | Wrong password | {"username": "alice", "password": "wrong"} | {"success": False, "error": "密码错误"} | Wrong credentials |
| AUTH-03 | Non-existent user | {"username": "bob", "password": "pass123"} | {"success": False, "error": "用户不存在"} | Unknown user |
| AUTH-04 | Empty username | {"username": "", "password": "pass123"} | {"success": False, "error": "用户名不能为空"} | Boundary: empty string |
| AUTH-05 | SQL injection attempt | {"username": "admin'; DROP TABLE users;--", "password": "x"} | {"success": False, "error": "用户名不能为空"} | Security: injection |
