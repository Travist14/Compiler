main:
    push rbp
    mov rbp, rsp
    sub rsp, 16
    mov eax, 4
    imul eax, 5
    mov DWORD PTR [rbp-8], eax
    mov eax, 3
    add eax, DWORD PTR [rbp-8]
    mov DWORD PTR [rbp-12], eax
    mov eax, DWORD PTR [rbp-12]
    pop rbp
    ret
