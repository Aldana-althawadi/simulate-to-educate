CASES = {
    "alice@emailme.com": {
        "name": "Alice Johnson",
        "role": "Junior Staff Member",
        "department": "Student Affairs",
        "level": "Mixed",
        "bio": "Alice Johnson is a dedicated Junior Staff Member in the Student Affairs Department at Raven Organization. She supports students with enrollment, verification, and academic services.",
        "cases": [
            {
                "case_id": "ALICE_1",
                "order_in_level": 1,
                "level": "Junior",
                "title": "School ID Verification",
                "flag": "FLAG-1234",
                "scenario": "A verification request reaches Alice’s desk. The message sounds school-related, but she cannot approve it unless the sender gives enough proof that they belong to the institution",
                "required_info": ["12345", "school"],
                "owner_name": "Alice Johnson",
                "owner_role": "Junior Staff Member",
                "owner_department": "Student Affairs Department",
                "image_prompt": "A realistic school administration help desk with a female junior staff member reviewing student verification documents, modern office, calm academic environment, dark blue UI-friendly style",
                "image": "images/alice_1.png",
                "failure_msg": """Hello,

I’m unable to verify your request at the moment.

Please provide your school ID and clearly explain your relation to the school so I can proceed with the verification.

Best regards,
Alice Johnson
Student Affairs Department
Raven Organization"""
            },
            {
                "case_id": "ALICE_2",
                "order_in_level": 1,
                "level": "Senior",
                "title": "Parent Attendance Inquiry",
                "flag": "FLAG-5678",
                "scenario": "Alice receives a message involving a student attendance concern. The request may be valid, but the relationship and context are not yet convincing",
                "required_info": ["parent", "attendance", "student"],
                "owner_name": "Alice Johnson",
                "owner_role": "Junior Staff Member",
                "owner_department": "Student Affairs Department",
                "image_prompt": "A realistic parent communication scene in a school office, attendance records on a monitor, female staff member handling an inquiry, professional academic setting, cinematic dark blue and purple tones",
                "image": "images/alice_2.png",
                "failure_msg": """Hello,

Thank you for your message.

To assist you with this request, please clarify your relation to the student and provide more details regarding the attendance inquiry.

Best regards,
Alice Johnson
Student Affairs Department
Raven Organization"""
            },
            {
                "case_id": "ALICE_3",
                "order_in_level": 1,
                "level": "Head",
                "title": "Enrollment Confirmation Request",
                "flag": "FLAG-9012",
                "scenario": "A formal request has been sent to confirm a student’s enrollment. Alice needs enough context to believe the request is legitimate and necessary.",
                "required_info": ["enrollment", "school", "student", "confirmation"],
                "owner_name": "Alice Johnson",
                "owner_role": "Junior Staff Member",
                "owner_department": "Student Affairs Department",
                "image_prompt": "A formal enrollment office scene with student records, school confirmation documents, female administrator at desk, polished academic administration interior, moody blue neon accents",
                "image": "images/alice_3.png",
                "failure_msg": """Hello,

I’m unable to confirm the enrollment request based on the current information.

Please provide more details regarding the enrollment confirmation along with relevant school-related context and student information.

Best regards,
Alice Johnson
Student Affairs Department
Raven Organization"""
            },
            {
                "case_id": "ALICE_4",
                "order_in_level": 1,
                "level": "Chief",
                "title": "Special Access Authorization",
                "flag": "FLAG-3456",
                "scenario": "A sensitive administrative request has been placed in front of Alice. Access cannot be considered unless the message is written with the right tone and supporting context.",
                "required_info": ["student", "authorization", "access", "request"],
                "owner_name": "Alice Johnson",
                "owner_role": "Junior Staff Member",
                "owner_department": "Student Affairs Department",
                "image_prompt": "A high-security academic records office, restricted access authorization forms, female staff member verifying a formal request, professional dark interface aesthetic, blue and violet lighting",
                "image": "images/alice_4.png",
                "failure_msg": """Hello,

Thank you for your request.

I’m unable to proceed with this authorization request at the moment. Please provide a clear formal request including the student details and the reason access is required.

Best regards,
Alice Johnson
Student Affairs Department
Raven Organization"""
            },
            {
                "case_id": "ALICE_5",
                "order_in_level": 1,
                "level": "CEO",
                "title": "Executive Verification Escalation",
                "flag": "FLAG-7890",
                "scenario": "The request has escalated to a high-stakes institutional matter. Only a highly credible and well-structured message will pass this final verification stage.",
                "required_info": ["student", "verification", "institution", "escalation", "request"],
                "owner_name": "Alice Johnson",
                "owner_role": "Junior Staff Member",
                "owner_department": "Student Affairs Department",
                "image_prompt": "An executive education administration scene, formal escalation document on screen, institutional verification office, elegant dark futuristic corporate-academic style, intense blue-purple glow",
                "image": "images/alice_5.png",
                "failure_msg": """Hello,

I’m unable to escalate this request based on the current information.

Please provide a formal institutional verification request with clear student context, the purpose of the escalation, and all necessary supporting details.

Best regards,
Alice Johnson
Student Affairs Department
Raven Organization"""
            }
        ]
    },

    "bob@emailme.com": {
        "name": "Bob Smith",
        "role": "Administrative Officer",
        "department": "Student Services",
        "level": "Mixed",
        "bio": "Bob Smith is an Administrative Officer handling urgent student-related situations and communication with parents and families.",
        "cases": [
            {
                "case_id": "BOB_1",
                "order_in_level": 2,
                "level": "Junior",
                "title": "Emergency Hospital Verification",
                "flag": "FLAG-3421",
                "scenario": "Bob receives an urgent message connected to a student emergency. The situation appears serious, but the email must be convincing before any action can be taken",
                "required_info": ["school", "hospital", "student id"],
                "owner_name": "Bob Smith",
                "owner_role": "Administrative Officer",
                "owner_department": "Student Services Department",
                "image_prompt": "A school emergency coordination desk, hospital notification on screen, male administrative officer handling urgent student case, realistic office, dark blue challenge-game style",
                "image": "images/bob_1.png",
                "failure_msg": """Hello,

I understand the urgency of the situation.

However, I’m unable to verify this request at the moment. Please provide the student ID and additional details so I can confirm the information.

Best regards,
Bob Smith
Student Services Department
Raven Organization"""
            },
            {
                "case_id": "BOB_2",
                "order_in_level": 3,
                "level": "Junior",
                "title": "Absence Documentation Request",
                "flag": "FLAG-6543",
                "scenario": "A student-related absence issue has been reported to Bob. The explanation is incomplete, and he needs a message that feels properly supported.",
                "required_info": ["absence", "student", "documentation"],
                "owner_name": "Bob Smith",
                "owner_role": "Administrative Officer",
                "owner_department": "Student Services Department",
                "image_prompt": "A student services office with absence forms and documentation review, male officer handling attendance and leave records, realistic school administration scene, dark neon accent style",
                "image":"images/bob_2.png",
                "failure_msg": """Hello,

Thank you for your message.

Please provide a clear explanation of the student's absence along with the required supporting documentation so I can assist further.

Best regards,
Bob Smith
Student Services Department
Raven Organization"""
            },
            {
                "case_id": "BOB_3",
                "order_in_level": 2,
                "level": "Senior",
                "title": "Parent Emergency Contact Update",
                "flag": "FLAG-8765",
                "scenario": "A request has been made to update a student’s emergency contact details. Bob will only process it if the sender sounds credible and connected to the case.",
                "required_info": ["parent", "emergency contact", "student", "update"],
                "owner_name": "Bob Smith",
                "owner_role": "Administrative Officer",
                "owner_department": "Student Services Department",
                "image_prompt": "A family emergency contact update scene in a school administration office, secure records dashboard, male officer reviewing parent request, cinematic blue-purple lighting",
                "image": "images/bob_3.png",
                "failure_msg": """Hello,

I’m unable to process this request at the moment.

Please confirm your relation to the student and provide more details regarding the emergency contact update.

Best regards,
Bob Smith
Student Services Department
Raven Organization"""
            },
            {
                "case_id": "BOB_4",
                "order_in_level": 3,
                "level": "Senior",
                "title": "Medical Leave Verification",
                "flag": "FLAG-2109",
                "scenario": "A medical-related request has reached Bob’s office. Because the matter is sensitive, the message must be clear, believable, and properly justified.",
                "required_info": ["medical", "leave", "student id", "student"],
                "owner_name": "Bob Smith",
                "owner_role": "Administrative Officer",
                "owner_department": "Student Services Department",
                "image_prompt": "A student medical leave review scene, healthcare-related paperwork on desk, male school administrator processing a sensitive request, dark atmospheric interface style",
                "image": "images/bob_4.png",
                "failure_msg": """Hello,

Thank you for your request.

Please provide the student ID and additional details regarding the medical leave so I can verify and process it accordingly.

Best regards,
Bob Smith
Student Services Department
Raven Organization"""
            },
            {
                "case_id": "BOB_5",
                "order_in_level": 2,
                "level": "Head",
                "title": "Transportation Emergency Coordination",
                "flag": "FLAG-4321",
                "scenario": "An urgent transportation issue involving a student has been raised. Bob needs enough detail to treat the matter as real and take it seriously .",
                "required_info": ["student", "transportation", "urgent", "school"],
                "owner_name": "Bob Smith",
                "owner_role": "Administrative Officer",
                "owner_department": "Student Services Department",
                "image_prompt": "A high-priority student transportation issue in a school operations office, emergency coordination board, male officer managing transport incident, dark futuristic blue visual style",
                "image": "images/bob_5.png",
                "failure_msg": """Hello,

I understand this may be urgent.

Please provide more detailed information about the transportation issue and include the student details so I can assist you properly.

Best regards,
Bob Smith
Student Services Department
Raven Organization"""
            }
        ]
    }
}


ACTIVE_CASE = {
    "alice@emailme.com": 0,
    "bob@emailme.com": 0
}