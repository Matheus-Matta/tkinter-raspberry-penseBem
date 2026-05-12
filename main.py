import customtkinter as ctk
import gabarito

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLOR_TO_OPTION = {
    "Vermelho": "A",
    "Amarelo": "B",
    "Azul": "C",
    "Verde": "D"
}

KEY_TO_OPTION = {
    "q": "A",
    "w": "B",
    "e": "C",
    "r": "D"
}

QUESTIONS_PER_PROGRAM = 30
REGULAR_PROGRAMS = 5
FINAL_PROGRAM_NUMBER = 6
FINAL_PROGRAM_QUESTIONS = 6
MAX_ATTEMPTS = 3

# Paleta Pastel
BG_APP = "#F0F4F8"          # Azul suave / gelo
CARD_BG = "#FFFFFF"         # Branco gelo
TEXT_MAIN = "#2D3142"       # Cinza escuro para contraste
TEXT_SUB = "#9095A0"        # Cinza claro
BTN_START = "#4CC9F0"       # Azul vibrante (Start/✓)
BTN_START_HOVER = "#3BAED0"
BTN_SCROLL = "#E2E8F0"      # Cinza botões de scroll
BTN_SCROLL_HOVER = "#CBD5E1"

# Cores Alternativas Pastel
COLOR_A = "#4CC9F0"         # Azul Claro
COLOR_B = "#06D6A0"         # Verde Água
COLOR_C = "#FFD166"         # Amarelo Claro
COLOR_D = "#EF476F"         # Coral

