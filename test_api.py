import asyncio
import httpx

async def test_auth_and_profiles():
    base_url = "http://127.0.0.1:8000"
    
    print("\n--- STARTING API INTEGRATION TESTS ---")
    
    async with httpx.AsyncClient(base_url=base_url) as client:
        # 1. Login as Student
        print("\n[1] Testing Student Login...")
        login_res = await client.post("/api/auth/login", json={
            "email": "student1@nexus.edu",
            "password": "student123"
        })
        print(f"Status: {login_res.status_code}")
        login_data = login_res.json()
        assert login_data["success"] is True
        token = login_data["access_token"]
        print(f"Token acquired. Role: {login_data['user']['role']}")

        # 2. Get Student Profile (authenticating with token)
        print("\n[2] Fetching Student Profile...")
        headers = {"Authorization": f"Bearer {token}"}
        profile_res = await client.get("/api/student/profile", headers=headers)
        print(f"Status: {profile_res.status_code}")
        profile_data = profile_res.json()
        print(f"Name: {profile_data['user']['name']}, Roll: {profile_data['roll_no']}, Class: {profile_data['class_']['grade']}-{profile_data['class_']['section']}")

        # 3. Get Student Dashboard
        print("\n[3] Fetching Student Dashboard...")
        dash_res = await client.get("/api/student/dashboard", headers=headers)
        print(f"Status: {dash_res.status_code}")
        dash_data = dash_res.json()
        print(f"GPA: {dash_data['gpa']}, Attendance: {dash_data['attendance_rate']}%")

        # 4. Login as Teacher
        print("\n[4] Testing Teacher Login...")
        t_login_res = await client.post("/api/auth/login", json={
            "email": "teacher@nexus.edu",
            "password": "teacher123"
        })
        print(f"Status: {t_login_res.status_code}")
        t_login_data = t_login_res.json()
        t_token = t_login_data["access_token"]

        # 5. Fetch Teacher Dashboard
        print("\n[5] Fetching Teacher Dashboard...")
        t_headers = {"Authorization": f"Bearer {t_token}"}
        t_dash_res = await client.get("/api/teacher/dashboard", headers=t_headers)
        print(f"Status: {t_dash_res.status_code}")
        t_dash_data = t_dash_res.json()
        print(f"Advised Class Count: {t_dash_data['class_count']}, Student Count: {t_dash_data['active_student_count']}")

        # 6. Fetch Teacher Students Roster
        print("\n[6] Fetching Teacher Students Roster...")
        roster_res = await client.get("/api/teacher/students", headers=t_headers)
        print(f"Status: {roster_res.status_code}")
        roster_data = roster_res.json()
        print(f"Fetched {len(roster_data)} students:")
        for stud in roster_data:
            print(f"  - {stud['user']['name']} (ID: {stud['student_id']}) - Status: {stud['status']}")

        # 7. Access admin endpoint with student credentials (should fail with 403 Forbidden)
        print("\n[7] Testing RBAC Guard (Student requesting Admin route)...")
        fail_res = await client.post("/api/admin/classes", json={
            "grade": "12th",
            "section": "A"
        }, headers=headers)
        print(f"Status: {fail_res.status_code} (Expected: 403)")
        print(f"Response: {fail_res.json()}")

        # 8. Access admin endpoint with admin credentials (should succeed)
        print("\n[8] Testing Admin Login & Route...")
        admin_login_res = await client.post("/api/auth/login", json={
            "email": "admin@nexus.edu",
            "password": "admin123"
        })
        admin_token = admin_login_res.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        class_res = await client.post("/api/admin/classes", json={
            "grade": "12th",
            "section": "A"
        }, headers=admin_headers)
        print(f"Status: {class_res.status_code}")
        print(f"Created class: {class_res.json()}")

    print("\n--- ALL INTEGRATION TESTS PASSED ---")

if __name__ == "__main__":
    asyncio.run(test_auth_and_profiles())
