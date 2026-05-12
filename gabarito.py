from gabarito_data import gabaritos

def get_available_book_codes():
    return sorted(gabaritos.keys())

def normalize_book_code(code):
    only_digits = ''.join(filter(str.isdigit, str(code)))[:3]
    if not only_digits:
        return None
    return only_digits.zfill(3)

def get_book_answer_key(book_code):
    normalized_code = normalize_book_code(book_code)
    if not normalized_code:
        return {"normalizedCode": None, "answerKey": None}
    
    return {
        "normalizedCode": normalized_code,
        "answerKey": gabaritos.get(normalized_code)
    }

def get_question_total_by_program(program_number, answer_key):
    if program_number == 6:
        return 6
        
    if not answer_key:
        return 30
        
    program_key = f"programa_{program_number}"
    program_data = answer_key.get(program_key)
    if not program_data:
        return 30
        
    return len(program_data)
