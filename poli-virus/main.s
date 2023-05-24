section .text
    global _start

    _start:
        mov rcx, counter
        
    loop_start:
        mov rax, 2
        lea rdi, base_filename
        mov rsi, 0x0211
        mov rdx, 0644
        syscall

        cmp rax, 0
        jl error
        
        mov rdi, rax
        mov rax, 1
        mov rsi, buffer
        mov rdx, bufferLen
        syscall

        mov rax, 3
        syscall

        dec rcx
        cmp rcx, 0
        jnz loop_start

        mov rax, 60
        mov rdi, 42
        syscall

    error:
        mov rax, 1
        mov rdi, 1
        mov rsi, errorm
        mov rdx, errormLen
        syscall 

        mov rax, 60
        mov rdi, 0
        syscall
        

section .data
    base_filename: db "quine.txt", 0
    base_filenameLen: equ $-base_filename

    buffer: db "this is a test", 0
    bufferLen: equ $-buffer

    errorm: db "An error occurred.", 0
    errormLen: equ $-errorm

    counter: equ 1
