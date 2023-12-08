main:
    push rbp
    mov rbp, rsp
    sub rsp, 40
    mov ebx, 3 + 4
    mov DWORD PTR [rbp0], ebx
    mov DWORD PTR [rbp0], eax
    mov DWORD PTR [rbp-4], 4
    mov ebx, a + 5
    mov DWORD PTR [rbp0], ebx
    mov DWORD PTR [rbp0], eax
    mov ebx, b * 4
    mov DWORD PTR [rbp0], ebx
    mov ebx, t2 - 5
    mov DWORD PTR [rbp0], ebx
    mov ebx, a + t3
    mov DWORD PTR [rbp0], ebx
    mov DWORD PTR [rbp0], eax
    mov eax, DWORD PTR [rbp0]
    pop rbp
    ret
