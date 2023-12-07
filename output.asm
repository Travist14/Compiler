main:
    push rbp
    mov rbp, rsp
    sub rsp, 48
    mov eax, 4
    add eax, 5
    mov DWORD PTR [rbp-8], eax
    mov eax, 3
    imul eax, 3
    mov DWORD PTR [rbp-12], eax
    mov eax, DWORD PTR [rbp-8]
    imul eax, DWORD PTR [rbp-12]
    mov DWORD PTR [rbp-16], eax
    mov DWORD PTR [rbp-16], 8
    mov eax, 4
    add eax, 8
    mov DWORD PTR [rbp-20], eax
    mov eax, 6
    add eax, DWORD PTR [rbp-20]
    mov DWORD PTR [rbp-24], eax
    mov eax, DWORD PTR [rbp-16]
    add eax, DWORD PTR [rbp-24]
    mov DWORD PTR [rbp-28], eax
    mov eax, DWORD PTR [rbp-28]
    pop rbp
    ret