def build_final_program_questions(book_code, all_question_numbers):
    all_questions = list(all_question_numbers)
    seed = (int(book_code) if book_code.isdigit() else 1) * 7919

    for i in range(len(all_questions) - 1, 0, -1):
        seed = (seed * 1664525 + 1013904223) % 4294967296
        j = seed % (i + 1)
        all_questions[i], all_questions[j] = all_questions[j], all_questions[i]

    return all_questions[:FINAL_PROGRAM_QUESTIONS]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pense Bem - Modo Game")
        self.attributes("-fullscreen", True)
        self.configure(fg_color=BG_APP)

        # Game State
        self.active_book_code = ""
        self.active_answer_key = None
        self.stage = "ENTRY"
        self.program_number = 1
        self.question_number = 1
        self.attempt_number = 1
        self.program_score = 0
        self.total_score = 0
        self.program_correct = 0
        self.program_wrong = 0
        self.total_correct = 0
        self.total_wrong = 0
        self.program_results = []
        self.feedback = ""
        self.final_program_questions = []
        self.color_by_question = {}
        self.all_questions = []
        self.wrong_attempts_current_q = []

        self.container = ctk.CTkFrame(self, fg_color=BG_APP)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.available_books = gabarito.get_available_book_codes()
        self.current_book_index = 0

        self.show_entry_screen()

        self.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        key = event.keysym.lower()
        
        # Tecla ESC para voltar à Home ou Sair (se já estiver na Home)
        if event.keysym == "Escape":
            if self.stage != "ENTRY":
                self.show_entry_screen()
            else:
                self.quit()
            return

        if self.stage == "ENTRY":
            if key == "q":
                self.scroll_up()
            elif key == "w" or event.keysym == "Return":
                self.start_book()
            elif key == "e":
                self.scroll_down()
            return

        if self.stage == "RUNNING":
            if key in KEY_TO_OPTION:
                self.handle_answer(KEY_TO_OPTION[key])
            return

        if self.stage == "PROGRAM_END":
            if key == "w":
                self.start_next_program()
            return

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def update_rolodex(self):
        idx = self.current_book_index
        total = len(self.available_books)
        
        prev_book = self.available_books[idx - 1] if idx > 0 else ""
        curr_book = self.available_books[idx] if total > 0 else "N/A"
        next_book = self.available_books[idx + 1] if idx < total - 1 else ""

        self.lbl_prev.configure(text=f"Livro {prev_book}" if prev_book else "")
        self.lbl_curr.configure(text=f"Livro {curr_book}" if curr_book else "Vazio")
        self.lbl_next.configure(text=f"Livro {next_book}" if next_book else "")

        self.btn_up.configure(state="normal" if idx > 0 else "disabled")
        self.btn_down.configure(state="normal" if idx < total - 1 else "disabled")

    def scroll_up(self):
        if self.current_book_index > 0:
            self.current_book_index -= 1
            self.update_rolodex()

    def scroll_down(self):
        if self.current_book_index < len(self.available_books) - 1:
            self.current_book_index += 1
            self.update_rolodex()

    def show_entry_screen(self):
        self.stage = "ENTRY"
        self.clear_container()

        card = ctk.CTkFrame(self.container, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="both", expand=True, pady=30)

        title = ctk.CTkLabel(card, text="PENSE BEM", font=("Helvetica", 28, "bold"), text_color=TEXT_MAIN)
        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(card, text="Escolha a fase (Livro)", font=("Helvetica", 14), text_color=TEXT_SUB)
        subtitle.pack(pady=(0, 20))

        # ROLODEX AREA
        rolodex_frame = ctk.CTkFrame(card, fg_color="transparent")
        rolodex_frame.pack(fill="both", expand=True, padx=20)

        # Container Centralizado para Labels e Botões
        center_container = ctk.CTkFrame(rolodex_frame, fg_color="transparent")
        center_container.place(relx=0.5, rely=0.5, anchor="center")

        # Esquerda: Labels
        labels_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        labels_frame.pack(side="left", padx=(0, 20))

        self.lbl_prev = ctk.CTkLabel(labels_frame, text="", font=("Helvetica", 16), text_color=TEXT_SUB)
        self.lbl_prev.pack(pady=(10, 5), anchor="center")

        curr_frame = ctk.CTkFrame(labels_frame, fg_color="#F8F9FA", border_width=2, border_color=BTN_START, corner_radius=15)
        curr_frame.pack(pady=10, fill="x", padx=10)
        self.lbl_curr = ctk.CTkLabel(curr_frame, text="", font=("Helvetica", 26, "bold"), text_color=BTN_START)
        self.lbl_curr.pack(pady=15)

        self.lbl_next = ctk.CTkLabel(labels_frame, text="", font=("Helvetica", 16), text_color=TEXT_SUB)
        self.lbl_next.pack(pady=(5, 10), anchor="center")

        # Direita: Botões
        controls_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        controls_frame.pack(side="left")

        self.btn_up = ctk.CTkButton(controls_frame, text="▲", width=50, height=50, corner_radius=4, 
                                    fg_color=BTN_SCROLL, hover_color=BTN_SCROLL_HOVER, text_color=TEXT_MAIN,
                                    command=self.scroll_up)
        self.btn_up.pack(pady=(0, 2))
        ctk.CTkLabel(controls_frame, text="[Q]", font=("Helvetica", 10, "bold"), text_color=TEXT_SUB).pack(pady=(0, 5))

        btn_select = ctk.CTkButton(controls_frame, text="✓", width=50, height=50, corner_radius=4,
                                   fg_color=BTN_START, hover_color=BTN_START_HOVER, text_color="white", font=("Helvetica", 24, "bold"),
                                   command=self.start_book)
        btn_select.pack(pady=(5, 2))
        ctk.CTkLabel(controls_frame, text="[W]", font=("Helvetica", 10, "bold"), text_color=TEXT_SUB).pack(pady=(0, 5))

        self.btn_down = ctk.CTkButton(controls_frame, text="▼", width=50, height=50, corner_radius=4,
                                      fg_color=BTN_SCROLL, hover_color=BTN_SCROLL_HOVER, text_color=TEXT_MAIN,
                                      command=self.scroll_down)
        self.btn_down.pack(pady=(5, 2))
        ctk.CTkLabel(controls_frame, text="[E]", font=("Helvetica", 10, "bold"), text_color=TEXT_SUB).pack(pady=(0, 5))

        self.update_rolodex()

        self.error_label = ctk.CTkLabel(card, text="", text_color="#EF476F", font=("Helvetica", 13))
        self.error_label.pack(pady=5)
        
        ctk.CTkLabel(card, text="ESC: Voltar", font=("Helvetica", 11), text_color=TEXT_SUB).pack(pady=(0, 10))

        btn = ctk.CTkButton(card, text="JOGAR!", fg_color=BTN_START, hover_color=BTN_START_HOVER, height=55, 
                            corner_radius=20, font=("Helvetica", 20, "bold"), text_color="white", command=self.start_book)
        btn.pack(fill="x", padx=30, pady=30)

    def start_book(self):
        if not self.available_books:
            return
            
        code = self.available_books[self.current_book_index]
        res = gabarito.get_book_answer_key(code)
        
        if not res["normalizedCode"]:
            self.error_label.configure(text="Digite um código válido!")
            return
            
        if not res["answerKey"]:
            self.error_label.configure(text="Livro não encontrado, digite novamente!")
            return

        self.active_book_code = res["normalizedCode"]
        self.active_answer_key = res["answerKey"]
        
        all_question_numbers = []
        self.all_questions = []
        for p in range(1, REGULAR_PROGRAMS + 1):
            prog_data = self.active_answer_key.get(f"programa_{p}", [])
            self.all_questions.extend(prog_data)
            for item in prog_data:
                all_question_numbers.append(item["questao"])

        self.color_by_question = {item["questao"]: item["cor"] for item in self.all_questions}
        self.final_program_questions = build_final_program_questions(self.active_book_code, all_question_numbers)

        self.program_number = 1
        self.question_number = 1
        self.attempt_number = 1
        self.program_score = 0
        self.total_score = 0
        self.program_correct = 0
        self.program_wrong = 0
        self.total_correct = 0
        self.total_wrong = 0
        self.program_results = []
        self.feedback = ""
        self.wrong_attempts_current_q = []

        self.show_running_screen()

    def get_current_question_total(self):
        return gabarito.get_question_total_by_program(self.program_number, self.active_answer_key)

    def get_current_question_key(self):
        if self.program_number == FINAL_PROGRAM_NUMBER:
            if self.question_number - 1 < len(self.final_program_questions):
                return self.final_program_questions[self.question_number - 1]
            return self.question_number

        program_key = f"programa_{self.program_number}"
        if not self.active_answer_key or program_key not in self.active_answer_key:
            return (self.program_number - 1) * QUESTIONS_PER_PROGRAM + self.question_number

        prog_data = self.active_answer_key[program_key]
        if self.question_number - 1 < len(prog_data):
            return prog_data[self.question_number - 1]["questao"]
        return self.question_number

    def handle_answer(self, selected):
        if selected in self.wrong_attempts_current_q:
            return # Ignore already clicked wrong answers
            
        current_q_key = self.get_current_question_key()
        color = self.color_by_question.get(current_q_key)
        
        if not color:
            self.feedback = "Questao sem gabarito. Pulando para a proxima."
            self.wrong_attempts_current_q = []
            self.go_to_next_question(self.program_score)
            return

        correct_option = COLOR_TO_OPTION.get(color)
        
        if selected == correct_option:
            points = MAX_ATTEMPTS - self.attempt_number + 1
            self.program_score += points
            self.total_score += points
            self.program_correct += 1
            self.total_correct += 1
            self.feedback = f"Parabéns! Acertou na tentativa {self.attempt_number} (+{points} pts)!"
            self.wrong_attempts_current_q = []
            self.go_to_next_question(self.program_score)
            return

        # Wrong guess
        self.wrong_attempts_current_q.append(selected)

        if self.attempt_number < MAX_ATTEMPTS:
            self.attempt_number += 1
            self.feedback = f"Ops! Tentativa {self.attempt_number}/{MAX_ATTEMPTS}."
            self.show_running_screen()
            return

        self.program_wrong += 1
        self.total_wrong += 1
        self.feedback = "Errou as 3 tentativas. Seguindo para a próxima."
        self.wrong_attempts_current_q = []
        self.go_to_next_question(self.program_score)

    def go_to_next_question(self, next_program_score):
        total_q = self.get_current_question_total()
        if self.question_number < total_q:
            self.question_number += 1
            self.attempt_number = 1
            self.show_running_screen()
            return

        # Save program result
        self.program_results.append({
            "programNumber": self.program_number,
            "score": next_program_score,
            "totalQuestions": total_q,
            "correct": self.program_correct,
            "wrong": self.program_wrong
        })

        if self.program_number == FINAL_PROGRAM_NUMBER:
            self.show_summary_screen("BOOK_END")
        else:
            self.show_summary_screen("PROGRAM_END")

    def show_running_screen(self):
        self.stage = "RUNNING"
        self.clear_container()

        display_card = ctk.CTkFrame(self.container, fg_color=CARD_BG, corner_radius=20)
        display_card.pack(fill="x", pady=(0, 16), padx=10)

        header_frame = ctk.CTkFrame(display_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(header_frame, text=f"LIVRO {self.active_book_code}", text_color=TEXT_SUB, font=("Helvetica", 12, "bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text=f"PROG {str(self.program_number).zfill(3)}", text_color=TEXT_SUB, font=("Helvetica", 12, "bold")).pack(side="right")

        current_q_key = self.get_current_question_key()
        ctk.CTkLabel(display_card, text=f"Pergunta {str(current_q_key).zfill(3)}", text_color=TEXT_MAIN, font=("Helvetica", 18, "bold")).pack(pady=5)
        
        ctk.CTkLabel(display_card, text=f"Tentativa {self.attempt_number}/{MAX_ATTEMPTS}", text_color=BTN_START, font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        # Puzzle / Grid area
        grid_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        grid_frame.pack(pady=10, expand=True)
        
        def get_color(opt, base_color):
            if opt in self.wrong_attempts_current_q:
                return "#E2E8F0" # Dimmed grey for wrong attempt
            return base_color
            
        def get_text_color(opt):
            if opt in self.wrong_attempts_current_q:
                return "#94A3B8"
            return "white"

        # Quad A
        btn_a_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
        btn_a_container.grid(row=0, column=0, padx=15, pady=15)
        btn_a = ctk.CTkButton(btn_a_container, text="A", 
                              fg_color=get_color("A", COLOR_A), hover_color=COLOR_A, text_color=get_text_color("A"), 
                              font=("Helvetica", 42, "bold"), width=120, height=120, corner_radius=20, 
                              command=lambda: self.handle_answer("A"))
        btn_a.pack()
        ctk.CTkLabel(btn_a_container, text="[Q]", font=("Helvetica", 12, "bold"), text_color=TEXT_SUB).pack(pady=2)

        # Quad B
        btn_b_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
        btn_b_container.grid(row=0, column=1, padx=15, pady=15)
        btn_b = ctk.CTkButton(btn_b_container, text="B", 
                              fg_color=get_color("B", COLOR_B), hover_color=COLOR_B, text_color=get_text_color("B"), 
                              font=("Helvetica", 42, "bold"), width=120, height=120, corner_radius=20, 
                              command=lambda: self.handle_answer("B"))
        btn_b.pack()
        ctk.CTkLabel(btn_b_container, text="[W]", font=("Helvetica", 12, "bold"), text_color=TEXT_SUB).pack(pady=2)

        # Quad C
        btn_c_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
        btn_c_container.grid(row=1, column=0, padx=15, pady=15)
        btn_c = ctk.CTkButton(btn_c_container, text="C", 
                              fg_color=get_color("C", COLOR_C), hover_color=COLOR_C, text_color=get_text_color("C"), 
                              font=("Helvetica", 42, "bold"), width=120, height=120, corner_radius=20, 
                              command=lambda: self.handle_answer("C"))
        btn_c.pack()
        ctk.CTkLabel(btn_c_container, text="[E]", font=("Helvetica", 12, "bold"), text_color=TEXT_SUB).pack(pady=2)

        # Quad D
        btn_d_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
        btn_d_container.grid(row=1, column=1, padx=15, pady=15)
        btn_d = ctk.CTkButton(btn_d_container, text="D", 
                              fg_color=get_color("D", COLOR_D), hover_color=COLOR_D, text_color=get_text_color("D"), 
                              font=("Helvetica", 42, "bold"), width=120, height=120, corner_radius=20, 
                              command=lambda: self.handle_answer("D"))
        btn_d.pack()
        ctk.CTkLabel(btn_d_container, text="[R]", font=("Helvetica", 12, "bold"), text_color=TEXT_SUB).pack(pady=2)

        if self.feedback:
            fb_color = "#06D6A0" if "Parabéns" in self.feedback else "#EF476F"
            ctk.CTkLabel(self.container, text=self.feedback, text_color=fb_color, font=("Helvetica", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(self.container, text="ESC: Sair do jogo", font=("Helvetica", 12), text_color=TEXT_SUB).pack(pady=5)

        change_btn = ctk.CTkButton(self.container, text="Trocar Livro", fg_color="transparent", border_width=2, border_color=TEXT_SUB,
                                   hover_color=BTN_SCROLL, text_color=TEXT_SUB, height=45, corner_radius=15, font=("Helvetica", 14, "bold"), 
                                   command=self.show_entry_screen)
        change_btn.pack(fill="x", pady=(10, 0), padx=20, side="bottom")

    def show_summary_screen(self, new_stage):
        self.stage = new_stage
        self.clear_container()

        summary_card = ctk.CTkFrame(self.container, fg_color=CARD_BG, corner_radius=20)
        summary_card.pack(fill="x", pady=20, ipadx=14, ipady=14, padx=10)

        ctk.CTkLabel(summary_card, text=f"PROGRAMA {str(self.program_number).zfill(3)}", 
                     text_color=TEXT_MAIN, font=("Helvetica", 18, "bold")).pack(pady=(10, 5))
        
        prog_total_ans = self.program_correct + self.program_wrong
        prog_perc = (self.program_correct / prog_total_ans * 100) if prog_total_ans > 0 else 0
        max_program_points = self.get_current_question_total() * MAX_ATTEMPTS
        
        ctk.CTkLabel(summary_card, text=f"Pontos: {self.program_score}/{max_program_points}", 
                     text_color=BTN_START, font=("Helvetica", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(summary_card, text=f"Acertos: {self.program_correct} | Erros: {self.program_wrong} ({prog_perc:.1f}%)", 
                     text_color=TEXT_SUB, font=("Helvetica", 14)).pack(pady=(0, 10))

        if self.stage == "PROGRAM_END":
            next_prog_text = f"PRÓXIMA FASE ({str(self.program_number + 1).zfill(3)})" if self.program_number < REGULAR_PROGRAMS else "FASE FINAL (006)"
            btn_next = ctk.CTkButton(summary_card, text=next_prog_text, fg_color=COLOR_B, hover_color="#05B888", text_color="white",
                          height=50, corner_radius=15, font=("Helvetica", 16, "bold"), 
                          command=self.start_next_program)
            btn_next.pack(pady=(15, 2), fill="x", padx=20)
            ctk.CTkLabel(summary_card, text="[W]", font=("Helvetica", 12, "bold"), text_color=TEXT_SUB).pack(pady=(0, 10))

        if self.stage == "BOOK_END":
            ctk.CTkLabel(summary_card, text="RESULTADO FINAL", text_color=TEXT_MAIN, font=("Helvetica", 16, "bold")).pack(pady=(15, 5))
            for res in self.program_results:
                perc = (res['correct'] / (res['correct'] + res['wrong']) * 100) if (res['correct'] + res['wrong']) > 0 else 0
                max_prog_points = res['totalQuestions'] * MAX_ATTEMPTS
                ctk.CTkLabel(summary_card, text=f"Prog {str(res['programNumber']).zfill(3)}: {res['score']}/{max_prog_points} pts | {res['correct']} acertos", 
                             text_color=TEXT_SUB, font=("Helvetica", 13)).pack()
            
            book_total_ans = self.total_correct + self.total_wrong
            book_perc = (self.total_correct / book_total_ans * 100) if book_total_ans > 0 else 0
            book_total_points = sum(r['totalQuestions'] * MAX_ATTEMPTS for r in self.program_results)
            ctk.CTkLabel(summary_card, text=f"TOTAL: {self.total_score}/{book_total_points} pts\n{self.total_correct} acertos, {self.total_wrong} erros ({book_perc:.1f}%)", 
                         text_color=COLOR_D, font=("Helvetica", 16, "bold")).pack(pady=(15, 0))

        change_btn = ctk.CTkButton(self.container, text="Trocar Livro", fg_color="transparent", border_width=2, border_color=TEXT_SUB, 
                                   hover_color=BTN_SCROLL, text_color=TEXT_SUB, height=45, corner_radius=15, font=("Helvetica", 14, "bold"), command=self.show_entry_screen)
        change_btn.pack(fill="x", pady=(20, 0), side="bottom", padx=20)

    def start_next_program(self):
        self.program_number += 1
        self.question_number = 1
        self.attempt_number = 1
        self.program_score = 0
        self.program_correct = 0
        self.program_wrong = 0
        self.feedback = ""
        self.wrong_attempts_current_q = []
        self.show_running_screen()

if __name__ == "__main__":
    app = App()
    app.mainloop()
