BASE_SYSTEM_PROMPT = """
Với tư cách là một language model, nhiệm vụ của bạn là trả lời bất kỳ câu hỏi nào được hỏi một cách ngắn gọn và trung thực. Hãy đảm bảo rằng bạn đưa ra những câu trả lời đa dạng và giàu thông tin để giữ cho cuộc trò chuyện luôn hấp dẫn
"""

EXTRACT_KEYWORDS_SYSTEM_PROMPT = """
Bạn có trong tay bộ tài liệu hỗ trợ về các thủ tục pháp luật gồm các trường: 
- 'Tên tài liệu' (chứa tóm tắt nội dung chính của tài liệu) 
và các trường khác như:
- 'Trạng thái tài liệu'
- 'Trình tự thực hiện'
- 'Đối tượng thực hiện'
- 'Cách thức thực hiện'
- 'Thành phần hồ sơ'-
- 'Căn cứ pháp lý'
- 'Biểu mẫu đính kèm'
- 'Phí'
- 'Lệ phí'
- 'Yêu cầu điều kiện'
- 'Số bộ hồ sơ'
- 'Kết quả thực hiện'
- 'Thời hạn giải quyết'
- 'Cơ quan thực hiện'
- 'Cơ quan ban hành'
- 'Cơ quan phối hợp'
- 'Thủ tục hành chính liên quan'
Nhiệm vụ của bạn đó là lấy ra các từ khoá chính trong câu hỏi sau để sao cho phù hợp nhất với việc đi tìm tệp dữ liệu thích hợp trong vector database với trường được embedding là tên của các tài liệu. 
Bởi vậy hay bỏ đi các từ khoá không cần thiết ví dụ như các từ khoá gần giống nghhĩa với các trường khác có trong nội dung của tài liệu. 
Hay đưa ra phân tích của bạn về câu hỏi trên và các từ khoá theo format sau:
<analysis>
[Phân tích ngắn gọn câu hỏi, chỉ ra các từ, cụm từ quan trọng và giải thích lý do của bạn]
</analysis>
<keywords>
[Danh sách các cụm từ khoá được bọc trong dấu nháy kép, giữ đúng thứ tự trong câu hỏi]
</keywords>
"""

EXTRACT_KEYWORDS_USER_PROMPT = """
Nội dung câu hỏi: "{user_message}" 
"""

FILTER_DOCUMENTS_SYSTEM_PROMPT = """
Tôi có được 1 danh sách các tên tài liệu về pháp luật như sau:
{document_titles}

Với câu hỏi của user, bạn hãy chọn ra 3 tài liệu liên quan nhất vấn đề của người dùng. 

Hay đưa ra phân tích của bạn và các tài liệu được chọn:

<analysis>
[Phân tích ngắn gọn tại sao bạn chọn 3 tài liệu này]
</analysis>

<documents>
[Danh sách số thứ tự của 3 tài liệu được chọn, dưới dạng list JSON]
</documents>
"""

FILTER_DOCUMENTS_USER_PROMPT = """
Nội dung câu hỏi: "{user_message}" 
"""

ASK_FOLLOW_UP_QUESTION_SYSTEM_PROMPT = BASE_SYSTEM_PROMPT

ASK_FOLLOW_UP_QUESTION_USER_PROMPT = """
Với câu hỏi của người dùng như sau "{user_message}"
Tôi có được 1 danh sách các tài liệu về pháp luật có liên quan:
{documents}

Hãy phân tích câu hỏi người dùng và các tài liệu trên và đặt một câu hỏi để xác định xem đâu là tài liệu thích hợp nhất với thắc mắc của người dùng.

Hãy đưa ra phân tích của bạn và câu hỏi theo dạng như sau:

<analysis>
[Phân tích ngắn gọn, chỉ ra các điểm khác nhau cơ bản của các tài liệu và lựa chọn 1 ý để đặt câu hỏi]
</analysis>

<question>
[Đặt một câu hỏi ngắn gọn để giúp người dùng đưa ra câu trả lời có thể giúp xác định tài liệu phù hợp nhất]
</question>
"""

FILTER_FINAL_DOCUMENT_SYSTEM_PROMPT = BASE_SYSTEM_PROMPT

FILTER_FINAL_DOCUMENT_USER_PROMPT = """
Phân tích đoạn hội thoại dưới đây giữa nhân viên tư vấn và khách hàng:
{conversation}

Tôi có được 1 danh sách các tài liệu về pháp luật có liên quan:
{documents}

Hãy phân tích đoạn hội thoại và các tài liệu trên và xác định xem đâu là 1 tài liệu thích hợp nhất với thắc mắc của người dùng.
Hãy đưa ra phân tích của bạn và câu hỏi theo dạng như sau:

<analysis>
[Phân tích đoạn hội thoại, chỉ ra các điểm khác nhau cơ bản của các tài liệu và mong muốn của người dùng từ đó chọn ra 1 tài liệu phù hợp nhất]
</analysis>

<document>
[In ra số thứ tự của tài liệu phù hợp nhất]
</document>
"""

FINAL_CHAT_SYSTEM_PROMPT = """
Từ những thông tin dưới đầy, hãy chọn lọc để trả lời chính xác câu hỏi được cung cấp
<context>
{context}
</context>
"""

FINAL_CHAT_USER_PROMPT = """
## Đây là lịch sử chat:
<history>
{history}
</history>

## Đây là câu hỏi chính của người dùng:
<question>
{user_message}
</question>
"""