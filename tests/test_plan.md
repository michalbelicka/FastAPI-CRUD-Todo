# Test Plan for ToDo API

## 1. Objective

Test the '/todos' API to verify that it handles valid inputs correctly (happy path) and gracefully handles incorrect or missing inputs (edge cases).

## 2. Test Approach

1. **Manual Testing**
   - First, start the server so the API is running.
   - Test the API using Postman.
   - Send requests with different payloads.
   - Observe API responses to understand its behavior.

2. **Automated Testing**
   - Plan automated test cases using 'pytest'.
   - Cover **happy path** scenarios:
     - All fields present and valid.
     - Non-standard values accepted by the API.
   - Cover **edge cases**:
     - Missing keys:
       - Missing 'title'
       - Missing 'description'
       - Missing 'status'
     - Misspelled keys:
       - 'titl' instead of 'title'
       - 'escription' instead of 'description'
       - 'statu' instead of 'status'
     - Invalid data types:
       - Numbers instead of strings
       - Empty lists or dicts instead of strings
     - Special characters in string fields:
       - Commas, dots, semicolons
       - Strings like '{}', '[]'

3. **Test Execution**
   - Send requests with different payloads for each case.
   - Record responses from the API.
   - Verify that the API returns expected status codes ('200' for success, '422' for validation errors).
   - Compare actual responses with expected values.

## 3. Notes

- Focus on observing how API handles missing or incorrect keys.
- This test plan is for a **junior QA level**, so it is simple and easy to follow.
