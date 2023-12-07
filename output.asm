main:
    push rbp
    mov rbp, rsp
    sub rsp, 8
    mov DWORD PTR [rbp-4], 1
    pop rbp
    ret
